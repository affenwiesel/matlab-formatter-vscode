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


class Formatter:
    # control sequences
    ctrl_1line = re.compile(r'(\s*)(if|while|for|try)(\W\s*\S.*\W)((end|endif|endwhile|endfor);?)(\s+\S.*|\s*$)')
    fcnstart = re.compile(r'(\s*)(function|classdef)\s*(\W\s*\S.*|\s*$)')
    ctrlstart = re.compile(r'(\s*)(if|while|for|parfor|try|methods|properties|events|arguments|enumeration|spmd)\s*(\W\s*\S.*|\s*$)')
    ctrl_ignore = re.compile(r'(\s*)(import|clear|clearvars)(.*$)')
    ctrlstart_2 = re.compile(r'(\s*)(switch)\s*(\W\s*\S.*|\s*$)')
    ctrlcont = re.compile(r'(\s*)(elseif|else|case|otherwise|catch)\s*(\W\s*\S.*|\s*$)')
    ctrlend = re.compile(r'(\s*)((end|endfunction|endif|endwhile|endfor|endswitch);?)(\s+\S.*|\s*$)')
    linecomment = re.compile(r'(\s*)%.*$')
    ellipsis = re.compile(r'.*\.\.\..*$')
    blockcomment_open = re.compile(r'(\s*)%\{\s*$')
    blockcomment_close = re.compile(r'(\s*)%\}\s*$')
    block_close = re.compile(r'\s*[\)\]\}].*$')
    ignore_command = re.compile(r'.*formatter\s+ignore\s+(\d*).*$')

    # patterns
    p_string = re.compile(r'(.*?[\(\[\{,;=\+\-\*\/\|\&\s]|^)\s*(\'([^\']|\'\')+\')([\)\}\]\+\-\*\/=\|\&,;].*|\s+.*|$)')
    p_string_dq = re.compile(r'(.*?[\(\[\{,;=\+\-\*\/\|\&\s]|^)\s*(\"([^\"])*\")([\)\}\]\+\-\*\/=\|\&,;].*|\s+.*|$)')
    p_comment = re.compile(r'(.*\S|^)\s*(%.*)')
    p_blank = re.compile(r'^\s+$')
    p_num_sc = re.compile(r'(.*?\W|^)\s*(\d+\.?\d*)([eE][+-]?)(\d+)(.*)')
    p_num_R = re.compile(r'(.*?\W|^)\s*(\d+)\s*(\/)\s*(\d+)(.*)')
    p_incr = re.compile(r'(.*?\S|^)\s*(\+|\-)\s*(\+|\-)\s*([\)\]\},;].*|$)')
    p_sign = re.compile(r'(.*?[\(\[\{,;:=\*/\s]|^)\s*(\+|\-)(\w.*)')
    p_colon = re.compile(r'(.*?\S|^)\s*(:)\s*(\S.*|$)')
    p_ellipsis = re.compile(r'(.*?\S|^)\s*(\.\.\.)\s*(\S.*|$)')
    p_op_dot = re.compile(r'(.*?\S|^)\s*(\.)\s*(\+|\-|\*|/|\^)\s*(=)\s*(\S.*|$)')
    p_pow_dot = re.compile(r'(.*?\S|^)\s*(\.)\s*(\^)\s*(\S.*|$)')
    p_pow = re.compile(r'(.*?\S|^)\s*(\^)\s*(\S.*|$)')
    p_op_comb = re.compile(r'(.*?\S|^)\s*(\.|\+|\-|\*|\\|/|=|<|>|\||\&|!|~|\^)\s*(<|>|=|\+|\-|\*|/|\&|\|)\s*(\S.*|$)')
    p_not = re.compile(r'(.*?\S|^)\s*(!|~)\s*(\S.*|$)')
    p_op = re.compile(r'(.*?\S|^)\s*(\+|\-|\*|\\|/|=|!|~|<|>|\||\&)\s*(\S.*|$)')
    p_func = re.compile(r'(.*?\w)(\()\s*(\S.*|$)')
    p_open = re.compile(r'(.*?)(\(|\[|\{)\s*(\S.*|$)')
    p_close = re.compile(r'(.*?\S|^)\s*(\)|\]|\})(.*|$)')
    p_comma = re.compile(r'(.*?\S|^)\s*(,|;)\s*(\S.*|$)')
    p_multiws = re.compile(r'(.*?\S|^)(\s{2,})(\S.*|$)')

    def cellIndent(self, line, cellOpen:str, cellClose:str, indent):
        # clean line from strings and comments
        pattern = re.compile(fr'(\s*)((\S.*)?)(\{cellOpen}.*$)')
        line = self.cleanLineFromStringsAndComments(line)
        opened = line.count(cellOpen) - line.count(cellClose)
        if opened > 0:
            m = pattern.match(line)
            n = len(m.group(2))
            indent = (n+1) if self.matrixIndent else self.iwidth
        elif opened < 0:
            indent = 0
        return (opened, indent)

    def multilinematrix(self, line):
        tmp, self.matrix = self.cellIndent(line, '[', ']', self.matrix)
        return tmp

    def cellarray(self, line):
        tmp, self.cell = self.cellIndent(line, '{', '}', self.cell)
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
    ignoreLines = 0

    def __init__(self, indentwidth, separateBlocks, indentMode, operatorSep, matrixIndent):
        self.iwidth = indentwidth
        self.separateBlocks = separateBlocks
        self.indentMode = indentMode
        self.operatorSep = operatorSep
        self.matrixIndent = matrixIndent

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
            sep = ' ' if self.operatorSep > 0 else ''
            return (m.group(1) + sep, m.group(2) + m.group(3) + m.group(4), sep + m.group(5))

        # .power (.^)
        m = self.p_pow_dot.match(part)
        if m:
            sep = ' ' if self.operatorSep > 0.5 else ''
            return (m.group(1) + sep, m.group(2) + m.group(3), sep + m.group(4))

        # power (^)
        m = self.p_pow.match(part)
        if m:
            sep = ' ' if self.operatorSep > 0.5 else ''
            return (m.group(1) + sep, m.group(2), sep + m.group(3))

        # combined operator (e.g. +=, .+, etc.)
        m = self.p_op_comb.match(part)
        if m:
            # sep = ' ' if m.group(3) == '=' or self.operatorSep > 0 else ''
            sep = ' ' if self.operatorSep > 0 else ''
            return (m.group(1) + sep, m.group(2) + m.group(3), sep + m.group(4))

        # not (~ or !)
        m = self.p_not.match(part)
        if m:
            return (m.group(1) + ' ', m.group(2), m.group(3))

        # single operator (e.g. +, -, etc.)
        m = self.p_op.match(part)
        if m:
            # sep = ' ' if m.group(2) == '=' or self.operatorSep > 0 else ''
            sep = ' ' if self.operatorSep > 0 else ''
            return (m.group(1) + sep, m.group(2), sep + m.group(3))

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
    def indent(self, addspaces=0):
        indnt = ((self.ilvl+self.continueline)*self.iwidth + addspaces)*' '
        return indnt

    # take care of indentation and call format(line)
    def formatLine(self, line):

        if (self.ignoreLines > 0):
            self.ignoreLines -= 1
            return (0, self.indent() + line.strip())

        # determine if linecomment
        if re.match(self.linecomment, line):
            self.islinecomment = 2
        else:
            # we also need to track whether the previous line was a commment
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
        ellipsisInComment = self.islinecomment == 2 or self.isblockcomment
        if re.match(self.block_close, strippedline) or ellipsisInComment:
            self.continueline = 0
        else:
            self.continueline = self.longline
        if re.match(self.ellipsis, strippedline) and not ellipsisInComment:
            self.longline = 1
        else:
            self.longline = 0

        # find comments
        if self.isblockcomment:
            return(0, line.rstrip()) # don't modify indentation in block comments
        if self.islinecomment == 2:
            # check for ignore statement
            m = re.match(self.ignore_command, line)
            if m:
                if m.group(1) and int(m.group(1)) > 1:
                    self.ignoreLines =  int(m.group(1))
                else:
                    self.ignoreLines =  1
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
            return (0, self.indent(-self.iwidth) + m.group(2) + ' ' + self.format(m.group(3)).strip())

        m = re.match(self.ctrlend, line)
        if m:
            if len(self.istep) > 0:
                step = self.istep.pop()
            elif len(self.fstep) > 0:
                step = self.fstep.pop()
            else:
                print('There are more end-statements than blocks!', file=sys.stderr)
                step = 0
            return (-step, self.indent(-step*self.iwidth) + m.group(2) + ' ' + self.format(m.group(4)).strip())

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
    options = dict(startLine=1, endLine=None, indentWidth=4,
                   separateBlocks=True, indentMode='',
                   addSpaces='', matrixIndent='')

    indentModes = dict(all_functions=1, only_nested_functions=-1, classic=0)
    operatorSpaces = dict(all_operators=1, exclude_pow=0.5, no_spaces=0)
    matrixIndentation = dict(aligned=1, simple=0)

    if len(sys.argv) < 2:
        usage = 'usage: matlab_formatter.py filename [options...]\n'
        opt = '  OPTIONS:\n'
        for key in options:
            val = options[key]
            key_type = re.match(r'\<class \'(.*)\'\>', str(type(val))).group(1)
            key_type = key_type.replace('NoneType', 'int')
            opt += '    --%s=%s\n' % (key, key_type)

        print('%s%s' % (usage, opt), file=sys.stderr)

    else:
        for arg in sys.argv[2:]:
            key, value = arg.split('=')
            if any(char.isdigit() for char in value):
                value = int(value)
            elif value.lower() == 'true':
                value = True
            elif value.lower() == 'false':
                value = False
            options[key.strip().strip('-')] = value

        indent = options['indentWidth']
        start = options['startLine']
        end = options['endLine']
        sep = options['separateBlocks']
        mode = indentModes.get(options['indentMode'], indentModes['all_functions'])
        opSp = operatorSpaces.get(options['addSpaces'], operatorSpaces['exclude_pow'])
        matInd = matrixIndentation.get(options['matrixIndent'], matrixIndentation['aligned'])

        formatter = Formatter(indent, sep, mode, opSp, matInd)
        formatter.formatFile(sys.argv[1], start, end)


if __name__ == '__main__':
    main()
