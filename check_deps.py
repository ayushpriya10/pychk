from packaging import version
from fetch_resources import fetch_jsons

insecure_deps, insecure_deps_full = fetch_jsons()

def find_advisory(dep_name, version):
    advisory_list = insecure_deps_full[dep_name]

    for advisory in advisory_list:
        if advisory['v'] == version:
            return {
                'advisory': advisory['advisory'],
                'cve': advisory['cve'],
                'vulnerable_versions': version
            }

def compare_versions(vuln_ver, dep_version):
    if '<' in vuln_ver and '=' not in vuln_ver:
        if version.parse(dep_version) < version.parse(vuln_ver[1:]):
            return True

    if '<=' in vuln_ver:
        if version.parse(dep_version) <= version.parse(vuln_ver[2:]):
            return True
    
    if '>' in vuln_ver and '=' not in vuln_ver:
        if version.parse(dep_version) > version.parse(vuln_ver[1:]):
            return True
    
    if '>=' in vuln_ver:
        if version.parse(dep_version) >= version.parse(vuln_ver[2:]):
            return True
    
    if '==' in vuln_ver:
        if version.parse(dep_version) == version.parse(vuln_ver[2:]):
            return True
    
    return False

def check_dependency(dep_name, dep_version=''):

    '''
    ADVISORY STRUCTURE:
        [
            {
                'Dependency Name':<Package Name>
                'Advisory List':[
                    {
                        'Advisory': <Advisory Value>,
                        'Vulnerable Version': <Version Value>
                    }, ...
                ],
                'Dependency Version': <Version Value>
            }, ...
        ]
    '''

    output_set = set()
    full_output = dict()

    if dep_version == '':
        print(f'[ERR] Please specify version to check if "{dep_name}" is vulnerable.')
        return None
    
    if dep_name in insecure_deps:
        # full_output['Dependency Name'] = dep_name
        # full_output['Advisory List'] = list()
        # print(full_output)
        vuln_versions = insecure_deps[dep_name]
        full_output = {
            'package_name': dep_name,
            'advisory_list': list(),
            "package_version": dep_version
        }

        for ver in vuln_versions:
            ver_list = [i.strip() for i in ver.split(',')]

            for vuln_ver in ver_list:

                if len(ver_list) != 2:
                    if compare_versions(vuln_ver, dep_version):
                        output_set.add((dep_name, dep_version, vuln_ver))
                        advisory = find_advisory(dep_name, ver)
                        # print(full_output)
                        full_output['advisory_list'] += [advisory]

                if len(ver_list) == 2:
                    if compare_versions(ver_list[0], dep_version) and compare_versions(ver_list[1], dep_version):
                        output_set.add((dep_name, dep_version, vuln_ver))
                        advisory = find_advisory(dep_name, ver)
                        full_output['advisory_list'] += [advisory]
                        break
        
        while None in full_output['advisory_list']:
            full_output['advisory_list'].remove(None)
    
    if full_output == {} or full_output['advisory_list'] == []:
        return (output_set, None)

    return (output_set, full_output)


if __name__ == "__main__":

    # '<' type versions
    check_dependency('aiohttp', '0.16.1') #True
    check_dependency('aiohttp', '0.16.3') #False
    check_dependency('aiohttp', '10.0.0') #False

    # '<=' type versions
    check_dependency('conference-scheduler-cli', '0.10.1') #True
    check_dependency('conference-scheduler-cli', '0.10.0') #True
    check_dependency('conference-scheduler-cli', '0.10.2') #False

    # '>' type versions
    check_dependency('setup-tools', '-1') #True
    check_dependency('setup-tools', '0') #False
    check_dependency('setup-tools', '1') #True

    # '>=' type version
    check_dependency('kinto-dist', '6.0.0') #True
    check_dependency('kinto-dist', '6.0.1') #True
    check_dependency('cryptography', '2.2.0') #True
    check_dependency('kinto-dist', '9.0.0') #True

    # '==' type version
    check_dependency('django', '1.8.14') #True
    check_dependency('django', '2.0.9') #True
    check_dependency('plone', '3.3.2') #True

    # Misc. type version
    check_dependency('marshmallow', '2.15') #True

    # Breaking cases
    check_dependency('Random Package')

    # Functional Testing for compare_version()
    print(compare_versions('>=2.1', '2.4.0'), compare_versions('<=2.5.3', '2.4.0')) # True, True