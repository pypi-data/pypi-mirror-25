import fileinput
import re
import sys
import types

import ete2

import phyltr.utils.phyoptparse as optparse

_BEAST_ANNOTATION_REGEX = "([a-zA-Z0-9_ \-]*?):(\[&.*?\])([0-9\.]+)([Ee])?(\-)?([0-9])*"
_BEAST_ANNOTATION_REGEX_2 = "([a-zA-Z0-9_ \-]*?)(\[&.*?\]):([0-9\.]+)([Ee])?(\-)?([0-9])*"
regex1 = re.compile(_BEAST_ANNOTATION_REGEX)
regex2 = re.compile(_BEAST_ANNOTATION_REGEX_2)

class PhyltrCommand:

    def consume(self, stream):
        for tree in stream:
            try:
                res = self.process_tree(tree)
                if res:
                    yield res
            except StopIteration:
                stream.close()
                break
        for tree in self.postprocess():
            yield tree

    def process_tree(self, t):
        return t

    def postprocess(self):
        return []

class ComplexNewickParser:

    def consume(self, stream):

        firstline = True
        for line in stream:
            # Skip blank lines
            if not line:
                continue
            
            # Detect Nexus file format by checking first line
            if firstline:
                if line.strip() == "#NEXUS":
                    isNexus = True
                    inTranslate = False
                    nexus_trans = {}
                else:
                    isNexus = False
                firstline = False

            # Detect beginning of Nexus translate block
            if isNexus and "translate" in line.lower():
                inTranslate = True
                continue

            # Handle Nexus translate block
            if isNexus and inTranslate:
                # Detect ending of translate block...
                if line.strip() == ";":
                    inTranslate = False
                # ...or handle a line of translate block
                else:
                    if line.strip().endswith(";"):
                        line = line[:-1]
                        inTranslate = False
                    index, name = line.strip().split()
                    if name.endswith(","):
                        name = name[:-1]
                    nexus_trans[index] = name

            # Try to find a likely tree on this line and extract it
            if (
                    ")" in line and
                    ";" in line and
                    line.count("(") == line.count(")")
               ):
                # Smells like a tree!
                start = line.index("(")
                end = line.rindex(";") + 1
                tree_string = line[start:end]
                t = get_tree(tree_string)
                if not t:
                    continue
                if isNexus and nexus_trans:
                    for node in t.traverse():
                        if node.name and node.name in nexus_trans:
                            node.name = nexus_trans[node.name]
                yield t

def get_tree(tree_string):
    # FIXME
    # Make this much more elegant
    # Also, once a successful parse is achieved, remember the strategy and avoid brute force on subsequent trees

    # Do we need regex magic?
    if "[&" in tree_string and "&&NHX" not in tree_string:
        tree_string = regex1.sub(repl, tree_string)
        if "NHX" not in tree_string:
            tree_string = regex2.sub(repl, tree_string)

    # Try to parse tree as is
    try:
        t = ete2.Tree(tree_string)
        return t
    except (ValueError,ete2.parser.newick.NewickError):
        pass

    # Try to parse tree with internal node labels
    try:
        t = ete2.Tree(tree_string, format=1)
        return t
    except (ValueError,ete2.parser.newick.NewickError):
        # That didn't fix it.  Give up
        return None

def repl(m):
    name, annotation, dist = m.groups()[0:3]
    if len(m.groups()) > 3:
        # Exponential notation
        dist += "".join([str(x) for x in m.groups()[3:] if x])
    dist = float(dist)
    if annotation:
        bits = annotation[2:-1].split(",")
        # Handle BEAST's "vector annotations"
        # (comma-separated elements inside {}s)
        # by replacing the commas with pipes
        # (this approach subject to change?)
        newbits = []
        inside = False
        for bit in bits:
            if inside:
                newbits[-1] += "|" + bit
                if "}" in bit:
                    inside = False
            else:
                newbits.append(bit)
                if "{" in bit:
                    inside = True
        annotation = "[&&NHX:%s]" % ":".join(newbits)
    return "%s:%f%s" % (name, dist, annotation)

class NewickParser:

    def consume(self, stream):
        for tree_string in stream:
            # Try to parse tree as is
            try:
                t = ete2.Tree(tree_string)
                yield t
                continue
            except (ValueError,ete2.parser.newick.NewickError):
                pass

            # Try to parse tree with internal node labels
            try:
                t = ete2.Tree(tree_string, format=1)
                yield t
            except (ValueError,ete2.parser.newick.NewickError):
                # That didn't fix it.  Give up
                continue

class NewickFormatter:

    def __init__(self, out):
        self.out = out

    def consume(self, stream):
        for t in stream:
            self.out.write(t.write(features=[],format_root_node=True))
            self.out.write("\n")

class StringFormatter:

    def __init__(self, out):
        self.out = out

    def consume(self, stream):
        for x in stream:
            if isinstance(x, types.StringTypes):                self.our.write(x)
            else:
                try:
                    self.out.write("\n".join((str(element) for element in x)))
                except TypeError:
                    self.out.write(str(x))
            self.out.write("\n")

class ListPerLineFormatter:

    def __init__(self, out):
        self.out = out

    def consume(self, stream):
        for lst in stream:
            print("\n".join(lst))

def plumb(command, files="-"):
    source = fileinput.input(files)
    trees_from_stdin = NewickParser().consume(source)
    output_trees = command.consume(trees_from_stdin)
    NewickFormatter(sys.stdout).consume(output_trees)

def complex_plumb(command, files="-"):
    source = fileinput.input(files)
    trees_from_stdin = ComplexNewickParser().consume(source)
    output_trees = command.consume(trees_from_stdin)
    NewickFormatter(sys.stdout).consume(output_trees)

def plumb_strings(command, files="-"):
    source = fileinput.input(files)
    trees_from_stdin = NewickParser().consume(source)
    output_trees = command.consume(trees_from_stdin)
    StringFormatter(sys.stdout).consume(output_trees)

def plumb_list(command, files="-"):
    source = fileinput.input(files)
    trees_from_stdin = NewickParser().consume(source)
    output_lists = command.consume(trees_from_stdin)
    ListPerLineFormatter(sys.stdout).consume(output_lists)
