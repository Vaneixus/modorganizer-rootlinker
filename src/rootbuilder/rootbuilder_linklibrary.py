###############################################################################
#                                                                             #
#                  Copyright(C) 2021 Deorder & VaneixusPrime                  #
#                                                                             #
# Root Builder Link Library is a derieved work and is licensed under the      #
# terms and conditions of the MIT License. Please see the accompanying file   #
# named LICENSE_MIT for the full license, if the file is missing or damaged,  #
# please see <https://mit-license.org/> for the full MIT license.             #
#                                                                             #
###############################################################################
# The following code has been created for Root Builder by VaneixusPrime based #
# on Deorder's link deploy code, please see below for the full original code. #
# https://github.com/deorder/mo2-plugins/tree/link-deploy/link_deploy.py      #
###############################################################################

import hashlib
from pathlib import Path

from . import rootbuilder_helperfunctions as _helperf
from PyQt5.QtCore import qDebug, qInfo, qWarning

class RootBuilderLinkLibrary():
    def __init__(self, organizer):
        self.iOrganizer = organizer
        self.helperf = _helperf.HelperFunctions(organizer)
        super(RootBuilderLinkLibrary, self).__init__()

    ###
    # @Parameter targetPath: Path of file to be checked. (Path Object)
    # @return: weather file is link or not. (Boolean)
    ###
    def isLink(self, targetPath):
        return targetPath.is_symlink()

    ###
    # @Parameter rootPath: Path of file to be unlinked. (Path Object)
    ###
    def unlink(self, targetPath):
        qDebug("Root Builder Link Library: (%s) link removed." % targetPath)
        targetPath.unlink(True)

    ###
    # @Parameter targetPath: root directory for the search. (Path Object)
    # @return: hexdigit md5 hash. (String)
    ###
    def fileHash(self, targetPath):
        # Initialize a new hasher object.
        hasher = hashlib.md5()
        with open(str(targetPath), 'rb') as file:
            fileBinaryData = file.read()
            hasher.update(fileBinaryData)
            return hasher.hexdigest()
    
    ###
    # @Parameter rootPath: root directory for the search. (Path Object)
    # @Parameter allwdExt: list of allowed extensions. (String List)
    # @Parameter searchlevel: how deep should the search go. (integer, default=2)
    # @return filesList: get list of files with extensions matching ones in
    #       allwdExt. (Path Object List)
    ###
    def getAllwedFilesList(self, rootPath, allwdExt, searchLevel = 2):
        searchLevel -= 1
        filesList = []
        for file in rootPath.iterdir():
            if file.is_dir() and searchLevel >= 0:
                filesList += self.getAllwedFilesList(rootPath / file, allwdExt, searchLevel)
                continue 
            for ext in allwdExt:
                if file.suffix.lower() == "." + ext:
                    filesList.append(rootPath / file)
        return filesList

    def LinkFiles(self, gamePath, filesPathList):
        linkedFilesList = []
        for file in filesPathList:
            fileStr = str(file).lower()
            fileRootPath = Path(fileStr[(fileStr.find("\\root") + 6):])
            fileGamePath = gamePath / fileRootPath 
            if fileGamePath.exists():
                if fileGamePath.samefile(file):
                    print("File Detected is the same as one in game folder.")
                    continue
                OldfileGamePath = fileGamePath
                OldfileBackupPath = OldfileGamePath.parent / (OldfileGamePath.name + ".rootbuilder")
                OldfileGamePath.rename(OldfileBackupPath)
            file.link_to(fileGamePath)
            qDebug("Root Builder Link Library: Hardlink created for (%s) at (%s)." % (file, fileGamePath))
        return linkedFilesList