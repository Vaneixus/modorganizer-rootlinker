###############################################################################
#                                                                             #
# Root Folder Builder                                                         #
#                                                                             #
# @Short Description: Allows loading of mod files into the root game folder.  #
#                                                                             #
# @Authors & Contributers:                                                    #
#       - Vaneixus Prime                                                      #
#       - AL                                                                  #
#       - AnyOldName3                                                         #
#       - isa                                                                 #
#       - & Many Others!                                                      #
#                                                                             #
# @Installation:                                                              #
#   Drop RootBuilder.py in the Mod Organizer 2 Plugins folder,                #
#   situated inside the MO2 installation directory.                           #
#                                                                             #
# @Usage:                                                                     #
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
#    Copyright(C) 2020 Vaneixus Prime                                         #
#                                                                             #
#  This program is free software: you can redistribute it and/or modify       #
#  it under the terms of the GNU General Public License as published by       #
#  the Free Software Foundation, either version 3 of the License, or          #
#  (at your option) any later version.                                        #
#                                                                             #
#  This program is distributed in the hope that it will be useful,            #
#  but WITHOUT ANY WARRANTY                                                   #
#  without even the implied warranty of                                       #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the              #
#  GNU General Public License for more details.                               #
#                                                                             #
#  You should have received a copy of the GNU General Public License          #
#  along with this program.  If not, see https://www.gnu.org/licenses/.       #
#                                                                             #
###############################################################################


from PyQt5.QtCore import QCoreApplication

from pathlib import Path


class RootBuilder(mobase.IPluginFileMapper):

    ###############################
    ## Standard Plugin Structure ##
    ###############################

    def __init__(self):
        super(RootBuilder, self).__init__()

    def init(self, organizer):
        # Initialise variables
        self.iOrganizer = organizer
        return True

    def name(self):
        return "Root Folder Builder"

    def author(self):
        return "Vaneixus Prime & Contributers"

    def description(self):
        return self.__tr("Adds support for root-Level modding")

    def version(self):
        return mobase.VersionInfo(0, 0, 1, mobase.ReleaseType.beta)

    def settings(self):
        return [mobase.PluginSetting(
            "enabled",
            self.__tr("Enable Plugin"),
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

    ##################################
    ## File Mapper Plugin Structure ##
    ##################################

    ###
    # @Summary: Called by MO2 when starting programs to get what to re-route.
    #           Prepares root game folder mod mappings and sets up the
    #            overwrite/Root creation target folder.
    # @Returns: A Mapping Object list.(Mapping Object list)
    ###

    def mappings(self):
        self.mappedFiles = []
        rootOverwriteMapping = mobase.Mapping()
        rootOverwriteMapping.source = str(self.rootOverwritePath())
        rootOverwriteMapping.destination = str(self.gamePath())
        rootOverwriteMapping.isDirectory = True
        rootOverwriteMapping.createTarget = True
        self.mountRootModsDirs()
        self.mappedFiles.append(rootOverwriteMapping)
        return self.mappedFiles

    #############################
    ## Custom Plugin Structure ##
    #############################

    iOrganizer = None

    mappedFiles = []

    ###
    # @Return: A list of all (mod)/Root folders, skipping (mod)/Root/Data cases.
    #         (Strings List)
    ###
    def getRootMods(self):
        modslist = self.iOrganizer.modList().allModsByProfilePriority()
        rootMods = []
        for modName in modslist:
            if (self.iOrganizer.modList().state(modName) &
                    mobase.ModState.active):
                if (self.modsPath() / modName / "Root").exists():
                    if not (self.modsPath() / modName
                            / "Root" / "Data").exists():
                        qDebug("RootBuilder: /Root detected, adding mod to "
                               + "root mapping: " + modName + ".")
                        rootMods.append(modName)
                    else:
                        qDebug(
                            "RootBuilder: Root/Data detected, skipping: " +
                            modName + ".")
        return rootMods

    ###
    # @Summary: Mounts the files
    ###
    def mountRootModsDirs(self):
        # Cleanup root overwrite directory
        if self.rootOverwritePath().exists():
            self.cleanupOverwriteFolder()
        else:
            os.mkdir(self.rootOverwritePath())
        qDebug("RootBuilder: About to mount Root mods")
        modsNameList = self.getRootMods()
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
                   + str(self.modsPath() / modName / "Root")
                   + "\") To (\"" + str(self.gamePath()) + "\")")
            rootMapping = mobase.Mapping()
            rootMapping.source = str(self.modsPath() / modName
                                     / "Root")
            rootMapping.destination = str(self.gamePath())
            rootMapping.isDirectory = True
            rootMapping.createTarget = False
            self.mappedFiles.append(rootMapping)

    ###
    # @Summary: Cleans up the overwrite folder from useless files/folders.
    ###
    def cleanupOverwriteFolder(self):
        if not self.iOrganizer.pluginSetting(self.name(), "ow_cleanup"):
            return
        print("RootBuilder: Cleaning up root overwrite folder...")
        # Delete root overwrite folder in case it's empty
        if not self.rootOverwritePath().exists():
            return
        if len(os.listdir(self.rootOverwritePath())) == 0:
            print("RootBuilder: cleaning up empty overwrite/Root folder")
            os.rmdir(self.rootOverwritePath())
        else:
            print("RootBuilder: there are files in overwrite/Root, no cleanup")
        return

    ######################
    ## Helper Functions ##
    ######################

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
            self._rootOverwritePath = Path(
                self.iOrganizer.overwritePath()) / "Root"
        return self._rootOverwritePath


def createPlugin():
    return RootBuilder()
