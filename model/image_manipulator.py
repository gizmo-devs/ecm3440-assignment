import cv2 as cv
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QLabel, QVBoxLayout, QHBoxLayout, QGridLayout, QWidget, QGraphicsView, QGraphicsScene, QShortcut
from PyQt5.QtGui import QPixmap, QImage, QKeySequence
from PyQt5.QtCore import Qt, QTimer

import model.image_effect as image_effect
import model.gui_parts as gui_parts
from model.file_handler import FileHandler

media_width, media_height = 500, 400

class ImageManipulator(QMainWindow):
    def __init__(self):
        super().__init__()

        self.EFFECTS = [
            "None", 
            "Blur", 
            "Grey", 
            "Canny", 
            "Sobel"
        ]

        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Image Manipulation')

        self.quitSc = QShortcut(QKeySequence('Ctrl+Q'), self)
        self.quitSc.activated.connect(QApplication.instance().quit)

        # Create widgets
        self.view = QGraphicsView(self)
        self.scene = QGraphicsScene(self)
        self.view.setScene(self.scene)

        tabs = QTabWidget()
        tabs.addTab(gui_parts.Tabs(self).image, "Image")
        tabs.addTab(gui_parts.Tabs(self).video, "Video")
        tabs.addTab(gui_parts.Tabs(self).stream, "Stream")

        self.image_label = QLabel()
        self.image_pixmap = None

        self.layoutRoot = QVBoxLayout()
        layoutGrid = QGridLayout()
        effectlayout = QHBoxLayout()
        
        self.layoutRoot.addWidget(tabs)

        for i, effect in enumerate(self.EFFECTS, start=0):
            effectlayout.addWidget(gui_parts.Radio(self, effect, i))
        
        self.layoutRoot.addLayout(layoutGrid)
        self.layoutRoot.addLayout(effectlayout)

        self.layoutRoot.addWidget(self.image_label)
        self.layoutRoot.addWidget(self.view)

        self.container = QWidget()
        self.container.setLayout(self.layoutRoot)

        self.setCentralWidget(self.container)

        self.webcam = None
        self.timer = None
        self.effect = None
        self.raw_image = None

        self.is_recording = False
        self.video_writer = None
        self.video_player = None
    
    def toggle_effect(self, effect):
        self.effect=effect
        print(f"Updated effect = {effect}")
        if not self.webcam:
            height, width, channel = self.raw_image.shape
            bytes_per_line = 3 * width
            adjusted_img = image_effect.apply_effect(self, self.raw_image)
            q_image = QImage(adjusted_img, width, height, bytes_per_line, QImage.Format_RGB888)
            self.image_pixmap = QPixmap.fromImage(q_image)
        self.update_preview()
    
    def update_preview(self):
        self.image_label.setPixmap(self.image_pixmap)

    def open_image(self):
        file_name = FileHandler(self, "Img").openDialog()

        if file_name:
            self.raw_image = cv.imread(cv.samples.findFile(file_name))
            self.image_pixmap = QPixmap.fromImage(QImage(file_name))
            self.update_preview()

            self.save_button.setEnabled(True)
    
    def start_webcam(self):
        self.initCamera()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(10)  # Adjust the time interval (ms) as needed
        self.start_webcam_button.setEnabled(False)
        self.stop_webcam_button.setEnabled(True)

    def initCamera(self):
        self.webcam = cv.VideoCapture(0)  # Use the default webcam (change the index if you have multiple webcams)
        self.webcam.set(cv.CAP_PROP_FRAME_WIDTH, media_width)
        self.webcam.set(cv.CAP_PROP_FRAME_HEIGHT, media_height)
    
    def stop_webcam(self):
        if self.timer:
            self.timer.stop()
        self.start_webcam_button.setEnabled(True)
        self.stop_webcam_button.setEnabled(False)
        self.webcam = None
        self.image_label.clear()

    def update_frame(self):
        ret, frame = self.webcam.read()
        if ret:
            height, width, channel = frame.shape
            bytes_per_line = 3 * width
            if self.effect:
                frame.data = image_effect.apply_effect(self, frame)
            q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
            self.image_pixmap = QPixmap.fromImage(q_image)
            self.update_preview()

    def save_image(self):
        if self.image_pixmap:
            # options = QFileDialog.Options()
            # options |= QFileDialog.ReadOnly
            # file_name, _ = QFileDialog.getSaveFileName(self, 'Save Image', '', 'Image Files (*.png *.jpg *.jpeg *.gif *.bmp *.tiff)', options=options)
            file_name = FileHandler(self, "Img").saveDialog()
            if file_name:
                self.image_pixmap.save(file_name)

    def record_video(self):
        if not self.is_recording:
            file_name = FileHandler(self, "Vid").saveDialog()
            self.initCamera()
            if file_name:
                fourcc = cv.VideoWriter_fourcc(*'XVID')  # Codec for AVI format
                self.video_writer = cv.VideoWriter(file_name, fourcc, 20.0, (640, 480))
                self.is_recording = True
                self.record_button.setText('Stop Recording')
        else:
            if self.video_writer:
                self.video_writer.release()
                self.is_recording = False
                self.record_button.setText('Record Video')
                self.play_button.setEnabled(True)  # Enable the "Play Video" button after recording

    def play_video(self):
        if self.is_recording and self.video_writer:
            self.video_player = cv.VideoCapture(self.video_writer.get_filename())
            self.play_button.setEnabled(False)  # Disable "Play Video" during playback

            if self.video_player.isOpened():
                while True:
                    ret, frame = self.video_player.read()
                    if not ret:
                        break

                    height, width, channel = frame.shape
                    bytes_per_line = 3 * width
                    q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
                    pixmap = QPixmap.fromImage(q_image)
                    self.image_label.setPixmap(pixmap)
                    QApplication.processEvents()  # Allow GUI updates
                self.video_player.release()
                self.play_button.setEnabled(True)  # Enable "Play Video" after playback

    def open_saved_video(self):
        file_name = FileHandler(self, "Vid").openDialog()
        # file_name, _ = QFileDialog.getOpenFileName(self, 'Open Video', '', 'Video Files (*.avi *.mp4)')
        if file_name:
            self.video_player = cv.VideoCapture(file_name)
            self.play_button.setEnabled(False)  # Disable "Play Video" during playback

            if self.video_player.isOpened():
                while True:
                    ret, frame = self.video_player.read()
                    if not ret:
                        break

                    height, width, channel = frame.shape
                    bytes_per_line = 3 * width
                    q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
                    pixmap = QPixmap.fromImage(q_image)
                    self.image_label.setPixmap(pixmap)
                    QApplication.processEvents()  # Allow GUI updates
                self.video_player.release()
                self.play_button.setEnabled(True)  # Enable "Play Video" after playback
