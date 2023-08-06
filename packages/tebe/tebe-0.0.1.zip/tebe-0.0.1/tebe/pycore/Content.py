import os
import tempfile

class Content():
    def __init__(self):
        #----
        self.source_dir_path = '/home/lul/Desktop/SOURCE_TEBE/testst'
    
    def set_source_dir(self, source_dir_path):
        self.source_dir_path = source_dir_path
    
    def has_conf_file(self):
        return False
        