import tkinter as tk
from tkinter import filedialog, messagebox
from reportlab.pdfgen import canvas
from reportlab.lib.colors import white
from PIL import Image
import os
from pathlib import Path

# Get Downloads folder dynamically
DOWNLOADS = str(Path.home() / "Downloads")

class ipconvtr:
    def __init__(self, root):
        self.root = root
        self.root.configure(bg="#e0e0e0")
        self.image_paths = []
        self.output_pdf_name = tk.StringVar()
        self.selected_images_listbox = tk.Listbox(root, selectmode=tk.MULTIPLE)
        self.ui()

    def neumorphic_button(self, parent, text, command):
        frame = tk.Frame(parent, bg="#e0e0e0")
        frame.pack(pady=10)
        top = tk.Frame(frame, bg="#ffffff")
        top.pack()
        btn = tk.Button(
            top, text=text, command=command,
            bg="#e0e0e0", fg="#333333",
            relief="flat", font=("Helvetica", 10, "bold"),
            padx=20, pady=10
        )
        btn.pack()
        shadow = tk.Frame(frame, bg="#a3a3a3", height=2)
        shadow.pack(fill="x")

    def ui(self):
        title = tk.Label(
            self.root, text="Image to PDF Converter",
            bg="#e0e0e0", fg="#333333",
            font=("Helvetica", 16, "bold")
        )
        title.pack(pady=20)

        self.neumorphic_button(self.root, "Select Images", self.select_images)

        self.selected_images_listbox.pack(padx=20, pady=10, fill=tk.BOTH)

        label = tk.Label(self.root, text="Enter PDF name", bg="#e0e0e0", fg="#333333")
        label.pack(pady=(10,5))

        entry_frame = tk.Frame(self.root, bg="#ffffff")
        entry_frame.pack(padx=20)
        self.pdf_name_entry = tk.Entry(entry_frame, textvariable=self.output_pdf_name,
                                       relief="flat", justify="center", font=("Helvetica", 10), width=30)
        self.pdf_name_entry.pack(ipady=6)

        self.neumorphic_button(self.root, "Convert to PDF", self.convert_images)

    def select_images(self):
        self.image_paths = filedialog.askopenfilenames(
            title="Select Images",
            filetypes=[("Image Files", "*.png *.jpg *.jpeg")]
        )
        self.update_selected_images_listbox()

    def update_selected_images_listbox(self):
        self.selected_images_listbox.delete(0, tk.END)
        for path in self.image_paths:
            name = os.path.basename(path)
            self.selected_images_listbox.insert(tk.END, name)

    def convert_images(self):
        if not self.image_paths:
            return

        # Save PDF in Downloads folder automatically
        filename = self.output_pdf_name.get() if self.output_pdf_name.get() else "output"
        output_pdfpath = os.path.join(DOWNLOADS, filename + ".pdf")

        pdf = canvas.Canvas(output_pdfpath, pagesize=(612, 792))

        for image_path in self.image_paths:
            img = Image.open(image_path)
            available_width = 540
            available_height = 720
            scale_factor = min(available_width / img.width, available_height / img.height)
            new_width = img.width * scale_factor
            new_height = img.height * scale_factor
            x_centered = (612 - new_width) / 2
            y_centered = (792 - new_height) / 2

            pdf.setFillColor(white)
            pdf.rect(0, 0, 612, 792, fill=True)
            pdf.drawInlineImage(img, x_centered, y_centered, width=new_width, height=new_height)
            pdf.showPage()

        pdf.save()
        messagebox.showinfo("Done", f"watch Downloads folder:\n{output_pdfpath}")

def main():
    root = tk.Tk()
    root.title("Image to PDF")
    root.geometry("420x600")
    root.resizable(False, False)
    ipconvtr(root)
    root.mainloop()

if __name__ == "__main__":
    main()
