import json
import urllib2
import os
import urllib


class ProviderProfileServiceClient:
    DEFAULT_URL = os.getenv('PROVIDER_PROFILE_SVC_URL', 'http://127.0.0.1:8013/providerProfile/');
    content_type = {'Content-Type': 'application/json'}

    def __init__(self, url):
        if url:
            self.url = url
        else:
            self.url = ProviderProfileServiceClient.DEFAULT_URL

    def get(self, ids):
        if not ids:
            return [];
        result = urllib2.urlopen(self.url + 'search?ids=' + ",".join(ids)).read()
        parsed = json.loads(result)
        return parsed

    def search_by_name(self, names):
        if not names:
            return {};
        names_str = ",".join(names)
        params = {'has': names_str}
        params_str = urllib.urlencode(params)

        result = urllib2.urlopen(self.url + 'search?' + params_str).read()
        parsed = json.loads(result)
        d = {}
        for p in parsed:
            d[p['profileId']] = p
        return d

    def search_by_text(self, names, id_only=False):
        if not names:
            return {};
        names_str = ",".join(names)
        data = {
            'has': names_str,
            'idOnly': id_only
        }
        json_text = json.dumps(data)
        req = urllib2.Request(self.url + 'byText', json_text, self.content_type)
        response = urllib2.urlopen(req)
        result = response.read()
        parsed = json.loads(result)
        return parsed


def test_get_ids():
    client = ProviderProfileServiceClient(None);
    test_ids = ['fb876c21-1da3-48c4-8761-ced53509f37d']
    obj = client.get(test_ids)
    print(json.dumps(obj))


def test_get_names():
    client = ProviderProfileServiceClient(None);
    # names = ['sang','am1480','am1490']
    # names = ['sang', 'am1480', 'congee village']
    names = ['sang']
    obj = client.search_by_name(names)
    print(json.dumps(obj))


def test_get_text():
    client = ProviderProfileServiceClient(None);
    # names = ['sang','am1480','am1490']
    names = ['sang', 'am1480', 'congee village']
    # names = ['sang']
    obj = client.search_by_text(names)
    print(json.dumps(obj))
    obj = client.search_by_text(names, True)
    print(json.dumps(obj))


if __name__ == '__main__':
    # test_get_ids()
    # test_get_names()
    test_get_text()
