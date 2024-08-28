import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageDraw, ImageFont
import os
import shutil

class WatermarkApp:
    def __init__(self, master):
        self.master = master
        master.title("Image Watermarking Tool")
        master.geometry("400x350")

        self.image_path = None
        self.watermark_text = tk.StringVar()
        self.output_path = None

        # Create GUI elements
        tk.Label(master, text="Select an image:").pack(pady=10)
        tk.Button(master, text="Browse", command=self.browse_image).pack()

        tk.Label(master, text="Enter watermark text:").pack(pady=10)
        tk.Entry(master, textvariable=self.watermark_text).pack()

        tk.Button(master, text="Add Watermark", command=self.add_watermark).pack(pady=20)
        
        self.download_button = tk.Button(master, text="Download Watermarked Image", command=self.download_image, state=tk.DISABLED)
        self.download_button.pack(pady=10)

    def browse_image(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if self.image_path:
            messagebox.showinfo("Image Selected", f"Image selected: {os.path.basename(self.image_path)}")

    def add_watermark(self):
        if not self.image_path:
            messagebox.showerror("Error", "Please select an image first.")
            return

        if not self.watermark_text.get():
            messagebox.showerror("Error", "Please enter watermark text.")
            return

        try:
            # Open the image
            with Image.open(self.image_path) as img:
                # Create a drawing object
                draw = ImageDraw.Draw(img)

                # Choose a font
                font = ImageFont.truetype("arial.ttf", 36)

                # Get image size
                width, height = img.size

                # Calculate text size
                text_width, text_height = draw.textsize(self.watermark_text.get(), font=font)

                # Calculate text position (bottom right corner)
                x = width - text_width - 10
                y = height - text_height - 10

                # Add the watermark text
                draw.text((x, y), self.watermark_text.get(), font=font, fill=(255, 255, 255, 128))

                # Save the watermarked image
                self.output_path = os.path.splitext(self.image_path)[0] + "_watermarked.png"
                img.save(self.output_path)

                messagebox.showinfo("Success", f"Watermarked image saved as {os.path.basename(self.output_path)}")
                self.download_button.config(state=tk.NORMAL)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def download_image(self):
        if not self.output_path:
            messagebox.showerror("Error", "No watermarked image available for download.")
            return

        download_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
            initialfile=os.path.basename(self.output_path)
        )

        if download_path:
            try:
                shutil.copy2(self.output_path, download_path)
                messagebox.showinfo("Success", f"Watermarked image downloaded as {os.path.basename(download_path)}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to download image: {str(e)}")

root = tk.Tk()
app = WatermarkApp(root)
root.mainloop()