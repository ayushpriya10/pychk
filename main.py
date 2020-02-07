import custom_parser

def scan(path, verbose=False):
    from file_management import read_from_requirement
    requirements = read_from_requirement(path)

    from check_deps import check_dependency

    for req in requirements:
        try:
            output_set = check_dependency(dep_name=req[0], dep_version=req[1])
            if output_set:
                print()
                for output in output_set:
                    print(output)

        except:
            print('[ERR] An error occurred while scanning for vulnerable dependencies.')


if __name__ == "__main__":
    parser = custom_parser.Parser()

    parser.add_argument(
        '-p',
        '--path',
        help='Path to requirements.txt file. By default, Pychk looks for requirements.txt in the current directory.'
    )

    parser.add_argument(
        '--json',
        default="JSON",
        help='Print output in JSON format.'
    )

    parser.add_argument(
        '-o',
        '--out-file',
        default='.',
        help='File path to save output as a JSON. Defaults to saving the JSON in the current directory if no path is specified.'
    )

    # parser.add_argument(
    #     '-v',
    #     '--verbose',
    #     help='Enable verbose output logging.'
    # )

    args = parser.parse_args()

    if args.path:
        scan(path=args.path)
    
    else:
        print('[INFO] No path supplied to check. Checking for "requirements.txt" in current directory.')
        scan(path='.')

    # args.out_file