def read_from_requirement(path="requirements.txt"):
    requirements = list()

    with open(path) as requirements_file:
        content = requirements_file.read().split('\n')
        requirements = [dependency.split('==') for dependency in content]
    
    return requirements


if __name__ == "__main__":
    requirements = read_from_requirement()
    print(requirements)