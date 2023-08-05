from __future__ import print_function
import sys
import os
from os.path import join, exists, getmtime
import inspect
import types
import re

import chemfp
import chemfp.arena
import chemfp.bitops
import chemfp.fps_io
import chemfp.encodings

## if chemfp.has_toolkit("openbabel"):
##     from chemfp import openbabel_toolkit, openbabel_types, openbabel_patterns

## if chemfp.has_toolkit("openeye"):
##     from chemfp import openeye_toolkit, openeye_types, openeye_patterns

## if chemfp.has_toolkit("rdkit"):
##     from chemfp import rdkit_toolkit, rdkit_types, rdkit_patterns

## name = sys.argv[1]
## template_name = name + ".txt"
## rst_name = name + ".rst"
template_name, rst_name = sys.argv[1:]

from jinja2 import Template, Environment, BaseLoader, TemplateNotFound

seen_functions = {}
seen_classes = {}
seen_methods = {}

def get_obj_by_name(name):
    terms = name.split(".")
    assert terms[0] == "chemfp", name
    del terms[0]
    obj = chemfp
    for term in terms:
        obj = getattr(obj, term)

    ## if isinstance(obj, types.FunctionType):
    ##     seen_functions[name] = obj
    ## elif isinstance(obj, types.ObjectType):
    ##     seen_classes[name] = obj
    ## elif isinstance(obj, types.UnboundMethodType):
    ##     seen_methods[name] = obj
    ## else:
    ##     raise AssertionError(obj)
    seen_functions[name] = obj

    return obj

class LocalDirLoader(BaseLoader):
    def __init__(self):
        self.path = "."
    
    def get_source(self, environment, template):
        path = join(self.path, template)
        if not exists(path):
            raise TemplateNotFound(template)
        mtime = getmtime(path)
        with open(path, "rb") as f:
            source = f.read().decode('utf-8')
        return source, path, lambda: mtime == getmtime(path)
        

def docstring(name):
    obj = get_obj_by_name(name)
    doc = inspect.getdoc(obj)
    if doc is None:
        raise AssertionError("Missing docstring for " + name)
    doc = inspect.cleandoc(inspect.getdoc(obj)).rstrip("\n")
    return doc



# Remove the common part in all of the reader subclasses
def reader_header(name, classname):
    doc = docstring(name)
    lines = doc.splitlines(True)
    new_lines = []
    for line in lines:
        if "The public properties are:" in line:
            line = line.replace("The public properties are:",
                        "This class implements the :class:`chemfp.base_toolkit." + classname + "` API.")
        elif ("The public properties are" in line or
            "* metadata" in line or
            "* location" in line or
            "* closed" in line):
            continue
        new_lines.append(line)

    return "".join(new_lines)

    
def docstring_body(name):
    doc = docstring(name)
    lines = doc.splitlines(True)
    if len(lines) <= 1:
        return ""
    if lines[1].strip():
        raise AssertionError("Why is there a line 2?")
    return "".join(lines[2:])

def doublescore(value):
    return value + u"\n" + u'=' * len(value)

def singlescore(value):
    return value + u"\n" + u'-' * len(value)

def label(name):
    return "_" + name.replace(".", "_")

def get_title(first, second):
    return first or second

def indent3(text):  # indent by 3 spaces
    return "   " + text.replace("\n", "\n   ") + "\n"

def indent5(text):  # indent by 5 spaces
    return "     " + text.replace("\n", "\n     ") + "\n"


_whitespace = re.compile(r"\s+")

def call(name, depth):
    obj = get_obj_by_name(name)
    terms = name.split(".")
    ## if title is not None:
    ##     return terms[-2] + "." + terms[-1] + "() " + title
    
    if isinstance(obj, types.BuiltinFunctionType):
        return obj.__doc__.partition("\n")[0]
    
    source = inspect.getsource(obj)
    assert source, name
    try:
        start = source.index("def ") + 4
        end = source.index(":")
    except ValueError as err:
        raise ValueError(str(err) + " from " + repr(name))

    prefix_terms = terms[-1-depth:-1]
    if 0 and prefix_terms:
        text = ".".join(prefix_terms) + "."  + source[start:end]
    else:
        text = source[start:end]
    #text = terms[-2] + "." + source[start:end]
    text = text.replace("\n", "")
    return _whitespace.sub(" ", text).replace("(self, ", "(").replace("(self)", "()")


def tkname(name):
    left, mid, right = name.partition(".")
    assert left == "chemfp"
    return right

def basename(name):
    left, mid, right = name.rpartition(".")
    return right

def biname(name):  # the last two terms ("binomial name")
    terms = name.split(".")
    return terms[-2] + "." + terms[-1]

def toolkit_title(name):
    # Convert something like "chemfp.toolkit.name" into "toolkit name"
    terms = name.split(".")
    assert len(terms) == 3
    return "%s (%s)" % (terms[2], terms[1])

env = Environment(loader = LocalDirLoader())
env.filters['docstring'] = docstring
env.filters["doublescore"] = doublescore
env.filters["singlescore"] = singlescore
env.filters["label"] = label
env.filters["indent3"] = indent3
env.filters["indent5"] = indent5
env.globals["get_title"] = get_title
env.globals["call"] = call
env.globals["docstring"] = docstring
env.globals["reader_header"] = reader_header
env.globals["docstring_body"] = docstring_body
env.globals["tkname"] = tkname
env.globals["basename"] = basename
env.globals["biname"] = biname
env.globals["toolkit_title"] = toolkit_title

template = env.get_template(template_name)



chemfp_functions = []


page = template.render(
    {"chemfp": chemfp,
     "chemfp_functions": chemfp_functions})


with open(rst_name, "w") as f:
    f.write(page)
