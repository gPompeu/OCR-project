import UserInterface

import EnvironmentSettings

import FolderHandler


if __name__ == '__main__':

    UserInterface.removeTkinterRootWindow()

    EnvironmentSettings.setTesseractPath()

    folder = FolderHandler.Folder()

    folder.askUserForFolder()

    if folder.userSelectedFolderPath:

        folder.watchUserFolder()
