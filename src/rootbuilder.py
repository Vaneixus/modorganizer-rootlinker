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
        # Initialise variables
        self.iOrganizer = organizer
        # self.iOrganizer.onAboutToRun(
        #    lambda appName: self.mountModRootFolders())
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
            "enabled",
            self.__tr("Enable Plugin"),
            True),
            mobase.PluginSetting(
            "load_use_symlink",
            self.__tr("use Symlink instead"
                      + " of MO2's internal mounting system (Beta)?"
                      + "\nRequired for DLLs to work on some games"),
            False),
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

    ##################################
    ## File Mapper Plugin Structure ##
    ##################################

    ###
    # @Summary: Tells USVFS what to re-route to root game folder & sets up the
    #           custom overwrite folder.
    # @returns: A Mapping Object list.(Mapping Object list)
    ###

    def mappings(self):
        rootOverwriteMapping = mobase.Mapping()
        rootOverwriteMapping.source = str(self.helperf_getRootOverwritePath())
        rootOverwriteMapping.destination = str(self.helperf_getGamePath())
        rootOverwriteMapping.isDirectory = True
        rootOverwriteMapping.createTarget = True
        self.mountModRootFolders()
        if self.helperf_getUseSymlink():
            return [rootOverwriteMapping]
        else:
            self.mappedFiles.append(rootOverwriteMapping)
            return self.mappedFiles

    #############################
    ## Custom Plugin Structure ##
    #############################

    iOrganizer = None

    mappedFiles = []

    ###
    # @return: A list of all (mod)/Root folders.(Strings List)
    ###
    def getRootMods(self):
        modsList = []
        for modName in self.helperf_getPrioritisedMods():
            if (self.iOrganizer.modList().state(modName) &
                    mobase.ModState.active):
                if (self.helperf_getModsPath() / modName / "Root").exists():
                    if not (self.helperf_getModsPath() / modName
                            / "Root" / "Data").exists():
                        qDebug(
                            "RootBuilder: /Root detected adding mod to root mapping: " + modName)
                        modsList.append(modName)
                    else:
                        qDebug(
                            "RootBuilder: Root/Data detected, skipping: " + modName)
        return modsList

    ###
    # @Summary: Mounts the files using either the user's prefered mount method.
    ###
    def mountModRootFolders(self):
        # Cleanup root overwrite directory
        if self.helperf_getRootOverwritePath().exists():
            self.cleanupOverwriteFolder()
        else:
            os.mkdir(self.helperf_getRootOverwritePath())
        # Cleanup in case of unexpected program exit.
        qDebug("RootBuilder: About to mount Root mods")
        self.symlink_unlink(self.mappedFiles)
        modsNameList = self.getRootMods()
        if self.helperf_getUseSymlink():
            self.symlink_link(modsNameList)
        else:
            self.usvfsReroute(modsNameList)
        return True
    ###
    # @Summary: Re-route files using USVFS
    # @Parameter: Active mods' name list.(String List)
    ###

    def usvfsReroute(self, modsNameList):
        qDebug("Root Builder: Mounting using USVFS")
        for modName in modsNameList:
            qDebug("Root Builder: Re-routing (\""
                   + str(self.helperf_getModsPath() / modName / "Root")
                   + "\") To (\"" + str(self.helperf_getGamePath()) + "\")")
            rootMapping = mobase.Mapping()
            rootMapping.source = str(self.helperf_getModsPath() / modName
                                     / "Root")
            rootMapping.destination = str(self.helperf_getGamePath())
            rootMapping.isDirectory = True
            rootMapping.createTarget = False
            self.mappedFiles.append(rootMapping)

    ###
    # @Summary: Creates a list of files to be mounted.
    # @Note: Files are ignored if already exist in the list.
    # @Parameter: Active mods' name list.(String List)
    # TODO
    def symlink_prioritisedFiles(self, modsNameList):
        return

    ###
    # @Summary: Link files using Symlink
    # @Parameter: Active mods' name list.(String List)
    ###
    def symlink_link(self, modsNameList):
        qDebug("Root Builder: Mounting using Symlinks")
        return

    ###
    # @Summary: Unlink files from game root directory
    # @Parameter: Active mods' name list.(String List)
    ###
    def symlink_unlink(self, modsNameList):
        qDebug("Root Builder: Un-mounting symlinked files.")
        return

    ###
    # @Summary: Updates cached relative mapped paths list.
    # @Parameter: The updated relative mapped paths list.(Path Object List)
    ###
    def updateMountStructureTable(self, updatedTable):
        if not self.helperf_getUseSymlink():
            # No need to save it locally, USVFS will handle it.
            return
        with open(str(self.helperf_getInstancePath()
                      / "mountedfiles.json"), 'w') as mountDataJSONFile:
            json.dump(self.mappedFiles)
        return

    ###
    # @Summary: retrieves the saved relative mapped paths list.
    # @returns: The saved relative mapped paths list.(Path Object List)
    # TODO Not Finished.
    def retrieveMountStructureTable(self):
        with open(str(self.helperf_getInstancePath()
                      / "mountedfiles.json"), 'r') as mountDataJSONFile:
            mappedFiles = json.loads(mountDataJSONFile)
        return

    ###
    # @Summary: Cleans up the overwrite folder from useless files/folders.
    ###
    def cleanupOverwriteFolder(self):
        if not self.iOrganizer.pluginSetting(self.name(), "ow_cleanup"):
            return
        print("RootBuilder: Cleaning up root overwrite folder...")
        qDebug("Looking for any \"Device\" or \"MMCSS\" folders "
               + "to be removed.")
        for path, sub_dirs, files in os.walk(self.iOrganizer.overwritePath()):
            for sub_dir in sub_dirs:
                if sub_dir == ("Device" or "MMCSS"):
                    if Path(path, sub_dir).exists():
                        qDebug("RootBuilder: Found a \"Device\" or \"MMCSS\""
                               + " folder, cleaning up...")
                        try:
                            os.rmdir(path + "\\" + sub_dir)
                        except OSError:
                            print("Root Builder: File is not accessable!")
        # Delete root overwrite folder in case it's empty
        if not self.helperf_getRootOverwritePath().exists():
            return
        if len(os.listdir(self.helperf_getRootOverwritePath())) == 0:
            print("RootBuilder: cleaning up empty overwrite/Root folder")
            os.rmdir(self.helperf_getRootOverwritePath())
        else:
            print("RootBuilder: there are files in overwrite/Root, no cleanup")
        return

    ######################
    ## Helper Functions ##
    ######################

    ###
    # @return: If Symlink is enabled.(Boolean)
    ###
    useSymlink = None

    def helperf_getUseSymlink(self):
        self.UseSymlink = self.iOrganizer.pluginSetting(self.name(),
                                                        "load_use_symlink")

    ###
    # @return: the prioritised Mods.(Strings list)
    ###
    def helperf_getPrioritisedMods(self):
        if self.useSymlink:
            return self.iOrganizer.modsSortedByProfilePriority().reverse()
        else:
            return self.iOrganizer.modsSortedByProfilePriority()

    ###
    # @return: Path to the root game directory.(Path Object)
    ###
    gamePath = None

    def helperf_getGamePath(self):
        if not self.gamePath:
            self.gamePath = Path(
                self.iOrganizer.managedGame().gameDirectory().path())
            return self.gamePath
        else:
            return self.gamePath

    ###
    # @return: Path to the current instance.(Path Object)
    ###
    instancePath = None

    def helperf_getInstancePath(self):
        if not self.instancePath:
            self.instancePath = Path(self.iOrganizer.basePath())
            return self.instancePath
        else:
            return self.instancePath

    ###
    # @return: Path to the current mods folder.(Path Object)
    ###
    modsPath = None

    def helperf_getModsPath(self):
        if not self.modsPath:
            self.modsPath = Path(self.iOrganizer.modsPath())
            return self.modsPath
        else:
            return self.modsPath

    ###
    # @return: Path to the root-level overwrite directory.(Path Object)
    ###
    rootOverwritePath = None

    def helperf_getRootOverwritePath(self):
        if not self.rootOverwritePath:
            self.rootOverwritePath = Path(
                self.iOrganizer.overwritePath()) / "Root"
            return self.rootOverwritePath
        else:
            return self.rootOverwritePath


def createPlugin():
    return RootBuilder()
