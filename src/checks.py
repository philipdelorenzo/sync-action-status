# Author: Philip De lorenzo <philip.delorenzo@gmail.com>

import os
from src.exceptions import GHTokenNotSet

def check_gh_token() -> None:
    """This function checks to ensure that the GH_TOKEN environment variable is set.

    Raises:
        GHTokenNotSet: If the GH_TOKEN environment variable is not set.
    """
    if not os.environ.get('GH_TOKEN'):
        raise GHTokenNotSet()
