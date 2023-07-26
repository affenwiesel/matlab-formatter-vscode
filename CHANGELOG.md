# Change Log

### 2.11.0
important security update:
remove options `pythonPath` and `formatterPath`

### 2.10.5
bugfix: comments before multiline statement

### 2.10.4
add option to customize indentation of matrices/cells

### 2.10.3
bugfix: formatting of strings

### 2.10.2
add support for spmd

### 2.10.1
bugfix: default value addSpaces

### 2.10.0
* add option to customize wrapping of operators with spaces
* add option to switch of formatter for selected lines via comment `% formatter ignore N`

### 2.9.2
bugfix: unary minus at start of line

### 2.9.1
feature: extend indent mode to `classdef`

### 2.9.0
feature: add support for block comments

### 2.8.12
bugfix: `if` statement with attached parenthesis

### 2.8.11
* bugfix: semicolon after `end`
* bugfix: add warning in case of mismatching `begin` and `end` statements

### 2.8.10
bugfix: handle strings containing quotes

### 2.8.9
bugfix: handle empty files correctly

### 2.8.8
* bugfix: operator/assignment issue, e.g., `+=`
* feature: indentation modes (thanks to Arturo Mendoza Quispe for adding this feature)

### 2.8.7
bugfix: comments at end of line starting an `if`/`for`/... block

### 2.8.6
add support for inline try;catch;end block

### 2.8.5
bugfix: python path

### 2.8.4
bugfixes:
* fix formatting of expression clear
* indentation of multiline statements with comments

### 2.8.3
bugfix: comma-less vectors (again...)

### 2.8.2
bugfix:
issue with comments containing quotes

performance:
precompile regular expressions

### 2.8.1
bugfixes:
* brackets in strings and comments
* multiline array at beginning of line

### 2.8.0
features:
* option to set custom path for formatter
* support multiline cell arrays

bugfix: error with multiple spaces after `for`/`if`/etc.

### 2.7.1
bugfix: fix formatting issues with imports

### 2.7.0
add support for arguments and enumeration

### 2.6.0
features:
* option to set custom python path
* option to choose whether (for/if/...) blocks shall be wrapped with empty lines

bugfix: whitespaces (yet again)

### 2.5.2
bugfix: yet another attempt to fix all the spaces between expressions

### 2.5.1
bugfix: keep spaces between expressions

### 2.5.0
features:
* pipe python error to vs-code error message (credits to AlexanderLieret)
* add support for utf-8 (credits to wuyudi)

bugfixes:
* correct handling of non-comma-separated vectors and matrices
* correct treatment of identifiers with names containing 'end'

### 2.4.12
bugfix: correct formatting for strings containing quotes

### 2.4.11
bugfix: correct line break - again

### 2.4.10
bugfix: correct line break

### 2.4.9
bugfix: correct formatting of unary minus

### 2.4.8
bugfix: ignore ellipsis in comments

### 2.4.7
bugfix: remove additional spaces in rational numbers and scientific notation e.g 1/7 or 1.7e42

### 2.4.6
bugfix: correct formatting of identifiers ending on decimal

### 2.4.5
bugfix: exclude non-comma-separated vectors from formatting to prevent negative entries from being converted to subtractions

### 2.4.4
bugfix: correct indentation for multiline matrices

### 2.4.3
bugfix: undo changes from 2.4.2 because they lead to problems with other unicode-characters (e.g. greek letters)

### 2.4.2
bugfix: better support for chinese comments

### 2.4.0
feature: Add indentation after linebreak (`...`)

### 2.3.0
feature: Add support for object oriented Matlab code

### 2.2.3
bugfix: support braces after control keyword e.g. `if()`

### 2.2.2
* bugfix: quoting of shell command
* bugfix: implement formatting of doublequote-strings

### 2.2.1
Remove trailing whitespaces at lineend

### 2.2.0
Call python script relative from extension.js -> Remove now obsolete setting `path`

### 2.1.2
Bugfix: add `parfor` control sequence

### 2.1.1
Improve matrix formatting

### 2.1.0
* Feature: Add better formatting for matrices

* Bugfix: Remove unwanted newlines after block-introducing comment

### 2.0.0
Rewrite the formatter in an object oriented way to implement new features more easily.

### 1.2.1
Bugfix: whitespace after string

### 1.2.0
Feature: Add support for one-line control sequence (if, for, while)

### 1.1.8
Bugfix: Correct indenting of try-catch block

### 1.1.7
Bugfix: Don't break words into block-start-keywords

### 1.1.6
Change default formatter-path to it's default windows location

### 1.1.5
Bugfix: implement support for combined dot-operator + assignment (e.g. .+=)

### 1.1.4
Bugfix: implement support for more combined operators
    Thanks to davidxujiayang for finding this bug and providing a solution!

### 1.1.3
Bugfix: include last line when formatting
    Thanks to fasiha for finding the bug!

### 1.1.2
Bugfix: enable variable indentwidth for format selection

### 1.1.1
Add compatibility for python 3.6

### 1.1.0
New Features:
* format selection
* variable indent width → setting: `matlab-formatter.indentwidth`

### 1.0.1
Bugfix: Removed a remaining debug output that corrupted the output file

### 1.0.0
Initial release of matlab-formatter
