"""

"""
import os


def generate_file_tree(startpath, output_file):
    """

    :param startpath:
    :param output_file:
    :return:
    """
    with open(output_file, 'w') as f:
        for root, dirs, files in os.walk(startpath):
            level = root.replace(startpath, '').count(os.sep)
            indent = '│   ' * level
            if level > 0:
                indent += '├── '
            f.write('{}{}/\n'.format(indent, os.path.basename(root)))
            subindent = '│   ' * (level + 1)
            file_entries = ['{}{}'.format(subindent, file) for file in files]
            f.write('\n'.join(file_entries))
            if file_entries:
                f.write('\n')


start_path = './../apl_aws'
output_file = 'file_tree.txt'

generate_file_tree(start_path, output_file)
