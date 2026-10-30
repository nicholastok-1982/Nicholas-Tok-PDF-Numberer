import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import fitz  # PyMuPDF library
import os
import sys
from PIL import Image, ImageTk

thumbnail_references = []
checkbox_vars = {}
checkbox_widgets = {}

# --- Translations Dictionary ---
translations = {
    "EN": {
        "app_title": "STA Singapore QC - PDF Manager",
        "name_label": "Nicholas Tok\nSTA Singapore QC Lab Instrument",
        "frame1": "1. Select PDF",
        "browse": "Browse",
        "frame2": "2. Page Number Styling",
        "font": "Font:",
        "position": "Position:",
        "size": "Size:",
        "color": "Color:",
        "bg_chk": "Solid White Box Behind Number\n(Fixes unreadable scanned pages)",
        "frame3": "3. Rotation Settings",
        "rot_angle": "Checked Angle:",
        "process": "PROCESS & SAVE PDF",
        "status_ready": "Status: Ready",
        "preview_frame": "PDF Preview & Rotation",
        "lang": "Language / 语言:",
        "positions": ["Bottom Left", "Bottom Center", "Bottom Right", "Top Left", "Top Center", "Top Right"],
        "colors": ["Black", "Red", "Blue", "Green", "Gray", "White"],
        "err_no_pdf": "Please select a valid PDF file.",
        "save_as": "Save New PDF As...",
        "stat_loading": "Status: Loading previews... please wait.",
        "stat_generating": "Status: Generating preview {0}/{1}...",
        "stat_processing": "Status: Processing... Please wait.",
        "stat_finished": "Status: Finished successfully!",
        "stat_err": "Status: Error occurred.",
        "msg_success": "PDF saved successfully!\nTotal Pages: {0}",
        "msg_err": "Error",
        "msg_success_title": "Success",
        "pg_rotate": "Pg {0} Rotate"
    },
    "CN": {
        "app_title": "STA 新加坡 QC - PDF 管理器",
        "name_label": "Nicholas Tok\nSTA 新加坡 QC 实验室仪器",
        "frame1": "1. 选择 PDF 文件",
        "browse": "浏览",
        "frame2": "2. 页码样式",
        "font": "字体：",
        "position": "位置：",
        "size": "大小：",
        "color": "颜色：",
        "bg_chk": "页码添加纯白背景框\n(修复扫描件看不清页码的问题)",
        "frame3": "3. 旋转设置",
        "rot_angle": "勾选页旋转角度：",
        "process": "处理并保存 PDF",
        "status_ready": "状态：就绪",
        "preview_frame": "PDF 预览与旋转",
        "lang": "语言 / Language:",
        "positions": ["左下", "中下", "右下", "左上", "中上", "右上"],
        "colors": ["黑色", "红色", "蓝色", "绿色", "灰色", "白色"],
        "err_no_pdf": "请选择有效的 PDF 文件。",
        "save_as": "另存新 PDF 为...",
        "stat_loading": "状态：正在加载预览... 请稍候。",
        "stat_generating": "状态：正在生成预览 {0}/{1}...",
        "stat_processing": "状态：正在处理... 请稍候。",
        "stat_finished": "状态：处理成功！",
        "stat_err": "状态：发生错误。",
        "msg_success": "PDF 保存成功！\n总页数：{0}",
        "msg_err": "错误",
        "msg_success_title": "成功",
        "pg_rotate": "第 {0} 页 旋转"
    }
}

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def change_language(event=None):
    lang_code = "EN" if lang_var.get() == "English" else "CN"
    t = translations[lang_code]

    root.title(t["app_title"])
    name_label.config(text=t["name_label"])
    file_frame.config(text=t["frame1"])
    browse_btn.config(text=t["browse"])
    num_frame.config(text=t["frame2"])
    font_lbl.config(text=t["font"])
    pos_lbl.config(text=t["position"])
    size_lbl.config(text=t["size"])
    color_lbl.config(text=t["color"])
    bg_chk.config(text=t["bg_chk"])
    rot_frame.config(text=t["frame3"])
    rot_angle_lbl.config(text=t["rot_angle"])
    process_btn.config(text=t["process"])
    right_frame.config(text=t["preview_frame"])
    lang_label.config(text=t["lang"])
    
    # Safe update comboboxes
    pos_idx = pos_dropdown.current()
    pos_dropdown['values'] = t["positions"]
    pos_dropdown.current(pos_idx if pos_idx >= 0 else 1)

    col_idx = color_dropdown.current()
    color_dropdown['values'] = t["colors"]
    color_dropdown.current(col_idx if col_idx >= 0 else 0)

    # Update status if ready
    if "Ready" in status_label.cget("text") or "就绪" in status_label.cget("text"):
        status_label.config(text=t["status_ready"])

    # Update preview checkboxes
    for i, chk in checkbox_widgets.items():
        chk.config(text=t["pg_rotate"].format(i+1))

def select_input_file():
    filepath = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if filepath:
        input_entry.delete(0, tk.END)
        input_entry.insert(0, filepath)
        load_previews(filepath)

