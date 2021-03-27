from directory_handler import DirectoryHandler

if __name__ == '__main__':
    dirHandler = DirectoryHandler()

    if dirHandler.userSelectedFolderPath:
        dirHandler.watchUserFolder()