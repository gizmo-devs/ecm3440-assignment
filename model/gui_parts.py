from PyQt5.QtWidgets import QMainWindow, QRadioButton, QWidget, QVBoxLayout, QPushButton, QCheckBox

class Widgit:
    def __init__(self, conf, app):
        self.conf = conf
        self.app = app

    def init(self):
        match self.conf.get("controler_type"):
            case "radio":
                return Radio(self.app, self.conf)
            case "checkbox":
                return Checkbox(self.app, self.conf)
        

class Radio(QRadioButton):
    def __init__(self, app: QMainWindow, conf) -> None:
        """_summary_

        Args:
            app (QMainWindow): The Qt application this radio is being added to
            effect (str): The effect name. This is defined in the app.EFFECTS
            effect_index (int): The number in the array
        """
        super().__init__()

        self.setText(conf["name"])
        self.group = "Effects"
        self.clicked.connect(lambda: app.toggle_effect(conf["id"]))


class Checkbox(QCheckBox):
    def __init__(self, app: QMainWindow, conf) -> None:
        """_summary_

        Args:
            app (QMainWindow): The Qt application this radio is being added to
            effect (str): The effect name. This is defined in the app.EFFECTS
            effect_index (int): The number in the array
        """
        super().__init__()

        self.setText(conf["name"])
        self.clicked.connect(lambda: app.toggle_effect(conf["id"]))


class Tabs():
    def __init__(self, app: QMainWindow) -> None:
        """Iniatlises the Tab class

        Args:
            app (QMainWindow): The main app.
        """
        self.app = app

    @property 
    def image(self) -> QWidget:
        """Initalises the Images Tab with the options associated.

        Returns:
            QWidget: Used with the QTabsWidget and the tab label
        """
        imageTab = QWidget()
        layout = QVBoxLayout()
        self.app.open_button = QPushButton('Open Image', self.app)
        self.app.open_button.clicked.connect(self.app.open_image)

        self.app.save_button = QPushButton('Save Image', self.app)
        self.app.save_button.clicked.connect(self.app.save_image)
        self.app.save_button.setEnabled(False)

        layout.addWidget(self.app.open_button)
        layout.addWidget(self.app.save_button)
        imageTab.setLayout(layout)
        return imageTab

    @property
    def video(self):
        """Initalises the Videos Tab with the options associated.

        Returns:
            QWidget: Used with the QTabsWidget and the tab label
        """
        videoTab = QWidget()
        layout = QVBoxLayout()

        self.app.record_button = QPushButton('Record Video', self.app)
        self.app.record_button.clicked.connect(self.app.record_video)
        self.app.record_button.setEnabled(True)

        self.app.play_button = QPushButton('Play Video', self.app)
        self.app.play_button.clicked.connect(self.app.play_video)
        self.app.play_button.setEnabled(False)

        self.app.open_saved_video_button = QPushButton('Open Saved Video', self.app)
        self.app.open_saved_video_button.clicked.connect(self.app.open_saved_video)

        layout.addWidget(self.app.record_button)
        layout.addWidget(self.app.play_button)
        layout.addWidget(self.app.open_saved_video_button)
        videoTab.setLayout(layout)
        return videoTab

    @property
    def stream(self):
        """Initalises the Stream Tab with the options associated.

        Returns:
            QWidget: Used with the QTabsWidget and the tab label
        """
        streamTab = QWidget()
        layout = QVBoxLayout()
        self.app.start_webcam_button = QPushButton('Start Webcam', self.app)
        self.app.start_webcam_button.clicked.connect(self.app.start_webcam)
        self.app.start_webcam_button.setEnabled(True)

        self.app.stop_webcam_button = QPushButton('Stop Webcam', self.app)
        self.app.stop_webcam_button.clicked.connect(self.app.stop_webcam)
        self.app.stop_webcam_button.setEnabled(False)

        layout.addWidget(self.app.start_webcam_button)
        layout.addWidget(self.app.stop_webcam_button)
        streamTab.setLayout(layout)

        return streamTab