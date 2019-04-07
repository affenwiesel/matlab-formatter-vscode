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
        this.py = ''
        if (this.machine_os == 'win32') {
            this.py = 'python ';
        }
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
            let formatter = this.py +'"'+ __dirname + '/formatter/matlab_formatter.py"';
            let indentwidth = " --indentWidth=" + vscode.workspace.getConfiguration('matlab-formatter')['indentwidth'];
            let filename = ' -';
            let start = " --startLine=" + (range.start.line + 1);
            let end = " --endLine=" + (range.end.line + 1);
            var p = cp.exec(formatter + filename + indentwidth + start + end, (err, stdout, stderr) => {
                if (stdout != '') {
                    let toreplace = document.validateRange(new vscode.Range(range.start.line, 0, range.end.line + 1, 0));
                    var edit = [vscode.TextEdit.replace(toreplace, stdout)];
                    if (stderr != '') {
                        vscode.window.showWarningMessage('formatting warning\n'+stderr);
                    }
                    return resolve(edit);
                }
                vscode.window.showErrorMessage('formatting failed\n'+stderr);
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
