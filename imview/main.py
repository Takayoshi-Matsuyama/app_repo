# Copyright 2026 Takayoshi Matsuyama
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
import cv2
import numpy as np
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QFileDialog,
    QSlider,
    QHBoxLayout,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QImage, QPixmap


class ImageViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Viewer & Processor")
        self.resize(800, 600)

        # 画像データを保持する変数
        self.original_image = None
        self.processed_image = None

        # UIのセットアップ
        self.init_ui()

    def init_ui(self):
        # メインウィジェットとレイアウト
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)

        # 画像表示用のラベル
        self.image_label = QLabel("ここに画像が表示されます")
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setMinimumSize(400, 300)
        self.image_label.setStyleSheet("border: 1px solid black;")
        layout.addWidget(self.image_label)

        # 操作パネル（ボタンとスライダー）
        control_layout = QHBoxLayout()

        self.load_button = QPushButton("画像を読み込む")
        self.load_button.clicked.connect(self.load_image)
        control_layout.addWidget(self.load_button)

        # 特徴抽出（二値化）のパラメータ調整用スライダー
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(0, 255)
        self.slider.setValue(127)  # 初期値
        self.slider.valueChanged.connect(self.apply_image_processing)
        control_layout.addWidget(self.slider)

        layout.addLayout(control_layout)

    def load_image(self):
        # ファイル選択ダイアログ
        file_name, _ = QFileDialog.getOpenFileName(
            self, "画像を開く", "", "Image Files (*.png *.jpg *.bmp)"
        )
        if file_name:
            # OpenCVで画像を読み込み (日本語パス対応などが必要な場合は np.fromfile 等を使用)
            self.original_image = cv2.imread(file_name)
            if self.original_image is not None:
                self.apply_image_processing()

    def apply_image_processing(self):
        if self.original_image is None:
            return

        # スライダーの値を取得してパラメータとして使用
        threshold_val = self.slider.value()

        # 例: グレースケール化して二値化（特徴抽出の前処理などを想定）
        gray = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray, threshold_val, 255, cv2.THRESH_BINARY)

        # 表示用にカラー(BGR)に戻す
        self.processed_image = cv2.cvtColor(binary, cv2.COLOR_GRAY2BGR)
        self.update_preview()

    def update_preview(self):
        if self.processed_image is None:
            return

        # OpenCV(BGR)の配列をPyQt(RGB)のQImageに変換
        # Note: ここでは、表示する画像として processed_image を使用していますが、
        #       必要に応じて original_image を使用することもできます。
        #       (右辺を original_image に変更する)
        image = self.processed_image

        height, width, channel = image.shape
        bytes_per_line = 3 * width

        # BGRからRGBへ変換してQImageを作成
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        q_image = QImage(
            rgb_image.data, width, height, bytes_per_line, QImage.Format.Format_RGB888
        )

        # QPixmapに変換してラベルにセット
        pixmap = QPixmap.fromImage(q_image)
        # ラベルのサイズに合わせて縮小表示
        self.image_label.setPixmap(
            pixmap.scaled(
                self.image_label.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageViewer()
    window.show()
    sys.exit(app.exec())
