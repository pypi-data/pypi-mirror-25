from .truth import TruthMagics
from .pep8 import Pep8Magics
from .tutor import TutorMagics

def load_ipython_extension(ipython):
    """Load the extension in IPython."""
    ipython.register_magics(Pep8Magics)
    ipython.register_magics(TruthMagics)
    ipython.register_magics(TutorMagics)
