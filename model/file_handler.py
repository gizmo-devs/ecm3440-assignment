from PyQt5.QtWidgets import QFileDialog
class FileHandler():
    def __init__(self,app, media_type) -> None:
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

    def saveDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getSaveFileName(self.app, f'Save {self.media_type}', '', self.dialog_helper, options=options)
        return file_name

    def openDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(self.app, f'Open {self.media_type}', '', self.dialog_helper, options=options)
        return file_name