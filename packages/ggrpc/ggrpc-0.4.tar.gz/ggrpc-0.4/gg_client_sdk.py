import sys
import traceback

from ggrpc.rpc_client import client_factory


def import_class(import_str):
    """Returns a class from a string including module and class.
    .. versionadded:: 0.3
    """
    mod_str, _sep, class_str = import_str.rpartition('.')
    __import__(mod_str)
    try:
        return getattr(sys.modules[mod_str], class_str)
    except AttributeError:
        raise ImportError('Class %s cannot be found (%s)' %
                          (class_str,
                           traceback.format_exception(*sys.exc_info())))


def main(argv=None):
    if argv is None:
        argv = sys.argv

    kls_path = argv[1]
    if len(argv) > 2:
        opath = argv[2]
    else:
        opath = None

    kls = import_class(kls_path)
    code = client_factory(kls)

    opath = opath or "client_sdk.py"
    with open(opath, 'w') as ofile:
        ofile.write(code)


if __name__ == '__main__':
    sys.exit(main())
