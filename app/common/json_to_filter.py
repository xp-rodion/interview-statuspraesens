"""
Django query filter specification from JSON

based on https://djangosnippets.org/snippets/676/

* python3, django2
* "in" command with comma separator with escaping
"""

__author__ = "Victor Borisov <borisov@borisovcode.com>"
__copyright__ = "Copyright (C) 2019 Victor Borisov"
__license__ = "Public Domain"
__version__ = "1.0"

from django.db.models.query import Q


def _qop(cmd, q1, q2=None):
    if cmd == 'and':
        # raise ValueError('"and" filters must have at least one subfilter')
        return q1 & q2
    elif cmd == 'or':
        # raise ValueError('"or" filters must have at least one subfilter')
        return q1 | q2
    elif cmd == 'not':
        return ~q1
    else:
        raise ValueError('unknown logical operation "{}"'.format(cmd))


def build_query_filter_from_spec(spec, field_mapping=None):
    """
    Assemble a django "Q" query filter object from a specification that consists
    of a possibly-nested list of query filter descriptions.  These descriptions
    themselves specify Django primitive query filters, along with boolean
    "and", "or", and "not" operators.  This format can be serialized and
    deserialized, allowing django queries to be composed client-side and
    sent across the wire using JSON.

    Each filter description is a list.  The first element of the list is always
    the filter operator name. This name is one of either django's filter
    operators, "eq" (a synonym for "exact"), or the boolean operators
    "and", "or", and "not".

    Primitive query filters have three elements:

    [filteroperator, fieldname, queryarg]

    "filteroperator" is a string name like "in", "range", "icontains", etc.
    "fieldname" is the django field being queried.  Any name that django
    accepts is allowed, including references to fields in foreign keys
    using the "__" syntax described in the django API reference.
    "queryarg" is the argument you'd pass to the `filter()` method in
    the Django database API.

    "and" and "or" query filters are lists that begin with the appropriate
    operator name, and include subfilters as additional list elements:

    ['or', [subfilter], ...]
    ['and', [subfilter], ...]

    "not" query filters consist of exactly two elements:

    ['not', [subfilter]]

    As a special case, the empty list "[]" or None return all elements.

    If field_mapping is specified, the field name provided in the spec
    is looked up in the field_mapping dictionary.  If there's a match,
    the result is subsitituted. Otherwise, the field name is used unchanged
    to form the query. This feature allows client-side programs to use
    "nice" names that can be mapped to more complex django names. If
    you decide to use this feature, you'll probably want to do a similar
    mapping on the field names being returned to the client.

    This function returns a Q object that can be used anywhere you'd like
    in the django query machinery.

    This function raises ValueError in case the query is malformed, or
    perhaps other errors from the underlying DB code.

    Example queries:

    ['and', ['contains', 'name', 'Django'], ['range', 'apps', [1, 4]]]
    ['not', ['in', 'tags', ['colors', 'shapes', 'animals']]]
    ['or', ['eq', 'id', 2], ['icontains', 'city', 'Boston']]

    """

    if spec is None or len(spec) == 0:
        return Q()

    if spec[1] == 'facts:user.viivii.percent':
        spec = [
            'and',
            ['eq', 'facts__category__code', 'user.viivii.percent', ''],
            ['gte', 'facts__float_val', 0.3, ''],
            ['gte', 'facts__int_val', 240, ''],
            ['in', 'facts__tag_id', spec[2], '']
        ]

    cmd = spec[0]

    if cmd == 'and' or cmd == 'or':
        # ["or",  [filter],[filter],[filter],...]
        # ["and", [filter],[filter],[filter],...]
        if len(spec) < 2:
            raise ValueError('"and" or "or" filters must have at least one subfilter')

        result_q = None
        for arg in spec[1:]:
            q = build_query_filter_from_spec(arg)
            if q is not None:
                if result_q is None:
                    result_q = q
                else:
                    result_q = _qop(cmd, result_q, q)

    elif cmd == 'not':
        # ["not", [query]]
        if len(spec) != 2:
            raise ValueError('"not" filters must have exactly one subfilter')
        q = build_query_filter_from_spec(spec[1])
        if q is not None:
            result_q = _qop(cmd, q)

    else:
        # some other query, will be validated in the query machinery
        # ["cmd", "field_name", "arg"]

        # Закомментировал это, мб тут не 4, а 3?
        # if len(spec) < 4:
        if len(spec) < 3:
            raise ValueError('primitive filters must have two arguments (fieldname and query arg) : {}'.format(spec))

        # provide an intuitive alias for exact field equality
        if cmd == 'eq':
            cmd = 'exact'

        if cmd == 'in':
            arg = spec[2]  # re.split(r'(?<!\\),', spec[2])
        else:
            arg = spec[2]

        field_name = spec[1]
        if field_mapping:
            # see if the mapping contains an entry for the field_name
            # (for example, if you're mapping an external database name
            # to an internal django one).  If not, use the existing name.
            field_name = field_mapping.get(field_name, field_name)

        result_q = Q(**{'{}__{}'.format(field_name, cmd): arg})

    return result_q
