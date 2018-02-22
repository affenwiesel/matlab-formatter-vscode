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

    formatDocument(document) {
        let name = document.fileName;
        return new Promise((resolve, reject) => {
            this.format(name, document).then((res) => {
                return resolve(res);
            });

        });
    }

    format(filename, document) {
        return new Promise((resolve, reject) => {
            let formatter = vscode.workspace.getConfiguration('matlab-formatter')['path'];
            cp.exec(this.py + formatter + ' "' + filename + '"', (err, stdout, stderr) => {
                if (stdout != '') {
                    var edit = [vscode.TextEdit.replace(fullRange(document), stdout)];
                    return resolve(edit);
                }
                vscode.window.showErrorMessage('path to matlab_formatter not found')
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
            return this.formatter.formatDocument(document);
        });
    }
}

function activate(context) {
    channel = vscode.window.createOutputChannel('matlab-formatter');
    context.subscriptions.push(vscode.languages.registerDocumentFormattingEditProvider(MODE, new MatlabDocumentRangeFormatter()));
}
exports.activate = activate;
// this method is called when your extension is deactivated
function deactivate() {
}
exports.deactivate = deactivate;
//# sourceMappingURL=extension.js.map
