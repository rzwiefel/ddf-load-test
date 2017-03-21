import json
from functools import reduce

lines = []
with open('resources/wordsEn.txt') as f:
    lines = list(filter(lambda x: len(x) > 1, map(str.strip, f.readlines())))

metacard_types = {}
with open('resources/metacardtypes.json') as f:
    metacard_types = json.loads(f.read())

attributes = reduce(lambda l, r: {**l, **r}, map(metacard_types.get, metacard_types))

from .values import get_random_attrvalue, get_random_value, attribute_constraints, get_random_geo_polygon

__all__ = ['metacard_types', 'attributes', 'lines', 'get_random_attrvalue', 'get_random_value', 'attribute_constraints',
           'get_random_geo_polygon']
