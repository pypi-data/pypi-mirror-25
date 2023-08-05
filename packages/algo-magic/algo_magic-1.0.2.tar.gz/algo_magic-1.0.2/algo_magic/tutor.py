from IPython.core.magic import Magics, magics_class, line_cell_magic
from IPython.display import HTML, display
import urllib
import re

@magics_class
class TutorMagics(Magics):

    @line_cell_magic
    def tutor(self, line, cell=None):
        """
        Python Tutor IPython magic extension

        Magic methods:
            %%tutor 
            < python code ... >
    
            %tutor filename

            %%tutor 640x400
            < python code ... >
    
            %tutor 640x400 filename
        """
        (width, height, filename) = (None, None, None)
        source = cell
        m = re.match(r" *(?:(\d+).(\d+))? *(.*)", line)
        if m:
            (width, height, filename) = m.groups()
            if filename:
                source = open(filename).read()
            else:
                source = cell
        if not width or not height:
            (width, height) = (800, 500)
        code = urllib.parse.urlencode({"code": source})
        display(HTML('<iframe width="%s" height="%s" frameborder="0" src="http://pythontutor.com/iframe-embed.html#%s&py=3"></iframe>' % (width, height, code)))
