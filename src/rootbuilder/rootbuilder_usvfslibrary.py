###############################################################################
#                                                                             #
#                  Copyright(C) 2020 Vaneixus Prime                           #
#                                                                             #
#  Root Builder USVFS Library is free software: you can redistribute it       #
#  and/or modify it under the terms of the GNU Lesser General Public License  #
#  as published by the Free Software Foundation, either version 3 of the      #
#  License, or any later version.                                             #
#                                                                             #
#  Root Builder USVFS Library is distributed in the hope that it will be      #
#  useful, but WITHOUT ANY WARRANTY without even the implied warranty of      #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the Lesser GNU   #
#  General Public License for more details.                                   #
#                                                                             #
#  You should have received a copy of the Lesser GNU General Public License   #
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.     #
#                                                                             #
###############################################################################


from PyQt5.QtCore import qDebug, qInfo, qWarning
from pathlib import Path
import os

import mobase
from . import rootbuilder_helperfunctions as _helperf

class RootBuilderUSVFSLibrary():

    def __init__(self, organizer):
        self.iOrganizer = organizer
        self.helperf = _helperf.helperf(organizer)
        super(RootBuilderUSVFSLibrary, self).__init__()

    ###
    # @Return: list of all mods containing /Root folders, skipping /Root/Data cases.
    #         (Strings List)
    ###
    def usvfsGetRootMods(self):
        modslist = self.iOrganizer.modList().allModsByProfilePriority()
        rootMods = []
        for modName in modslist:
            if (self.iOrganizer.modList().state(modName) &
                    mobase.ModState.active):
                if (self.helperf.modsPath() / modName / "Root").exists():
                    if not (self.helperf.modsPath() / modName / "Root/Data").exists():
                        qDebug("Root Builder USVFS Library: /Root detected, "
                            + " adding mod(%s) to root mapping." % modName)
                        rootMods.append(modName)
                    else:
                        qWarning("Root Builder USVFS Library: Root/Data"
                            + " detected, skipping: %s." % modName)
        return rootMods

    ###
    # @Parameter: mods' name list.(String List)
    # @return: 
    ###
    def usvfsGetMappingList(self, modsNameList):
        rootMappingList = []
        for modName in modsNameList:
            qDebug("Root Builder USVFS Library: Re-routing (%s) To (%s)"
                % (self.helperf.modsPath() / modName / "Root",
                   self.helperf.gamePath()))
            rootMapping = mobase.Mapping()
            rootMapping.source = str(self.helperf.modsPath() / modName
                / "Root")
            rootMapping.destination = str(self.helperf.gamePath())
            rootMapping.isDirectory = True
            rootMapping.createTarget = False
            rootMappingList.append(rootMapping)
        return rootMappingList

    ###
    # @Summary: Cleans up the root overwrite folder from useless files/folders.
    ###
    def cleanupRootOverwriteFolder(self):
        qInfo("Root Builder USVFS Library: Cleaning up root overwrite folder...")
        if not self.helperf.rootOverwritePath().exists():
            return
        if len(os.listdir(self.helperf.rootOverwritePath())) == 0:
            qInfo("Root Builder USVFS Library: cleaning up empty overwrite/Root"
                + " folder")
            os.rmdir(self.helperf.rootOverwritePath())
        else:
            qInfo("Root Builder USVFS Library: there are files in"
                + " overwrite/Root, no cleanup")
            return
        qInfo("Root Builder USVFS Library: Finished cleaning up root overwrite"
            + " folder")
        return