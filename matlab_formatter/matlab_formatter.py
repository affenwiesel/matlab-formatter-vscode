#!/usr/bin/env python3

'''
    This file is part of matlab-formatter-vscode
    Copyright(C) 2019-2021 Benjamin "Mogli" Mann

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http: //www.gnu.org/licenses/>.

 '''

import re
import sys
import argparse
import enum 

class Formatter:
    # control sequences
    ctrl_1line = re.compile(r'(^|\s*)(if|while|for|try)(\W\s*\S.*\W)((end|endif|endwhile|endfor);?)(\s+\S.*|\s*$)')
    fcnstart = re.compile(r'(^|\s*)(function|classdef)\s*(\W\s*\S.*|\s*$)')
    ctrlstart = re.compile(r'(^|\s*)(if|while|for|parfor|try|methods|properties|events|arguments|enumeration)\s*(\W\s*\S.*|\s*$)')
    ctrl_ignore = re.compile(r'(^|\s*)(import|clear|clearvars)(.*$)')
    ctrlstart_2 = re.compile(r'(^|\s*)(switch)\s*(\W\s*\S.*|\s*$)')
    ctrlcont = re.compile(r'(^|\s*)(elseif|else|case|otherwise|catch)\s*(\W\s*\S.*|\s*$)')
    ctrlend = re.compile(r'(^|\s*)((end|endfunction|endif|endwhile|endfor|endswitch);?)(\s+\S.*|\s*$)')
    linecomment = re.compile(r'(^|\s*)%.*$')
    ellipsis = re.compile(r'.*\.\.\..*$')
    blockcomment_open = re.compile(r'(^|\s*)%\{\s*$')
    blockcomment_close = re.compile(r'(^|\s*)%\}\s*$')
    block_close = re.compile(r'\s*[\)\]\}].*$')

    # patterns
    p_string = re.compile(r'(^|.*[\(\[\{,;=\+\-\s])\s*(\'([^\']|\'\')+\')([\)\}\]\+\-,;].*|\s+.*|$)')
    p_string_dq = re.compile(r'(^|.*[\(\[\{,;=\+\-\s])\s*(\"([^\"])*\")([\)\}\]\+\-,;].*|\s+.*|$)')
    p_comment = re.compile(r'(^|.*\S)\s*(%.*)')
    p_blank = re.compile(r'^\s+$')
    p_num_sc = re.compile(r'(^|.*\W)\s*(\d+\.?\d*)([eE][+-]?)(\d+)(.*)')
    p_num_R = re.compile(r'(^|.*\W)\s*(\d+)\s*(\/)\s*(\d+)(.*)')
    p_incr = re.compile(r'(^|.*\S)\s*(\+|\-)\s*(\+|\-)\s*([\)\]\},;].*|$)')
    p_sign = re.compile(r'(.*[\(\[\{,;:=\*/\s])\s*(\+|\-)(\w.*)')
    p_colon = re.compile(r'(^|.*\S)\s*(:)\s*(\S.*|$)')
    p_ellipsis = re.compile(r'(^|.*\S)\s*(\.\.\.)\s*(\S.*|$)')
    p_op_dot = re.compile(r'(^|.*\S)\s*(\.)\s*(\+|\-|\*|/|\^)\s*(=)\s*(\S.*|$)')
    p_pow_dot = re.compile(r'(^|.*\S)\s*(\.)\s*(\^)\s*(\S.*|$)')
    p_pow = re.compile(r'(^|.*\S)\s*(\^)\s*(\S.*|$)')
    p_op_comb = re.compile(r'(^|.*\S)\s*(\.|\+|\-|\*|\\|/|=|<|>|\||\&|!|~|\^)\s*(<|>|=|\+|\-|\*|/|\&|\|)\s*(\S.*|$)')
    p_not = re.compile(r'(^|.*\S)\s*(!|~)\s*(\S.*|$)')
    p_op = re.compile(r'(^|.*\S)\s*(\+|\-|\*|\\|/|=|!|~|<|>|\||\&)\s*(\S.*|$)')
    p_func = re.compile(r'(.*\w)(\()\s*(\S.*|$)')
    p_open = re.compile(r'(^|.*)(\(|\[|\{)\s*(\S.*|$)')
    p_close = re.compile(r'(^|.*\S)\s*(\)|\]|\})(.*|$)')
    p_comma = re.compile(r'(^|.*\S)\s*(,|;)\s*(\S.*|$)')
    p_multiws = re.compile(r'(^|.*\S)(\s{2,})(\S.*|$)')

    p_matrixid = re.compile(r'(^|\s*)((\S.*)?)(\[.*$)')
    p_cellid = re.compile(r'(^|\s*)((\S.*)?)(\{.*$)')

    def multilinematrix(self, line):
        line = self.cleanLineFromStringsAndComments(line)
        tmp = line.count('[') - line.count(']')
        if tmp > 0:
            m = self.p_matrixid.match(line)
            p = (len(m.group(2))-self.iwidth/2) // self.iwidth
            self.matrix = int(max(1, p))
        if tmp < 0:
            self.matrix = 0
        return tmp

    def cellarray(self, line):
        # clean line from strings and comments
        line = self.cleanLineFromStringsAndComments(line)
        tmp = line.count('{') - line.count('}')
        if tmp > 0:
            m = self.p_cellid.match(line)
            p = (len(m.group(2))-self.iwidth/2) // self.iwidth
            self.cell = int(max(1, p))
        if tmp < 0:
            self.cell = 0
        return tmp

    # indentation
    ilvl = 0
    istep = []
    fstep = []
    iwidth = 0
    matrix = 0
    cell = 0
    isblockcomment = 0
    islinecomment = 0
    longline = 0
    continueline = 0
    iscomment = 0
    separateBlocks = False

    def __init__(self, indentwidth, separateBlocks, indentMode):
        self.iwidth = indentwidth
        self.separateBlocks = separateBlocks
        self.indentMode = indentMode

    def cleanLineFromStringsAndComments(self, line):
        split = self.extract_string_comment(line)
        if split:
            return self.cleanLineFromStringsAndComments(split[0]) + ' ' + \
                self.cleanLineFromStringsAndComments(split[2])
        else:
            return line

    # divide string into three parts by extracting and formatting certain
    # expressions

    def extract_string_comment(self, part):
        # string
        m = self.p_string.match(part)
        m2 = self.p_string_dq.match(part)
        # choose longer string to avoid extracting subexpressions
        if m2 and (not m or len(m.group(2)) < len(m2.group(2))):
            m = m2
        if m:
            return (m.group(1), m.group(2), m.group(4))

        # comment
        m = self.p_comment.match(part)
        if m:
            self.iscomment = 1
            return (m.group(1) + ' ',  m.group(2), '')

        return 0

    def extract(self, part):
        # whitespace only
        m = self.p_blank.match(part)
        if m:
            return ('', ' ', '')

        # string, comment
        stringOrComment = self.extract_string_comment(part)
        if stringOrComment:
            return stringOrComment

        # decimal number (e.g. 5.6E-3)
        m = self.p_num_sc.match(part)
        if m:
            return (m.group(1) + m.group(2), m.group(3), m.group(4) + m.group(5))

        # rational number (e.g. 1/4)
        m = self.p_num_R.match(part)
        if m:
            return (m.group(1) + m.group(2), m.group(3), m.group(4) + m.group(5))

        # incrementor (++ or --)
        m = self.p_incr.match(part)
        if m:
            return (m.group(1), m.group(2) + m.group(3), m.group(4))

        # signum (unary - or +)
        m = self.p_sign.match(part)
        if m:
            return (m.group(1), m.group(2), m.group(3))

        # colon
        m = self.p_colon.match(part)
        if m:
            return (m.group(1), m.group(2), m.group(3))

        # dot-operator-assignment (e.g. .+=)
        m = self.p_op_dot.match(part)
        if m:
            return (m.group(1) + ' ', m.group(2) + m.group(3) + m.group(4), ' ' + m.group(5))

        # .power (.^)
        m = self.p_pow_dot.match(part)
        if m:
            return (m.group(1), m.group(2) + m.group(3), m.group(4))

        # power (^)
        m = self.p_pow.match(part)
        if m:
            return (m.group(1), m.group(2), m.group(3))

        # combined operator (e.g. +=, .+, etc.)
        m = self.p_op_comb.match(part)
        if m:
            return (m.group(1) + ' ', m.group(2) + m.group(3), ' ' + m.group(4))

        # not (~ or !)
        m = self.p_not.match(part)
        if m:
            return (m.group(1) + ' ', m.group(2), m.group(3))

        # single operator (e.g. +, -, etc.)
        m = self.p_op.match(part)
        if m:
            return (m.group(1) + ' ', m.group(2), ' ' + m.group(3))

        # function call
        m = self.p_func.match(part)
        if m:
            return (m.group(1), m.group(2), m.group(3))

        # parenthesis open
        m = self.p_open.match(part)
        if m:
            return (m.group(1), m.group(2), m.group(3))

        # parenthesis close
        m = self.p_close.match(part)
        if m:
            return (m.group(1), m.group(2), m.group(3))

        # comma/semicolon
        m = self.p_comma.match(part)
        if m:
            return (m.group(1), m.group(2), ' ' + m.group(3))

        # ellipsis
        m = self.p_ellipsis.match(part)
        if m:
            return (m.group(1) + ' ', m.group(2), ' ' + m.group(3))

        # multiple whitespace
        m = self.p_multiws.match(part)
        if m:
            return (m.group(1), ' ', m.group(3))

        return 0

    # recursively format string
    def format(self, part):
        m = self.extract(part)
        if m:
            return self.format(m[0]) + m[1] + self.format(m[2])
        return part

    # compute indentation
    def indent(self, add=0):
        return (self.ilvl+self.continueline+add)*self.iwidth*' '

    # take care of indentation and call format(line)
    def formatLine(self, line):

        # determine if linecomment
        if re.match(self.linecomment, line):
            self.islinecomment = 2
        else:
            self.islinecomment = max(0, self.islinecomment-1)

        # determine if blockcomment
        if re.match(self.blockcomment_open, line):
            self.isblockcomment = float("inf")
        elif re.match(self.blockcomment_close, line):
            self.isblockcomment = 1
        else:
            self.isblockcomment = max(0, self.isblockcomment-1)

        # find ellipsis
        self.iscomment = 0
        strippedline = self.cleanLineFromStringsAndComments(line)
        if re.match(self.block_close, strippedline) or self.islinecomment or self.isblockcomment:
            self.continueline = 0
        else:
            self.continueline = self.longline
        if re.match(self.ellipsis, strippedline) and not self.islinecomment and not self.isblockcomment:
            self.longline = 1
        else:
            self.longline = 0

        # find comments
        if self.isblockcomment:
            return(0, line.rstrip()) # don't modify indentation in block comments
        if self.islinecomment == 2:
            return (0, self.indent() + line.strip())

        # find imports, clear, etc.
        m = re.match(self.ctrl_ignore, line)
        if m:
            return (0, self.indent() + line.strip())

        # find matrices
        tmp = self.matrix
        if self.multilinematrix(line) or tmp:
            return (0, self.indent(tmp) + self.format(line).strip())

        # find cell arrays
        tmp = self.cell
        if self.cellarray(line) or tmp:
            return (0, self.indent(tmp) + self.format(line).strip())

        # find control structures
        m = re.match(self.ctrl_1line, line)
        if m:
            return (0, self.indent() + m.group(2) + ' ' + self.format(m.group(3)).strip() + ' ' + m.group(4) + ' ' + self.format(m.group(6)).strip())

        m = re.match(self.fcnstart, line)
        if m:
            offset = self.indentMode
            self.fstep.append(1)
            if self.indentMode == -1:
                offset = int(len(self.fstep) > 1)
            return (offset, self.indent() + m.group(2) + ' ' + self.format(m.group(3)).strip())

        m = re.match(self.ctrlstart, line)
        if m:
            self.istep.append(1)
            return (1, self.indent() + m.group(2) + ' ' + self.format(m.group(3)).strip())

        m = re.match(self.ctrlstart_2, line)
        if m:
            self.istep.append(2)
            return (2, self.indent() + m.group(2) + ' ' + self.format(m.group(3)).strip())

        m = re.match(self.ctrlcont, line)
        if m:
            return (0, self.indent(-1) + m.group(2) + ' ' + self.format(m.group(3)).strip())

        m = re.match(self.ctrlend, line)
        if m:
            if len(self.istep) > 0:
                step = self.istep.pop()
            elif len(self.fstep) > 0:
                step = self.fstep.pop()
            else:
                print('There are more end-statements than blocks!', file=sys.stderr)
                step = 0
            return (-step, self.indent(-step) + m.group(2) + ' ' + self.format(m.group(4)).strip())

        return (0, self.indent() + self.format(line).strip())

    # format file from line 'start' to line 'end'
    def formatFile(self, filename, start, end):
        # read lines from file
        wlines = rlines = []

        if filename == '-':
            with sys.stdin as f:
                rlines = f.readlines()[start-1:end]
        else:
            with open(filename, 'r', encoding='UTF-8') as f:
                rlines = f.readlines()[start-1:end]

        # take care of empty input
        if not rlines:
            rlines = ['']

        # get initial indent lvl
        p = r'(\s*)(.*)'
        m = re.match(p, rlines[0])
        if m:
            self.ilvl = len(m.group(1))//self.iwidth
            rlines[0] = m.group(2)

        blank = True
        for line in rlines:
            # remove additional newlines
            if re.match(r'^\s*$', line):
                if not blank:
                    blank = True
                    wlines.append('')
                continue

            # format line
            (offset, line) = self.formatLine(line)

            # adjust indent lvl
            self.ilvl = max(0, self.ilvl + offset)

            # add newline before block
            if (self.separateBlocks and offset > 0 and
                    not blank and not self.islinecomment):
                wlines.append('')

            # add formatted line
            wlines.append(line.rstrip())

            # add newline after block
            if self.separateBlocks and offset < 0:
                wlines.append('')
                blank = True
            else:
                blank = False

        # remove last line if blank
        while wlines and not wlines[-1]:
            wlines.pop()

        # take care of empty output
        if not wlines:
            wlines = ['']

        # write output
        for line in wlines:
            print(line)


