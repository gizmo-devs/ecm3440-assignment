import cv2 as cv
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QLabel, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton, QWidget, QRadioButton, QGraphicsView, QGraphicsScene, QShortcut
from PyQt5.QtGui import QPixmap, QImage, QKeySequence
from PIL import Image
from PyQt5.QtCore import Qt, QTimer
from numpy import array

# import model.image_effect as image_effect

media_width, media_height = 500, 400

class ImageManipulator(QMainWindow):
    def __init__(self):
        super().__init__()

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

        self.open_button = QPushButton('Open Image', self)
        self.open_button.clicked.connect(self.open_image)

        self.save_button = QPushButton('Save Image', self)
        self.save_button.clicked.connect(self.save_image)
        self.save_button.setEnabled(False)

        self.start_webcam_button = QPushButton('Start Webcam', self)
        self.start_webcam_button.clicked.connect(self.start_webcam)
        self.start_webcam_button.setEnabled(True)

        self.stop_webcam_button = QPushButton('Stop Webcam', self)
        self.stop_webcam_button.clicked.connect(self.stop_webcam)
        self.stop_webcam_button.setEnabled(False)

        self.image_label = QLabel()
        self.image_pixmap = None

        self.layoutRoot = QVBoxLayout()
        layoutGrid = QGridLayout()
        effectlayout = QHBoxLayout()
        
        layoutGrid.addWidget(self.open_button, 1,1)
        layoutGrid.addWidget(self.save_button, 1,2)
        layoutGrid.addWidget(self.start_webcam_button, 2,1)
        layoutGrid.addWidget(self.stop_webcam_button, 2,2)

        # for effect in ["None", "Blur", "Grey", "Canny", "Sobel"]:
        #     effectlayout.addWidget(effect.Radio(effect))

        EffectNone = QRadioButton("None")
        EffectNone.group = "Effect"
        EffectNone.clicked.connect(lambda: self.toggle_effect(0))

        EffectBlur = QRadioButton("Blur")
        EffectBlur.group = "Effect"
        EffectBlur.clicked.connect(lambda: self.toggle_effect(1))
        
        EffectGrey = QRadioButton("Grey")
        EffectGrey.group = "Effect"
        EffectGrey.clicked.connect(lambda: self.toggle_effect(2))

        EffectCanny = QRadioButton("Canny")
        EffectCanny.group = "Effect"
        EffectCanny.clicked.connect(lambda: self.toggle_effect(3))
        
        EffectSobel = QRadioButton("Sobel")
        EffectSobel.group = "Effect"
        EffectSobel.clicked.connect(lambda: self.toggle_effect(4))

        effectlayout.addWidget(EffectNone)
        effectlayout.addWidget(EffectBlur)
        effectlayout.addWidget(EffectGrey)
        effectlayout.addWidget(EffectCanny)
        effectlayout.addWidget(EffectSobel)
        
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

    def apply_effect(self, input):
        if self.effect == 1:
            # blur
            blur = cv.blur(input,(5,5))
            return cv.cvtColor(blur,cv.COLOR_BGR2RGB)
        if self.effect == 2:
            # grey
            gray = cv.cvtColor(input, cv.COLOR_BGR2GRAY)
            return cv.cvtColor(gray,cv.COLOR_BGR2RGB)
        if self.effect == 3:
            # Canny
            edges = cv.Canny(input,100,200)
            return cv.cvtColor(edges,cv.COLOR_BGR2RGB)
        if self.effect == 4:
            # Sobel
            gsobel = cv.Sobel(input,cv.CV_8U,1,0,ksize=3)
            return cv.cvtColor(gsobel,cv.COLOR_BGR2RGB)
            
        return cv.cvtColor(input, cv.COLOR_BGR2RGB)
    
    def toggle_effect(self, effect):
        self.effect=effect
        print(f"Updated effect = {effect}")
        if not self.webcam:
            height, width, channel = self.raw_image.shape
            bytes_per_line = 3 * width
            adjusted_img = self.apply_effect(self.raw_image)
            q_image = QImage(adjusted_img, width, height, bytes_per_line, QImage.Format_RGB888)
            self.image_pixmap = QPixmap.fromImage(q_image)
        self.update_preview()
    
    def update_preview(self):
        self.image_label.setPixmap(self.image_pixmap)

    def open_image(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(self, 'Open Image', '', 'Image Files (*.png *.jpg *.jpeg *.gif *.bmp *.tiff)', options=options)

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
                frame.data = self.apply_effect(frame)
            q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
            self.image_pixmap = QPixmap.fromImage(q_image)
            self.update_preview()

    def save_image(self):
        if self.image_pixmap:
            options = QFileDialog.Options()
            options |= QFileDialog.ReadOnly
            file_name, _ = QFileDialog.getSaveFileName(self, 'Save Image', '', 'Image Files (*.png *.jpg *.jpeg *.gif *.bmp *.tiff)', options=options)

            if file_name:
                self.image_pixmap.save(file_name)
