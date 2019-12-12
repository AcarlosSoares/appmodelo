#
# Conteudo do arquivo `wsgi.py`
#

python_home = 'C:/Users/carlos.soares.ETICE/.virtualenvs/demo1-F7BoWnH9'
activator = python_home + '/Scripts/activate_this.py'
with open(activator) as f:
    exec(f.read(), {'__file__': activator})

import sys

sys.path.insert(0, "e:/python/demo1")

from app import app as application
