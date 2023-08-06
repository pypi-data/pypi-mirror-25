
import sys
import os
import tempfile
import subprocess
import shutil

from PyQt4 import QtCore, QtGui

import core_utils
from sphinx.application import Sphinx


class SphinxBuilder():
    def __init__(self):
        self.tmp_html_dir = self.__get_tempdir('tebeHTML')
        self.tmp_pdf_dir = self.__get_tempdir('tebePDF')
        self.confdir = core_utils.abspath('pycore/sphinx_conf_template')
        self.Content = None
        #----
        self.where_pdf_saved = None
    
    def __get_tempdir(self, prefix_string):
        dirpath = tempfile.mkdtemp()
        dirname = os.path.basename(dirpath)
        new_dirname = prefix_string + '_' + dirname
        new_dirpath = dirpath.replace(dirname, new_dirname)
        os.rename(dirpath, new_dirpath)
        return new_dirpath
        
    #-----------------------------------------------------
    
    def assign_content_object(self, ContentObject):
        self.Content = ContentObject
        
    #-----------------------------------------------------
    
    @property
    def source_dir_path(self):
        if self.Content:
            return self.Content.source_dir_path
        else:
            return None
    
    #-----------------------------------------------------
    
    '''
    def _build(self, buildername='html'):
        if self.Content.has_conf_file():
            confdir = self.source_dir_path
        else:
            confdir = self.confdir
        #---
        if buildername == 'html':
            outdir = self.tmp_html_dir
            doctreedir = self.tmp_html_dir
        if buildername == 'pdf':
            outdir = self.tmp_pdf_dir
            doctreedir = self.tmp_pdf_dir
        #---
        sphinx_app = Sphinx(    srcdir = self.source_dir_path, 
                                confdir = confdir,
                                outdir = outdir, 
                                doctreedir = self.tmp_html_dir, 
                                buildername = buildername   )
        #---
        sphinx_app.build()  

    def build_html(self):
        if self.source_dir_path:
            self._build('html')
            print 'build_html done'

    def build_pdf(self):
        if self.source_dir_path:
            self._build('pdf')
            print 'build_pdf done'
    '''


    def build_html(self):
        if self.source_dir_path:
            #---
            scrdir = self.source_dir_path
            outdir = self.tmp_html_dir
            #---
            if self.Content.has_conf_file():
                proc = subprocess.Popen([   'sphinx-build', 
                                            '-b', 'html',
                                            scrdir, outdir ])  
            else:
                proc = subprocess.Popen([   'sphinx-build', 
                                            '-b', 'html',
                                            '-c', self.confdir,
                                            scrdir, outdir ])  
            proc.wait()
            print 'build_html done'


    def build_pdf(self):
        self.where_pdf_saved = None
        #---
        for fname in os.listdir(self.tmp_pdf_dir):  
            if  '.pdf' in fname:
                file_pth = os.path.join(self.tmp_pdf_dir, fname)
                os.remove(file_pth)
        #---
        if self.source_dir_path:
            #---
            scrdir = self.source_dir_path
            outdir = self.tmp_pdf_dir
            #---
            if self.Content.has_conf_file():
                proc = subprocess.Popen([   'sphinx-build',
                                            '-b', 'pdf',
                                            scrdir, outdir])
            else:
                proc = subprocess.Popen([   'sphinx-build',
                                            '-b', 'pdf',
                                            '-c', self.confdir,
                                            scrdir, outdir])
            proc.wait()
            #---
            for fname in os.listdir(self.tmp_pdf_dir):  
                if  '.pdf' in fname:
                    scr_file = os.path.join(self.tmp_pdf_dir, fname)
                    dst_file = os.path.join(self.source_dir_path, fname)
                    shutil.copyfile(scr_file, dst_file)
            #---
            self.where_pdf_saved = dst_file
        print 'build_pdf done'

    #-----------------------------------------------------
    
    def delete_tmpdirs(self):
        shutil.rmtree(self.tmp_html_dir)
        shutil.rmtree(self.tmp_pdf_dir)

    def close (self):
        self.delete_tmpdirs()
        self.tmp_html_dir = None
        self.tmp_pdf_dir = None

    def __del__ (self):
        if self.tmp_html_dir:
            self.close()

# Test if main
if __name__ == '__main__':
    from Content import Content
    CONTENT = Content()
    BUILDER = SphinxBuilder()
    BUILDER.assign_content_object(CONTENT)
    
    #BUILDER.assign_content_object(CONTENT)
    #BUILDER.build_html()
    #CONTENT.set_source_dir('/home/lul/Dropbox/PYAPPS_STRUCT/SOURCE_TEBE/testrst/')
    #BUILDER.build_html()
    #BUILDER.build_pdf()