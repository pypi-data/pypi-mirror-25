import io
import re
import sys
import pcpp
import types
from .functions import CFunction
try:
    from pathlib2 import Path
except ImportError:
    from pathlib import Path

template_header = '''\
import {libname}
import cfficloak
lib = cfficloak.cloak({libname})

'''
template_fn = '''\

@cfficloak.function_skeleton(lib)
def {name}({args}):
    """
    {desc}
{params}
    :returns: {rettype}
    """

'''
template_param = '''\
    :param {argtype} {argname}: {argdesc}'''


def generate_function_skeletons(wrappedlib, skeleton_file):

    skeleton_file = Path(skeleton_file)
    functions = {attr : wrappedlib[attr] for attr in wrappedlib if isinstance(wrappedlib[attr], CFunction)}

    if skeleton_file.exists():
        with skeleton_file.open() as handle:
            content = handle.read()
        skels = import_file(skeleton_file)

    else:
        skels = None
        content = template_header.format(libname=wrappedlib.__name__)

    fn_skels = []
    for name, func in functions.items():  # type: str, CFunction
        if not skels or not hasattr(skels, name):
            args = []
            params = []
            for idx, arg in enumerate(func.args):
                argname = "arg%d" % idx
                argtype = ('"%s"' % arg.cname) if ' ' in arg.cname else arg.cname
                params.append(template_param.format(argtype=argtype,
                                                    argname=argname,
                                                    argdesc=str(arg)))
                args.append(argname)
            rettype = 'None' if func.result.cname == 'void' else func.result.cname
            fn_skel = template_fn.format(name=name,
                                         args=', '.join(args),
                                         desc="%s: %s" % (name, str(func.cname)),
                                         params='\n'.join(params),
                                         rettype=rettype)
            fn_skels.append(fn_skel)

    with skeleton_file.open('w') as handle:
        handle.write(content)
        handle.write(''.join(fn_skels))


def import_file(filename):
    """
    Import a module directly from a filename, without touching sys.path
    :param str, Path filename: path to module to import
    :return: module
    """

    PY2 = sys.version_info.major == 2
    if PY2:
        import imp
        mod = imp.load_source('clib', str(filename))
    else:
        import importlib.machinery
        loader = importlib.machinery.SourceFileLoader('clib', str(filename))
        mod = types.ModuleType(loader.name)
        loader.exec_module(mod)
    return mod


# The original _parse_error raises an exception during cdef parsing and
# stops the cdef operation. This will capture the error and let it continue
# trying to parse the rest of the file

# TODO this is completely not thread-safe!
errors = []
# import pycparser.plyparser
# class PLYParser(pycparser.plyparser.PLYParser):
#
#     def _parse_error(self, msg, coord):
#         global errors
#         errors.append((coord, msg))
#
# pycparser.plyparser.PLYParser._parse_error = PLYParser._parse_error
#
# import pycparser.c_parser
# pycparser.c_parser.CParser.p_error = lambda self, x: x

# import pycparser.ply.yacc
# # Utility function to call the p_error() function with some deprecation hacks
# _orig_call_errorfunc = pycparser.ply.yacc.call_errorfunc
# def call_errorfunc(errorfunc, token, parser):
#     try:
#         parser.errorok = True
#         _orig_call_errorfunc(errorfunc, token, parser)
#     except Exception as ex:
#         global errors
#         errors.append(ex)
#     return token
#
# pycparser.ply.yacc.call_errorfunc = call_errorfunc


def parse_header(content=None, filename=None, includes=None):
    """
    Runs the content (if provided) then the read file (if provided)
     through the c preprocessor.
    :param str, bytes content: header content to process
    :param filename: header file to read
    :param list,tuple,set includes: list of include dirs to add to search path
    :return: bytes
    """
    if not any((filename, content)):
        raise ValueError("Must provide filename or content")
    filename = Path(filename)
    content = '\n'.join(((content or ""), filename.read_text()))
    pp = pcpp.Preprocessor()
    pp.add_path(str(Path(__file__).parent / 'include'))
    if includes:
        for include in includes:
            pp.add_path(str(include))
    pp.parse(content)
    out = io.StringIO()
    pp.write(out)
    parsed = out.getvalue()
    parsed = re.sub(r'^\s*#\s*(line|include).*\n', '', parsed, flags=re.MULTILINE)
    return parsed



