import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import fitz  # PyMuPDF library
import os
import sys
from PIL import Image, ImageTk

# Store references to images to prevent them from turning blank
thumbnail_references = []
checkbox_vars = {}

def resource_path(relative_path):
    """ Get the absolute path to a resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def get_color_rgb(color_name):
    colors = {
        "Black": (0, 0, 0), "Red": (1, 0, 0), "Blue": (0, 0, 1),
        "Green": (0, 0.5, 0), "Gray": (0.5, 0.5, 0.5), "White": (1, 1, 1)
    }
    return colors.get(color_name, (0, 0, 0))

def get_font_name(display_name):
    fonts = {
        "Arial / Helvetica": "helv",
        "Times New Roman": "times-roman",
        "Courier": "cour"
    }
    return fonts.get(display_name, "helv")

def select_input_file():
    filepath = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if filepath:
        input_entry.delete(0, tk.END)
        input_entry.insert(0, filepath)
        load_previews(filepath)

def load_previews(filepath):
    """ Generates thumbnails and checkboxes for every page """
    # Clear existing previews
    for widget in scrollable_frame.winfo_children():
        widget.destroy()
    thumbnail_references.clear()
    checkbox_vars.clear()

    status_label.config(text="Status: Loading previews... please wait.", foreground="blue")
    root.update()

    try:
        doc = fitz.open(filepath)
        total_pages = len(doc)
        
        columns = 4 # How many previews per row
        
        for i in range(total_pages):
            # Update UI occasionally so it doesn't freeze on huge PDFs
            if i % 10 == 0:
                status_label.config(text=f"Status: Generating preview {i}/{total_pages}...")
                root.update()

            page = doc[i]
            # Create a small thumbnail image
            pix = page.get_pixmap(matrix=fitz.Matrix(0.1, 0.1))
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            photo = ImageTk.PhotoImage(img)
            thumbnail_references.append(photo)

            row = (i // columns) * 2
            col = i % columns

            # Display thumbnail
            lbl = tk.Label(scrollable_frame, image=photo, bd=1, relief="solid")
            lbl.grid(row=row, column=col, padx=10, pady=(10, 0))

            # Display checkbox
            var = tk.BooleanVar()
            checkbox_vars[i] = var
            chk = ttk.Checkbutton(scrollable_frame, text=f"Pg {i+1} Rotate", variable=var)
            chk.grid(row=row+1, column=col, pady=(0, 10))

        doc.close()
        status_label.config(text="Status: Ready", foreground="black")

    except Exception as e:
        status_label.config(text="Status: Error loading previews.", foreground="red")
        messagebox.showerror("Error", f"Could not load PDF previews:\n{str(e)}")

def process_pdf():
    input_pdf = input_entry.get()
    
    if not input_pdf or not os.path.exists(input_pdf):
        messagebox.showerror("Error", "Please select a valid PDF file.")
        return

    output_pdf = filedialog.asksaveasfilename(
        defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")],
        title="Save New PDF As..."
    )
    if not output_pdf: return

    status_label.config(text="Status: Processing... Please wait.", foreground="blue")
    root.update()

    try:
        # Get UI Settings
        fontsize = int(size_var.get())
        color = get_color_rgb(color_var.get())
        fontname = get_font_name(font_var.get())
        position = pos_var.get()
        rotation_angle = int(rot_angle_var.get().replace("°", ""))

        doc = fitz.open(input_pdf)
        total_pages = len(doc)
        
        for page_num in range(total_pages):
            page = doc[page_num]
            
            # 1. Rotate the page if checked in the preview window
            if page_num in checkbox_vars and checkbox_vars[page_num].get():
                page.set_rotation(page.rotation + rotation_angle)

            # 2. Add Page Numbers
            text = f"Page {page_num + 1} of {total_pages}"
            text_length = fitz.get_text_length(text, fontname=fontname, fontsize=fontsize)
            
            page_rect = page.rect
            margin_x = 30
            margin_y = 30
            
            # X coordinate
            if "Left" in position: x = margin_x
            elif "Right" in position: x = page_rect.width - margin_x - text_length
            else: x = (page_rect.width / 2) - (text_length / 2) # Center
                
            # Y coordinate
            if "Top" in position: y = margin_y + fontsize
            else: y = page_rect.height - margin_y # Bottom
            
            page.insert_text((x, y), text, fontsize=fontsize, fontname=fontname, color=color)
            
        doc.save(output_pdf)
        doc.close()
        
        status_label.config(text="Status: Finished successfully!", foreground="green")
        messagebox.showinfo("Success", f"PDF saved successfully!\nTotal Pages: {total_pages}")
        
    except Exception as e:
        status_label.config(text="Status: Error occurred.", foreground="red")
        messagebox.showerror("Error", str(e))

# --- GUI Setup ---
root = tk.Tk()
root.title("STA Singapore QC - PDF Manager")
root.geometry("1100x700")
root.eval('tk::PlaceWindow . center')

style = ttk.Style(root)
style.theme_use('clam')

# --- Header with Logo and Name ---
header_frame = tk.Frame(root, bg="#ffffff", bd=2, relief="groove")
header_frame.pack(fill="x", padx=10, pady=10)

name_label = tk.Label(header_frame, text="Nicholas Tok\nSTA Singapore QC Lab Instrument", 
                      font=("Arial", 14, "bold"), bg="#ffffff", justify="left")
name_label.pack(side="left", padx=15, pady=10)

try:
    logo_path = resource_path("logo.jpg")
    logo_img = Image.open(logo_path)
    logo_img.thumbnail((200, 80)) # Resizes logo beautifully
    logo_photo = ImageTk.PhotoImage(logo_img)
    logo_label = tk.Label(header_frame, image=logo_photo, bg="#ffffff")
    logo_label.image = logo_photo # Keep reference
    logo_label.pack(side="right", padx=15, pady=5)
except Exception:
    tk.Label(header_frame, text="[WuXi AppTec Logo Missing]", bg="#ffffff").pack(side="right", padx=15)

# --- Main Split Window ---
main_paned = ttk.PanedWindow(root, orient=tk.HORIZONTAL)
main_paned.pack(fill="both", expand=True, padx=10, pady=5)

# Left Panel: Controls
left_frame = ttk.Frame(main_paned)
main_paned.add(left_frame, weight=1)

# Right Panel: Previews
right_frame = ttk.LabelFrame(main_paned, text="PDF Preview & Rotation")
main_paned.add(right_frame, weight=3)

# -- Left Panel Controls --
file_frame = ttk.LabelFrame(left_frame, text="1. Select PDF")
file_frame.pack(fill="x", pady=10)

input_entry = ttk.Entry(file_frame)
input_entry.pack(fill="x", padx=10, pady=5)
ttk.Button(file_frame, text="Browse", command=select_input_file).pack(pady=5)

num_frame = ttk.LabelFrame(left_frame, text="2. Page Number Styling")
num_frame.pack(fill="x", pady=10)

# Font Style
ttk.Label(num_frame, text="Font:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
font_var = tk.StringVar(value="Arial / Helvetica")
ttk.Combobox(num_frame, textvariable=font_var, state="readonly", width=17, 
             values=("Arial / Helvetica", "Times New Roman", "Courier")).grid(row=0, column=1, pady=5)

# Position
ttk.Label(num_frame, text="Position:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
pos_var = tk.StringVar(value="Bottom Center")
ttk.Combobox(num_frame, textvariable=pos_var, state="readonly", width=17,
             values=("Bottom Left", "Bottom Center", "Bottom Right", "Top Left", "Top Center", "Top Right")).grid(row=1, column=1, pady=5)

# Font Size
ttk.Label(num_frame, text="Size:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
size_var = tk.StringVar(value="11")
ttk.Spinbox(num_frame, from_=6, to=36, textvariable=size_var, width=15).grid(row=2, column=1, pady=5)

# Font Color
ttk.Label(num_frame, text="Color:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
color_var = tk.StringVar(value="Black")
ttk.Combobox(num_frame, textvariable=color_var, state="readonly", width=17,
             values=("Black", "Red", "Blue", "Green", "Gray", "White")).grid(row=3, column=1, pady=5)

# Rotation Angle for Checked Pages
rot_frame = ttk.LabelFrame(left_frame, text="3. Rotation Settings")
rot_frame.pack(fill="x", pady=10)
ttk.Label(rot_frame, text="Checked Angle:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
rot_angle_var = tk.StringVar(value="90°")
ttk.Combobox(rot_frame, textvariable=rot_angle_var, state="readonly", width=10,
             values=("90°", "180°", "270°")).grid(row=0, column=1, pady=5)

# Process Button
tk.Button(left_frame, text="PROCESS & SAVE PDF", command=process_pdf, 
          bg="#004C99", fg="white", font=("Arial", 11, "bold"), pady=10).pack(fill="x", pady=20)

status_label = ttk.Label(left_frame, text="Status: Ready", font=("Arial", 10, "bold"))
status_label.pack()

# -- Right Panel Previews (Scrollable Canvas) --
canvas = tk.Canvas(right_frame, bg="#e0e0e0")
scrollbar = ttk.Scrollbar(right_frame, orient="vertical", command=canvas.yview)
scrollable_frame = ttk.Frame(canvas)

scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

root.mainloop()
