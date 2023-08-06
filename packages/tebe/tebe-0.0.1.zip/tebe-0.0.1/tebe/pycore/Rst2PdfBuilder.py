
import os
import subprocess

import core_utils

class Rst2PdfBuilder():
    def __init__(self):
        #---
        self.confdir = core_utils.abspath('pycore/rst2pdf_conf_template')
        self.where_pdf_saved = None

    def build_pdf_from_rst_file(self, source_rst_filname_path):
        self.where_pdf_saved = None
        #---
        out_pdf_filname_path = source_rst_filname_path.replace('.rst', '.pdf')
        print out_pdf_filname_path
        proc = subprocess.Popen([   'rst2pdf',
                                    source_rst_filname_path,
                                    out_pdf_filname_path        ])
        proc.wait()
        #---
        self.where_pdf_saved = out_pdf_filname_path 
        print 'Rst2PdfBuilder build_pdf done'

if __name__ == "__main__":
    Builder = Rst2PdfBuilder()
    Builder.build_pdf_from_rst_file('/home/lul/Dropbox/PYAPPS_STRUCT/SOURCE_TEBE/example_rst_documentaion/features.rst')