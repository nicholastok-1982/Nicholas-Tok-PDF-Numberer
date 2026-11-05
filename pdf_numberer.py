import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinterdnd2 import TkinterDnD, DND_FILES
import fitz  # PyMuPDF library
import os
import sys
from PIL import Image, ImageTk

thumbnail_references = []
checkbox_vars = {}
checkbox_widgets = {}
preview_canvases = []

# --- Translations Dictionary ---
translations = {
    "EN": {
        "app_title": "STA Singapore QC - PDF Workstation",
        "name_label": "Nicholas Tok\nSTA Singapore QC Lab Instrument",
        "tab_number": "1. Numbering & Rotate",
        "tab_merge": "2. Merge & Mix",
        "tab_split": "3. Split & Extract",
        # Tab 1
        "frame1": "Select PDF (or Drag & Drop anywhere)",
        "browse": "Browse",
        "frame2": "Page Number Styling",
        "font": "Font:",
        "position": "Position:",
        "size": "Size:",
        "color": "Color:",
        "bg_chk": "Solid White Box Behind Number",
        "frame3": "Rotation Settings",
        "rot_angle": "Checked Angle:",
        "process": "PROCESS & SAVE",
        "preview_frame": "PDF Preview (Scroll & Check to Rotate)",
        "lang": "Language / 语言:",
        "positions": ["Bottom Left", "Bottom Center", "Bottom Right", "Top Left", "Top Center", "Top Right"],
        "colors": ["Black", "Red", "Blue", "Green", "Gray", "White"],
        # Tab 2
        "add_files": "Add PDFs",
        "remove_files": "Remove Selected",
        "move_up": "Move Up",
        "move_down": "Move Down",
        "merge_btn": "MERGE PDFs",
        "mix_btn": "ALTERNATE MIX (Requires 2 PDFs)",
        "merge_lbl": "Add files in order (or Drag & Drop multiple here):",
        # Tab 3
        "split_file": "Select File to Split/Extract (or Drag & Drop):",
        "mode_extract": "Extract / Duplicate Pages (e.g., 1-5, 8, 9, 9, 9):",
        "mode_split_n": "Split after every X pages:",
        "mode_split_bm": "Split by Bookmarks",
        "mode_split_size": "Split by Target Size (MB) - approximate:",
        "split_btn": "EXECUTE SPLIT / EXTRACT",
        # Status/Messages
        "stat_ready": "Status: Ready",
        "stat_loading": "Status: Working... please wait.",
        "stat_success": "Status: Finished successfully!",
        "stat_err": "Status: Error occurred.",
        "err_no_pdf": "Please select a valid PDF file.",
        "save_as": "Save New PDF As...",
        "save_dir": "Select Folder to Save Split Files",
        "msg_success": "Operation completed successfully!",
        "msg_err": "Error",
        "pg_rotate": "Pg {0} Rotate"
    },
    "CN": {
        "app_title": "STA 新加坡 QC - PDF 工作站",
        "name_label": "Nicholas Tok\nSTA 新加坡 QC 实验室仪器",
        "tab_number": "1. 页码与旋转",
        "tab_merge": "2. 合并与交替",
        "tab_split": "3. 拆分与提取",
        # Tab 1
        "frame1": "选择 PDF 文件 (或直接拖放至此)",
        "browse": "浏览",
        "frame2": "页码样式",
        "font": "字体：",
        "position": "位置：",
        "size": "大小：",
        "color": "颜色：",
        "bg_chk": "页码添加纯白背景框 (修复扫描件)",
        "frame3": "旋转设置",
        "rot_angle": "勾选页旋转角度：",
        "process": "处理并保存",
        "preview_frame": "PDF 预览 (滑动滚轮，勾选旋转)",
        "lang": "语言 / Language:",
        "positions": ["左下", "中下", "右下", "左上", "中上", "右上"],
        "colors": ["黑色", "红色", "蓝色", "绿色", "灰色", "白色"],
        # Tab 2
        "add_files": "添加 PDF",
        "remove_files": "移除选中",
        "move_up": "上移",
        "move_down": "下移",
        "merge_btn": "合并 PDF",
        "mix_btn": "交替合并 (需2个PDF)",
        "merge_lbl": "按合并顺序添加文件 (或直接拖放多个文件):",
        # Tab 3
        "split_file": "选择要拆分/提取的文件 (或直接拖放):",
        "mode_extract": "提取/复制页码 (如: 1-5, 8, 9, 9):",
        "mode_split_n": "按页数拆分 (每 X 页):",
        "mode_split_bm": "按书签 (Bookmarks) 拆分",
        "mode_split_size": "按目标大小 (MB) 拆分 - 估算:",
        "split_btn": "执行拆分 / 提取",
        # Status/Messages
        "stat_ready": "状态：就绪",
        "stat_loading": "状态：正在处理... 请稍候。",
        "stat_success": "状态：处理成功！",
        "stat_err": "状态：发生错误。",
        "err_no_pdf": "请选择有效的 PDF 文件。",
        "save_as": "另存新 PDF 为...",
        "save_dir": "选择保存拆分文件的文件夹",
        "msg_success": "操作成功完成！",
        "msg_err": "错误",
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
    t = translations["EN" if lang_var.get() == "English" else "CN"]
    root.title(t["app_title"])
    name_label.config(text=t["name_label"])
    lang_label.config(text=t["lang"])
    
    notebook.tab(tab1_frame, text=t["tab_number"])
    notebook.tab(tab2_frame, text=t["tab_merge"])
    notebook.tab(tab3_frame, text=t["tab_split"])

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

    pos_idx = pos_dropdown.current()
    pos_dropdown['values'] = t["positions"]
    pos_dropdown.current(pos_idx if pos_idx >= 0 else 1)

    col_idx = color_dropdown.current()
    color_dropdown['values'] = t["colors"]
    color_dropdown.current(col_idx if col_idx >= 0 else 0)

    for i, chk in checkbox_widgets.items():
        chk.config(text=t["pg_rotate"].format(i+1))

    merge_lbl.config(text=t["merge_lbl"])
    btn_add_merge.config(text=t["add_files"])
    btn_rem_merge.config(text=t["remove_files"])
    btn_up_merge.config(text=t["move_up"])
    btn_dn_merge.config(text=t["move_down"])
    btn_do_merge.config(text=t["merge_btn"])
    btn_do_mix.config(text=t["mix_btn"])

    split_file_lbl.config(text=t["split_file"])
    split_browse_btn.config(text=t["browse"])
    rb_ext.config(text=t["mode_extract"])
    rb_div.config(text=t["mode_split_n"])
    rb_bm.config(text=t["mode_split_bm"])
    rb_size.config(text=t["mode_split_size"])
    btn_do_split.config(text=t["split_btn"])

    update_status(t["stat_ready"], "black")

def update_status(msg, color="black"):
    status_lbl_1.config(text=msg, foreground=color)
    status_lbl_2.config(text=msg, foreground=color)
    status_lbl_3.config(text=msg, foreground=color)
    root.update()

# ================= DRAG AND DROP HANDLER =================
def handle_drop(event):
    # Parse dropped files safely
    dropped_files = root.tk.splitlist(event.data)
    pdf_files = [f for f in dropped_files if f.lower().endswith('.pdf')]
    
    if not pdf_files:
        return

    current_tab = notebook.index(notebook.select())
    
    if current_tab == 0:  # Numbering Tab
        filepath = pdf_files[0]
        input_entry.delete(0, tk.END)
        input_entry.insert(0, filepath)
        load_previews(filepath)
        
    elif current_tab == 1:  # Merge Tab
        for f in pdf_files:
            merge_listbox.insert(tk.END, f)
            
    elif current_tab == 2:  # Split Tab
        filepath = pdf_files[0]
        split_entry.delete(0, tk.END)
        split_entry.insert(0, filepath)

# ================= TAB 1: Numbering & Preview =================
def select_input_file():
    filepath = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if filepath:
        input_entry.delete(0, tk.END)
        input_entry.insert(0, filepath)
        load_previews(filepath)

def load_previews(filepath):
    t = translations["EN" if lang_var.get() == "English" else "CN"]
    for widget in scrollable_frame.winfo_children(): widget.destroy()
    thumbnail_references.clear(); checkbox_vars.clear(); checkbox_widgets.clear(); preview_canvases.clear()
    update_status(t["stat_loading"], "blue")

    try:
        doc = fitz.open(filepath)
        total_pages = len(doc)
        columns = 4 
        for i in range(total_pages):
            if i % 10 == 0:
                update_status(f"Loading preview {i}/{total_pages}...", "blue")
            
            page = doc[i]
            pix = page.get_pixmap(matrix=fitz.Matrix(0.1, 0.1))
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            photo = ImageTk.PhotoImage(img)
            thumbnail_references.append(photo)

            row, col = (i // columns) * 2, i % columns
            canvas_thumb = tk.Canvas(scrollable_frame, width=img.width, height=img.height, bd=1, relief="solid", highlightthickness=0)
            canvas_thumb.grid(row=row, column=col, padx=10, pady=(10, 0))
            canvas_thumb.create_image(0, 0, anchor="nw", image=photo)

            preview_canvases.append({"canvas": canvas_thumb, "width": img.width, "height": img.height, "dot_id": None})
            var = tk.BooleanVar()
            checkbox_vars[i] = var
            chk = ttk.Checkbutton(scrollable_frame, text=t["pg_rotate"].format(i+1), variable=var)
            chk.grid(row=row+1, column=col, pady=(0, 10))
            checkbox_widgets[i] = chk

        doc.close()
        update_status(t["stat_ready"])
        update_preview_dots()
    except Exception as e:
        update_status(t["stat_err"], "red")
        messagebox.showerror(t["msg_err"], str(e))

def update_preview_dots(*args):
    pos_idx = pos_dropdown.current()
    if pos_idx < 0: pos_idx = 1
    margin, r = 8, 5
    for item in preview_canvases:
        c, w, h = item["canvas"], item["width"], item["height"]
        if pos_idx in (0, 3): x = margin
        elif pos_idx in (2, 5): x = w - margin
        else: x = w / 2
        if pos_idx in (3, 4, 5): y = margin
        else: y = h - margin
        
        if item["dot_id"] is None:
            item["dot_id"] = c.create_oval(x-r, y-r, x+r, y+r, fill="#00FF00", outline="black")
        else:
            c.coords(item["dot_id"], x-r, y-r, x+r, y+r)

def process_numbering():
    t = translations["EN" if lang_var.get() == "English" else "CN"]
    input_pdf = input_entry.get()
    if not os.path.exists(input_pdf): return messagebox.showerror(t["msg_err"], t["err_no_pdf"])
    
    output_pdf = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")], title=t["save_as"])
    if not output_pdf: return
    update_status(t["stat_loading"], "blue")

    try:
        fontsize = int(size_var.get())
        use_bg = bg_var.get()
        rot_angle = int(rot_angle_var.get().replace("°", ""))
        fontname = ["helv", "times-roman", "cour"][max(0, font_dropdown.current())]
        pos_idx = max(0, pos_dropdown.current())
        color = [(0,0,0), (1,0,0), (0,0,1), (0,0.5,0), (0.5,0.5,0.5), (1,1,1)][max(0, color_dropdown.current())]

        doc = fitz.open(input_pdf)
        total_pages = len(doc)
        
        for p in range(total_pages):
            page = doc[p]
            page.wrap_contents()
            orig_rot = page.rotation
            page.set_rotation(0) 
            
            text = f"Page {p + 1} of {total_pages}"
            text_len = fitz.get_text_length(text, fontname=fontname, fontsize=fontsize)
            rect = page.cropbox 
            mx, my = 30, 30
            
            if pos_idx in (0, 3): x = rect.x0 + mx
            elif pos_idx in (2, 5): x = rect.x1 - mx - text_len
            else: x = rect.x0 + (rect.width / 2) - (text_len / 2)
            if pos_idx in (3, 4, 5): y = rect.y0 + my + fontsize
            else: y = rect.y1 - my
            
            if use_bg:
                page.draw_rect(fitz.Rect(x-5, y-fontsize-2, x+text_len+5, y+5), color=(1,1,1), fill=(1,1,1), overlay=True)

            page.insert_text((x, y), text, fontsize=fontsize, fontname=fontname, color=color, overlay=True)
            
            if p in checkbox_vars and checkbox_vars[p].get(): orig_rot += rot_angle
            page.set_rotation(orig_rot)

        doc.save(output_pdf)
        doc.close()
        update_status(t["stat_success"], "green")
        messagebox.showinfo(t["app_title"], t["msg_success"])
    except Exception as e:
        update_status(t["stat_err"], "red")
        messagebox.showerror(t["msg_err"], str(e))

# ================= TAB 2: Merge & Alternate Mix =================
def t2_add():
    files = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")])
    for f in files: merge_listbox.insert(tk.END, f)

def t2_rem():
    selections = merge_listbox.curselection()
    for i in reversed(selections): merge_listbox.delete(i)

def t2_up():
    selections = merge_listbox.curselection()
    for i in selections:
        if i == 0: continue
        val = merge_listbox.get(i)
        merge_listbox.delete(i)
        merge_listbox.insert(i-1, val)
        merge_listbox.selection_set(i-1)

def t2_dn():
    selections = merge_listbox.curselection()
    for i in reversed(selections):
        if i == merge_listbox.size() - 1: continue
        val = merge_listbox.get(i)
        merge_listbox.delete(i)
        merge_listbox.insert(i+1, val)
        merge_listbox.selection_set(i+1)

def process_merge():
    t = translations["EN" if lang_var.get() == "English" else "CN"]
    files = merge_listbox.get(0, tk.END)
    if len(files) < 2: return messagebox.showerror(t["msg_err"], "Please add at least 2 PDFs.")
    
    out_file = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
    if not out_file: return
    update_status(t["stat_loading"], "blue")

    try:
        out_doc = fitz.open()
        for f in files:
            doc = fitz.open(f)
            out_doc.insert_pdf(doc)
            doc.close()
        out_doc.save(out_file)
        out_doc.close()
        update_status(t["stat_success"], "green")
        messagebox.showinfo(t["app_title"], t["msg_success"])
    except Exception as e:
        update_status(t["stat_err"], "red")
        messagebox.showerror(t["msg_err"], str(e))

def process_mix():
    t = translations["EN" if lang_var.get() == "English" else "CN"]
    files = merge_listbox.get(0, tk.END)
    if len(files) != 2: return messagebox.showerror(t["msg_err"], "Alternate Mix requires exactly 2 PDFs.")
    
    out_file = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
    if not out_file: return
    update_status(t["stat_loading"], "blue")

    try:
        doc1 = fitz.open(files[0])
        doc2 = fitz.open(files[1])
        out_doc = fitz.open()
        max_p = max(len(doc1), len(doc2))
        
        for i in range(max_p):
            if i < len(doc1): out_doc.insert_pdf(doc1, from_page=i, to_page=i)
            if i < len(doc2): out_doc.insert_pdf(doc2, from_page=i, to_page=i)
            
        out_doc.save(out_file)
        doc1.close(); doc2.close(); out_doc.close()
        update_status(t["stat_success"], "green")
        messagebox.showinfo(t["app_title"], t["msg_success"])
    except Exception as e:
        update_status(t["stat_err"], "red")
        messagebox.showerror(t["msg_err"], str(e))

# ================= TAB 3: Split & Extract =================
def t3_sel():
    filepath = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if filepath:
        split_entry.delete(0, tk.END)
        split_entry.insert(0, filepath)

def process_split():
    t = translations["EN" if lang_var.get() == "English" else "CN"]
    in_pdf = split_entry.get()
    if not os.path.exists(in_pdf): return messagebox.showerror(t["msg_err"], t["err_no_pdf"])
    
    mode = split_mode_var.get()
    
    try:
        doc = fitz.open(in_pdf)
        base_name = os.path.splitext(os.path.basename(in_pdf))[0]
        
        if mode == "extract":
            out_file = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")], title=t["save_as"])
            if not out_file: return
            update_status(t["stat_loading"], "blue")
            
            page_list = []
            parts = split_ext_val.get().replace(" ", "").split(',')
            for part in parts:
                if '-' in part:
                    s, e = part.split('-')
                    page_list.extend(range(int(s)-1, int(e)))
                elif part:
                    page_list.append(int(part)-1)
            
            out_doc = fitz.open()
            for p in page_list:
                if 0 <= p < len(doc):
                    out_doc.insert_pdf(doc, from_page=p, to_page=p)
            out_doc.save(out_file)
            out_doc.close()

        else:
            out_dir = filedialog.askdirectory(title=t["save_dir"])
            if not out_dir: return
            update_status(t["stat_loading"], "blue")
            
            if mode == "div":
                n = int(split_div_val.get())
                part = 1
                for i in range(0, len(doc), n):
                    out_doc = fitz.open()
                    out_doc.insert_pdf(doc, from_page=i, to_page=min(i+n-1, len(doc)-1))
                    out_doc.save(os.path.join(out_dir, f"{base_name}_part{part}.pdf"))
                    out_doc.close()
                    part += 1

            elif mode == "bm":
                toc = doc.get_toc()
                bms = sorted(list(set([item[2]-1 for item in toc if item[2] > 0])))
                if 0 not in bms: bms.insert(0, 0)
                bms.append(len(doc))
                
                part = 1
                for i in range(len(bms)-1):
                    start_p = bms[i]
                    end_p = bms[i+1]-1
                    if start_p <= end_p:
                        out_doc = fitz.open()
                        out_doc.insert_pdf(doc, from_page=start_p, to_page=end_p)
                        out_doc.save(os.path.join(out_dir, f"{base_name}_part{part}.pdf"))
                        out_doc.close()
                        part += 1
                        
            elif mode == "size":
                target_bytes = float(split_sz_val.get()) * 1048576
                out_doc = fitz.open()
                part = 1
                for p in range(len(doc)):
                    out_doc.insert_pdf(doc, from_page=p, to_page=p)
                    if len(out_doc.tobytes(garbage=4)) >= target_bytes and out_doc.page_count > 1:
                        out_doc.save(os.path.join(out_dir, f"{base_name}_part{part}.pdf"))
                        out_doc.close()
                        out_doc = fitz.open() 
                        part += 1
                
                if out_doc.page_count > 0:
                    out_doc.save(os.path.join(out_dir, f"{base_name}_part{part}.pdf"))
                out_doc.close()

        doc.close()
        update_status(t["stat_success"], "green")
        messagebox.showinfo(t["app_title"], t["msg_success"])

    except Exception as e:
        update_status(t["stat_err"], "red")
        messagebox.showerror(t["msg_err"], str(e))

# ================= MOUSE SCROLL (TAB 1) =================
def _on_mousewheel(event):
    if notebook.index(notebook.select()) != 0: return
    try:
        if scrollable_frame.winfo_height() > canvas.winfo_height():
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    except Exception: pass

# ================= GUI CONSTRUCTION =================
# Use TkinterDnD.Tk() instead of standard tk.Tk() to enable Drag and Drop
root = TkinterDnD.Tk()
root.title("STA Singapore QC - PDF Workstation")
root.geometry("1100x750")
root.eval('tk::PlaceWindow . center')
style = ttk.Style(root)
style.theme_use('clam')

# REGISTER ENTIRE WINDOW AS DROP TARGET
root.drop_target_register(DND_FILES)
root.dnd_bind('<<Drop>>', handle_drop)

# HEADER
header_frame = tk.Frame(root, bg="#ffffff", bd=2, relief="groove")
header_frame.pack(fill="x", padx=5, pady=5)

lang_frame = tk.Frame(header_frame, bg="#ffffff")
lang_frame.pack(side="left", padx=10)
lang_label = tk.Label(lang_frame, text="Language / 语言:", bg="#ffffff", font=("Arial", 9, "bold"))
lang_label.pack()
lang_var = tk.StringVar(value="English")
lang_dropdown = ttk.Combobox(lang_frame, textvariable=lang_var, state="readonly", width=8, values=("English", "中文"))
lang_dropdown.pack()
lang_dropdown.bind("<<ComboboxSelected>>", change_language)

name_label = tk.Label(header_frame, text="Nicholas Tok\nSTA Singapore QC Lab Instrument", font=("Arial", 14, "bold"), bg="#ffffff", justify="left")
name_label.pack(side="left", padx=20, pady=10)

try:
    logo_path = resource_path("logo.jpg")
    logo_img = Image.open(logo_path).resize((180, 70), Image.LANCZOS)
    logo_photo = ImageTk.PhotoImage(logo_img)
    logo_label = tk.Label(header_frame, image=logo_photo, bg="#ffffff")
    logo_label.image = logo_photo
    logo_label.pack(side="right", padx=15, pady=5)
except Exception: pass

# NOTEBOOK (TABS)
notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True, padx=10, pady=5)

tab1_frame = ttk.Frame(notebook)
tab2_frame = ttk.Frame(notebook)
tab3_frame = ttk.Frame(notebook)

notebook.add(tab1_frame, text="1. Numbering & Rotate")
notebook.add(tab2_frame, text="2. Merge & Mix")
notebook.add(tab3_frame, text="3. Split & Extract")

# ========== TAB 1 UI ==========
t1_paned = ttk.PanedWindow(tab1_frame, orient=tk.HORIZONTAL)
t1_paned.pack(fill="both", expand=True, padx=5, pady=5)

left_frame = ttk.Frame(t1_paned)
t1_paned.add(left_frame, weight=1)
right_frame = ttk.LabelFrame(t1_paned, text="PDF Preview")
t1_paned.add(right_frame, weight=3)

file_frame = ttk.LabelFrame(left_frame, text="Select PDF (or Drag & Drop anywhere)")
file_frame.pack(fill="x", pady=5)
input_entry = ttk.Entry(file_frame)
input_entry.pack(fill="x", padx=10, pady=5)
browse_btn = ttk.Button(file_frame, text="Browse", command=select_input_file)
browse_btn.pack(pady=5)

num_frame = ttk.LabelFrame(left_frame, text="Page Number Styling")
num_frame.pack(fill="x", pady=10)
font_lbl = ttk.Label(num_frame, text="Font:"); font_lbl.grid(row=0, column=0, padx=5, pady=5, sticky="e")
font_dropdown = ttk.Combobox(num_frame, state="readonly", width=17, values=("Arial / Helvetica", "Times New Roman", "Courier"))
font_dropdown.current(0); font_dropdown.grid(row=0, column=1, pady=5)

pos_lbl = ttk.Label(num_frame, text="Position:"); pos_lbl.grid(row=1, column=0, padx=5, pady=5, sticky="e")
pos_dropdown = ttk.Combobox(num_frame, state="readonly", width=17, values=("Bottom Left", "Bottom Center", "Bottom Right", "Top Left", "Top Center", "Top Right"))
pos_dropdown.current(1); pos_dropdown.grid(row=1, column=1, pady=5)
pos_dropdown.bind("<<ComboboxSelected>>", update_preview_dots)

size_lbl = ttk.Label(num_frame, text="Size:"); size_lbl.grid(row=2, column=0, padx=5, pady=5, sticky="e")
size_var = tk.StringVar(value="11")
ttk.Spinbox(num_frame, from_=6, to=36, textvariable=size_var, width=15).grid(row=2, column=1, pady=5)

color_lbl = ttk.Label(num_frame, text="Color:"); color_lbl.grid(row=3, column=0, padx=5, pady=5, sticky="e")
color_dropdown = ttk.Combobox(num_frame, state="readonly", width=17, values=("Black", "Red", "Blue", "Green", "Gray", "White"))
color_dropdown.current(0); color_dropdown.grid(row=3, column=1, pady=5)

bg_var = tk.BooleanVar(value=False)
bg_chk = ttk.Checkbutton(num_frame, text="Solid White Box Behind Number", variable=bg_var)
bg_chk.grid(row=4, column=0, columnspan=2, pady=5, padx=5, sticky="w")

rot_frame = ttk.LabelFrame(left_frame, text="Rotation Settings")
rot_frame.pack(fill="x", pady=5)
rot_angle_lbl = ttk.Label(rot_frame, text="Checked Angle:")
rot_angle_lbl.grid(row=0, column=0, padx=5, pady=5, sticky="e")
rot_angle_var = tk.StringVar(value="90°")
ttk.Combobox(rot_frame, textvariable=rot_angle_var, state="readonly", width=10, values=("90°", "180°", "270°")).grid(row=0, column=1, pady=5)

process_btn = tk.Button(left_frame, text="PROCESS & SAVE", command=process_numbering, bg="#004C99", fg="white", font=("Arial", 11, "bold"), pady=10)
process_btn.pack(fill="x", pady=10)
status_lbl_1 = ttk.Label(left_frame, text="Status: Ready", font=("Arial", 10, "bold"))
status_lbl_1.pack()

canvas = tk.Canvas(right_frame, bg="#e0e0e0")
scrollbar = ttk.Scrollbar(right_frame, orient="vertical", command=canvas.yview)
scrollable_frame = ttk.Frame(canvas)
scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")
root.bind_all("<MouseWheel>", _on_mousewheel)

# ========== TAB 2 UI ==========
t2_center = tk.Frame(tab2_frame)
t2_center.pack(pady=30)
merge_lbl = ttk.Label(t2_center, text="Add files in order (or Drag & Drop multiple here):", font=("Arial", 11, "bold"))
merge_lbl.pack(anchor="w")

listbox_frame = tk.Frame(t2_center)
listbox_frame.pack(pady=5)
merge_listbox = tk.Listbox(listbox_frame, width=80, height=15, selectmode=tk.EXTENDED, font=("Arial", 10))
merge_listbox.pack(side=tk.LEFT, fill=tk.BOTH)
scroll_lb = tk.Scrollbar(listbox_frame, command=merge_listbox.yview)
scroll_lb.pack(side=tk.RIGHT, fill=tk.Y)
merge_listbox.config(yscrollcommand=scroll_lb.set)

btn_frame_2 = tk.Frame(t2_center)
btn_frame_2.pack(fill="x", pady=10)
btn_add_merge = ttk.Button(btn_frame_2, text="Add PDFs", command=t2_add)
btn_add_merge.grid(row=0, column=0, padx=5)
btn_rem_merge = ttk.Button(btn_frame_2, text="Remove Selected", command=t2_rem)
btn_rem_merge.grid(row=0, column=1, padx=5)
btn_up_merge = ttk.Button(btn_frame_2, text="Move Up", command=t2_up)
btn_up_merge.grid(row=0, column=2, padx=5)
btn_dn_merge = ttk.Button(btn_frame_2, text="Move Down", command=t2_dn)
btn_dn_merge.grid(row=0, column=3, padx=5)

btn_do_merge = tk.Button(t2_center, text="MERGE PDFs", command=process_merge, bg="#28A745", fg="white", font=("Arial", 11, "bold"), width=30, pady=5)
btn_do_merge.pack(pady=10)
btn_do_mix = tk.Button(t2_center, text="ALTERNATE MIX", command=process_mix, bg="#17A2B8", fg="white", font=("Arial", 11, "bold"), width=30, pady=5)
btn_do_mix.pack(pady=5)
status_lbl_2 = ttk.Label(t2_center, text="Status: Ready", font=("Arial", 10, "bold"))
status_lbl_2.pack(pady=10)

# ========== TAB 3 UI ==========
t3_center = tk.Frame(tab3_frame)
t3_center.pack(pady=30, padx=50, fill="x")

split_file_lbl = ttk.Label(t3_center, text="Select File to Split/Extract (or Drag & Drop):", font=("Arial", 11, "bold"))
split_file_lbl.pack(anchor="w")
t3_f = tk.Frame(t3_center)
t3_f.pack(fill="x", pady=5)
split_entry = ttk.Entry(t3_f, width=70)
split_entry.pack(side="left")
split_browse_btn = ttk.Button(t3_f, text="Browse", command=t3_sel)
split_browse_btn.pack(side="left", padx=10)

modes_frame = ttk.LabelFrame(t3_center, text="Action Mode")
modes_frame.pack(fill="x", pady=20, ipadx=10, ipady=10)

split_mode_var = tk.StringVar(value="extract")

f_ext = tk.Frame(modes_frame)
f_ext.pack(fill="x", pady=5)
rb_ext = ttk.Radiobutton(f_ext, text="Extract/Duplicate Pages (e.g. 1-5, 8, 9, 9):", variable=split_mode_var, value="extract")
rb_ext.pack(side="left")
split_ext_val = ttk.Entry(f_ext, width=20); split_ext_val.pack(side="left", padx=10)
split_ext_val.insert(0, "1-3, 5")

f_div = tk.Frame(modes_frame)
f_div.pack(fill="x", pady=5)
rb_div = ttk.Radiobutton(f_div, text="Split after every X pages:", variable=split_mode_var, value="div")
rb_div.pack(side="left")
split_div_val = ttk.Entry(f_div, width=10); split_div_val.pack(side="left", padx=10)
split_div_val.insert(0, "5")

f_bm = tk.Frame(modes_frame)
f_bm.pack(fill="x", pady=5)
rb_bm = ttk.Radiobutton(f_bm, text="Split by Bookmarks", variable=split_mode_var, value="bm")
rb_bm.pack(side="left")

f_sz = tk.Frame(modes_frame)
f_sz.pack(fill="x", pady=5)
rb_size = ttk.Radiobutton(f_sz, text="Split by Target Size (MB) - approximate:", variable=split_mode_var, value="size")
rb_size.pack(side="left")
split_sz_val = ttk.Entry(f_sz, width=10); split_sz_val.pack(side="left", padx=10)
split_sz_val.insert(0, "10")

btn_do_split = tk.Button(t3_center, text="EXECUTE", command=process_split, bg="#DC3545", fg="white", font=("Arial", 11, "bold"), width=30, pady=10)
btn_do_split.pack(pady=20)
status_lbl_3 = ttk.Label(t3_center, text="Status: Ready", font=("Arial", 10, "bold"))
status_lbl_3.pack()

change_language()
root.mainloop()
