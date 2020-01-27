from PyQt5.QtCore import QCoreApplication
from PyQt5.QtCore import QDir
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import qWarning
from pathlib import Path

if "mobase" not in sys.modules:
    import mock_mobase as mobase


class RootBuilder(mobase.IPluginFileMapper):

    def __init__(self):
        super(RootBuilder, self).__init__()
        IOrganizer = None

    mappedfolders = []

    def MountRootFolders(self):
        Mods = self.IOrganizer.modsSortedByProfilePriority()
        gamePath = self.IOrganizer.managedGame().gameDirectory()
        dataOverwritePath = Path(self.IOrganizer.overwritePath())
        rootOverwritePath = dataOverwritePath / "Root"
        for modStr in Mods:
            modState = self.IOrganizer.modList().state(modStr)
            modAbsLocation = Path(
                self.IOrganizer.getMod(modStr).absolutePath())
            if modState & mobase.ModState.active:  # Is Mod Active
                if (modAbsLocation / "Root").exists():
                    currentModRootFolder = modAbsLocation / "Root"
                    if (currentModRootFolder / "data").exists():
                        qWarning("RootBuilder: Skipping root mapping of " + modStr +
                                 "/Root because it contains a Data folder! Please move Data files outside the Root folder.")
                    else:
                        print("RootBuilder: adding game root mapping: " +
                              modStr + "/Root ")
                        mapping = mobase.Mapping()
                        mapping.source = str(currentModRootFolder)
                        mapping.destination = str(gamePath.path())
                        mapping.isDirectory = True
                        mapping.createTarget = False
                        self.mappedfolders.append(mapping)

        # Add RootOverwrite mapping
        if not rootOverwritePath.exists():
            print("RootBuilder: creating missing overwrite/Root folder")
            os.mkdir(rootOverwritePath)
        else:
            print("RootBuilder: overwrite/Root is present, no creation needed")

        mapping = mobase.Mapping()
        mapping.source = str(rootOverwritePath)
        mapping.destination = str(gamePath.path())
        mapping.isDirectory = True
        mapping.createTarget = True
        self.mappedfolders.append(mapping)
        return True

    def onFinishedRunCallback(self):

        # Clean up Overwrite/Root if it's empty
        dataOverwritePath = Path(self.IOrganizer.overwritePath())
        rootOverwritePath = dataOverwritePath / "Root"
        if rootOverwritePath.exists() and len(os.listdir(rootOverwritePath)) == 0:
            print("RootBuilder: cleaning up empty overwrite/Root folder")
            os.rmdir(rootOverwritePath)
        else:
            print("RootBuilder: there are files in overwrite/Root, no cleanup")
        return

    def init(self, organizer):
        self.IOrganizer = organizer
        organizer.onAboutToRun(lambda appName: self.MountRootFolders())
        organizer.onFinishedRun(
            lambda appname, code: self.onFinishedRunCallback())
        return True

    def mappings(self):
        return self.mappedfolders

    def name(self):
        return "Root Folder Builder"

    def author(self):
        return "Vaneixus"

    def description(self):
        # TODO Still needs a new Description. does not fit small plugin window.
        return self.__tr("Allows Mods to add files to the main game directory.\n\n" \
            "Steps on how to use:\n" \
            "   1. Create or use an existing Managed-Mod Folder\n" \
            "   2. Open that mod in explorer\n" \
            "   3. Create a new folder named \"Root\"\n" \
            "       - Should be next to other folders and files like\n" \
            "       Audio, Video, ESPs, ESLs, ESMs, Scripts, meshes, etc\n" \
            "   4. Put all your desired files in the newly created Folder\n" \
            "       - Please know that no Data folders is allowed inside a Root Folder\n" \
            "   5. Enjoy!\n" \
            "\nCouldn't have been possible without the help of\nMod Organizer's Development Team & Contributers!")

    def version(self):
        return mobase.VersionInfo(0, 0, 1, mobase.ReleaseType.prealpha)

    def isActive(self):
        return True

    def settings(self):
        return [mobase.PluginSetting("enabled", self.__tr("Enable Plugin"), True),
            mobase.PluginSetting("Symlink", self.__tr("use Symlink instead of MO2's internal Mounting System(Experimental)?\nAllows DLL Loading"), False)]

    def __tr(self, str):
        return QCoreApplication.translate("RootBuilder", str)


def createPlugin():
    return RootBuilder()
