import json
import urllib2
import os
import urllib


class ProfileServiceClient:
    DEFAULT_URL = os.getenv('PROFILE_SVC_URL', 'http://127.0.0.1:8013/profile/');

    def __init__(self, url):
        if url:
            self.url = url
        else:
            self.url = ProfileServiceClient.DEFAULT_URL

    def get(self, ids):
        if not ids:
            return [];
        result = urllib2.urlopen(self.url + 'search?ids=' + ",".join(ids)).read()
        parsed = json.loads(result)
        return parsed

    # TODO end point might not exists on server side
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


if __name__ == '__main__':
    client = ProfileServiceClient();
    test_ids = ['fb876c21-1da3-48c4-8761-ced53509f37d']
    obj = client.get(test_ids)
    print(json.dumps(obj))
