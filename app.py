import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import math
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_TYPES = [("Képek", "*.png *.jpg *.jpeg *.bmp *.webp")]


class ImageComparer:
    def __init__(self, root):
        self.root = root
        self.root.title("Kép Egyezés Exportáló")

        self.image1_path = ""
        self.image2_path = ""
        self.output_path = ""

        tk.Button(root, text="Első kép", command=self.select_image1).pack(pady=5)
        self.label1 = tk.Label(root, text="Nincs kiválasztva")
        self.label1.pack()

        tk.Button(root, text="Második kép", command=self.select_image2).pack(pady=5)
        self.label2 = tk.Label(root, text="Nincs kiválasztva")
        self.label2.pack()

        tk.Label(root, text="Minimum átlátszatlanság (%)").pack(pady=(10, 0))

        self.min_opacity = tk.DoubleVar(value=50)
        tk.Scale(
            root,
            from_=0,
            to=100,
            orient="horizontal",
            variable=self.min_opacity
        ).pack(fill="x", padx=10)

        tk.Button(root, text="Export hely", command=self.select_output).pack(pady=5)
        self.label3 = tk.Label(root, text="Nincs kiválasztva")
        self.label3.pack()

        tk.Button(root, text="Export", command=self.export, bg="lightgreen").pack(pady=15)

    def select_image1(self):
        path = filedialog.askopenfilename(initialdir=BASE_DIR, filetypes=IMAGE_TYPES)
        if path:
            self.image1_path = path
            self.label1.config(text=os.path.basename(path))

    def select_image2(self):
        path = filedialog.askopenfilename(initialdir=BASE_DIR, filetypes=IMAGE_TYPES)
        if path:
            self.image2_path = path
            self.label2.config(text=os.path.basename(path))

    def select_output(self):
        path = filedialog.asksaveasfilename(
            initialdir=BASE_DIR,
            defaultextension=".png",
            filetypes=[("PNG", "*.png")]
        )
        if path:
            self.output_path = path
            self.label3.config(text=os.path.basename(path))

    def export(self):
        if not self.image1_path:
            messagebox.showerror("Hiba", "Nincs első kép.")
            return

        if not self.image2_path:
            messagebox.showerror("Hiba", "Nincs második kép.")
            return

        if not self.output_path:
            messagebox.showerror("Hiba", "Nincs export hely.")
            return

        img1 = Image.open(self.image1_path).convert("RGBA")
        img2 = Image.open(self.image2_path).convert("RGBA")

        if img1.size != img2.size:
            messagebox.showerror("Hiba", "A két kép mérete nem egyezik.")
            return

        width, height = img1.size
        result = Image.new("RGBA", (width, height))

        min_alpha = self.min_opacity.get() / 100.0
        max_distance = math.sqrt(3 * 255 * 255)

        for y in range(height):
            for x in range(width):
                r1, g1, b1, _ = img1.getpixel((x, y))
                r2, g2, b2, _ = img2.getpixel((x, y))

                distance = math.sqrt(
                    (r1 - r2) ** 2 +
                    (g1 - g2) ** 2 +
                    (b1 - b2) ** 2
                )

                difference = distance / max_distance
                similarity = 1.0 - difference
                alpha = min_alpha + similarity * (1.0 - min_alpha)

                result.putpixel(
                    (x, y),
                    (
                        (r1 + r2) // 2,
                        (g1 + g2) // 2,
                        (b1 + b2) // 2,
                        int(alpha * 255)
                    )
                )

        result.save(self.output_path)
        messagebox.showinfo("Kész", f"Sikeresen exportálva:\n{self.output_path}")


root = tk.Tk()
root.geometry("450x350")
ImageComparer(root)
root.mainloop()