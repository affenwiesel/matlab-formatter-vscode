'use strict';
Object.defineProperty(exports, "__esModule", { value: true });
const vscode = require("vscode");
const cp = require("child_process");
const os = require("os");
var channel = null;
const fullRange = doc => doc.validateRange(new vscode.Range(0, 0, Number.MAX_VALUE, Number.MAX_VALUE));
const MODE = { language: 'matlab', scheme: 'file' };

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
            let filename = ' "' + document.fileName + '"';
            let start = " --startLine=" + (range.start.line + 1);
            let end = " --endLine=" + (range.end.line + 1);
            cp.exec(formatter + filename + indentwidth + start + end, (err, stdout, stderr) => {
                if (stdout != '') {
                    let toreplace = document.validateRange(new vscode.Range(range.start.line, 0, range.end.line + 1, 0));
                    var edit = [vscode.TextEdit.replace(toreplace, stdout)];
                    return resolve(edit);
                }
                if (stderr != '') {
                    vscode.window.showErrorMessage('formatting error: '+stderr);
                    return resolve(null);
                }
                vscode.window.showErrorMessage('formatting failed');
                return resolve(null);
            });
        });
    }
}

exports.MatlabFormatter = MatlabFormatter;

class MatlabDocumentRangeFormatter {
    constructor() {
        this.formatter = new MatlabFormatter();
    }
    provideDocumentFormattingEdits(document, options, token) {
        return document.save().then(() => {
            return this.formatter.formatDocument(document, fullRange(document));
        });
    }
    provideDocumentRangeFormattingEdits(document, range, options, token) {
        return document.save().then(() => {
            return this.formatter.formatDocument(document, range);
        });
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
