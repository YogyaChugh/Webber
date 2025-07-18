class NoInternetConnection(Exception):
    def __init__(self, message="No valid internet connection."):
        super().__init__(message)


class FileDownloadError(Exception):
    def __init__(self,file, message="Couldn't download file !"):
        super().__init__(message)
        self.file = file


class CharacterEncodingError(Exception):
    def __init__(self,file, indexes, message="Character's not supported !"):
        super().__init__(message)
        self.file = file
        self.indexes = indexes

class FileSaveError(Exception):
    def __init__(self,file, message = "Error in saving the file !"):
        super().__init__(message)
        self.file = file