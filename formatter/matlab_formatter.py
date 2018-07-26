#!/usr/bin/env python3
import re
import sys


class Formatter:
    # control sequences
    ctrl_1line = r'(^|\s*)(if|while|for)(\s+\S.*)(end|endif|endwhile|endfor)(\s*$)'
    ctrlstart = r'(^|\s*)(function|if|while|for|try)(\s+\S.*|\s*$)'
    ctrlstart_2 = r'(^|\s*)(switch)(\s+\S.*|\s*$)'
    ctrlcont = r'(^|\s*)(elseif|else|case|otherwise|catch)(\s+\S.*|\s*$)'
    ctrlend = r'(^|\s*)(end|endfunction|endif|endwhile|endfor|endswitch)(\s+\S.*|\s*$)'

    # indentation
    ilvl=0
    istep=0
    iwidth=0

    def __init__(self, indentwidth):
        self.istep=[]
        self.iwidth=indentwidth

    # divide string into three parts by extracting and formatting certain expressions
    def extract(self, part):
        # string
        m = re.match(r'(^|.*[\(\[\{,;=\+\s])\s*(\'[^\']*\')\s*([\)\}\],;].*|\s.*|$)', part)
        if m:
            return (m.group(1), m.group(2), m.group(3))

        # comment
        m = re.match(r'(^|.*\S)\s*(%.*)', part)
        if m:
            return (m.group(1), m.group(2), '')

        # decimal number (e.g. 5.6E-3)
        m = re.match(r'(^|.*[^\d\.]|.*\s)\s*(\d+\.?\d*)([eE][+-]?)(\d+)\s*(\S.*|$)', part)
        if m:
            return (m.group(1) + ' ' + m.group(2), m.group(3), m.group(4) + ' ' + m.group(5))

        # rational number (e.g. 1/4)
        m = re.match(r'(^|.*[^\d\.]|.*\s)\s*(\d+\.?\d*)\s*(\/)\s*(\d+\.?\d*)\s*(\S.*|$)', part)
        if m:
            return (m.group(1) + ' ' + m.group(2), m.group(3), m.group(4) + ' ' + m.group(5))

        # signum (unary - or +)
        m = re.match(r'(^|.*[\(\[\{,;:=])\s*(\+|\-)\s*(\S.*|$)', part)
        if m:
            return (m.group(1), m.group(2), m.group(3))

        # incrementor (++ or --)
        m = re.match(r'(^|.*\S)\s*(\+|\-)\s*(\+|\-)\s*([\)\]\},;].*|$)', part)
        if m:
            return (m.group(1), m.group(2) + m.group(3), m.group(4))

        # colon
        m = re.match(r'(^|.*\S)\s*(:)\s*(\S.*|$)', part)
        if m:
            return (m.group(1), m.group(2), m.group(3))

        # dot-operator-assignmet (e.g. .+=)
        m = re.match(r'(^|.*\S)\s*(\.)\s*(\+|\-|\*|/|\^)\s*(=)\s*(\S.*|$)', part)
        if m:
            return (m.group(1) + ' ', m.group(2) + m.group(3) + m.group(4), ' ' + m.group(5))

        # .power (.^)
        m = re.match(r'(^|.*\S)\s*(\.)\s*(\^)\s*(\S.*|$)', part)
        if m:
            return (m.group(1), m.group(2) + m.group(3), m.group(4))

        # power (^)
        m = re.match(r'(^|.*\S)\s*(\^)\s*(\S.*|$)', part)
        if m:
            return (m.group(1), m.group(2), m.group(3))

        # combined operator (e.g. +=, .+, etc.)
        m = re.match(r'(^|.*\S)\s*(\.|\+|\-|\*|\\|/|=|<|>|\||\&|!|~|\^)\s*(<|>|=|\+|\-|\*|/|\&|\|)\s*(\S.*|$)', part)
        if m:
            return (m.group(1) + ' ', m.group(2) + m.group(3), ' ' + m.group(4))

        # not (~ or !)
        # m = re.match(r'(^|.*\S)\s*(!|~)\s*(\S.*|$)', part)
        # if m:
        #     return (m.group(1), m.group(2), m.group(3))

        # single operator (e.g. +, -, etc.)
        m = re.match(r'(^|.*\S)\s*(\+|\-|\*|\\|/|=|!|~|<|>|\||\&)\s*(\S.*|$)', part)
        if m:
            return (m.group(1) + ' ', m.group(2), ' ' + m.group(3))

        # function call
        m = re.match(r'(.*[A-Za-z0-9_])\s*(\()\s*(\S.*|$)', part)
        if m:
            return (m.group(1), m.group(2), m.group(3))

        # parenthesis open
        m = re.match(r'(^|.*)(\(|\[|\{)\s*(\S.*|$)', part)
        if m:
            return (m.group(1), m.group(2), m.group(3))

        # parenthesis close
        m = re.match(r'(^|.*\S)\s*(\)|\]|\})(.*|$)', part)
        if m:
            return (m.group(1), m.group(2), m.group(3))

        # comma/semicolon
        m = re.match(r'(^|.*\S)\s*(,|;)\s*(\S.*|$)', part)
        if m:
            return (m.group(1), m.group(2), ' ' + m.group(3))

        # multiple whitespace
        m = re.match(r'(^|.*\S)(\s{2,})(\S.*|$)', part)
        if m:
            return (m.group(1), ' ', m.group(3))

        return 0

    # recursively format string
    def format(self, part):
        m = self.extract(part)
        if m:
            return self.format(m[0]) + m[1] + self.format(m[2])
        return part

    # take care of indentation and call format(line)
    def formatLine(self, line):

        width = self.iwidth*' '

        m = re.match(self.ctrl_1line, line)
        if m:
            return (0, self.ilvl*width + m.group(2) + ' ' + self.format(m.group(3)).strip() + ' ' + m.group(4))

        m = re.match(self.ctrlstart, line)
        if m:
            self.istep.append(1)
            return (1, self.ilvl*width + m.group(2) + ' ' + self.format(m.group(3)).strip())

        m = re.match(self.ctrlstart_2, line)
        if m:
            self.istep.append(2)
            return (2, self.ilvl*width + m.group(2) + ' ' + self.format(m.group(3)).strip())

        m = re.match(self.ctrlcont, line)
        if m:
            return (0, (self.ilvl-1)*width + m.group(2) + ' ' + self.format(m.group(3)).strip())

        m = re.match(self.ctrlend, line)
        if m:
            step = self.istep.pop()
            return (-step, (self.ilvl-step)*width + m.group(2) + ' ' + self.format(m.group(3)).strip())

        return (0, self.ilvl*width + self.format(line).strip())

    # format file from line 'start' to line 'end'
    def formatFile(self, filename, start, end):

        # read lines from file
        wlines = rlines = []
        with open(filename, 'r') as f:
            rlines = f.readlines()[start-1:end]

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
            self.ilvl += offset

            # add newline before block
            if offset > 0 and not blank:
                wlines.append('')

            # add formatted line
            wlines.append(line)

            # add newline after block
            if offset < 0:
                wlines.append('')
                blank = True
            else:
                blank = False

        # remove last line if blank
        while wlines and not wlines[-1]:
            wlines.pop()

        # write output
        for line in wlines:
            print(line)


def main():
    options = {'--startLine': 1, '--endLine': None, '--indentWidth': 4}

    if len(sys.argv) < 2:
        print('usage: matlab_formatter.py filename [options...]\n  OPTIONS:\n    --startLine=\\d\n    --endLine=\\d\n    --indentWidth=\\d\n', file=sys.stderr)
    else:
        for arg in sys.argv[2:]:
            key, value = arg.split('=')
            try:
                value = eval(value)
            finally:
                options[key.strip()] = value

        indent = options['--indentWidth']
        start = options['--startLine']
        end = options['--endLine']

        formatter = Formatter(indent)
        formatter.formatFile(sys.argv[1], start, end)

if __name__ == '__main__':
    main()
