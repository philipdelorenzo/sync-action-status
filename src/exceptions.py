# Author: Philip De lorenzo <philip.delorenzo@gmail.com>

class GHTokenNotSet(Exception):
    def __init__(self, message=None, errors=None):            
        # Call the base class constructor with the parameters it needs
        super().__init__(message)

        # Now for your custom code...
        self.errors = errors
        self.message = "GH_TOKEN not set"
