
def and_filter(node):
    return '(%s)' % (' AND '.join(map(write, node['filters'])))


def or_filter(node):
    return '(%s)' % (' OR '.join(map(write, node['filters'])))


def equal_filter(node):
    return '''("%s" = '%s')''' % (node['property'], node['value'])


def ilike_filter(node):
    return '''("%s" ILIKE '%s')''' % (node['property'], node['value'])


def not_filter(node):
    return 'NOT (%s)' % write(node['filters'][0])


def bbox_filter(node):
    return 'BBOX(%s, %s, %s, %s, %s)' % (node['property'], *node['value'])


# def contains_filter(node):
#     return 'CONTAINS(%s, %s)' % (node['property'], write(node['value']))

def intersects_filter(node):
    return '(INTERSECTS(%s, %s))' % (node['property'], write(node['value']))


def geo_writer(node):
    return node['value'].wkt


types = {
    'AND': and_filter,
    'OR': or_filter,
    '=': equal_filter,
    'ILIKE': ilike_filter,
    'NOT': not_filter,
    'BBOX': bbox_filter,
    # 'CONTAINS': contains_filter,
    'INTERSECTS': intersects_filter,
    'GEO': geo_writer
}


def write(node):
    return types[node['type']](node)


