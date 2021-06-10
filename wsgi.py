import sys
import os
from App.routes import create_backend

sys.path.append(os.path.abspath(os.curdir))

application = create_backend()
#application.run()
