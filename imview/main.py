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

# 変更点: PyQt6 を PySide6 に変更
from PySide6.QtWidgets import (
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
from PySide6.QtCore import Qt
from PySide6.QtGui import QImage, QPixmap


class ImageViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Viewer & Processor")
        # 左右に並べるため、ウィンドウサイズを横長に変更
        self.resize(1000, 500)

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

        # --- 変更点: 左右に画像を並べるレイアウト ---
        image_layout = QHBoxLayout()

        # 左側 (元画像用)
        self.label_original = QLabel("元画像")
        self.label_original.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_original.setMinimumSize(400, 300)
        self.label_original.setStyleSheet("border: 1px solid black;")
        image_layout.addWidget(self.label_original)

        # 右側 (処理結果用)
        self.label_processed = QLabel("処理結果")
        self.label_processed.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_processed.setMinimumSize(400, 300)
        self.label_processed.setStyleSheet("border: 1px solid black;")
        image_layout.addWidget(self.label_processed)

        layout.addLayout(image_layout)
        # ----------------------------------------

        # 操作パネル（ボタンとスライダー）
        control_layout = QHBoxLayout()

        self.load_button = QPushButton("画像を読み込む")
        self.load_button.clicked.connect(self.load_image)
        control_layout.addWidget(self.load_button)

        # 特徴抽出（二値化）のパラメータ調整用スライダー
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(0, 255)
        self.slider.setValue(127)
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
                # 読み込んだらすぐに左側に元画像を表示
                self.display_image(self.original_image, self.label_original)
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

        # 右側に処理結果を表示
        self.display_image(self.processed_image, self.label_processed)

    # --- 変更点: 表示処理を共通の関数化 ---
    def display_image(self, cv_image, label_widget):
        height, width, channel = cv_image.shape
        bytes_per_line = 3 * width

        # BGRからRGBへ変換してQImageを作成
        rgb_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        q_image = QImage(
            rgb_image.data, width, height, bytes_per_line, QImage.Format.Format_RGB888
        )

        # QPixmapに変換してラベルにセット
        pixmap = QPixmap.fromImage(q_image)
        # ラベルのサイズに合わせて縮小表示
        label_widget.setPixmap(
            pixmap.scaled(
                label_widget.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageViewer()
    window.show()
    sys.exit(app.exec())
