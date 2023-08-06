
import sys

this = sys.modules[__name__]

# These global variables are updated by functions in matador.cli.decorators
this.environment = None
this.ticket = None
