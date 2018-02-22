const vscode = require('vscode');
const fs = require('fs');
const path = require('path');
const childProcess = require('child_process');
const diffMatchPatch = require('diff-match-patch');

class MatlabFormatter {
    constructor() {
        this.statusBar = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left);
    }

    // interface required by vscode.DocumentFormattingEditProvider
    provideDocumentFormattingEdits(document, options, token) {
        return new Promise((resolve, reject) => {
            let formatterPath = vscode.workspace.getConfiguration('matlab-formatter')['path'] || 'python matlab_formatter';

            formatterPath = formatterPath.replace(/\${workspaceRoot}/g, vscode.workspace.rootPath);

            vscode.window.showErrorMessage('here');
            let matlab_formatter = childProcess.execFile(formatterPath, {}, {}, (err, stdout, stderr) => {
                vscode.window.showErrorMessage('error');
                if (err && err.code == 'ENOENT') {
                    vscode.window.showErrorMessage('Can\'t find matlab_formatter. (' + formatterPath + ')');
                    reject(null);
                    return;
                }

                if (err) {
                    vscode.window.showErrorMessage('Failed to launch matlab_formatter. (reason: "' + stderr.split(/\r\n|\r|\n/g).join(',') + '")');
                    reject(null);
                    return;
                }

                let editors = this.generateTextEditors(document, stdout);
                this.updateStatusBar(editors);
                resolve(editors);
            });

            vscode.window.showErrorMessage('matlab_formatter');


            if (matlab_formatter.pid) {
                matlab_formatter.stdin.write(document.getText());
                matlab_formatter.stdin.end();
            }
        });
    }

    generateTextEditors(document, formattedText) {
        let dmp = new diffMatchPatch.diff_match_patch();
        let diffs = dmp.diff_main(document.getText(), formattedText.replace(/\r\n|\r|\n/g, document.eol == 2 ? '\r\n' : '\n'));
        let editors = [];
        let line = 0, character = 0;

        diffs.forEach((diff) => {
            let op = diff[0];
            let text = diff[1];
            let start = new vscode.Position(line, character);
            let lines = text.split(/\r\n|\r|\n/g);

            line += lines.length - 1;

            if (lines.length > 1) {
                character = lines[lines.length - 1].length;
            } else if (lines.length == 1) {
                character += lines[0].length;
            }

            switch (op) {
                case diffMatchPatch.DIFF_INSERT:
                    editors.push(vscode.TextEdit.insert(start, text));
                    // this new part should not affect counting of original document
                    line = start.line;
                    character = start.character;
                    break;
                case diffMatchPatch.DIFF_DELETE:
                    let end = new vscode.Position(line, character);
                    editors.push(vscode.TextEdit.delete(new vscode.Range(start, end)));
                    break;
                case diffMatchPatch.DIFF_EQUAL:
                    break;
            }
        });

        return editors;
    }

    updateStatusBar(editors) {
        if (editors.length == 0) {
            this.statusBar.text = 'No changes';
        } else {
            this.statusBar.text = '$(pencil) Formatted';
        }

        this.statusBar.show();

        setTimeout(() => {
            this.statusBar.hide();
        }, 500);
    }

    dispose() {
        this.statusBar.dispose();
    }
};

// this method is called when your extension is activated
// your extension is activated the very first time the command is executed
function activate(context) {
    let formatter = new MatlabFormatter();
    let disposable = vscode.languages.registerDocumentFormattingEditProvider("matlab", formatter);
    context.subscriptions.push(disposable);
    context.subscriptions.push(formatter);
}

exports.activate = activate;
