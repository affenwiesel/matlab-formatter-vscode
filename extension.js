/*
    This file is part of matlab - formatter - vscode
    Copyright(C) 2019 - 2023 Benjamin "Mogli" Mann

    This program is free software: you can redistribute it and / or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
        (at your option) any later version.

    This program is distributed in the hope that it will be useful,
        but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.See the
    GNU General Public License for more details.

        You should have received a copy of the GNU General Public License
    along with this program.If not, see < http: //www.gnu.org/licenses/>.
*/

'use strict';
Object.defineProperty(exports, "__esModule", { value: true });
const vscode = require("vscode");
const cp = require("child_process");
const stream = require('stream');
const os = require("os");
var channel = null;
const fullRange = doc => doc.validateRange(new vscode.Range(0, 0, Number.MAX_VALUE, Number.MAX_VALUE));
const MODE = { language: 'matlab' };

class MatlabFormatter {
    constructor() {
        this.machine_os = os.platform();
        console.log(this.machine_os);
        this.py = '';
        if (this.machine_os == 'win32') {
            this.py = 'python ';
        }
        this.formatter = '"'+ __dirname + '/formatter/matlab_formatter.py"';
    }

    formatDocument(document, range) {
        return new Promise((resolve, reject) => {
            this.format(document, range).then((res) => {
                return resolve(res);
            });

        });
    }

    format(document, range) {
        return new Promise((resolve, reject) => {
            let indentwidth = " --indentWidth=" + vscode.workspace.getConfiguration('matlab-formatter')['indentwidth'];
            let separateBlocks = " --separateBlocks=" + vscode.workspace.getConfiguration('matlab-formatter')['separateBlocks'];
            let indentMode = " --indentMode=" + vscode.workspace.getConfiguration('matlab-formatter')['indentMode'];
            let addSpaces = " --addSpaces=" + vscode.workspace.getConfiguration('matlab-formatter')['addSpaces'];
            let matrixIndent = " --matrixIndent=" + vscode.workspace.getConfiguration('matlab-formatter')['matrixIndent'];
            let filename = ' -';
            let start = " --startLine=" + (range.start.line + 1);
            let end = " --endLine=" + (range.end.line + 1);
            var p = cp.exec(this.py + " " + this.formatter + " " + filename + indentwidth + separateBlocks + indentMode + addSpaces + matrixIndent + start + end, (err, stdout, stderr) => {
                if (stdout != '') {
                    let toreplace = document.validateRange(new vscode.Range(range.start.line, 0, range.end.line + 1, 0));
                    var edit = [vscode.TextEdit.replace(toreplace, stdout)];
                    if (stderr != '') {
                        vscode.window.showWarningMessage('formatting warning:\n'+stderr);
                    }
                    return resolve(edit);
                }
                vscode.window.showErrorMessage('formatting failed:\n'+stderr);
                return resolve(null);
            });
            var stdinStream = new stream.Readable();
            stdinStream.push(document.getText());
            stdinStream.push(null);
            stdinStream.pipe(p.stdin);
        });
    }
}

exports.MatlabFormatter = MatlabFormatter;

class MatlabDocumentRangeFormatter {
    constructor() {
        this.formatter = new MatlabFormatter();
    }
    provideDocumentFormattingEdits(document, options, token) {
        return this.formatter.formatDocument(document, fullRange(document));
    }
    provideDocumentRangeFormattingEdits(document, range, options, token) {
        return this.formatter.formatDocument(document, range);
    }
}

function activate(context) {
    channel = vscode.window.createOutputChannel('matlab-formatter');
    const formatter = new MatlabDocumentRangeFormatter();
    context.subscriptions.push(vscode.languages.registerDocumentFormattingEditProvider(MODE, formatter));
    context.subscriptions.push(vscode.languages.registerDocumentRangeFormattingEditProvider(MODE, formatter));
}
exports.activate = activate;
// this method is called when your extension is deactivated
function deactivate() {
}
exports.deactivate = deactivate;
//# sourceMappingURL=extension.js.map
