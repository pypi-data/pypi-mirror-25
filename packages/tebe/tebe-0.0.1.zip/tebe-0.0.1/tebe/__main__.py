import sys
import os
import subprocess

from PyQt4 import QtGui, QtCore
from unipath import Path

from gui.dialogs import OpenDialog
from gui.Editor import Editor
from gui.preview import preview
from gui.tree import Tree

import pycore.Core as Core
from pycore.markup_utils import rst_to_html
from pycore.core_utils import abspath

class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        #---
        self.Core = Core
        #---
        self.tree = Tree()
        self.editor = Editor()
        #---
        self.tab_widget = QtGui.QTabWidget()
        self.preview_live = preview()
        self.preview_this = preview()
        self.preview_all = preview()
        self.tab_widget.addTab(self.preview_live, "this page live")
        self.tab_widget.addTab(self.preview_this, "sphinx build this page")
        self.tab_widget.addTab(self.preview_all, "sphinx build index page")

        #---
        splitter = QtGui.QSplitter(QtCore.Qt.Horizontal)
        self.setCentralWidget(splitter)
        splitter.addWidget(self.tree)
        splitter.addWidget(self.editor)
        splitter.addWidget(self.tab_widget)
        #---
        self.setupActions()
        #---
        self.setWindowTitle("Tebe - sphinx writer 0.0.1")
        self.createMenus()
        self.createToolBars()
        self.showMaximized()
        
    def setupActions(self):
        
        # File Menu --------------------------------------------------
        self.openAction = QtGui.QAction(
            QtGui.QIcon(abspath("icons/open_file.png")),
            "Open File",
            self,
            shortcut="Ctrl+O",
            statusTip="Open File",
            triggered=self.openFile
        )

        self.openFolderAction = QtGui.QAction(
            QtGui.QIcon(abspath("icons/open_folder.png")),
            "Open Folder",
            self,
            shortcut="Ctrl+Shift+O",
            statusTip="Open Folder",
            triggered=self.openFolder
        )

        self.saveAction = QtGui.QAction(
            QtGui.QIcon(abspath("icons/save.png")),
            "Save File",
            self,
            shortcut="Ctrl+S",
            statusTip="Save File",
            triggered=self.saveFile
        )

        self.saveAsAction = QtGui.QAction(
            QtGui.QIcon(abspath("icons/save_as.png")),
            "Save As File",
            self,
            shortcut="Ctrl+Shift+S",
            statusTip="Save File As...",
            triggered=self.saveFileAs
        )

        self.quitAction = QtGui.QAction(
            QtGui.QIcon(abspath("icons/quit.png")),
            "Quit",
            self,
            shortcut="Ctrl+Q",
            statusTip="Quit",
            triggered=self.close
        )


        self.buildHTMLAction = QtGui.QAction(
            QtGui.QIcon(abspath("icons/build.png")),
            "Sphinx build",
            self,
            shortcut="Ctrl+B",
            statusTip="Build HTML",
            triggered=self.buildHTML
        )

        self.sphinx_buildPDFAction = QtGui.QAction(
            QtGui.QIcon(abspath("icons/pdf_sphinx.png")),
            "Export to PDF",
            self,
            shortcut="Ctrl+Shift+B",
            statusTip="Build PDF",
            triggered=self.buildPDF
        )

        self.this_buildPDFAction = QtGui.QAction(
            QtGui.QIcon(abspath("icons/pdf_this.png")),
            "Export to PDF",
            self,
            shortcut="Ctrl+Shift+B",
            statusTip="Build PDF",
            triggered=self.build_this_PDF
        )

        self.printAction = QtGui.QAction(
            QtGui.QIcon(abspath("icons/print.png")),
            "Print live preview",
            self,
            shortcut="Ctrl+Shift+P",
            statusTip="Print live preview",
            triggered=self.buildPDF
        )
        
        QtCore.QObject.connect(self.editor, QtCore.SIGNAL("textChanged()"),self.live_update)
        
        # -- Statusbar --
        self.status = self.statusBar()
        
        # -- Window settings --
        self.setWindowIcon(QtGui.QIcon("icons/logo.png"))
        #self.show()


    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("File")
        self.fileMenu.addAction(self.openAction)
        self.fileMenu.addAction(self.openFolderAction)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.saveAction)
        self.fileMenu.addAction(self.saveAsAction)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.quitAction)
        #---
        self.buildMenu = self.menuBar().addMenu("Sphinx build")
        self.buildMenu.addAction(self.buildHTMLAction)
        self.buildMenu.addAction(self.sphinx_buildPDFAction)
        #---
        self.this_buildMenu = self.menuBar().addMenu("This page build")
        self.this_buildMenu.addAction(self.this_buildPDFAction)
        self.this_buildMenu.addAction(self.printAction)
        #---
        self.this_buildMenu = self.menuBar().addMenu("Help")
        

    def createToolBars(self):
        self.fileToolBar = self.addToolBar("File")
        self.fileToolBar.addAction(self.openAction)
        self.fileToolBar.addAction(self.openFolderAction)
        self.fileToolBar.addAction(self.saveAction)
        #--
        self.sphinxbuildToolBar = self.addToolBar("Sphinx build")
        self.sphinxbuildToolBar.addAction(self.buildHTMLAction)
        self.sphinxbuildToolBar.addAction(self.sphinx_buildPDFAction)
        #--
        self.thisbuildToolBar = self.addToolBar("This build")
        self.thisbuildToolBar.addAction(self.printAction)
        self.thisbuildToolBar.addAction(self.this_buildPDFAction)
        
    #---------------------------------
    
    def openFile(self, path=None):
        """
            Ask the user to open a file via the Open File dialog.
            Then open it in the tree, editor, and HTML preview windows.
        """
        if not path:
            dialog = OpenDialog()
            dialog.set_folders_only(False)
            path = dialog.getOpenFileName(
                self,
                "Open File",
                '',
                "ReStructuredText Files (*.rst *.txt)"
            )
        if path:    
            file_path = Path(str(path))
            #---
            selcted_filename = file_path.name
            selcted_dirname = file_path.parent.absolute()
            #---
            self.handleFileChanged(selcted_dirname, selcted_filename)

    def saveFile(self):
        if self.editor.file_path:
            text = self.editor.toPlainText()
            text = str(text)
            try:
                f = open(self.editor.file_path.absolute(), "wb")
                f.write(text)
                f.close()
            except IOError:
                QtGui.QMessageBox.information(
                    self,
                    "Unable to save file: %s" % self.file_path.absolute()
                )
            self.live_update()

    def saveFileAs(self):
        filename = QtGui.QFileDialog.getSaveFileName(
            self,
            'Save File As',
            '',
            "ReStructuredText Files (*.rst *.txt)"
        )
        if filename:
            text = self.editor.toPlainText()
            print text
            text = str(text)
            try:
                f = open(filename, "wb")
                f.write(text)
                f.close()
            except IOError:
                QtGui.QMessageBox.information(
                    self,
                    "Unable to open file: %s" % filename
                )

    def openFolder(self, path=None):
        """
            Ask the user to open a folder (directory) via
            the Open Folder dialog. Then open it in the tree,
            editor, and HTML preview windows.
        """
        if not path:
            dialog = OpenDialog()
            dialog.set_folders_only(True)
            path = dialog.getExistingDirectory(self, "Open Folder", '')
            path = str( path)
        if path:
            self.handleFileChanged(path)

    def handleFileChanged(self, dir, filename=None):
        """
            This is called whenever the active file is changed.
            It sets the tree, editor, and preview panes to the new file.
        """
        
        if not filename:
            filename = "index.rst"
        
        self.Core.Content.set_source_dir(dir)

        # Load the file into the editor
        self.editor.open_file(Path(dir, filename))
        
        # Load the directory containing the file into the tree.
        self.tree.load_from_dir(dir)

        # Update live preview
        self.live_update()
        
        # Update sphinx previews
        self.reload_sphinx_previews()
    
    def reload_sphinx_previews(self):
        
        # Preview all
        index_html_path = os.path.join(Core.SphinxBuilder.tmp_html_dir, 'index.html')
        self.preview_all.show_html(index_html_path)
        
        # Preview this
        this_file_html = self.editor.file_path.name.replace('.rst', '.html')
        this_file_html = this_file_html.replace('.rst', '.html')
        this_file_html = this_file_html.replace('.md', '.html')
        this_file_html_path = os.path.join(Core.SphinxBuilder.tmp_html_dir, this_file_html)
        print this_file_html_path
        self.preview_this.show_html(this_file_html_path)
        
    def buildHTML(self):
        """
        Builds the .html version of the active file and reloads
        it in the preview pane.
        """
        # Build html
        self.cursor_wait(True)
        Core.SphinxBuilder.build_html()
        self.cursor_wait(False)
        # Update sphinx previews
        self.reload_sphinx_previews()
        #---
        print 'buildHTML done'

    def buildPDF(self):
        """
        Builds the .pdf version of the active sphinx filder.
        """
        self.cursor_wait(True)
        Core.SphinxBuilder.build_pdf()
        self.cursor_wait(False)
        #---
        QtGui.QMessageBox.information(None, 'Info', 'Pdf saved as %s'%window.Core.SphinxBuilder.where_pdf_saved)
        
    def build_this_PDF(self):
        """
        Builds the .pdf version of the active file.
        """
        if self.editor.is_rst_file():
            self.cursor_wait(True)
            self.Core.Rst2PdfBuilder.build_pdf_from_rst_file(self.editor.file_path)
            self.cursor_wait(False)
        #---
        QtGui.QMessageBox.information(None, 'Info', 'Pdf saved as %s'%window.Core.Rst2PdfBuilder.where_pdf_saved)

    def cursor_wait(self, wait=False):
        if wait:
            QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        else:
            QtGui.QApplication.restoreOverrideCursor()
            
    def live_update(self):
        markup_text = self.editor.toPlainText()
        markup_text = u'%s'%markup_text
        html = rst_to_html(markup_text)
        
        #---
        window.preview_live.setHtml(html)  
        
def main():
    global app, window
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    #---
    window.preview_live.setHtml('<h3><< Try to write something</h3>')
    #---
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()