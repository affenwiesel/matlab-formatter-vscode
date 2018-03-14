#!/usr/bin/env python3
import re
import sys

# divide string into three parts by extracting and formatting certain expressions
def extract(part):
    # string
    m = re.match(r'(^|.*[\(\[\{,;=\+])\s*(\'.*\')\s*(\S.*|$)', part)
    if m:
        return (m.group(1), m.group(2), m.group(3))

    # comment
    m = re.match(r'(^|.*\S)\s*(%.*)', part)
    if m:
        return (m.group(1), m.group(2), '')

    # decimal number
    m = re.match(r'(^|.*[^\d\.]|.*\s)\s*(\d+\.?\d*)([eE][+-]?)(\d+)\s*(\S.*|$)', part)
    if m:
        return (m.group(1) + ' ' + m.group(2), m.group(3), m.group(4) + ' ' + m.group(5))

    # rational number
    m = re.match(r'(^|.*[^\d\.]|.*\s)\s*(\d+\.?\d*)\s*(\/)\s*(\d+\.?\d*)\s*(\S.*|$)', part)
    if m:
        return (m.group(1) + ' ' + m.group(2), m.group(3), m.group(4) + ' ' + m.group(5))

    # signum
    m = re.match(r'(^|.*[\(\[\{,;:])\s*(\+|\-)\s*(\S.*|$)', part)
    if m:
        return (m.group(1), m.group(2), m.group(3))

    # incrementor
    m = re.match(r'(^|.*\S)\s*(\+|\-)\s*(\+|\-)\s*([\)\]\},;].*|$)', part)
    if m:
        return (m.group(1), m.group(2) + m.group(3), m.group(4))

    # not
    m = re.match(r'(^|.*\S)\s*(!|~)\s*(\S.*|$)', part)
    if m:
        return (m.group(1), m.group(2), m.group(3))

    # colon
    m = re.match(r'(^|.*\S)\s*(:)\s*(\S.*|$)', part)
    if m:
        return (m.group(1), m.group(2), m.group(3))

    # .power
    m = re.match(r'(^|.*\S)\s*(\.)\s*(\^)\s*(\S.*|$)', part)
    if m:
        return (m.group(1), m.group(2) + m.group(3), m.group(4))

    # power
    m = re.match(r'(^|.*\S)\s*(\^)\s*(\S.*|$)', part)
    if m:
        return (m.group(1), m.group(2), m.group(3))

    # 2 operators
    m = re.match(r'(^|.*\S)\s*(\.|\+|\-|\*|\\|/|=|<|>|\||\&)\s*(<|>|=|\+|\-|\*|\&|\|)\s*(\S.*|$)', part)
    if m:
        return (m.group(1) + ' ', m.group(2) + m.group(3), ' ' + m.group(4))

    # 1 operator
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
def format(part):
    m = extract(part)
    if m:
        return format(m[0]) + m[1] + format(m[2])
    return part


# take care of indentation and call format(line)
def formatLine(ilvl, iwidth, line):
    ctrlstart = r'(^|\s*)(function|if|while|for|switch)\s*(\S.*|$)'
    ctrlcont = r'(^|\s*)(elseif|else|case|catch|otherwise)\s*(\S.*|$)'
    ctrlend = r'(^|\s*)(end|endfunction|endif|endwhile|endfor|endswitch)\s*(\S.*|$)'

    width = iwidth*' '

    m = re.match(ctrlstart, line)
    if m:
        return (ilvl+1, ilvl*width + m.group(2) + ' ' + format(m.group(3)).rstrip())

    m = re.match(ctrlcont, line)
    if m:
        return (ilvl, (ilvl-1)*width + m.group(2) + ' ' + format(m.group(3)).rstrip())

    m = re.match(ctrlend, line)
    if m:
        return (ilvl-1, (ilvl-1)*width + m.group(2) + ' ' + format(m.group(3)).rstrip())

    return (ilvl, ilvl*width + format(line).strip())


def main(filename, indentwidth, start, end):
    indent_new = 0
    wlines = rlines = []
    blank = True
    with open(filename, 'r') as f:
        rlines = f.readlines()[start:end]

    # get initial indent lvl
    p = r'(\s*)(.*)'
    m = re.match(p, rlines[0])
    if m:
        indent_new = len(m.group(1))//indentwidth
        rlines[0] = m.group(2)

    for line in rlines:
        # remove additional newlines
        if re.match(r'^\s*$', line):
            if not blank:
                blank = True
                wlines.append('')
            continue

        # format line
        indent = indent_new
        (indent_new, line) = formatLine(indent, indentwidth, line)

        # add newline before block
        if indent < indent_new and not blank:
            wlines.append('')

        # add formatted line
        wlines.append(line)

        # add newline after block
        if (indent > indent_new):
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


if __name__ == '__main__':
    argc = len(sys.argv)
    if argc < 2:
        print('usage: matlab_formatter.py filename [indentwidth] [startLine endLine]', file=sys.stderr)
    else:
        indent = 4
        if argc > 2:
            indent = int(sys.argv[2])
        start = 0
        end = -1
        if argc > 4:
            start = int(sys.argv[3]) - 1
            end = int(sys.argv[4])
        main(sys.argv[1], indent, start, end)
