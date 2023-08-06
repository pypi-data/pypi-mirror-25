
from Content import Content as _Content
from SphinxBuilder import SphinxBuilder as _SphinxBuilder
from Rst2PdfBuilder import Rst2PdfBuilder as _Rst2PdfBuilder

Content = _Content()
SphinxBuilder = _SphinxBuilder()
Rst2PdfBuilder = _Rst2PdfBuilder()

SphinxBuilder.assign_content_object(Content)