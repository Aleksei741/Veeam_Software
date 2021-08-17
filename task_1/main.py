import xml.etree.ElementTree as ET
import os
import shutil

def copy_file():

    tree = ET.parse('config.xml')
    root = tree.getroot()

    for element in root.findall('file'):
        file = element.attrib

        path_source = os.path.join(file['source_path'], file['file_name'])
        path_destination = os.path.join(file['destination_path'], file['file_name'])

        if (os.path.exists(path_source)):
            if (os.path.exists(path_destination)):
                os.remove(path_destination)
                print(f'remove {path_destination}')
            shutil.copy(path_source, path_destination)
            print(f'copy {path_source} {path_destination}')


if __name__ == '__main__':
    copy_file()
