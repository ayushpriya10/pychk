import json
import pprint

import custom_parser

def scan(path, json_output=False, out_file=None):
    from file_management import read_from_requirement
    requirements = read_from_requirement(path)

    from check_deps import check_dependency

    complete_advisory = list()
    for req in requirements:
        try:
            output_set, full_output = check_dependency(dep_name=req[0], dep_version=req[1])
    
            if full_output != None:
                complete_advisory.append(full_output)

        except:
            print('[ERR] An error occurred while scanning for vulnerable dependencies.')
        
    if out_file != None:
        with open(out_file, 'w') as out_file_handler:
            try:
                out_file_handler.write(json.dumps(complete_advisory))
                print(f'[INFO] Wrote the advisory JSON to \'{out_file}\' successfully.')
            except:
                print(f'[ERR] Could not write to \'{out_file}\'. Please try again.')
    else:
        pprint.pprint(complete_advisory)
    
    return complete_advisory



if __name__ == "__main__":
    parser = custom_parser.Parser()

    parser.add_argument(
        '-p',
        '--path',
        help='Path to requirements.txt file. By default, Pychk looks for requirements.txt in the current directory.'
    )

    parser.add_argument(
        '-o',
        '--out-file',
        help='File path to save output as a JSON. Defaults to saving the JSON in the current directory if no path is specified.'
    )

    args = parser.parse_args()
    if args.path:
        if args.out_file:
            scan(path=args.path, out_file=args.out_file)
        else:
            scan(path=args.path)
    
    else:
        print('[INFO] No path supplied to check. Checking for "requirements.txt" in current directory.')
        if args.out_file:
            scan(path='.', out_file=args.out_file)
        else:
            scan(path='.')
