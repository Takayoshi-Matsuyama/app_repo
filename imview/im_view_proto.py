import customtkinter as ctk
import cv2
from tkinter import filedialog
from PIL import Image

# 画面の基本設定
ctk.set_appearance_mode("System")  # Windowsの設定に合わせてライト/ダークを自動切り替え
ctk.set_default_color_theme("blue")


class ImageProcessorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("画像処理アプリ")
        self.geometry("400x250")

        self.image_path = None

        # --- UIレイアウト ---
        self.label = ctk.CTkLabel(
            self, text="画像を選択してください", font=("Arial", 16)
        )
        self.label.pack(pady=20)

        self.btn_open = ctk.CTkButton(self, text="画像を開く", command=self.open_image)
        self.btn_open.pack(pady=10)

        self.btn_process = ctk.CTkButton(
            self,
            text="白黒に変換して保存",
            command=self.process_image,
            state="disabled",
        )
        self.btn_process.pack(pady=10)

    # 画像を開く処理
    def open_image(self):
        self.image_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")]
        )
        if self.image_path:
            self.label.configure(text=f"選択中: {self.image_path.split('/')[-1]}")
            self.btn_process.configure(state="normal")  # ボタンを有効化

    # 画像処理と保存
    def process_image(self):
        if not self.image_path:
            return

        # OpenCVで画像を読み込み
        img = cv2.imread(self.image_path)

        # グレースケール変換（画像処理の例）
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # 保存先を選択
        save_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")],
        )

        if save_path:
            cv2.imwrite(save_path, gray_img)
            self.label.configure(text="保存が完了しました！")


if __name__ == "__main__":
    app = ImageProcessorApp()
    app.mainloop()
