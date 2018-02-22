'use strict';
Object.defineProperty(exports, "__esModule", { value: true });
const vscode = require("vscode");
const cp = require("child_process");
const os = require("os");
var channel = null;
const fullRange = doc => doc.validateRange(new vscode.Range(0, 0, Number.MAX_VALUE, Number.MAX_VALUE));
const MODE = { language: 'matlab', scheme: 'file' };
class OperatingSystem {
    constructor(name, file_ext, checker) {
        this.name = name;
        this.file_ext = file_ext;
        this.checker = checker;
    }
}
exports.OperatingSystem = OperatingSystem;
const windows = new OperatingSystem('win32', '.py', 'where');
const linux = new OperatingSystem('linux', '.py', 'which');
const mac = new OperatingSystem('darwin', '.py', 'which');
class MatlabFormatter {
    constructor() {
        this.machine_os = os.platform();
        console.log(this.machine_os);
        this.formatter = vscode.workspace.getConfiguration('matlab-formatter')['path'];
        if (this.machine_os == windows.name) {
            this.formatter = 'python ' + this.formatter;
        }
    }

    formatDocument(document) {
        return new Promise((resolve, reject) => {
            let filename = document.fileName;
            this.format(filename, document).then((res) => {
                return resolve(res);
            });

        });
    }

    format(filename, document) {

        return new Promise((resolve, reject) => {
            showErrorMessage(this.formatter + ' "' + filename + '"');
            cp.exec(this.formatter + ' "' + filename + '"', (err, stdout, stderr) => {
                if (stdout != '') {
                    var edit = [vscode.TextEdit.replace(fullRange(document), stdout)];
                    return resolve(edit);
                }
                return resolve(null);
            });
        });
    }
}
exports.MatlabFormatter = MatlabFormatter;
function showErrorMessage(msg) {
    vscode.window.showErrorMessage(msg);
}
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
