###############################################################################
#                                                                             #
#                  Copyright(C) 2020 Vaneixus Prime                           #
#                                                                             #
#  Root Builder is free software: you can redistribute it and/or modify       #
#  it under the terms of the GNU General Public License as published by       #
#  the Free Software Foundation, either version 3 of the License, or          #
#  any later version.                                                         #
#                                                                             #
#  Root Builder is distributed in the hope that it will be useful, but        #
#  WITHOUT ANY WARRANTY without even the implied warranty of MERCHANTABILITY  #
#  or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License   #
#  for more details.                                                          #
#                                                                             #
#  You should have received a copy of the GNU General Public License          #
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.     #
#                                                                             #
###############################################################################


from PyQt5.QtCore import QCoreApplication, qDebug, qInfo
import mobase
import os

from . import rootbuilder_helperfunctions as _helperf
from . import rootbuilder_usvfslibrary as _usvfslib
# from . import rootbuilder_linklibrary as linklib

class RootBuilder(mobase.IPluginFileMapper):

    ############################
    ## IPlugin Data Structure ##
    ############################

    def __init__(self):
        super(RootBuilder, self).__init__()

    def init(self, organizer):
        # Initialise variables
        self.iOrganizer = organizer
        self.helperf = _helperf.helperf(organizer)
        self.usvfslib = _usvfslib.RootBuilderUSVFSLibrary(organizer)
        self.iOrganizer.onFinishedRun(lambda x = "", y = 0: 
            self.usvfslib.cleanupRootOverwriteFolder())
        return True

    def name(self):
        return "Root Builder"

    def author(self):
        return "Vaneixus Prime"

    def description(self):
        return self.__tr("Adds support for root-Level game modding.")

    def version(self):
        return mobase.VersionInfo(2, 0, 0, 1, mobase.ReleaseType.prealpha)

    def settings(self):
        return [mobase.PluginSetting(
            "enabled",
            self.__tr("Enable Plugin"),
            True),
            mobase.PluginSetting(
            "link_enabled",
            self.__tr("Enable Linking Files"),
            True),
            mobase.PluginSetting(
            "link_extensions",
            self.__tr("a list of extensions to be linked."),
            True),
            mobase.PluginSetting(
            "ow_cleanup",
            self.__tr("Clean up empty/useless folders and files from"
                      + " the overwrite folder."),
            True)
        ]

    def isActive(self):
        return self.iOrganizer.pluginSetting(self.name(), "enabled")

    def __tr(self, trstr):
        return QCoreApplication.translate("RootBuilder", trstr)

    ######################################
    ## IPluginFileMapper Data Structure ##
    ######################################

    def mappings(self):
        qDebug("Root Builder: Mounting using USVFS...")

        # Fixes Bug with the rootOverwriteMapping.
        if not self.helperf.rootOverwritePath().exists():
            qInfo("Root Builder: Creating Overwrite folder...")
            os.mkdir(self.helperf.rootOverwritePath())

        rootOverwriteMapping = mobase.Mapping()
        rootOverwriteMapping.source = str(self.helperf.rootOverwritePath())
        rootOverwriteMapping.destination = str(self.helperf.gamePath())
        rootOverwriteMapping.isDirectory = True
        rootOverwriteMapping.createTarget = True
         
        rootModsList = self.usvfslib.usvfsGetRootMods()
        filesMappingList = self.usvfslib.usvfsGetMappingList(rootModsList)
        filesMappingList.append(rootOverwriteMapping)
        return filesMappingList