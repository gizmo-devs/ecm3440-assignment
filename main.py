import sys
from PyQt5.QtWidgets import QApplication

from model.image_manipulator import ImageManipulator


def main():
    app = QApplication(sys.argv)
    window = ImageManipulator()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()