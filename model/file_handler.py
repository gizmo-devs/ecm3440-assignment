from PyQt5.QtWidgets import QFileDialog

class FileHandler():
    """The FileHandler Class. Designed for opening and saveing files using PyQt"""
    def __init__(self, app, media_type: str) -> None:
        """_summary_

        Args:
            app (_type_): the current Qt App
            media_type (str): Should be Img or Vid
        """
        self.app = app
        self.options = QFileDialog.Options()
        self.options |= QFileDialog.ReadOnly
        self.media_type = media_type
        if self.media_type.upper() == "IMG":
            self.media_type = "Image"
            self.dialog_helper = "Image Files (*.png *.jpg *.jpeg *.gif *.bmp *.tiff)"
        else:
            self.media_type = "Video" 
            self.dialog_helper = "Video Files (*.avi *.mp4)"

    def saveDialog(self) -> str:
        """Opens the save dialoge. Helper text will depend on the self.media_type value.

        Returns:
            str: The filename that the file will be saved under.
        """
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getSaveFileName(self.app, f'Save {self.media_type}', '', self.dialog_helper, options=options)
        return file_name

    def openDialog(self) -> str:
        """Opens the Open dialoge. Helper text will depend on the self.media_type value.

        Returns:
            str: The files name to open.
        """
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(self.app, f'Open {self.media_type}', '', self.dialog_helper, options=options)
        return file_name