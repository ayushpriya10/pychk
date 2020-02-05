import json
import requests


def fetch_jsons(verbose=False):
    print('[+] Fetching latest resource files.')

    try:
        insecure_deps = json.loads(requests.get('https://raw.githubusercontent.com/pyupio/safety-db/master/data/insecure.json').content)
        print('[+] Fetched list of Insecure Dependencies.')

        insecure_deps_full = json.loads(requests.get('https://raw.githubusercontent.com/pyupio/safety-db/master/data/insecure_full.json').content)
        print('[+] Fetched list of Security Advisories')

        return insecure_deps, insecure_deps_full
    
    except:
        print('[-] An error occurred while fetching resouce files.')


if __name__ == "__main__":
    insecure_deps, insecure_deps_full =  fetch_jsons()

    for deps in insecure_deps:
        ver_list = insecure_deps[deps]

        for ver in ver_list:
            if len(ver.split(',')) > 2:
                print(ver_list, ver)
