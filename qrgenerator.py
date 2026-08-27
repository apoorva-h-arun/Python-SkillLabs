import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox
from PIL import Image, ImageTk
import qrcode


class QRGeneratorApp:

    def __init__(self, root):
        self.root = root
        self.root.title("QR Code Generator")
        self.root.geometry("420x550")
        self.root.resizable(False, False)

        # Default color configurations
        self.fg_color = "#000000"
        self.bg_color = "#FFFFFF"
        self.qr_image = None

        self._build_ui()

    def _build_ui(self):
        # Entry Input Label & Box
        tk.Label(
            self.root, text="Enter Text or URL:", font=("Arial", 11, "bold")
        ).pack(pady=(15, 5))
        self.text_entry = tk.Entry(self.root, width=45, font=("Arial", 10))
        self.text_entry.pack(pady=5)

        # Color Selection Buttons Frame
        color_frame = tk.Frame(self.root)
        color_frame.pack(pady=10)

        self.fg_btn = tk.Button(
            color_frame,
            text="Foreground Color",
            command=self._choose_fg_color,
            bg=self.fg_color,
            fg="white",
        )
        self.fg_btn.grid(row=0, column=0, padx=10)

        self.bg_btn = tk.Button(
            color_frame,
            text="Background Color",
            command=self._choose_bg_color,
            bg=self.bg_color,
            fg="black",
        )
        self.bg_btn.grid(row=0, column=1, padx=10)

        # Generate Action Button
        tk.Button(
            self.root,
            text="Generate QR Code",
            font=("Arial", 10, "bold"),
            bg="#4CAF50",
            fg="white",
            padx=10,
            command=self.generate_qr,
        ).pack(pady=10)

        # Image Preview Display Area
        self.preview_label = tk.Label(
            self.root,
            text="QR Code preview will appear here",
            bg="#E0E0E0",
            width=35,
            height=14,
        )
        self.preview_label.pack(pady=10)

        # Save Action Button
        self.save_btn = tk.Button(
            self.root,
            text="Save QR Code",
            state=tk.DISABLED,
            command=self.save_qr,
        )
        self.save_btn.pack(pady=10)

    def _choose_fg_color(self):
        color = colorchooser.askcolor(title="Select Foreground Color")[1]
        if color:
            self.fg_color = color
            self.fg_btn.config(bg=color)

    def _choose_bg_color(self):
        color = colorchooser.askcolor(title="Select Background Color")[1]
        if color:
            self.bg_color = color
            self.bg_btn.config(bg=color)

    def generate_qr(self):
        data = self.text_entry.get().strip()
        if not data:
            messagebox.showwarning(
                "Input Error", "Please enter text or a URL first!"
            )
            return

        # Configure and build QR code instance
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)

        # Generate PIL image with selected colors
        self.qr_image = qr.make_image(
            fill_color=self.fg_color, back_color=self.bg_color
        ).convert("RGB")

        # Resize for preview inside UI window
        preview_img = self.qr_image.resize((220, 220), Image.Resampling.LANCZOS)
        self.tk_preview = ImageTk.PhotoImage(preview_img)

        # Update GUI label image
        self.preview_label.config(image=self.tk_preview, text="")
        self.save_btn.config(state=tk.NORMAL)

    def save_qr(self):
        if not self.qr_image:
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[
                ("PNG Files", "*.png"),
                ("JPEG Files", "*.jpg"),
                ("All Files", "*.*"),
            ],
            title="Save QR Code As",
        )
        if file_path:
            self.qr_image.save(file_path)
            messagebox.showinfo(
                "Success", f"QR Code saved successfully to:\n{file_path}"
            )


if __name__ == "__main__":
    root = tk.Tk()
    app = QRGeneratorApp(root)
    root.mainloop()
