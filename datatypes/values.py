import logging
import random
from multiprocessing import Queue

from shapely import geometry

from datatypes import metacard_types, lines
from util import timeit, switchable

logger = logging.getLogger(__name__)
__empty_polygons = []
geometry_collection = geometry.GeometryCollection()
explore_queue = Queue(100)


@timeit
@switchable('deadzone-elimination')
def report_empty_polygon(extras):
    global geometry_collection
    polygon = extras['filter']['value']['value']
    __empty_polygons.append(polygon)
    geometry_collection = geometry_collection.union(polygon)
    try:
        explore_queue.put(polygon.buffer(1).simplify(0.1).intersection(geometry.box(-180, -90, 180, 90)), block=False)
    except:
        pass
        # if len(__empty_polygons) % 100 == 0:
        #     logger.debug(geometry_collection.wkt)


@switchable('deadzone-elimination')
def get_explorer_polygon():
    if random.choice((True, False)):
        if not explore_queue.empty():
            try:
                return explore_queue.get(block=False)
            except:
                pass


attribute_constraints = {
    # 'sortOrder': lambda: '%s:%s' % ('modified', random.choice(('desc', 'asc'))),
    # 'resource-size': lambda: random.randint(0, 2 << 32),
    'metadata-content-type': lambda: random.choice(('city', 'landmark', 'adm1st', 'mountain', 'unknown', 'event',
                                                    'country',
                                                    'airport')),
    'metacard-type': lambda: random.choice(list(metacard_types.keys())),
    'title': lambda: random.choice(lines),
    'anyText': lambda: random.choice(lines)
}


def get_random_attrvalue():
    """
    Gets a set of attribute name and value pairs according to valid possible values
    :return: 2-tuple of the attribute name and a random attribute value
    """
    attr = random.choice(list(attribute_constraints.keys()))
    return attr, get_random_value(attr)


def get_random_value(attribute):
    return attribute_constraints[attribute]()


def get_random_geo_polygon(default_range=(0.1, 8), num_points=3):
    """
    gets a random polygon of somewhere in the world

    :param default_range: the range in degrees to use for min & max distance when generating polygons
    :type default_range: tuple
    :param num_points: The number of points to place before wrapping in a polygon
    :type num_points: int
    """
    assert num_points >= 3, "Must have 3 points minimum to define a polygon!"
    geo = _create_geometry(default_range, num_points)
    return geo


@timeit
def _create_geometry(default_range, num_points):
    if random.choice((True, False)):
        if not explore_queue.empty():
            try:
                return explore_queue.get(block=False)
            except:
                pass

    start_point = geometry.Point(random.uniform(-180, 180), random.uniform(-90, 90))
    tries = 1
    while geometry_collection.intersects(start_point):
        tries += 1
        start_point = geometry.Point(random.uniform(-180, 180), random.uniform(-90, 90))
    logger.debug('took %s tries to generate geo', tries)
    points = [start_point]
    for i in range(num_points - 1):
        new_x = start_point.x + random.uniform(*default_range)
        if new_x > 180:
            new_x = new_x % 180 + (-180)
        new_y = start_point.y + random.uniform(*default_range)
        if new_y > 90:
            new_y = new_y % 90 + (-90)
        points.append(geometry.Point(new_x, new_y))
    return geometry.Polygon(geometry.LinearRing(tuple(map(lambda x: (x.x, x.y), (*points, points[0])))))
