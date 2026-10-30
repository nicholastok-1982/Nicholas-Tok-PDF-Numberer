import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import fitz  # PyMuPDF library
import os

def select_input_file():
    filepath = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if filepath:
        input_entry.delete(0, tk.END)
        input_entry.insert(0, filepath)

def parse_pages(page_string, max_pages):
    """Converts a string like '1, 3, 5-7' into exact page numbers"""
    pages = set()
    if not page_string.strip():
        return pages
    
    parts = page_string.replace(" ", "").split(',')
    for part in parts:
        if '-' in part:
            try:
                start, end = part.split('-')
                start_idx = max(0, int(start) - 1) # 0-indexed
                end_idx = min(max_pages, int(end))
                pages.update(range(start_idx, end_idx))
            except ValueError:
                pass
        else:
            try:
                idx = int(part) - 1
                if 0 <= idx < max_pages:
                    pages.add(idx)
            except ValueError:
                pass
    return pages

def get_color_rgb(color_name):
    colors = {
        "Black": (0, 0, 0),
        "Red": (1, 0, 0),
        "Blue": (0, 0, 1),
        "Green": (0, 0.5, 0),
        "Gray": (0.5, 0.5, 0.5),
        "White": (1, 1, 1)
    }
    return colors.get(color_name, (0, 0, 0))

def process_pdf():
    input_pdf = input_entry.get()
    
    if not input_pdf or not os.path.exists(input_pdf):
        messagebox.showerror("Error", "Please select a valid PDF file.")
        return

    output_pdf = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("PDF files", "*.pdf")],
        title="Save New PDF As..."
    )
    
    if not output_pdf:
        return

    status_label.config(text="Status: Processing... Please wait.", foreground="blue")
    root.update()

    try:
        # Get UI Settings
        try:
            fontsize = int(size_var.get())
        except ValueError:
            fontsize = 11
            
        color = get_color_rgb(color_var.get())
        position = pos_var.get()
        rotation_angle = int(rot_angle_var.get().replace("°", ""))

        # Open the PDF
        doc = fitz.open(input_pdf)
        total_pages = len(doc)
        
        # Determine which pages to rotate
        pages_to_rotate = parse_pages(rotate_entry.get(), total_pages)
        
        for page_num in range(total_pages):
            page = doc[page_num]
            
            # 1. Rotate the page if requested
            if page_num in pages_to_rotate:
                page.set_rotation(page.rotation + rotation_angle)

            # 2. Add Page Numbers
            text = f"Page {page_num + 1} of {total_pages}"
            
            # Calculate text width to center/align properly
            text_length = fitz.get_text_length(text, fontname="helv", fontsize=fontsize)
            page_rect = page.rect
            margin_x = 30
            margin_y = 30
            
            # Determine X coordinate (Left, Center, Right)
            if "Left" in position:
                x = margin_x
            elif "Right" in position:
                x = page_rect.width - margin_x - text_length
            else: # Center
                x = (page_rect.width / 2) - (text_length / 2)
                
            # Determine Y coordinate (Top, Bottom)
            if "Top" in position:
                y = margin_y + fontsize
            else: # Bottom
                y = page_rect.height - margin_y
            
            # Insert the text
            page.insert_text((x, y), text, fontsize=fontsize, fontname="helv", color=color)
            
        # Save
        doc.save(output_pdf)
        doc.close()
        
        status_label.config(text="Status: Finished successfully!", foreground="green")
        messagebox.showinfo("Success", f"PDF saved successfully!\nTotal Pages: {total_pages}")
        
    except Exception as e:
        status_label.config(text="Status: Error occurred.", foreground="red")
        messagebox.showerror("Error", f"An error occurred:\n{str(e)}")

# --- GUI Setup ---
root = tk.Tk()
root.title("Advanced PDF Manager")
root.geometry("500x500")
root.eval('tk::PlaceWindow . center')

style = ttk.Style(root)
style.theme_use('clam')

# 1. File Selection Frame
file_frame = ttk.LabelFrame(root, text="1. Select PDF File")
file_frame.pack(fill="x", padx=15, pady=10)

input_entry = ttk.Entry(file_frame, width=45)
input_entry.pack(side=tk.LEFT, padx=10, pady=10)

browse_btn = ttk.Button(file_frame, text="Browse", command=select_input_file)
browse_btn.pack(side=tk.LEFT, padx=5, pady=10)

# 2. Page Number Options Frame
number_frame = ttk.LabelFrame(root, text="2. Page Number Styling")
number_frame.pack(fill="x", padx=15, pady=10)

# Position
ttk.Label(number_frame, text="Position:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
pos_var = tk.StringVar(value="Bottom Center")
pos_dropdown = ttk.Combobox(number_frame, textvariable=pos_var, state="readonly", width=15)
pos_dropdown['values'] = ("Bottom Left", "Bottom Center", "Bottom Right", "Top Left", "Top Center", "Top Right")
pos_dropdown.grid(row=0, column=1, padx=10, pady=5, sticky="w")

# Font Size
ttk.Label(number_frame, text="Font Size:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
size_var = tk.StringVar(value="11")
size_spinbox = ttk.Spinbox(number_frame, from_=6, to=36, textvariable=size_var, width=13)
size_spinbox.grid(row=1, column=1, padx=10, pady=5, sticky="w")

# Font Color
ttk.Label(number_frame, text="Font Color:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
color_var = tk.StringVar(value="Black")
color_dropdown = ttk.Combobox(number_frame, textvariable=color_var, state="readonly", width=15)
color_dropdown['values'] = ("Black", "Red", "Blue", "Green", "Gray", "White")
color_dropdown.grid(row=2, column=1, padx=10, pady=5, sticky="w")

# 3. Rotation Frame
rotate_frame = ttk.LabelFrame(root, text="3. Page Rotation (Optional)")
rotate_frame.pack(fill="x", padx=15, pady=10)

ttk.Label(rotate_frame, text="Pages to rotate\n(e.g. 1, 3, 5-10):").grid(row=0, column=0, padx=10, pady=5, sticky="e")
rotate_entry = ttk.Entry(rotate_frame, width=20)
rotate_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

ttk.Label(rotate_frame, text="Rotation Angle:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
rot_angle_var = tk.StringVar(value="90°")
rot_angle_dropdown = ttk.Combobox(rotate_frame, textvariable=rot_angle_var, state="readonly", width=10)
rot_angle_dropdown['values'] = ("90°", "180°", "270°")
rot_angle_dropdown.grid(row=1, column=1, padx=10, pady=5, sticky="w")

# 4. Process Button
process_btn = tk.Button(root, text="Process PDF", command=process_pdf, bg="#4CAF50", fg="white", font=("Arial", 11, "bold"), width=20)
process_btn.pack(pady=15)

# Status Label
status_label = ttk.Label(root, text="Status: Ready", font=("Arial", 10))
status_label.pack()

root.mainloop()
