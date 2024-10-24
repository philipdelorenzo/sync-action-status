# Author: Philip De lorenzo <philip.delorenzo@gmail.com>
# Copyright (c) 2024, Philip De Lorenzo
# All rights reserved.

# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. 
class GHTokenError(Exception):
    def __init__(self, message, errors={}):
        # Call the base class constructor with the parameters it needs
        super().__init__(message)

        # Now for your custom code...
        self.errors = errors


class RepoError(Exception):
    def __init__(self, message, errors={}):
        # Call the base class constructor with the parameters it needs
        super().__init__(message)

        # Now for your custom code...
        self.errors = errors


class OrgError(Exception):
    def __init__(self, message, errors={}):
        # Call the base class constructor
        super().__init__(message)

        # Now for your custom code...
        self.errors = errors


class GithubActorError(Exception):
    def __init__(self, message, errors={}):
        # Call the base class constructor
        super().__init__(message)

        # Now for your custom code...
        self.errors = errors


class RepoOwnershipMixmatch(Exception):
    def __init__(self, message, errors={}):
        # Call the base class constructor
        super().__init__(message)

        # Now for your custom code...
        self.errors = errors
