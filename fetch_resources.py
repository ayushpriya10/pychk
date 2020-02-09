import json
import requests
import sys


def fetch_jsons(json_output=False):
    print('[INFO] Fetching latest resource files.')

    try:
        insecure_deps = json.loads(requests.get('https://raw.githubusercontent.com/pyupio/safety-db/master/data/insecure.json').content)
        print('[INFO] Fetched list of Insecure Dependencies.')

        insecure_deps_full = json.loads(requests.get('https://raw.githubusercontent.com/pyupio/safety-db/master/data/insecure_full.json').content)
        print('[INFO] Fetched list of Security Advisories')

        print('[INFO] Fetch complete.')
        return insecure_deps, insecure_deps_full
    
    except:
        print('[ERR] An error occurred while fetching resouce files. Maybe you\'re not connected to the internet?')
        sys.exit(1)


if __name__ == "__main__":
    insecure_deps, insecure_deps_full =  fetch_jsons()

    for deps in insecure_deps:
        ver_list = insecure_deps[deps]

        for ver in ver_list:
            if len(ver.split(',')) > 2:
                print(ver_list, ver)
