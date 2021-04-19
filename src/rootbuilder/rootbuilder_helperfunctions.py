###############################################################################
#                                                                             #
#                 Copyright(C) 2021 Vaneixus Prime                            #
#                                                                             #
# This file is licensed under the terms and conditions of the MIT License.    #
# Please see the accompanying file named LICENSE_MIT for the full license,    #
# if the file is missing or damaged, please see <https://mit-license.org/>    #
# for the full MIT license.                                                   #
#                                                                             #
###############################################################################
   

import mobase
from pathlib import Path


class helperf():

    def __init__(self, organizer):
        self.iOrganizer = organizer
        super(helperf, self).__init__()
    
    ###
    # @Return: Path to the root game directory.(Path Object)
    ###
    _gamePath = None

    def gamePath(self):
        if not self._gamePath:
            self._gamePath = Path(
                self.iOrganizer.managedGame().gameDirectory().path())
        return self._gamePath

    ###
    # @Return: Path to the current instance.(Path Object)
    ###
    _instancePath = None

    def instancePath(self):
        if not self._instancePath:
            self._instancePath = Path(self.iOrganizer.basePath())
        return self._instancePath

    ###
    # @Return: Path to the current mods folder.(Path Object)
    ###
    _modsPath = None

    def modsPath(self):
        if not self._modsPath:
            self._modsPath = Path(self.iOrganizer.modsPath())
        return self._modsPath

    ###
    # @Return: Path to the root-level overwrite directory.(Path Object)
    ###
    _rootOverwritePath = None

    def rootOverwritePath(self):
        if not self._rootOverwritePath:
            self._rootOverwritePath = Path(self.iOrganizer.overwritePath()) / "Root"
        return self._rootOverwritePath