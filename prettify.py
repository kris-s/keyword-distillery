import json
import sys

if len(sys.argv) != 3:
    print 'Usage: python <path/to/ugly.json> <path/to/pretty.json>'
    exit()

def kiss_the_frog(filepath_ugly, filepath_pretty):
    with open(filepath_ugly, 'r') as jsonfile:
        ugly = json.load(jsonfile)

    with open(filepath_pretty, 'w') as jsonfile:
        jsonfile.write(json.dumps(ugly,
                                  sort_keys=True,
                                  indent=4,
                                  separators=(',', ': ')))

kiss_the_frog(str(sys.argv[1]), str(sys.argv[2]))
