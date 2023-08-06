
import os
from imp import reload


# the default resources dir
RESOURCES_DIR = "C:\\packresources"


def init_dir(resources_dir=RESOURCES_DIR):
    """ Make sure RESOURCES_DIR and resources.py exist """
    if not os.path.exists(resources_dir):
        os.makedirs(resources_dir)


def set(resorce_file, target_name=None):
    """
    set the resource file into resources.py
    the resorce_file should be a absolute path or a relative path
    """
    if not os.path.exists(resorce_file):
        print(resorce_file + ' not found!')
        return
    if not target_name:
        target_name = os.path.split(resorce_file)[-1]

    bin_str = open(resorce_file, "rb").read()

    try:
        import resources
        reload(resources)
        res_dict = resources.res_dict
    except ImportError:
        res_dict = {}

    res_dict[target_name] = bin_str
    res_data = repr(res_dict)
    out_str = "res_dict=%s" % res_data

    open("resources.py", "w").write(out_str)


def release(resources_dir=RESOURCES_DIR, cached=False):
    """ release the files in resources.py to resources dir (C:\packresources\) """
    try:
        import resources
        reload(resources)
        res_dict = resources.res_dict
    except ImportError:
        print('resources module not found!')
        res_dict = {}

    init_dir(resources_dir)
    for target_name, bin_str in res_dict.iteritems():
        path = get(target_name, resources_dir, need_release=False)
        if cached and not os.path.exists(path):
            continue
        open(path, "wb").write(bin_str)

    
def get(target_name, resources_dir=RESOURCES_DIR, cached=False, need_release=True):
    """ get target file path in resources dir (C:\packresources\) """
    if need_release:
        release(resources_dir, cached)
    path = os.path.join(resources_dir, target_name)
    if not os.path.exists(path) and need_release:
        return '<not_exists>'
    return path



