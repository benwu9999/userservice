import json
import os
import urllib2


class UserServiceClient:
    DEFAULT_URL = os.getenv('USER_SVC_URL', 'http://127.0.0.1:8013/user/');

    content_type = {'Content-Type': 'application/json'}

    def __init__(self, url):
        if url:
            self.url = url
        else:
            self.url = UserServiceClient.DEFAULT_URL

    def get(self, ids):
        if not ids:
            return [];
        result = urllib2.urlopen(self.url + 'search?ids=' + ",".join(ids)).read()
        parsed = json.loads(result)
        return parsed

    def get_user_and_alerts(self, ids=None, alert_ids=None):
        data = dict()
        if ids is not None:
            data['email'] = ",".join(ids)
        if alert_ids is not None:
            data['alert_ids'] = ",".join(alert_ids)
        if data:
            jsonText = json.dumps(data)
            req = urllib2.Request(self.url + 'rel/alert', jsonText, self.content_type)
        else:
            req = urllib2.Request(self.url + 'rel/alert', "", self.content_type)

        response = urllib2.urlopen(req)
        result = response.read()
        parsed = json.loads(result)
        return parsed


def test_get_user():
    global test_ids, obj
    test_ids = ['js06']
    obj = client.get(test_ids)
    print(json.dumps(obj))


def test_get_alert():
    # test_ids = ['js06']
    # obj = client.get_user_and_alerts(test_ids)
    # print(json.dumps(obj))
    # test_ids = None
    # obj = client.get_user_and_alerts(test_ids)
    # print(json.dumps(obj))
    alert_ids = ['7aa7569dd2974f8db65d8a686801ecb0']
    obj = client.get_user_and_alerts(alert_ids=alert_ids)
    print(json.dumps(obj))


if __name__ == '__main__':
    client = UserServiceClient(None);
    # test_get_user()

    test_get_alert()
