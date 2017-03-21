import json
import logging
import os
import re
import sys
from base64 import b64encode
from threading import Lock

import locust
import requests
from locust import task
from locust.main import main

import datatypes.values
import query

requests.packages.urllib3.disable_warnings()

logger = logging.getLogger(__name__)

# user_lock = Lock()
# users = list(map(lambda x: x.split('=', 1), open('resources/user.properties').readlines()))


def get_task_func(s):
    @task(1)
    def fn(self):
        self.client.get(s)

    return fn


class IntrigueTasks(locust.TaskSet):
    static_resources = ['/catalog/cesium/Widgets/widgets.css',
                        '/search/catalog/lib/bootstrap/dist/css/bootstrap.min.css',
                        '/search/catalog/lib/font-awesome/css/font-awesome.min.css',
                        '/search/catalog/lib/jquery-ui-multiselect-widget/jquery.multiselect.css',
                        '/search/catalog/lib/cesium-drawhelper/DrawHelper.css',
                        '/search/catalog/lib/eonasdan-bootstrap-datetimepicker/css/bootstrap-datetimepicker.css',
                        '/search/catalog/css/index.css',
                        '/search/catalog/bundle.js',
                        '/search/catalog/1.bundle.js',
                        '/search/catalog/2.bundle.js',
                        '/search/catalog/blank.html',
                        '/search/catalog/css/fonts/open-sans/open-sans-v13-latin-300.woff2',
                        '/search/catalog/css/fonts/open-sans/open-sans-v13-latin-regular.woff2'
                        ]
    tasks = [get_task_func(s) for s in static_resources]

    def on_start(self):
        # disable SSL cert verification on http client
        self.client.verify = False


        # user_properties = tuple()
        # pw = ''
        #
        # with user_lock:
        #     if len(users) > 0:
        #         user_properties = random.choice(users)
        #         users.remove(user_properties)'https://newui.phx.connexta.com:8993/search/catalog/internal/cql'
        #         print('Logging in as [%s]' % user_properties)
        #     else:
        #         print('Logging in as guest')
        # user = user_properties[0]
        # pw = user_properties[1].split(',')[0]
        # print('Authorization header: [%s]' % b64encode('%s:%s' % (user, pw)))
        # res = self.client.get('/search/catalog/internal/user',
        #                       headers={'Authorization': 'Basic %s' % b64encode('%s:%s' % (user, pw))})
        # print('login result: %s' % res.status_code)

    @task(1)
    def index(self):
        self.client.get('/search/catalog/')

    @task(10)
    def sources(self):
        self.client.get('/services/catalog/sources')

    @task(1)
    def catalogid(self):
        self.client.get('/search/catalog/internal/localcatalogid')

    @task(15)
    def workspace(self):
        self.client.get('/search/catalog/internal/enumerations/metacardtype/workspace')

    @task(30)
    def query(self):
        query_data, extra = query.get_cql_data()
        res = self.client.post('/search/catalog/internal/cql', json.dumps(query_data), timeout=30,
                               allow_redirects=False)
        print('req history: ', res.history)
        res.raise_for_status()

        if int(res.status_code / 100) == 3:
            raise Exception('Query got redirected!')

        if res.headers.get('content-type') != 'application/json':
            raise Exception(
                'The return type was not application/json! status_code: {0.status_code} text: {0.text}'.format(res))
        json_response = res.json()
        if res.status_code == 200 and json_response['status']['hits'] == 0 and extra['filter']['type'] == 'INTERSECTS':
            datatypes.values.report_empty_polygon(extra)


for resource in IntrigueTasks.static_resources:
    @task(1)
    def fn(self):
        self.client.get(resource)

    # set generated static resource tasks as functions on IntrigueTasks class
    setattr(IntrigueTasks, re.sub(r'\W', '_', resource)[1:], fn)


class IntrigueUser(locust.HttpLocust):
    task_set = IntrigueTasks
    min_wait = 5000
    max_wait = 10000
    # host = "https://newui.phx.connexta.com:8993"
    # host = "https://goten.local:8993"


if __name__ == '__main__':
    if any('-Ddeadzone-eliminiation=true' == x for x in sys.argv):
        os.putenv('deadzone-elimination', 'true')

    if '-f' not in sys.argv or '--locustfile' not in sys.argv:
        locust_file = os.path.join(os.path.split(sys.argv[0])[0], 'DDFLoadTest.py')
        sys.argv.append('--locustfile')
        sys.argv.append(locust_file)
        logger.debug("added locustfile to arguments: %s", sys.argv)
    sys.exit(main())
