import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QPushButton, QFileDialog, QWidget, QDialog, QCheckBox
from PyQt5.QtGui import QPixmap, QImage
import cv2
from PyQt5.QtCore import QTimer


class ObjectDetectionWindow(QDialog):
    def __init__(self):
        super(ObjectDetectionWindow, self).__init__()

        self.setWindowTitle("检测物品")
        self.setGeometry(200, 200, 400, 300)

        self.layout = QVBoxLayout(self)

        self.person_checkbox = QCheckBox("人", self)
        self.layout.addWidget(self.person_checkbox)

        self.pen_checkbox = QCheckBox("笔", self)
        self.layout.addWidget(self.pen_checkbox)

        self.book_checkbox = QCheckBox("书本", self)
        self.layout.addWidget(self.book_checkbox)

        self.confirm_button = QPushButton("确定", self)
        self.confirm_button.clicked.connect(self.confirm_selection)
        self.layout.addWidget(self.confirm_button)

    def confirm_selection(self):
        # Perform any action based on the selected items (e.g., display a checkmark)
        selected_items = []
        if self.person_checkbox.isChecked():
            selected_items.append("人")
        if self.pen_checkbox.isChecked():
            selected_items.append("笔")
        if self.book_checkbox.isChecked():
            selected_items.append("书本")

        print("Selected items:", selected_items)
        self.accept()


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Multimedia Window")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.image_label = QLabel(self)
        self.layout.addWidget(self.image_label)

        self.video_button = QPushButton("视频", self)
        self.video_button.clicked.connect(self.open_video)
        self.layout.addWidget(self.video_button)

        self.image_button = QPushButton("图片", self)
        self.image_button.clicked.connect(self.open_image)
        self.layout.addWidget(self.image_button)

        self.camera_button = QPushButton("摄像头", self)
        self.camera_button.clicked.connect(self.open_camera)
        self.layout.addWidget(self.camera_button)

        self.detect_button = QPushButton("检测物品", self)
        self.detect_button.clicked.connect(self.open_detection_window)
        self.layout.addWidget(self.detect_button)

        self.video_capture = None
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)

    def open_image(self):
        file_dialog = QFileDialog(self)
        file_path, _ = file_dialog.getOpenFileName(self, "图片", "", "图片 (*.png *.jpg *.bmp)")
        if file_path:
            pixmap = QPixmap(file_path)
            self.image_label.setPixmap(pixmap)

    def open_video(self):
        file_dialog = QFileDialog(self)
        file_path, _ = file_dialog.getOpenFileName(self, "视频", "", "视频 (*.mp4 *.avi)")
        if file_path:
            self.video_capture = cv2.VideoCapture(file_path)
            self.timer.start(33)  # Update every 33 milliseconds (30 fps)

    def update_frame(self):
        ret, frame = self.video_capture.read()
        if ret:
            height, width, channel = frame.shape
            bytes_per_line = 3 * width
            q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_image)
            self.image_label.setPixmap(pixmap)

    def open_camera(self):
        self.video_capture = cv2.VideoCapture(0)
        self.timer.start(33)  # Update every 33 milliseconds (30 fps)

    def open_detection_window(self):
        detection_window = ObjectDetectionWindow()
        result = detection_window.exec_()
        if result == QDialog.Accepted:
            print("Detection Confirmed")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
