from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division

import os.path

from mercurial.i18n import _
from mercurial import (
    context,
    node as nodemod,
    registrar,
    scmutil,
    util,
)

import pygraphviz

__author__ = """Boris Feld (boris.feld@octobus.net)"""

cmdtable = {}

if util.safehasattr(registrar, 'command'):
    commandfunc = registrar.command
else:  # compat with hg < 4.3
    from mercurial import cmdutil
    commandfunc = cmdutil.command

command = commandfunc(cmdtable)

NORMAL_COLOR = "#7F7FFF"
OBSOLETE_COLOR = "#DFDFFF"

DEFAULT_NODE_ARGS = {
    "fixedsize": "true",
    "width": 2,
    "height": 2,
    'style': "filled",
    'fillcolor': NORMAL_COLOR,
    'shape': "pentagon",
    "pin": "true"
}

PUBLIC_NODE_ARGS = {"shape": "circle"}
DRAFT_NODE_ARGS = {"shape": "pentagon"}
SECRET_NODE_ARGS = {"shape": "square"}

OBSOLETE_NODE_ARGS = {"fillcolor": "#DFDFFF", "style": "dotted, filled"}
ORPHAN_NODE_ARGS = {"fillcolor": "#FF3535"}
PHASE_DIVERGENT_NODE_ARGS = {}
CONTENT_DIVERGENT_NODE_ARGS = ORPHAN_NODE_ARGS
EXTINCT_NODE_ARGS = OBSOLETE_NODE_ARGS

OBSOLETE_EDGES = {"dir": "back", "style": "dotted", "arrowtail": "dot", "minlen": 0}

columns = {}

# Compat for evolve renaming
if not util.safehasattr(context.basectx, 'orphan'):
    context.basectx.orphan = context.basectx.unstable

if not util.safehasattr(context.basectx, 'contentdivergent'):
    context.basectx.contentdivergent = context.basectx.divergent

if not util.safehasattr(context.basectx, 'phasedivergent'):
    context.basectx.phasedivergent = context.basectx.bumped


@command('docgraph', [
        ('', 'rankdir', b'BT', _('randir graph property'), _('DIR')),
        ('r', 'rev', [], _('import up to source revision REV'), _('REV')),
        ('o', 'output', b'hg.png', _('image output filename'), _('OUTPUT')),
        ('', 'dot-output', b'',
         _('dot source output filename'), _('DOTOUTPUT')),
        ('', 'sphinx-directive', False,
         _('output a ".. graphviz" sphinx directive')),
     ],
     _('hg docgraph [OPTION] {REV}'))
def docgraph(ui, repo, *revs, **opts):

    # Get revset
    revs = list(revs) + opts['rev']
    if not revs:
        revs = ['.']
    revs = scmutil.revrange(repo, revs)

    # Create a graph
    graph = pygraphviz.AGraph(strict=True, directed=True)

    # Order from bottom to left
    graph.graph_attr['rankdir'] = opts['rankdir']
    graph.graph_attr['splines'] = "polyline"

    for rev in revs:
        nargs = DEFAULT_NODE_ARGS.copy()
        ctx = repo[rev]

        group = ctx.branch()

        # Phase
        if ctx.phasestr() == "draft":
            nargs.update(DRAFT_NODE_ARGS)
        elif ctx.phasestr() == "public":
            nargs.update(PUBLIC_NODE_ARGS)
        elif ctx.phasestr() == "secret":
            nargs.update(SECRET_NODE_ARGS)
        else:
            assert False

        # Troubles?
        if ctx.orphan():
            nargs.update(ORPHAN_NODE_ARGS)
            group = "%s_alt" % group
        elif ctx.phasedivergent():
            nargs.update(PHASE_DIVERGENT_NODE_ARGS)
            group = "%s_bumped" % group
        elif ctx.contentdivergent():
            nargs.update(CONTENT_DIVERGENT_NODE_ARGS)
            group = "%s_alt" % group
        elif ctx.extinct():
            nargs.update(EXTINCT_NODE_ARGS)
            group = "%s_extinct" % group
        elif ctx.obsolete():
            nargs.update(OBSOLETE_NODE_ARGS)
            group = "%s_alt" % group

        # Add links
        p1 = ctx.p1()
        if p1.rev() in revs:
            graph.add_edge(p1.rev(), rev)

        p2 = ctx.p2()
        if p2 and p2.rev() in revs:
            graph.add_edge(p2.rev(), rev)

        # Obs links
        for obsmakers in repo.obsstore.successors.get(ctx.node(), ()):
            successors = obsmakers[1]

            for successor in successors:
                if successor in repo:
                    successor_rev = repo[successor].rev()
                    if successor_rev in repo:
                        graph.add_edge(rev, successor_rev,
                                       **OBSOLETE_EDGES)

        # Get the position
        if group in columns:
            column = columns[group]
        else:
            max_column = max(columns.values() + [0])
            columns[group] = max_column + 1
            column = max_column + 1

        # Label
        nargs['label'] = "%d: %s" % (rev, nodemod.short(ctx.node()))

        graph.add_node(rev, group=group, pos="%d,%d!" % (column, rev), **nargs)

    dot_output = opts['dot_output']
    if dot_output:
        dot_output = os.path.abspath(dot_output)

        graph.write(dot_output)  # write to simple.dot
        print("Wrote %s" % dot_output)

    sphinx = opts['sphinx_directive']

    if not sphinx:
        output = os.path.abspath(opts['output'])
        graph.draw(output, prog="dot")  # draw to png using dot
        print("Wrote %s" % output)

    if sphinx:
        print(".. graphviz::\n")
        for line in graph.to_string().splitlines():
            print("    " + line)
