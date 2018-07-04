# Change Log
All notable changes to the "matlab-formatter" extension will be documented in this file.

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
