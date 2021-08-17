import hashlib
import os
import sys


arg = sys.argv

if not os.path.exists(arg[1]):
    print('The configuration file is not found ')
    sys.exit(0)

if not os.path.exists(arg[2]):
    print('Directory not found')
    sys.exit(0)

file_ini = open(arg[1], 'r')
data_ini = [line.strip() for line in file_ini]
file_ini.close()

for string in data_ini:
    param = str(string).split(' ')

    path_file = os.path.join(arg[2], param[0])
    if os.path.exists(path_file):
        with open(path_file) as file_to_check:
            data_file = file_to_check.read()
            if param[1] == 'sha1':
                hash = hashlib.sha1(data_file.encode('utf-8')).hexdigest()
            elif param[1] == 'sha256':
                hash = hashlib.sha256(data_file.encode('utf-8')).hexdigest()
            elif param[1] == 'md5':
                hash = hashlib.md5(data_file.encode('utf-8')).hexdigest()
            else:
                continue

        # print(f'{param[0]} hash {hash}')
        if hash == param[2]:
            print(f'{param[0]} OK')
        else:
            print(f'{param[0]} FAIL')
    else:
        print(f'{param[0]} NOT FOUND')

input()
