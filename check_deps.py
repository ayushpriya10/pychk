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
                'vulnerable versions': version
            }

def check_dependency(dep_name, dep_version=''):

    '''ADVISORY STRUCTURE:
        [
            {
                'Dependency Name':[
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
        vuln_versions = insecure_deps[dep_name]
        full_output = {
            dep_name: list(),
            "version": dep_version
        }

        for ver in vuln_versions:
            ver_list = [i.strip() for i in ver.split(',')]

            for vuln_ver in ver_list:
                if '<' in vuln_ver and '=' not in vuln_ver:
                    if version.parse(dep_version) < version.parse(vuln_ver[1:]):
                        output_set.add((dep_name, dep_version, vuln_ver))
                        advisory = find_advisory(dep_name, ver)
                        full_output[dep_name] += [advisory]

                if '<=' in vuln_ver:
                    if version.parse(dep_version) <= version.parse(vuln_ver[2:]):
                        output_set.add((dep_name, dep_version, vuln_ver))
                        advisory = find_advisory(dep_name, ver)
                        full_output[dep_name] += [advisory]
                
                if '>' in vuln_ver and '=' not in vuln_ver:
                    if version.parse(dep_version) > version.parse(vuln_ver[1:]):
                        output_set.add((dep_name, dep_version, vuln_ver))
                        advisory = find_advisory(dep_name, ver)
                        full_output[dep_name] += [advisory]
                
                if '>=' in vuln_ver:
                    if version.parse(dep_version) >= version.parse(vuln_ver[2:]):
                        output_set.add((dep_name, dep_version, vuln_ver))
                        advisory = find_advisory(dep_name, ver)
                        full_output[dep_name] += [advisory]
                
                if '==' in vuln_ver:
                    if version.parse(dep_version) == version.parse(vuln_ver[2:]):
                        output_set.add((dep_name, dep_version, vuln_ver))
                        advisory = find_advisory(dep_name, ver)
                        full_output[dep_name] += [advisory]
        
        while None in full_output[dep_name]:
            full_output[dep_name].remove(None)

    if full_output == {}:
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