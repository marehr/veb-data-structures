# coding=utf8


def indent(lines, amount, ch=' '):
    padding = amount * ch
    return padding + ('\n'+padding).join(lines.split('\n'))


class Formatter(object):

    @classmethod
    def format(cls, trie):
        root = trie.root or trie

        left_options, right_options = cls._children_format(root)

        d = {
            'left_child': indent(cls._format(root.left), 4),
            'right_child': indent(cls._format(root.right), 4),
            'left_options': ', '.join(left_options),
            'right_options': ', '.join(right_options),
        }

        str_ = """
\\documentclass[tikz,border=10pt]{standalone}
\\usepackage{verbatim}

\\usepackage{ifthen}

\\usepackage{tikz}
\\usetikzlibrary{calc, shapes, backgrounds, trees, decorations.pathmorphing, decorations.pathreplacing, positioning}

\\usepackage{amsmath, amssymb}

\\begin{document}


\\begin{tikzpicture}[
 scale=1.5,
    %% transform shape,
    every node/.style = {
      %%draw,
      color=black
    },
    every edge/.style = {
      none,
      color=black,
      thick, solid
    },
    grow = down,  %% alignment of characters
    sloped,
    level 0/.style = {sibling distance=0},
    level 1/.style = {sibling distance=16cm},
    level 2/.style = {sibling distance=8cm},
    level 3/.style = {sibling distance=4cm},
    level 4/.style = {sibling distance=2cm},
    level 5/.style = {sibling distance=1cm},
    level 6/.style = {sibling distance=0.5cm},
    level 7/.style = {sibling distance=0.25cm},
    level 8/.style = {sibling distance=0.125cm},
    level 9/.style = {sibling distance=0.0625cm},
    minimum size=1pt,
    levels/.style = {
      level distance = #1 * 1cm,
    },
    left-child/.style = {
      rotate=0,
      xscale=1,
      yscale=1,
      above,
    },
    right-child/.style = {
      rotate=0,
      xscale=1,
      yscale=1,
      above,
    }
  ]

  \\tikzset{
    normalnode/.style = {
      circle,
      thick,
      scale = 2,
      minimum size=1pt,
      inner sep=0pt,
      outer sep=0pt,
      %% mark size=1pt,
      color=black,
      fill = black!90!black,
      %% fill = orange!90!blue,
      %% label = center:\\textsf{\\Large H}
    },
    phat-edge/.style = {
      thick, solid,
      color=black
    },
    thin-edge/.style = {
      thin, dotted,
      color=black
    },
    cut-edge/.style = {
      color=red
    },
    join-edge/.style = {
      color=blue
    }
  }

  \\node[normalnode] (Root) {}
  child[%(left_options)s] {
%(left_child)s
  }
  child[%(right_options)s] {
%(right_child)s
  };

\\end{tikzpicture}

\\end{document}
""" % d
        return str_

    @classmethod
    def _children_format(cls, node):
        depth = node.depth() + 1

        depth_left = (node.left and node.left.depth()) or 0
        depth_right = (node.right and node.right.depth()) or 0

        levels_left = max(depth_left - node.depth(), 0)
        levels_right = max(depth_right - node.depth(), 0)

        left_options = []
        right_options = []

        left_options.append("levels=%s" % (levels_left))
        right_options.append("levels=%s" % (levels_right))

        right_options.append("level %s" % (depth))
        left_options.append("level %s" % (depth))

        return [left_options, right_options]

    @classmethod
    def _format(cls, node):
        if node is None:
            return """
node [draw=none] {}
edge from parent [draw=none]
""".strip()

        w = node.key.w
        x = node.key.x

        edgew = node.edge.w
        edgex = node.edge.x
        edge = ('{0:0%db}' % edgew).format(edgex)
        if node.parent.left is node:
            edge = edge[::-1]

        left_options, right_options = cls._children_format(node)

        node_options = ['normalnode']
        if node.left is None and node.right is None:
            node_options.append("label=270:\\scriptsize$%s$" % (node.key.x))

        d = {
            'name': ('{0:0%db}' % w).format(x),
            'edge': edge,
            'left_child': indent(cls._format(node.left), 4),
            'right_child': indent(cls._format(node.right), 4),
            'node_options': ', '.join(node_options),
            'left_options': ', '.join(left_options),
            'right_options': ', '.join(right_options),
        }

        str_ = """
node [%(node_options)s] (Node%(name)s) {}
child[%(left_options)s] {
%(left_child)s
}
child[%(right_options)s] {
%(right_child)s
}
edge from parent
node[above] {\\tiny %(edge)s}
""" % d

        return str_.strip()

if __name__ == '__main__':
    import Trie
    trie = Trie.Tree(5)

    trie.extend([
        # 0b0000,
        # 0b0001,
        # 0b0010,
        # 0b0011,
        # 0b0100,
        # 0b1000,
        # 0b1010,
        # 0b1011

        11 + 0,
        11 + 1,
        11 + 2,
        11 + 3,
        11 + 4,
        11 + 8,
        11 + 10,
        11 + 11

        # 0b101010,
        # 0b010111,
        # 0b111011,
        # 0b100100,
        # 0b011111
        # 0b000000,
        # 0b100010,
        # 0b000100,
        # 0b101010,
        # 0b010111,
        # 0b111011,
        # 0b100100,
        # 0b111110,
        # 0b101100,
        # 0b011000,
        # 0b111110,
        # 0b000001,
        # 0b101011
        # 0b0101101000111011,
        # 0b0111101010010111,
        # 0b0001010010110101,
        # 0b0110100011010001,
        # 0b0101010100000001,
        # 0b1100101010101110,
        # 0b1110001101101010,
        # 0b0010001001100001,
        # 0b0001101011100100,
        # 0b0111100011011101,
        # 0b0100000010000111,
        # 0b1100110011100000,
        # 0b0101010100110111,
        # 0b1000111001111010,
        # 0b0000101100001000,
        # 0b1000001010000011,
        # 0b0010011101100011,
        # 0b1010110101110111,
        # 0b0110100100101001,
        # 0b0011101101101101,
        # 0b0100010000000101,
        # 0b0000101001001101,
        # 0b1011000111100100
    ])

    print Formatter.format(trie)
