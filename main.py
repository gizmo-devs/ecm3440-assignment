import sys
import cv2 as cv
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QLabel, QVBoxLayout, QGridLayout, QPushButton, QWidget, QRadioButton, QGraphicsView, QGraphicsScene, QShortcut
from PyQt5.QtGui import QPixmap, QImage, QKeySequence
from PIL import Image
from PyQt5.QtCore import Qt, QTimer

width, height = 500, 400

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
        
        layoutGrid.addWidget(self.open_button, 1,1)
        layoutGrid.addWidget(self.save_button, 1,2)
        layoutGrid.addWidget(self.start_webcam_button, 2,1)
        layoutGrid.addWidget(self.stop_webcam_button, 2,2)
        
        EffectBlur = QRadioButton("Blur")
        EffectBlur.group = "Effect"
        EffectBlur.isChecked = self.toggle_effect(1)

        EffectGrey = QRadioButton("Grey")
        EffectGrey.group = "Effect"
        EffectGrey.isChecked = self.toggle_effect(2)

        layoutGrid.addWidget(EffectBlur, 3,1)
        layoutGrid.addWidget(EffectGrey, 3,2)
        
        self.layoutRoot.addLayout(layoutGrid)

        self.layoutRoot.addWidget(self.image_label)
        self.layoutRoot.addWidget(self.view)

        self.container = QWidget()
        self.container.setLayout(self.layoutRoot)

        self.setCentralWidget(self.container)

        self.webcam = None
        self.timer = None
    
    def toggle_effect(self, effect):
        self.effect=effect
        print(f"Updated effect = {effect}")

    def open_image(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(self, 'Open Image', '', 'Image Files (*.png *.jpg *.jpeg *.gif *.bmp *.tiff)', options=options)

        if file_name:
            image = Image.open(file_name)
            self.image_pixmap = QPixmap.fromImage(QImage(file_name))
            self.image_label.setPixmap(self.image_pixmap)

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
        self.webcam.set(cv.CAP_PROP_FRAME_WIDTH, width)
        self.webcam.set(cv.CAP_PROP_FRAME_HEIGHT, height)
    
    def stop_webcam(self):
        if self.timer:
            self.timer.stop()
        self.start_webcam_button.setEnabled(True)
        self.stop_webcam_button.setEnabled(False)
        self.image_label.clear()

    def update_frame(self):
        ret, frame = self.webcam.read()
        if ret:
            height, width, channel = frame.shape
            bytes_per_line = 3 * width
            if self.effect:
                adjusted_img = self.apply_effect(frame)
            q_image = QImage(adjusted_img, width, height, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_image)
            self.image_label.setPixmap(pixmap)
    
    def apply_effect(self, input):
        if self.effect == 1:
            gray = cv.cvtColor(input, cv.COLOR_BGR2GRAY)
            return cv.cvtColor(gray,cv.COLOR_BGR2RGB)
        return input

    def save_image(self):
        if self.image_pixmap:
            options = QFileDialog.Options()
            options |= QFileDialog.ReadOnly
            file_name, _ = QFileDialog.getSaveFileName(self, 'Save Image', '', 'Image Files (*.png *.jpg *.jpeg *.gif *.bmp *.tiff)', options=options)

            if file_name:
                self.image_pixmap.save(file_name)

def main():
    app = QApplication(sys.argv)
    
    window = ImageManipulator()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()