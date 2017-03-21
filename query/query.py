import itertools
import random
import uuid

import cql
import datatypes
from datatypes import get_random_geo_polygon


def get_cql_data(cql_generator=None, **kwargs):
    cql_gen = (cql_generator if cql_generator is not None
               else random_cql_generator())

    cql_tree = cql_gen()
    data = {
        'src': 'ddf.distribution',
        'start': 1,
        'count': 250,
        'cql': cql.write(cql_tree),
        'sort': 'modified:desc',
        'id': str(uuid.uuid4())
    }
    return {**data, **kwargs}, {'filter': cql_tree}


def anytext_like_star(value='*'):
    return {
        'type': 'ILIKE',
        'property': 'anyText',
        'value': value
    }


def ilike_query():
    attribute, value = datatypes.get_random_attrvalue()

    return {
        'type': 'ILIKE',
        'property': attribute,
        'value': value
    }


def random_geo_query():
    polygon = get_random_geo_polygon()

    return {
        'type': 'INTERSECTS',
        'property': 'anyGeo',
        'value': {
            'type': 'GEO',
            'value': polygon
        }
    }


def and_query(n=2, query_func=ilike_query):
    return {
        'type': 'AND',
        'filters': [query_func() for _ in range(n)]
    }


default_query_kinds = [(anytext_like_star, 1),
                       (ilike_query, 5),
                       (random_geo_query, 10)]


def random_cql_generator(query_kinds=default_query_kinds):
    chain = tuple()
    for kind in query_kinds:
        if isinstance(kind, tuple) or isinstance(kind, list):
            if len(kind) != 2 or not kind[1] > 0:
                raise NotImplementedError('only implemented for 2-tuples with weights > 0')
            chain = itertools.chain(chain, itertools.repeat(kind[0], kind[1]))
        else:
            chain = itertools.chain(chain, (kind,))

    query_generators = list(chain)

    def get_random_query():
        res = random.choice(query_generators)()
        return res

    return get_random_query
