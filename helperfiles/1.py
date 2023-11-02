# import sys

# from PyQt6.QtGui import QPixmap, QColor, QPalette
# from PyQt6.QtCore import QSize, Qt
# from PyQt6.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QWidget, QPushButton, QLabel


# # Subclass QMainWindow to customize your application's main window
# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
        
#         self.setWindowTitle("My App")

#         layout = QHBoxLayout()

#         img_widget = QLabel()
#         img = QPixmap("qt-tutorial/img.jpg")
#         img = img.scaled(100,100, Qt.AspectRatioMode aspectRatioMode = )
#         img_widget.setPixmap(img)
#         # img_widget.scaled

#         layout.addWidget(Color('red'))
#         layout.addWidget(img_widget)
#         layout.addWidget(Color('blue'))

#         widget = QWidget()
#         widget.setLayout(layout)

#         self.setFixedSize(QSize(1500, 800))

#         # self.setWindowTitle("My App")
#         # # self.setMinimumHeight(800)
#         # # self.setMinimumWidth(1000)

#         # button1 = QPushButton("Press Me!")
#         # button1.setCheckable(True)
#         # button1.clicked.connect(self.the_button_was_clicked)

#         # button = QPushButton("Press Me!")
#         # button.setCheckable(True)
#         # button.clicked.connect(self.the_button_was_clicked)
#         # button.clicked.connect(self.the_button_was_toggled)

#         # # Set the central widget of the Window.
#         # self.setCentralWidget(button)

#         # self.setFixedSize(QSize(1000, 800))

#         # widget = QLabel()
#         # widget.setPixmap(QPixmap("qt-tutorial/img.jpg"))

#         self.setCentralWidget(widget)


#     def the_button_was_clicked(self):
#         print("Clicked!")

#     def the_button_was_toggled(self, checked):
#         print("Checked?", checked)

# class Color(QWidget):

#     def __init__(self, color):
#         super(Color, self).__init__()
#         self.setAutoFillBackground(True)

#         palette = self.palette()
#         palette.setColor(QPalette.ColorRole.Window, QColor(color))
#         self.setPalette(palette)

# app = QApplication(sys.argv)

# window = MainWindow()
# window.show()

# app.exec()