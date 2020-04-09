# Change Log
All notable changes to the "matlab-formatter" extension will be documented in this file.

### 2.5.1
bugfix: keep spaces between expressions

### 2.5.0
feature: pipe python error to vs-code error message (credits to AlexanderLieret)
add support for utf-8 (credits to wuyudi)
bugfix: correct handling of non-comma-separated vectors and matrices
bugfix: correct treatment of identifiers with names containing 'end'

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