def main():

    class indentModes(enum.Enum):
        all = 1
        only_nested_functions = -1
        classic = 0

        def __str__(self):
            return self.name

        @staticmethod
        def from_string(s):
            try:
                return indentModes[s]
            except KeyError:
                raise ValueError()

    ap = argparse.ArgumentParser("matlab formatter main script", formatter_class=argparse.RawTextHelpFormatter)
    ap.add_argument("filename", type=str, help="Input file name")
    ap.add_argument("--startLine", type=int, default=1, metavar='', help="")
    ap.add_argument("--endLine", type=int, metavar='', help="")
    ap.add_argument("--indentWidth", type=int, default=4, metavar='', help="number of spaces used for indentation")
    ap.add_argument("--separateBlocks", action="store_true", help="add newlines before and after blocks (for, if, etc.)")
    ap.add_argument("--indentMode", type=indentModes.from_string, choices=list(indentModes), default="all", help=
"""all:                    Add indentation inside all functions and classdefs
only_nested_functions:  Only add indentation inside nested functions and class-methods
classic:                No indentation of functions and classes (not recommended)
""")
    args = ap.parse_args()

    indent = args.indentWidth
    start = args.startLine
    end = args.endLine
    sep = args.separateBlocks
    mode = args.indentMode.value
    formatter = Formatter(indent, sep, mode)
    formatter.formatFile(args.filename, start, end)


if __name__ == '__main__':
    main()
