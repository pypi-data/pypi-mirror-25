# pylint: skip-file
# See https://github.com/PyCQA/astroid/issues/437
"""PuppetDB backend."""
from string import capwords

import pyparsing as pp
import requests

from ClusterShell.NodeSet import NodeSet
from requests.packages import urllib3

from cumin.backends import BaseQuery, InvalidQueryError


CATEGORIES = (
    'F',  # Fact
    'R',  # Resource
)
""":py:func:`tuple`: available categories in the grammar."""

OPERATORS = ('=', '>=', '<=', '<', '>', '~')
""":py:func:`tuple`: available operators in the grammar, the same available in PuppetDB API."""


def grammar():
    """Define the query grammar.

    Some query examples:

    * All hosts: ``*``
    * Hosts globbing: ``host10*``
    * :py:class:`ClusterShell.NodeSet.NodeSet` syntax for hosts expansion: ``host10[10-42].domain``
    * Category based key-value selection:

      * ``R:Resource::Name``: query all the hosts that have a resource of type `Resource::Name`.
      * ``R:Resource::Name = 'resource-title'``: query all the hosts that have a resource of type `Resource::Name`
        whose title is ``resource-title``. For example ``R:Class = MyModule::MyClass``.
      * ``R:Resource::Name@field = 'some-value'``: query all the hosts that have a resource of type ``Resource::Name``
        whose field ``field`` has the value ``some-value``. The valid fields are: ``tag``, ``certname``, ``type``,
        ``title``, ``exported``, ``file``, ``line``. The previous syntax is a shortcut for this one with the field
        ``title``.
      * ``R:Resource::Name%param = 'some-value'``: query all the hosts that have a resource of type ``Resource::Name``
        whose parameter ``param`` has the value ``some-value``.
      * Mixed facts/resources queries are not supported, but the same result can be achieved by the main grammar using
        multiple subqueries.

    * A complex selection for facts:
      ``host10[10-42].*.domain or (not F:key1 = value1 and host10*) or (F:key2 > value2 and F:key3 ~ '^value[0-9]+')``

    Backus-Naur form (BNF) of the grammar::

            <grammar> ::= <item> | <item> <and_or> <grammar>
               <item> ::= [<neg>] <query-token> | [<neg>] "(" <grammar> ")"
        <query-token> ::= <token> | <hosts>
              <token> ::= <category>:<key> [<operator> <value>]

    Given that the pyparsing library defines the grammar in a BNF-like style, for the details of the tokens not
    specified above check directly the source code.

    Returns:
        pyparsing.ParserElement: the grammar parser.

    """
    # Boolean operators
    and_or = (pp.CaselessKeyword('and') | pp.CaselessKeyword('or'))('bool')
    # 'neg' is used as label to allow the use of dot notation, 'not' is a reserved word in Python
    neg = pp.CaselessKeyword('not')('neg')

    operator = pp.oneOf(OPERATORS, caseless=True)('operator')  # Comparison operators
    quoted_string = pp.quotedString.copy().addParseAction(pp.removeQuotes)  # Both single and double quotes are allowed

    # Parentheses
    lpar = pp.Literal('(')('open_subgroup')
    rpar = pp.Literal(')')('close_subgroup')

    # Hosts selection: glob (*) and clustershell (,!&^[]) syntaxes are allowed:
    # i.e. host10[10-42].*.domain
    hosts = quoted_string | (~(and_or | neg) + pp.Word(pp.alphanums + '-_.*,!&^[]'))

    # Key-value token for allowed categories using the available comparison operators
    # i.e. F:key = value
    category = pp.oneOf(CATEGORIES, caseless=True)('category')
    key = pp.Word(pp.alphanums + '-_.%@:')('key')
    selector = pp.Combine(category + ':' + key)  # i.e. F:key
    # All printables characters except the parentheses that are part of this or the global grammar
    all_but_par = ''.join([c for c in pp.printables if c not in ('(', ')', '{', '}')])
    value = (quoted_string | pp.Word(all_but_par))('value')
    token = selector + pp.Optional(operator + value)

    # Final grammar, see the docstring for its BNF based on the tokens defined above
    # Groups are used to split the parsed results for an easy access
    full_grammar = pp.Forward()
    item = pp.Group(pp.Optional(neg) + (token | hosts('hosts'))) | pp.Group(
        pp.Optional(neg) + lpar + full_grammar + rpar)
    full_grammar << item + pp.ZeroOrMore(pp.Group(and_or) + full_grammar)  # pylint: disable=expression-not-assigned

    return full_grammar


