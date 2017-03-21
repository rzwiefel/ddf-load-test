simple1 = {
    'type': '=',
    'property': 'id',
    'value': '1241-a482-4ab1-4918ad2-af41'
}

simpleand = {
    'type': 'AND',
    'filters': [
        {
            'type': '=',
            'property': 'id',
            'value': '1241-a482-4ab1-4918ad2-af41'
        },
        {
            'type': '=',
            'property': 'id',
            'value': '4444-1234-4ab1-bbbbbbbb-af41'
        }
    ]
}

nestedorand = {
    'type': 'OR',
    'filters': [
        {
            'type': 'ILIKE',
            'property': 'metacard.tags',
            'value': '*'
        },
        {
            'type': 'AND',
            'filters': [
                {
                    'type': 'ILIKE',
                    'property': 'title',
                    'value': 'banana'
                },
                {
                    'type': 'ILIKE',
                    'property': 'topic.category',
                    'value': 'cities'
                }
            ]
        }
    ]
}