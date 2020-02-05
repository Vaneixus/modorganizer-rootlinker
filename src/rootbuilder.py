###############################################################################
#                                                                             #
# Root Folder Builder                                                         #
#                                                                             #
# @Short Description: Allows loading of mod files into the root game folder.  #
#                                                                             #
# @Authors:                                                                   #
#       - Vaneixus Prime                                                      #
#       - AL                                                                  #
#       - AnyOldName3                                                         #
#       - isa                                                                 #
#       - & Many Others!                                                      #
#                                                                             #
# @Installation:                                                              #
#   1. Create or use an existing Managed-Mod Folder.                          #
#   2. Open that mod in explorer.                                             #
#   3. Create a new folder named "Root"(without quotation marks).             #
#       - Should be next to other folders and files like:                     #
#         Audio, Video, ESPs, ESLs, ESMs, Scripts, meshes, etc.               #
#   4. Put all your desired files in the newly created Folder.                #
#       - Please note that no Data folders is allowed inside a Root Folder.   #
#   5. Enjoy!                                                                 #
#                                                                             #
# @License: http://www.gnu.org/licenses/gpl-3.0.html                          #
#                                                                             #
###############################################################################


from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox

from pathlib import Path
import os
import json


class RootBuilder(mobase.IPluginFileMapper):

    ###############################
    ## Standard Plugin Structure ##
    ###############################

    def __init__(self):
        super(RootBuilder, self).__init__()

    def init(self, organizer):
        self.iOrganizer = organizer
        return True

    def name(self):
        return "Root Folder Builder"

    def author(self):
        return "Vaneixus Prime & MO2 Dev Team"

    def description(self):
        return self.__tr("Adds support for root-Level modding")

    def version(self):
        return mobase.VersionInfo(0, 0, 1, mobase.ReleaseType.alpha)

    def settings(self):
        return [mobase.PluginSetting(
                "Enabled",
                self.__tr("Enable Plugin"),
                True),
            mobase.PluginSetting(
                "Symlink",
                self.__tr("use Symlink instead"
                        + " of MO2's internal mounting system (Beta)?"
                        + "\nRequired for DLLs to work on some games"),
                False)
               ]

    def isActive(self):
        return self.iOrganizer.pluginSetting(self.name(), "Enabled")

    def __tr(self, str):
        return QCoreApplication.translate("RootBuilder", str)





    #############################
    ## Custom Plugin Structure ##
    #############################

    iOrganizer = None

    mappedFiles = []

    ###
    # @Summary: Tells USVFS what to re-route to root game folder & sets up the
    #           custom overwrite folder.
    # @returns: Mapping Object list.
    ###
    def mappings(self):
        rootOverwriteMapping = mobase.Mapping()
        rootOverwriteMapping.source = str(self.helperf_rootOverwritePath())
        rootOverwriteMapping.destination = str(self.helperf_gamePath())
        rootOverwriteMapping.isDirectory = True
        rootOverwriteMapping.createTarget = True
        if self.helperf_useSymlink():
            return [rootOverwriteMapping]
        else:
            self.mappedFiles.append(rootOverwriteMapping)
            return self.mappedFiles

    ###
    # @Summary: updates the cached file/folder structure of files to be
    #           mounted & saves it on the hard-disk.
    # @Parameter: The updated file structure table.
    # @return: The updated file structure table.
    ###
    def updateMountStructureTable(self, updatedTable):
        if not self.helperf_useSymlink():
            # No need to save it locally, USVFS will handle it.
            return updatedTable
        with open(str(self.helperf_instancePath()
                     / "mountedfiles.json", 'w')) as mountDataJSONFile:
            json.dump(self.mappedFiles)
        return updatedTable





    ######################
    ## Helper Functions ##
    ######################

    ###
    # @return: If Symlink is enabled.(Boolean)
    ###
    def helperf_useSymlink(self):
        return self.iOrganizer.pluginSetting(self.name(), "Symlink")

    ###
    # @return: Location of managed game.(Path Object)
    ###
    def helperf_gamePath(self):
        return Path(str(self.iOrganizer.managedGame().gameDirectory()))

    ###
    # @return: Location of current instance.(Path Object)
    ###
    def helperf_instancePath(self):
        return Path(self.iOrganizer.basePath())

    ###
    # @return: Location of root-level overwrite folder.(Path Object)
    ###
    def helperf_rootOverwritePath(self):
        return Path(self.iOrganizer.overwritePath()) / "Root"


def createPlugin():
    return RootBuilder()