class PuppetDBQuery(BaseQuery):
    """PuppetDB query builder.

    The `puppetdb` backend allow to use an existing PuppetDB instance for the hosts selection.
    At the moment only PuppetDB v3 API are implemented.
    """

    base_url_template = 'https://{host}:{port}/v3/'
    """:py:class:`str`: string template in the :py:meth:`str.format` style used to generate the base URL of the
    PuppetDB server."""

    endpoints = {'R': 'resources', 'F': 'nodes'}
    """:py:class:`dict`: dictionary with the mapping of the available categories in the grammar to the PuppetDB API
    endpoints."""

    hosts_keys = {'R': 'certname', 'F': 'name'}
    """:py:class:`dict`: dictionary with the mapping of the available categories in the grammar to the PuppetDB API
    field to query to get the hostname."""

    grammar = grammar()
    """:py:class:`pyparsing.ParserElement`: load the grammar parser only once in a singleton-like way."""

    def __init__(self, config, logger=None):
        """Query constructor for the PuppetDB backend.

        :Parameters:
            according to parent :py:meth:`cumin.backends.BaseQuery.__init__`.

        """
        super(PuppetDBQuery, self).__init__(config, logger=logger)
        self.grouped_tokens = None
        self.current_group = self.grouped_tokens
        self._category = None
        puppetdb_config = self.config.get('puppetdb', {})
        self.url = self.base_url_template.format(
            host=puppetdb_config.get('host', 'localhost'),
            port=puppetdb_config.get('port', 443))

        for exception in puppetdb_config.get('urllib3_disable_warnings', []):
            urllib3.disable_warnings(category=getattr(urllib3.exceptions, exception))

    @property
    def category(self):
        """Category for the current query.

        :Getter:
            Returns the current `category` or a default value if not set.

        :Setter:
            :py:class:`str`: the value to set the `category` to.

        Raises:
            cumin.backends.InvalidQueryError: if trying to set it to an invalid `category` or mixing categories in a
                single query.

        """
        return self._category or 'F'

    @category.setter
    def category(self, value):
        """Setter for the `category` property. The relative documentation is in the getter."""
        if value not in self.endpoints:
            raise InvalidQueryError("Invalid value '{category}' for category property".format(category=value))
        if self._category is not None and value != self._category:
            raise InvalidQueryError('Mixed F: and R: queries are currently not supported')

        self._category = value

    def _open_subgroup(self):
        """Handle subgroup opening."""
        token = PuppetDBQuery._get_grouped_tokens()
        token['parent'] = self.current_group
        self.current_group['tokens'].append(token)
        self.current_group = token

    def _close_subgroup(self):
        """Handle subgroup closing."""
        self.current_group = self.current_group['parent']

    @staticmethod
    def _get_grouped_tokens():
        """Return an empty grouped tokens structure.

        Returns:
            dict: the dictionary with the empty grouped tokens structure.

        """
        return {'parent': None, 'bool': None, 'tokens': []}

    def _build(self, query_string):
        """Override parent class _build method to reset tokens and add logging.

        :Parameters:
            according to parent :py:meth:`cumin.backends.BaseQuery._build`.

        """
        self.grouped_tokens = PuppetDBQuery._get_grouped_tokens()
        self.current_group = self.grouped_tokens
        super(PuppetDBQuery, self)._build(query_string)
        self.logger.trace('Query tokens: {tokens}'.format(tokens=self.grouped_tokens))

    def _execute(self):
        """Concrete implementation of parent abstract method.

        :Parameters:
            according to parent :py:meth:`cumin.backends.BaseQuery._execute`.

        Returns:
            ClusterShell.NodeSet.NodeSet: with the FQDNs of the matching hosts.

        """
        query = self._get_query_string(group=self.grouped_tokens).format(host_key=self.hosts_keys[self.category])
        hosts = self._api_call(query, self.endpoints[self.category])
        unique_hosts = NodeSet.fromlist([host[self.hosts_keys[self.category]] for host in hosts])
        self.logger.debug("Queried puppetdb for '{query}', got '{num}' results.".format(
            query=query, num=len(unique_hosts)))

        return unique_hosts

    def _add_category(self, category, key, value=None, operator='=', neg=False):
        """Add a category token to the query 'F:key = value'.

        Arguments:
            category (str): the category of the token, one of :py:const:`CATEGORIES`.
            key (str): the key for this category.
            value (str, optional): the value to match, if not specified the key itself will be matched.
            operator (str, optional): the comparison operator to use, one of :py:const:`OPERATORS`.
            neg (bool, optional): whether the token must be negated.

        Raises:
            cumin.backends.InvalidQueryError: on internal parsing error.

        """
        self.category = category
        if operator == '~':
            value = value.replace(r'\\', r'\\\\')  # Required by PuppetDB API

        if category == 'R':
            query = self._get_resource_query(key, value, operator)
        elif category == 'F':
            query = '["{op}", ["fact", "{key}"], "{val}"]'.format(op=operator, key=key, val=value)
        else:  # pragma: no cover - this should never happen
            raise InvalidQueryError(
                "Got invalid category '{category}', one of F|R expected".format(category=category))

        if neg:
            query = '["not", {query}]'.format(query=query)

        self.current_group['tokens'].append(query)

    def _add_hosts(self, hosts, neg=False):
        """Add a list of hosts to the query.

        Arguments:
            hosts (ClusterShell.NodeSet.NodeSet): with the list of hosts to search.
            neg (bool, optional): whether the token must be negated.
        """
        if not hosts:
            return

        hosts_tokens = []
        for host in hosts:
            operator = '='
            # Convert a glob expansion into a regex
            if '*' in host:
                operator = '~'
                host = r'^' + host.replace('.', r'\\.').replace('*', '.*') + r'$'

            hosts_tokens.append('["{op}", "{{host_key}}", "{host}"]'.format(op=operator, host=host))

        query = '["or", {hosts}]'.format(hosts=', '.join(hosts_tokens))
        if neg:
            query = '["not", {query}]'.format(query=query)

        self.current_group['tokens'].append(query)

    def _parse_token(self, token):
        """Concrete implementation of parent abstract method.

        :Parameters:
            according to parent :py:meth:`cumin.backends.BaseQuery._parse_token`.

        Raises:
            cumin.backends.InvalidQueryError: on internal parsing error.

        """
        if isinstance(token, str):
            return

        token_dict = token.asDict()

        # Based on the token type build the corresponding query object
        if 'open_subgroup' in token_dict:
            self._open_subgroup()
            for subtoken in token:
                self._parse_token(subtoken)
            self._close_subgroup()

        elif 'bool' in token_dict:
            self._add_bool(token_dict['bool'])

        elif 'hosts' in token_dict:
            token_dict['hosts'] = NodeSet(token_dict['hosts'])
            self._add_hosts(**token_dict)

        elif 'category' in token_dict:
            self._add_category(**token_dict)

        else:  # pragma: no cover - this should never happen
            raise InvalidQueryError(
                "No valid key found in token, one of bool|hosts|category expected: {token}".format(token=token_dict))

    def _get_resource_query(self, key, value=None, operator='='):  # pylint: disable=no-self-use
        """Build a resource query based on the parameters, resolving the special cases for ``%params`` and ``@field``.

        Arguments:
            key (str): the key of the resource.
            value (str, optional): the value to match, if not specified the key itself will be matched.
            operator (str, optional): the comparison operator to use, one of :py:const:`OPERATORS`.

        Returns:
            str: the resource query.

        Raises:
            cumin.backends.InvalidQueryError: on invalid combinations of parameters.

        """
        if all(char in key for char in ('%', '@')):
            raise InvalidQueryError(("Resource key cannot contain both '%' (query a resource's parameter) and '@' "
                                     "(query a  resource's field)"))

        elif '%' in key:
            # Querying a specific parameter of the resource
            if operator == '~':
                raise InvalidQueryError('Regex operations are not supported in PuppetDB API v3 for resource parameters')
            key, param = key.split('%', 1)
            query_part = ', ["{op}", ["parameter", "{param}"], "{value}"]'.format(op=operator, param=param, value=value)

        elif '@' in key:
            # Querying a specific field of the resource
            key, field = key.split('@', 1)
            query_part = ', ["{op}", "{field}", "{value}"]'.format(op=operator, field=field, value=value)

        elif value is None:
            # Querying a specific resource type
            query_part = ''

        else:
            # Querying a specific resource title
            if key.lower() == 'class' and operator != '~':
                value = capwords(value, '::')  # Auto ucfirst the class title
            query_part = ', ["{op}", "title", "{value}"]'.format(op=operator, value=value)

        query = '["and", ["=", "type", "{type}"]{query_part}]'.format(type=capwords(key, '::'), query_part=query_part)

        return query

    def _get_query_string(self, group):
        """Recursively build and return the PuppetDB query string.

        Arguments:
            group (dict): a dictionary with the grouped tokens.

        Returns:
            str: the query string for the PuppetDB API.

        """
        if group['bool']:
            query = '["{bool}", '.format(bool=group['bool'])
        else:
            query = ''

        last_index = len(group['tokens'])
        for i, token in enumerate(group['tokens']):
            if isinstance(token, dict):
                query += self._get_query_string(group=token)
            else:
                query += token

            if i < last_index - 1:
                query += ', '

        if group['bool']:
            query += ']'

        return query

    def _add_bool(self, bool_op):
        """Add a boolean AND or OR query block to the query and validate logic.

        Arguments:
            bool_op (str): the boolean operator to add to the query: ``and``, ``or``.

        Raises:
            cumin.backends.InvalidQueryError: if an invalid boolean operator was found.

        """
        if self.current_group['bool'] is None:
            self.current_group['bool'] = bool_op
        elif self.current_group['bool'] == bool_op:
            return
        else:
            raise InvalidQueryError("Got unexpected '{bool}' boolean operator, current operator was '{current}'".format(
                bool=bool_op, current=self.current_group['bool']))

    def _api_call(self, query, endpoint):
        """Execute a query to PuppetDB API and return the parsed JSON.

        Arguments:
            query (str): the query parameter to send to the PuppetDB API.
            endpoint (str): the endpoint of the PuppetDB API to call.

        Raises:
            requests.HTTPError: if the PuppetDB API call fails.

        """
        resources = requests.get(self.url + endpoint, params={'query': query}, verify=True)
        resources.raise_for_status()
        return resources.json()


GRAMMAR_PREFIX = 'P'
""":py:class:`str`: the prefix associate to this grammar, to register this backend into the general grammar.
Required by the backend auto-loader in :py:meth:`cumin.grammar.get_registered_backends`."""

query_class = PuppetDBQuery  # pylint: disable=invalid-name
"""Required by the backend auto-loader in :py:meth:`cumin.grammar.get_registered_backends`."""
