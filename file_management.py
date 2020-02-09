import sys

def read_from_requirement(path='requirements.txt'):
    requirements = list()

    if path == '.':
        path = 'requirements.txt'

    try:
        with open(path) as requirements_file:
            content = requirements_file.read().split('\n')
            requirements = [dependency.split('==') for dependency in content]

            while [''] in requirements:
                requirements.remove([''])
            
            copy_of_requirements = tuple(requirements)
            for dependency in copy_of_requirements:
                if len(dependency) == 1:
                    if '>=' in dependency[0] or '<=' in dependency[0]:
                        print(f'[MSG] Please specify exact version to check by replacing \'<=\' or \'>=\' with \'==\' for {dependency}.')
                        requirements.remove(dependency)
                        continue

                    if '#' in dependency[0]:
                        if '#' == dependency[0][0]:
                            print(f'[MSG] Skipping commented dependency "{dependency}"')
                            requirements.remove(dependency)
                            continue

                        else:
                            dependency = [dependency[0][:dependency[0].index('#')].strip()]

                    requirements[requirements.index(dependency)] += ['']

                if len(dependency) == 2:
                    if '#' in dependency[0]:
                        if dependency[0][0] == '#':
                            print(f'[MSG] Skipping commented dependency "{dependency}"')
                            requirements.remove(dependency)
                            continue

                    if '#' in dependency[1]:
                        version = dependency[1].split('#')[0].strip()
                        requirements.remove(dependency)
                        dependency = [dependency[0], version]
                        requirements += [dependency]

        return requirements
    
    except FileNotFoundError:
        print(f'[ERR] Could not open "{path}". Please check the path and try again.')
        sys.exit(1)
    
    except:
        print('[ERR] An error occurred while opening requirements file.')
        print(requirements)
        sys.exit(1)


if __name__ == "__main__":
    requirements = read_from_requirement()
    print(requirements)