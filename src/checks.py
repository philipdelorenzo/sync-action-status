# Author: Philip De lorenzo <philip.delorenzo@gmail.com>

import os
from exceptions import GHTokenNotSet

def check_gh_token() -> None:
    """This function checks to ensure that the GH_TOKEN environment variable is set.

    Raises:
        GHTokenNotSet: If the GH_TOKEN environment variable is not set.
    """
    if not os.environ.get('GH_TOKEN'):
        print('GH_TOKEN not set')
        raise GHTokenNotSet
