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


from PyQt5.QtCore import QCoreApplication
from pathlib import Path
import os

import mobase
from . import rootbuilder_helperfunctions as _helperf

class RootBuilderUSVFSLibrary():

    def __init__(self, organizer):
        self.iOrganizer = organizer
        self.helperf = _helperf.helperf(organizer)
        super(RootBuilderUSVFSLibrary, self).__init__()

    mappedFiles = []

    ###
    # @Return: get list of all (mod)/Root folders, skipping (mod)/Root/Data cases.
    #         (Strings List)
    ###
    def getRootMods(self):
        modslist = self.iOrganizer.modList().allModsByProfilePriority()
        rootMods = []
        for modName in modslist:
            if (self.iOrganizer.modList().state(modName) &
                    mobase.ModState.active):
                if (self.helperf.modsPath() / modName / "Root").exists():
                    if not (self.helperf.modsPath() / modName
                            / "Root" / "Data").exists():
                        #qDebug("RootBuilder: /Root detected, adding mod(" 
                        #       + modName + ") to root mapping.")
                        rootMods.append(modName)
                    #else:
                        #qDebug(
                        #    "RootBuilder: Root/Data detected, skipping: " +
                        #    modName + ".")
        return rootMods

    ###
    # @Summary: Mounts the files
    ###
    def mountRootModsDirs(self):
        # Cleanup root overwrite directory
        if self.helperf.rootOverwritePath().exists():
            self.cleanupOverwriteFolder()
        else:
            os.mkdir(self.helperf.rootOverwritePath())
        #qDebug("RootBuilder: About to mount Root mods")
        modsNameList = self.getRootMods()
        self.usvfsReroute(modsNameList)
        return self.mappedFiles

    ###
    # @Summary: Re-route files using USVFS
    # @Parameter: Active mods' name list.(String List)
    ###
    def usvfsReroute(self, modsNameList):
        #qDebug("Root Builder: Mounting using USVFS")
        for modName in modsNameList:
        #    qDebug("Root Builder: Re-routing (\""
        #           + str(self.helperf.modsPath() / modName / "Root")
        #           + "\") To (\"" + str(self.helperf.gamePath()) + "\")")
            rootMapping = mobase.Mapping()
            rootMapping.source = str(self.helperf.modsPath() / modName
                                     / "Root")
            rootMapping.destination = str(self.helperf.gamePath())
            rootMapping.isDirectory = True
            rootMapping.createTarget = False
            self.mappedFiles.append(rootMapping)

    ###
    # @Summary: Cleans up the overwrite folder from useless files/folders.
    ###
    def cleanupOverwriteFolder(self):
        if not self.iOrganizer.pluginSetting("Root Builder",
                                             "ow_cleanup"):
            return
        print("RootBuilder: Cleaning up root overwrite folder...")
        # Delete root overwrite folder in case it's empty
        if not self.helperf.rootOverwritePath().exists():
            return
        if len(os.listdir(self.helperf.rootOverwritePath())) == 0:
            print("RootBuilder: cleaning up empty overwrite/Root folder")
            os.rmdir(self.helperf.rootOverwritePath())
        else:
            print("RootBuilder: there are files in overwrite/Root, no cleanup")
        return
