import os
import sys
import shlex

def get_script_path():
    return os.path.dirname(os.path.realpath(sys.argv[0]))

_p = sys.platform
if _p.startswith('linux'):
    bin_path = 'linux'
elif _p == 'darwin':
    bin_path = 'osx'
elif _p == 'win32':
    bin_path = 'windows'
bin_path = os.path.join(os.path.dirname(get_script_path()), 'bin', bin_path, 'moxel')
print('bin_path', bin_path)
print(os.path.realpath('.'))

def main():
    cmd = ('{} ' * (len(sys.argv))).format(bin_path, *[shlex.quote(arg) for arg in sys.argv[1:]])
    os.system(cmd)