def load_previews(filepath):
    lang_code = "EN" if lang_var.get() == "English" else "CN"
    t = translations[lang_code]

    for widget in scrollable_frame.winfo_children():
        widget.destroy()
    thumbnail_references.clear()
    checkbox_vars.clear()
    checkbox_widgets.clear()

    status_label.config(text=t["stat_loading"], foreground="blue")
    root.update()

    try:
        doc = fitz.open(filepath)
        total_pages = len(doc)
        columns = 4 
        
        for i in range(total_pages):
            if i % 10 == 0:
                status_label.config(text=t["stat_generating"].format(i, total_pages))
                root.update()

            page = doc[i]
            pix = page.get_pixmap(matrix=fitz.Matrix(0.1, 0.1))
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            photo = ImageTk.PhotoImage(img)
            thumbnail_references.append(photo)

            row = (i // columns) * 2
            col = i % columns

            lbl = tk.Label(scrollable_frame, image=photo, bd=1, relief="solid")
            lbl.grid(row=row, column=col, padx=10, pady=(10, 0))

            var = tk.BooleanVar()
            checkbox_vars[i] = var
            chk = ttk.Checkbutton(scrollable_frame, text=t["pg_rotate"].format(i+1), variable=var)
            chk.grid(row=row+1, column=col, pady=(0, 10))
            checkbox_widgets[i] = chk

        doc.close()
        status_label.config(text=t["status_ready"], foreground="black")

    except Exception as e:
        status_label.config(text=t["stat_err"], foreground="red")
        messagebox.showerror(t["msg_err"], f"Preview Error:\n{str(e)}")

def process_pdf():
    lang_code = "EN" if lang_var.get() == "English" else "CN"
    t = translations[lang_code]

    input_pdf = input_entry.get()
    if not input_pdf or not os.path.exists(input_pdf):
        messagebox.showerror(t["msg_err"], t["err_no_pdf"])
        return

    output_pdf = filedialog.asksaveasfilename(
        defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")],
        title=t["save_as"]
    )
    if not output_pdf: return

    status_label.config(text=t["stat_processing"], foreground="blue")
    root.update()

    try:
        fontsize = int(size_var.get())
        use_bg = bg_var.get()
        rotation_angle = int(rot_angle_var.get().replace("°", ""))

        # Map dropdowns using index for language immunity
        font_idx = font_dropdown.current()
        font_map = ["helv", "times-roman", "cour"]
        fontname = font_map[font_idx if font_idx >= 0 else 0]

        pos_idx = pos_dropdown.current() # 0:BL, 1:BC, 2:BR, 3:TL, 4:TC, 5:TR
        col_idx = color_dropdown.current() # 0:Blk, 1:Red, 2:Blu, 3:Grn, 4:Gry, 5:Wht
        
        color_map = [(0, 0, 0), (1, 0, 0), (0, 0, 1), (0, 0.5, 0), (0.5, 0.5, 0.5), (1, 1, 1)]
        color = color_map[col_idx if col_idx >= 0 else 0]

        doc = fitz.open(input_pdf)
        total_pages = len(doc)
        
        for page_num in range(total_pages):
            page = doc[page_num]
            original_rotation = page.rotation
            page.set_rotation(0) # Un-rotate temporarily
            
            # Text remains English for official QC Lab compliance
            text = f"Page {page_num + 1} of {total_pages}"
            text_length = fitz.get_text_length(text, fontname=fontname, fontsize=fontsize)
            
            page_rect = page.rect
            margin_x = 30
            margin_y = 30
            
            # X coordinate
            if pos_idx in (0, 3): x = margin_x
            elif pos_idx in (2, 5): x = page_rect.width - margin_x - text_length
            else: x = (page_rect.width / 2) - (text_length / 2) # Center
                
            # Y coordinate
            if pos_idx in (3, 4, 5): y = margin_y + fontsize
            else: y = page_rect.height - margin_y # Bottom
            
            if use_bg:
                bg_rect = fitz.Rect(x - 5, y - fontsize - 2, x + text_length + 5, y + 5)
                page.draw_rect(bg_rect, color=(1,1,1), fill=(1,1,1), overlay=True)

            page.insert_text((x, y), text, fontsize=fontsize, fontname=fontname, color=color, overlay=True)
            
            final_rotation = original_rotation
            if page_num in checkbox_vars and checkbox_vars[page_num].get():
                final_rotation += rotation_angle
            page.set_rotation(final_rotation)

        doc.save(output_pdf)
        doc.close()
        
        status_label.config(text=t["stat_finished"], foreground="green")
        messagebox.showinfo(t["msg_success_title"], t["msg_success"].format(total_pages))
        
    except Exception as e:
        status_label.config(text=t["stat_err"], foreground="red")
        messagebox.showerror(t["msg_err"], str(e))

# --- GUI Setup ---
root = tk.Tk()
root.title("STA Singapore QC - PDF Manager")
root.geometry("1100x750")
root.eval('tk::PlaceWindow . center')

style = ttk.Style(root)
style.theme_use('clam')

# --- Header ---
header_frame = tk.Frame(root, bg="#ffffff", bd=2, relief="groove")
header_frame.pack(fill="x", padx=10, pady=10)

name_label = tk.Label(header_frame, text="Nicholas Tok\nSTA Singapore QC Lab Instrument", 
                      font=("Arial", 14, "bold"), bg="#ffffff", justify="left")
name_label.pack(side="left", padx=15, pady=10)

try:
    logo_path = resource_path("logo.jpg")
    logo_img = Image.open(logo_path)
    logo_img.thumbnail((200, 80))
    logo_photo = ImageTk.PhotoImage(logo_img)
    logo_label = tk.Label(header_frame, image=logo_photo, bg="#ffffff")
    logo_label.image = logo_photo
    logo_label.pack(side="right", padx=15, pady=5)
except Exception:
    pass

# --- Main Split Window ---
main_paned = ttk.PanedWindow(root, orient=tk.HORIZONTAL)
main_paned.pack(fill="both", expand=True, padx=10, pady=5)

left_frame = ttk.Frame(main_paned)
main_paned.add(left_frame, weight=1)

right_frame = ttk.LabelFrame(main_paned, text="PDF Preview & Rotation")
main_paned.add(right_frame, weight=3)

# -- Left Panel Controls --

# Language Toggle
lang_frame = tk.Frame(left_frame)
lang_frame.pack(fill="x", pady=(0, 10))
lang_label = ttk.Label(lang_frame, text="Language / 语言:")
lang_label.pack(side="left", padx=5)
lang_var = tk.StringVar(value="English")
lang_dropdown = ttk.Combobox(lang_frame, textvariable=lang_var, state="readonly", width=10, values=("English", "中文"))
lang_dropdown.pack(side="left")
lang_dropdown.bind("<<ComboboxSelected>>", change_language)

# File Selection
file_frame = ttk.LabelFrame(left_frame, text="1. Select PDF")
file_frame.pack(fill="x", pady=5)
input_entry = ttk.Entry(file_frame)
input_entry.pack(fill="x", padx=10, pady=5)
browse_btn = ttk.Button(file_frame, text="Browse", command=select_input_file)
browse_btn.pack(pady=5)

# Page Numbering
num_frame = ttk.LabelFrame(left_frame, text="2. Page Number Styling")
num_frame.pack(fill="x", pady=10)

font_lbl = ttk.Label(num_frame, text="Font:")
font_lbl.grid(row=0, column=0, padx=5, pady=5, sticky="e")
font_var = tk.StringVar(value="Arial / Helvetica")
font_dropdown = ttk.Combobox(num_frame, textvariable=font_var, state="readonly", width=17, 
             values=("Arial / Helvetica", "Times New Roman", "Courier"))
font_dropdown.grid(row=0, column=1, pady=5)

pos_lbl = ttk.Label(num_frame, text="Position:")
pos_lbl.grid(row=1, column=0, padx=5, pady=5, sticky="e")
pos_var = tk.StringVar(value="Bottom Center")
pos_dropdown = ttk.Combobox(num_frame, textvariable=pos_var, state="readonly", width=17,
             values=("Bottom Left", "Bottom Center", "Bottom Right", "Top Left", "Top Center", "Top Right"))
pos_dropdown.grid(row=1, column=1, pady=5)

size_lbl = ttk.Label(num_frame, text="Size:")
size_lbl.grid(row=2, column=0, padx=5, pady=5, sticky="e")
size_var = tk.StringVar(value="11")
ttk.Spinbox(num_frame, from_=6, to=36, textvariable=size_var, width=15).grid(row=2, column=1, pady=5)

color_lbl = ttk.Label(num_frame, text="Color:")
color_lbl.grid(row=3, column=0, padx=5, pady=5, sticky="e")
color_var = tk.StringVar(value="Black")
color_dropdown = ttk.Combobox(num_frame, textvariable=color_var, state="readonly", width=17,
             values=("Black", "Red", "Blue", "Green", "Gray", "White"))
color_dropdown.grid(row=3, column=1, pady=5)

bg_var = tk.BooleanVar(value=False)
bg_chk = ttk.Checkbutton(num_frame, text="Solid White Box Behind Number\n(Fixes unreadable scanned pages)", variable=bg_var)
bg_chk.grid(row=4, column=0, columnspan=2, pady=5, padx=5, sticky="w")

# Rotation
rot_frame = ttk.LabelFrame(left_frame, text="3. Rotation Settings")
rot_frame.pack(fill="x", pady=10)
rot_angle_lbl = ttk.Label(rot_frame, text="Checked Angle:")
rot_angle_lbl.grid(row=0, column=0, padx=5, pady=5, sticky="e")
rot_angle_var = tk.StringVar(value="90°")
ttk.Combobox(rot_frame, textvariable=rot_angle_var, state="readonly", width=10,
             values=("90°", "180°", "270°")).grid(row=0, column=1, pady=5)

# Process
process_btn = tk.Button(left_frame, text="PROCESS & SAVE PDF", command=process_pdf, 
          bg="#004C99", fg="white", font=("Arial", 11, "bold"), pady=10)
process_btn.pack(fill="x", pady=15)

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

# Initialize language on startup
change_language()
root.mainloop()
