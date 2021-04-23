###############################################################################
#                                                                             #
#                  Copyright(C) 2021 Vaneixus Prime                           #
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
from pathlib import Path
import mobase, os, json

from . import rootbuilder_helperfunctions as _helperf
from . import rootbuilder_usvfslibrary as _usvfslib
from . import rootbuilder_linklibrary as _linklib

class RootBuilder(mobase.IPluginFileMapper):

    ############################
    ## IPlugin Data Structure ##
    ############################

    def __init__(self):
        super(RootBuilder, self).__init__()

    def init(self, organizer):
        # Initialise variables
        self.iOrganizer = organizer
        self.helperf = _helperf.HelperFunctions(organizer)
        self.usvfslib = _usvfslib.RootBuilderUSVFSLibrary(organizer)
        self.linklib = _linklib.RootBuilderLinkLibrary(organizer)
        self.cleanupGameFolder()
        self.iOrganizer.onAboutToRun(lambda x = "": 
            self.linkFiles())
        self.iOrganizer.onFinishedRun(lambda x = "", y = 0: 
            self.usvfslib.cleanupRootOverwriteFolder())
        self.iOrganizer.onFinishedRun(lambda x = "", y = 0: 
            self.cleanupGameFolder())
        return True

    def name(self):
        return "Root Builder"

    def author(self):
        return "Vaneixus Prime"

    def description(self):
        return self.__tr("Adds support for root-Level game modding.")

    def version(self):
        return mobase.VersionInfo(2, 0, 0, 1, mobase.ReleaseType.alpha)

    def settings(self):
        return [mobase.PluginSetting("enabled",
                self.__tr("Enable Plugin"),
                True),
            mobase.PluginSetting("link_enabled",
                self.__tr("Enable Linking Files"),
                True),
            mobase.PluginSetting("link_extensions",
                self.__tr("A list of extensions of files to be linked. Seperated by commas"),
                "dll"),
            mobase.PluginSetting("link_cleanupMode",
                self.__tr("how should Rootbuilder react to files left behind by root overwrite:"
                    + "\n   1 - Move to Root overwrite"
                    + "\n   2 - Delete Files"
                    + "\n   3 - Leave Behind\n"),
                1),
            mobase.PluginSetting("link_searchLevel",
                self.__tr("how deep should the search go."),
                2),
            mobase.PluginSetting("ow_cleanup",
                self.__tr("Clean up empty/useless folders and files from the overwrite folder."),
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
        qDebug("Root Builder: Rerouting using USVFS...")

        # Fixes Bug with rootOverwriteMapping.
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
        return []#filesMappingList

    ###########################
    ## Custom Data Structure ##
    ###########################

    def linkFiles(self):
        if not self.iOrganizer.pluginSetting(self.name(), "link_enabled"):
            return
        filesList = []

        allwdExt = self.iOrganizer.pluginSetting(self.name(), "link_extensions")
        allwdExt = allwdExt.replace(" ", "")
        allwdExt = allwdExt.replace(".", "")
        allwdExtList = allwdExt.split(",")
        searchLevel = self.iOrganizer.pluginSetting(self.name(), "link_searchLevel")

        for mod in self.usvfslib.usvfsGetRootMods():
            modPath = self.helperf.modsPath() / mod
            filesList += self.linklib.getAllwedFilesList(modPath, allwdExtList, searchLevel)
        
        filesList += self.linklib.getAllwedFilesList(Path(self.iOrganizer.overwritePath()), allwdExtList, searchLevel)
        filesList.reverse()
        LinkedFiles = self.linklib.LinkFiles(self.helperf.gamePath(), filesList)

        if not (self.helperf.rootPluginDataPath() / "linkedfiles.json").exists():
            (self.helperf.rootPluginDataPath() / "linkedfiles.json").touch()
        with open(self.helperf.rootPluginDataPath() / "linkedfiles.json", "w") as jsonFile:
            json.dump(LinkedFiles, jsonFile)
        
        # Required to not interrupt MO2 Launch flow
        return True

    def cleanupGameFolder(self):
        if not (self.helperf.rootPluginDataPath() / "linkedfiles.json").exists():
            return
        linkedFiles = json.load(open(self.helperf.rootPluginDataPath() / "linkedfiles.json"))
        for file in linkedFiles:
            file = Path(file)
            modfile = file
            modfile.unlink(True)
            if Path(file.__str__() + "._rootbuilder").exists():
                Path(file.__str__() + "._rootbuilder").rename(file)
        (self.helperf.rootPluginDataPath() / "linkedfiles.json").unlink()