import munch
import varyaml


def get_config(config_path):
    """Reads the given yaml config file and return a munch object.

    :param str config_path: config file path.
    :return munch.Munch: config object.
    """
    return munch.Munch.fromDict(varyaml.load(open(config_path, 'r')))
