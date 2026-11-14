import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinterdnd2 import TkinterDnD, DND_FILES
import fitz  # PyMuPDF library
import os
import sys
import threading
from PIL import Image, ImageTk
from pdf2docx import Converter

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
        "tab_prem": "👑 Premium Tools",
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
        "add_files": "Add PDFs",
        "remove_files": "Remove Selected",
        "move_up": "Move Up",
        "move_down": "Move Down",
        "merge_btn": "MERGE PDFs",
        "mix_btn": "ALTERNATE MIX (Requires 2 PDFs)",
        "merge_lbl": "Add files in order (or Drag & Drop multiple here):",
        "split_file": "Select File to Split/Extract (or Drag & Drop):",
        "mode_extract": "Extract / Duplicate Pages (e.g., 1-5, 8, 9):",
        "mode_split_n": "Split after every X pages:",
        "mode_split_bm": "Split by Bookmarks",
        "mode_split_size": "Split by Target Size (MB) - approx:",
        "split_btn": "EXECUTE SPLIT / EXTRACT",
        "prem_lock_msg": "RESTRICTED ACCESS\nEnter developer access code to unlock Premium:",
        "prem_unlock_btn": "UNLOCK",
        "prem_f1_title": "Premium #1: Remove PDF Restrictions (Unlock Copy)",
        "prem_f1_btn": "STRIP RESTRICTIONS",
        "prem_f2_title": "Premium #2: Digital PDF to Word",
        "prem_f2_desc": "*For digital PDFs with highlightable text only.",
        "prem_f2_btn": "CONVERT DIGITAL TO WORD",
        "prem_f3_title": "Premium #3: SCANNED PDF to Word (Deep Learning OCR)",
        "prem_f3_desc": "*100% Offline AI. Extracts English & Chinese from flat images.",
        "prem_f3_btn": "RUN AI OCR CONVERSION",
        "stat_ready": "Status: Ready",
        "stat_loading": "Status: Working... please wait.",
        "stat_success": "Status: Finished successfully!",
        "stat_err": "Status: Error occurred.",
        "err_no_pdf": "Please select a valid PDF file.",
        "save_as": "Save As...",
        "save_dir": "Select Folder",
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
        "tab_prem": "👑 高级工具 (Premium)",
        "frame1": "选择 PDF 文件 (或直接拖放至此)",
        "browse": "浏览",
        "frame2": "页码样式",
        "font": "字体：",
        "position": "位置：",
        "size": "大小：",
        "color": "颜色：",
        "bg_chk": "页码添加纯白背景框",
        "frame3": "旋转设置",
        "rot_angle": "勾选页旋转角度：",
        "process": "处理并保存",
        "preview_frame": "PDF 预览 (滑动滚轮，勾选旋转)",
        "lang": "语言 / Language:",
        "positions": ["左下", "中下", "右下", "左上", "中上", "右上"],
        "colors": ["黑色", "红色", "蓝色", "绿色", "灰色", "白色"],
        "add_files": "添加 PDF",
        "remove_files": "移除选中",
        "move_up": "上移",
        "move_down": "下移",
        "merge_btn": "合并 PDF",
        "mix_btn": "交替合并 (需2个PDF)",
        "merge_lbl": "按合并顺序添加文件 (或拖放多个文件):",
        "split_file": "选择文件 (或拖放):",
        "mode_extract": "提取/复制页码 (如: 1-5, 8, 9):",
        "mode_split_n": "按页数拆分 (每 X 页):",
        "mode_split_bm": "按书签 (Bookmarks) 拆分",
        "mode_split_size": "按目标大小 (MB) 拆分 - 估算:",
        "split_btn": "执行拆分 / 提取",
        "prem_lock_msg": "受限访问\n请输入开发者访问代码以解锁高级功能：",
        "prem_unlock_btn": "解锁",
        "prem_f1_title": "高级 #1: 移除 PDF 限制 (解锁复制)",
        "prem_f1_btn": "移除限制",
        "prem_f2_title": "高级 #2: 数字 PDF 转 Word",
        "prem_f2_desc": "*仅适用于可高亮文本的数字PDF。",
        "prem_f2_btn": "数字 PDF 转换 WORD",
        "prem_f3_title": "高级 #3: 扫描版 PDF 转 Word (深度学习 OCR)",
        "prem_f3_desc": "*100% 离线 AI。从图像中提取中英文本。",
        "prem_f3_btn": "运行 AI OCR 转换",
        "stat_ready": "状态：就绪",
        "stat_loading": "状态：正在处理... 请稍候。",
        "stat_success": "状态：处理成功！",
        "stat_err": "状态：发生错误。",
        "err_no_pdf": "请选择有效的 PDF 文件。",
        "save_as": "另存为...",
        "save_dir": "选择保存文件夹",
        "msg_success": "操作成功完成！",
        "msg_err": "错误",
        "pg_rotate": "第 {0} 页 旋转"
    }
}

def resource_path(relative_path):
    try: base_path = sys._MEIPASS
    except Exception: base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def change_language(event=None):
    t = translations["EN" if lang_var.get() == "English" else "CN"]
    root.title(t["app_title"])
    name_label.config(text=t["name_label"])
    lang_label.config(text=t["lang"])
    notebook.tab(tab1_frame, text=t["tab_number"])
    notebook.tab(tab2_frame, text=t["tab_merge"])
    notebook.tab(tab3_frame, text=t["tab_split"])
    notebook.tab(tab4_frame, text=t["tab_prem"])

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
    for i, chk in checkbox_widgets.items(): chk.config(text=t["pg_rotate"].format(i+1))

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

    prem_lock_lbl.config(text=t["prem_lock_msg"])
    prem_unlock_btn.config(text=t["prem_unlock_btn"])
    prem_f1_lbl.config(text=t["prem_f1_title"])
    btn_do_unlock.config(text=t["prem_f1_btn"])
    prem_f2_lbl.config(text=t["prem_f2_title"])
    prem_f2_desc.config(text=t["prem_f2_desc"])
    btn_do_word.config(text=t["prem_f2_btn"])
    prem_f3_lbl.config(text=t["prem_f3_title"])
    prem_f3_desc.config(text=t["prem_f3_desc"])
    btn_do_ocr.config(text=t["prem_f3_btn"])

    update_status(t["stat_ready"], "black")

def update_status(msg, color="black"):
    status_lbl_1.config(text=msg, foreground=color)
    status_lbl_2.config(text=msg, foreground=color)
    status_lbl_3.config(text=msg, foreground=color)
    root.update()

# ================= DRAG AND DROP HANDLER =================
def handle_drop(event):
    dropped_files = root.tk.splitlist(event.data)
    pdf_files = [f for f in dropped_files if f.lower().endswith('.pdf')]
    if not pdf_files: return
    current_tab = notebook.index(notebook.select())
    if current_tab == 0:
        filepath = pdf_files[0]
        input_entry.delete(0, tk.END); input_entry.insert(0, filepath)
        load_previews(filepath)
    elif current_tab == 1:
        for f in pdf_files: merge_listbox.insert(tk.END, f)
    elif current_tab == 2:
        filepath = pdf_files[0]
        split_entry.delete(0, tk.END); split_entry.insert(0, filepath)
    elif current_tab == 3: # Premium Tab
        filepath = pdf_files[0]
        prem_f1_entry.delete(0, tk.END); prem_f1_entry.insert(0, filepath)

# ================= TAB 1: Numbering & Preview =================
def select_input_file():
    f = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if f: input_entry.delete(0, tk.END); input_entry.insert(0, f); load_previews(f)

def load_previews(filepath):
    t = translations["EN" if lang_var.get() == "English" else "CN"]
    for widget in scrollable_frame.winfo_children(): widget.destroy()
    thumbnail_references.clear(); checkbox_vars.clear(); checkbox_widgets.clear(); preview_canvases.clear()
    update_status(t["stat_loading"], "blue")
    try:
        doc = fitz.open(filepath)
        columns = 4 
        for i in range(len(doc)):
            if i % 10 == 0: update_status(f"Loading preview {i}/{len(doc)}...", "blue")
            pix = doc[i].get_pixmap(matrix=fitz.Matrix(0.1, 0.1))
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            photo = ImageTk.PhotoImage(img)
            thumbnail_references.append(photo)
            row, col = (i // columns) * 2, i % columns
            canvas_thumb = tk.Canvas(scrollable_frame, width=img.width, height=img.height, bd=1, relief="solid", highlightthickness=0)
            canvas_thumb.grid(row=row, column=col, padx=10, pady=(10, 0))
            canvas_thumb.create_image(0, 0, anchor="nw", image=photo)
            preview_canvases.append({"canvas": canvas_thumb, "width": img.width, "height": img.height, "dot_id": None})
            var = tk.BooleanVar(); checkbox_vars[i] = var
            chk = ttk.Checkbutton(scrollable_frame, text=t["pg_rotate"].format(i+1), variable=var)
            chk.grid(row=row+1, column=col, pady=(0, 10))
            checkbox_widgets[i] = chk
        doc.close(); update_status(t["stat_ready"]); update_preview_dots()
    except Exception as e: update_status(t["stat_err"], "red"); messagebox.showerror(t["msg_err"], str(e))

def update_preview_dots(*args):
    pos_idx = max(0, pos_dropdown.current())
    margin, r = 8, 5
    for item in preview_canvases:
        c, w, h = item["canvas"], item["width"], item["height"]
        if pos_idx in (0, 3): x = margin
        elif pos_idx in (2, 5): x = w - margin
        else: x = w / 2
        if pos_idx in (3, 4, 5): y = margin
        else: y = h - margin
        if item["dot_id"] is None: item["dot_id"] = c.create_oval(x-r, y-r, x+r, y+r, fill="#00FF00", outline="black")
        else: c.coords(item["dot_id"], x-r, y-r, x+r, y+r)

def process_numbering():
    t = translations["EN" if lang_var.get() == "English" else "CN"]
    input_pdf = input_entry.get()
    if not os.path.exists(input_pdf): return messagebox.showerror(t["msg_err"], t["err_no_pdf"])
    output_pdf = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")], title=t["save_as"])
    if not output_pdf: return
    update_status(t["stat_loading"], "blue")
    try:
        fontsize = int(size_var.get()); use_bg = bg_var.get(); rot_angle = int(rot_angle_var.get().replace("°", ""))
        fontname = ["helv", "times-roman", "cour"][max(0, font_dropdown.current())]
        pos_idx = max(0, pos_dropdown.current())
        color = [(0,0,0), (1,0,0), (0,0,1), (0,0.5,0), (0.5,0.5,0.5), (1,1,1)][max(0, color_dropdown.current())]
        doc = fitz.open(input_pdf)
        for p in range(len(doc)):
            page = doc[p]; page.wrap_contents(); orig_rot = page.rotation; page.set_rotation(0) 
            text = f"Page {p + 1} of {len(doc)}"
            text_len = fitz.get_text_length(text, fontname=fontname, fontsize=fontsize)
            rect = page.cropbox 
            mx, my = 30, 30
            if pos_idx in (0, 3): x = rect.x0 + mx
            elif pos_idx in (2, 5): x = rect.x1 - mx - text_len
            else: x = rect.x0 + (rect.width / 2) - (text_len / 2)
            if pos_idx in (3, 4, 5): y = rect.y0 + my + fontsize
            else: y = rect.y1 - my
            if use_bg: page.draw_rect(fitz.Rect(x-5, y-fontsize-2, x+text_len+5, y+5), color=(1,1,1), fill=(1,1,1), overlay=True)
            page.insert_text((x, y), text, fontsize=fontsize, fontname=fontname, color=color, overlay=True)
            if p in checkbox_vars and checkbox_vars[p].get(): orig_rot += rot_angle
            page.set_rotation(orig_rot)
        doc.save(output_pdf); doc.close(); update_status(t["stat_success"], "green"); messagebox.showinfo(t["app_title"], t["msg_success"])
    except Exception as e: update_status(t["stat_err"], "red"); messagebox.showerror(t["msg_err"], str(e))

# ================= TAB 2 & 3 FUNCTIONS =================
def t2_add():
    for f in filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")]): merge_listbox.insert(tk.END, f)
def t2_rem():
    for i in reversed(merge_listbox.curselection()): merge_listbox.delete(i)
def t2_up():
    for i in merge_listbox.curselection():
        if i == 0: continue
        val = merge_listbox.get(i); merge_listbox.delete(i); merge_listbox.insert(i-1, val); merge_listbox.selection_set(i-1)
def t2_dn():
    for i in reversed(merge_listbox.curselection()):
        if i == merge_listbox.size() - 1: continue
        val = merge_listbox.get(i); merge_listbox.delete(i); merge_listbox.insert(i+1, val); merge_listbox.selection_set(i+1)

def process_merge():
    t = translations["EN" if lang_var.get() == "English" else "CN"]
    files = merge_listbox.get(0, tk.END)
    if len(files) < 2: return messagebox.showerror(t["msg_err"], "Please add at least 2 PDFs.")
    out_file = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")], title=t["save_as"])
    if not out_file: return
    update_status(t["stat_loading"], "blue")
    try:
        out_doc = fitz.open()
        for f in files: doc = fitz.open(f); out_doc.insert_pdf(doc); doc.close()
        out_doc.save(out_file); out_doc.close(); update_status(t["stat_success"], "green"); messagebox.showinfo(t["app_title"], t["msg_success"])
    except Exception as e: update_status(t["stat_err"], "red"); messagebox.showerror(t["msg_err"], str(e))

def process_mix():
    t = translations["EN" if lang_var.get() == "English" else "CN"]
    files = merge_listbox.get(0, tk.END)
    if len(files) != 2: return messagebox.showerror(t["msg_err"], "Alternate Mix requires exactly 2 PDFs.")
    out_file = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")], title=t["save_as"])
    if not out_file: return
    update_status(t["stat_loading"], "blue")
    try:
        doc1 = fitz.open(files[0]); doc2 = fitz.open(files[1]); out_doc = fitz.open()
        for i in range(max(len(doc1), len(doc2))):
            if i < len(doc1): out_doc.insert_pdf(doc1, from_page=i, to_page=i)
            if i < len(doc2): out_doc.insert_pdf(doc2, from_page=i, to_page=i)
        out_doc.save(out_file); doc1.close(); doc2.close(); out_doc.close()
        update_status(t["stat_success"], "green"); messagebox.showinfo(t["app_title"], t["msg_success"])
    except Exception as e: update_status(t["stat_err"], "red"); messagebox.showerror(t["msg_err"], str(e))

def t3_sel():
    f = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if f: split_entry.delete(0, tk.END); split_entry.insert(0, f)

def process_split():
    t = translations["EN" if lang_var.get() == "English" else "CN"]
    in_pdf = split_entry.get()
    if not os.path.exists(in_pdf): return messagebox.showerror(t["msg_err"], t["err_no_pdf"])
    mode = split_mode_var.get()
    try:
        doc = fitz.open(in_pdf); base_name = os.path.splitext(os.path.basename(in_pdf))[0]
        if mode == "extract":
            out_file = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")], title=t["save_as"])
            if not out_file: return
            update_status(t["stat_loading"], "blue"); page_list = []
            for part in split_ext_val.get().replace(" ", "").split(','):
                if '-' in part: s, e = part.split('-'); page_list.extend(range(int(s)-1, int(e)))
                elif part: page_list.append(int(part)-1)
            out_doc = fitz.open()
            for p in page_list:
                if 0 <= p < len(doc): out_doc.insert_pdf(doc, from_page=p, to_page=p)
            out_doc.save(out_file); out_doc.close()
        else:
            out_dir = filedialog.askdirectory(title=t["save_dir"])
            if not out_dir: return
            update_status(t["stat_loading"], "blue")
            if mode == "div":
                n = int(split_div_val.get()); part = 1
                for i in range(0, len(doc), n):
                    out_doc = fitz.open(); out_doc.insert_pdf(doc, from_page=i, to_page=min(i+n-1, len(doc)-1))
                    out_doc.save(os.path.join(out_dir, f"{base_name}_part{part}.pdf")); out_doc.close(); part += 1
            elif mode == "bm":
                toc = doc.get_toc()
                bms = sorted(list(set([item[2]-1 for item in toc if item[2] > 0])))
                if 0 not in bms: bms.insert(0, 0)
                bms.append(len(doc))
                part = 1
                for i in range(len(bms)-1):
                    s_p, e_p = bms[i], bms[i+1]-1
                    if s_p <= e_p:
                        out_doc = fitz.open(); out_doc.insert_pdf(doc, from_page=s_p, to_page=e_p)
                        out_doc.save(os.path.join(out_dir, f"{base_name}_part{part}.pdf")); out_doc.close(); part += 1
            elif mode == "size":
                target_bytes = float(split_sz_val.get()) * 1048576
                out_doc = fitz.open(); part = 1
                for p in range(len(doc)):
                    out_doc.insert_pdf(doc, from_page=p, to_page=p)
                    if len(out_doc.tobytes(garbage=4)) >= target_bytes and out_doc.page_count > 1:
                        out_doc.save(os.path.join(out_dir, f"{base_name}_part{part}.pdf")); out_doc.close(); out_doc = fitz.open(); part += 1
                if out_doc.page_count > 0: out_doc.save(os.path.join(out_dir, f"{base_name}_part{part}.pdf"))
                out_doc.close()
        doc.close(); update_status(t["stat_success"], "green"); messagebox.showinfo(t["app_title"], t["msg_success"])
    except Exception as e: update_status(t["stat_err"], "red"); messagebox.showerror(t["msg_err"], str(e))

# ================= TAB 4: PREMIUM TOOLS =================
def unlock_premium():
    # THE UPDATED ACCESS CODE
    if prem_pass_entry.get() == "11066547":
        prem_lock_frame.pack_forget(); prem_content_frame.pack(fill="both", expand=True)
    else: messagebox.showerror("Access Denied", "Incorrect developer code.")

def t4_sel():
    f = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if f: prem_f1_entry.delete(0, tk.END); prem_f1_entry.insert(0, f)

def process_unlock():
    in_pdf = prem_f1_entry.get()
    if not os.path.exists(in_pdf): return messagebox.showerror("Error", "Select valid PDF")
    out_file = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
    if not out_file: return
    try:
        doc = fitz.open(in_pdf)
        if doc.is_encrypted: doc.authenticate("") 
        doc.save(out_file, encryption=fitz.PDF_ENCRYPT_NONE); doc.close()
        messagebox.showinfo("Success", "Restrictions Removed!")
    except Exception as e: messagebox.showerror("Error", str(e))

def process_pdf2word():
    in_pdf = prem_f1_entry.get()
    if not os.path.exists(in_pdf): return messagebox.showerror("Error", "Select valid PDF")
    out_file = filedialog.asksaveasfilename(defaultextension=".docx", filetypes=[("Word Document", "*.docx")])
    if not out_file: return
    try:
        root.update() 
        cv = Converter(in_pdf); cv.convert(out_file, start=0, end=None); cv.close()
        messagebox.showinfo("Success", "Converted to Word Document!")
    except Exception as e: messagebox.showerror("Error", str(e))

# --- Threaded RapidOCR (ONNX) Implementation ---
def log_msg(msg):
    root.after(0, lambda: [ocr_log_text.insert(tk.END, msg + "\n"), ocr_log_text.see(tk.END)])

def threaded_ocr_process(pdf_path, out_path, lang_code):
    try:
        log_msg("SYSTEM: Initializing RapidOCR (ONNX) AI Engine...")
        log_msg("SYSTEM: AI Models are embedded. 100% Offline processing enabled.")
        from rapidocr_onnxruntime import RapidOCR
        import cv2
        import numpy as np
        from docx import Document
        from docx.shared import Pt, RGBColor
        from docx.oxml.ns import qn
        
        # RapidOCR natively handles English and Chinese out of the box using Baidu's embedded ONNX models
        ocr = RapidOCR()
        
        doc_pdf = fitz.open(pdf_path)
        doc_word = Document()

        for page_num in range(len(doc_pdf)):
            log_msg(f"Processing Page {page_num+1}/{len(doc_pdf)}: Extracting high-res image...")
            page = doc_pdf[page_num]
            pix = page.get_pixmap(dpi=200)
            img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
            
            # Format image colorspace for OpenCV
            if pix.n == 4: img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)
            elif pix.n == 1: img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
            elif pix.n == 3: img = cv2.cvtColor(img, cv2.RGB2BGR)
            
            log_msg(f"Page {page_num+1}: Running Layout Analysis & Character Recognition...")
            result, elapse = ocr(img)
            
            if not result:
                doc_word.add_paragraph("")
                continue
                
            # result structure from RapidOCR: [ [ [[x,y],[x,y],[x,y],[x,y]], "text", confidence ], ... ]
            lines = result
            # Sort boxes top-to-bottom, then left-to-right
            lines.sort(key=lambda x: (x[0][0][1] // 15, x[0][0][0]))

            for line in lines:
                box, text, conf = line
                # box[3] is bottom-left, box[0] is top-left
                box_height = box[3][1] - box[0][1]
                font_size_pt = max(8, int(box_height * 0.70)) 
                
                p = doc_word.add_paragraph()
                
                # Basic alignment detection based on X coordinates
                if box[0][0] > (pix.width * 0.6): p.alignment = 2
                elif box[0][0] > (pix.width * 0.3): p.alignment = 1
                else: p.alignment = 0 

                run = p.add_run(text)
                run.font.size = Pt(font_size_pt)
                
                # Crucial Font Fallback for Chinese Characters to prevent missing glyphs
                run.font.name = 'Arial'
                run._element.rPr.rFonts.set(qn('w:eastAsia'), 'Microsoft YaHei')
                run.font.color.rgb = RGBColor(0, 0, 0)
                
            log_msg(f"Page {page_num+1} Completed successfully. (Process time: {elapse:.2f}s)")

        doc_word.save(out_path)
        log_msg("===========================================")
        log_msg(f"SUCCESS: Document saved to {out_path}")
        log_msg("===========================================")
        root.after(0, lambda: btn_do_ocr.config(state=tk.NORMAL))
        
    except Exception as e:
        log_msg(f"FATAL ERROR: {str(e)}")
        root.after(0, lambda: btn_do_ocr.config(state=tk.NORMAL))

def process_ai_ocr():
    in_pdf = prem_f1_entry.get()
    if not os.path.exists(in_pdf): return messagebox.showerror("Error", "Select valid PDF")
    out_file = filedialog.asksaveasfilename(defaultextension=".docx", filetypes=[("Word Document", "*.docx")])
    if not out_file: return
    
    lang_sel = ocr_lang_var.get()
    btn_do_ocr.config(state=tk.DISABLED) 
    ocr_log_text.delete(1.0, tk.END)
    
    thread = threading.Thread(target=threaded_ocr_process, args=(in_pdf, out_file, lang_sel))
    thread.daemon = True
    thread.start()

# ================= MOUSE SCROLL =================
def _on_mousewheel(event):
    if notebook.index(notebook.select()) != 0: return
    try:
        if scrollable_frame.winfo_height() > canvas.winfo_height(): canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    except Exception: pass

# ================= GUI CONSTRUCTION =================
root = TkinterDnD.Tk()
root.title("STA Singapore QC - PDF Workstation")
root.geometry("1100x850")
root.eval('tk::PlaceWindow . center')
style = ttk.Style(root)
style.theme_use('clam')

root.drop_target_register(DND_FILES)
root.dnd_bind('<<Drop>>', handle_drop)

header_frame = tk.Frame(root, bg="#ffffff", bd=2, relief="groove")
header_frame.pack(fill="x", padx=5, pady=5)
lang_frame = tk.Frame(header_frame, bg="#ffffff"); lang_frame.pack(side="left", padx=10)
lang_label = tk.Label(lang_frame, text="Language / 语言:", bg="#ffffff", font=("Arial", 9, "bold")); lang_label.pack()
lang_var = tk.StringVar(value="English")
lang_dropdown = ttk.Combobox(lang_frame, textvariable=lang_var, state="readonly", width=8, values=("English", "中文")); lang_dropdown.pack(); lang_dropdown.bind("<<ComboboxSelected>>", change_language)
name_label = tk.Label(header_frame, text="Nicholas Tok\nSTA Singapore QC Lab Instrument", font=("Arial", 14, "bold"), bg="#ffffff", justify="left"); name_label.pack(side="left", padx=20, pady=10)

try:
    logo_path = resource_path("logo.jpg"); logo_img = Image.open(logo_path).resize((180, 70), Image.LANCZOS)
    logo_photo = ImageTk.PhotoImage(logo_img); logo_label = tk.Label(header_frame, image=logo_photo, bg="#ffffff"); logo_label.image = logo_photo; logo_label.pack(side="right", padx=15, pady=5)
except Exception: pass

notebook = ttk.Notebook(root); notebook.pack(fill="both", expand=True, padx=10, pady=5)
tab1_frame = ttk.Frame(notebook); tab2_frame = ttk.Frame(notebook); tab3_frame = ttk.Frame(notebook); tab4_frame = ttk.Frame(notebook)
notebook.add(tab1_frame, text="1. Numbering & Rotate"); notebook.add(tab2_frame, text="2. Merge & Mix"); notebook.add(tab3_frame, text="3. Split & Extract"); notebook.add(tab4_frame, text="👑 Premium Tools")

# ========== TAB 1 UI ==========
t1_paned = ttk.PanedWindow(tab1_frame, orient=tk.HORIZONTAL); t1_paned.pack(fill="both", expand=True, padx=5, pady=5)
left_frame = ttk.Frame(t1_paned); t1_paned.add(left_frame, weight=1)
right_frame = ttk.LabelFrame(t1_paned, text="PDF Preview"); t1_paned.add(right_frame, weight=3)

file_frame = ttk.LabelFrame(left_frame, text="Select PDF (or Drag & Drop)"); file_frame.pack(fill="x", pady=5)
input_entry = ttk.Entry(file_frame); input_entry.pack(fill="x", padx=10, pady=5)
browse_btn = ttk.Button(file_frame, text="Browse", command=select_input_file); browse_btn.pack(pady=5)

num_frame = ttk.LabelFrame(left_frame, text="Page Number Styling"); num_frame.pack(fill="x", pady=10)
font_lbl = ttk.Label(num_frame, text="Font:"); font_lbl.grid(row=0, column=0, padx=5, pady=5, sticky="e")
font_dropdown = ttk.Combobox(num_frame, state="readonly", width=17, values=("Arial / Helvetica", "Times New Roman", "Courier")); font_dropdown.current(0); font_dropdown.grid(row=0, column=1, pady=5)
pos_lbl = ttk.Label(num_frame, text="Position:"); pos_lbl.grid(row=1, column=0, padx=5, pady=5, sticky="e")
pos_dropdown = ttk.Combobox(num_frame, state="readonly", width=17, values=("Bottom Left", "Bottom Center", "Bottom Right", "Top Left", "Top Center", "Top Right")); pos_dropdown.current(1); pos_dropdown.grid(row=1, column=1, pady=5); pos_dropdown.bind("<<ComboboxSelected>>", update_preview_dots)
size_lbl = ttk.Label(num_frame, text="Size:"); size_lbl.grid(row=2, column=0, padx=5, pady=5, sticky="e"); size_var = tk.StringVar(value="11"); ttk.Spinbox(num_frame, from_=6, to=36, textvariable=size_var, width=15).grid(row=2, column=1, pady=5)
color_lbl = ttk.Label(num_frame, text="Color:"); color_lbl.grid(row=3, column=0, padx=5, pady=5, sticky="e"); color_dropdown = ttk.Combobox(num_frame, state="readonly", width=17, values=("Black", "Red", "Blue", "Green", "Gray", "White")); color_dropdown.current(0); color_dropdown.grid(row=3, column=1, pady=5)
bg_var = tk.BooleanVar(value=False); bg_chk = ttk.Checkbutton(num_frame, text="Solid White Box Behind Number", variable=bg_var); bg_chk.grid(row=4, column=0, columnspan=2, pady=5, padx=5, sticky="w")

rot_frame = ttk.LabelFrame(left_frame, text="Rotation Settings"); rot_frame.pack(fill="x", pady=5)
rot_angle_lbl = ttk.Label(rot_frame, text="Checked Angle:"); rot_angle_lbl.grid(row=0, column=0, padx=5, pady=5, sticky="e")
rot_angle_var = tk.StringVar(value="90°"); ttk.Combobox(rot_frame, textvariable=rot_angle_var, state="readonly", width=10, values=("90°", "180°", "270°")).grid(row=0, column=1, pady=5)
process_btn = tk.Button(left_frame, text="PROCESS & SAVE", command=process_numbering, bg="#004C99", fg="white", font=("Arial", 11, "bold"), pady=10); process_btn.pack(fill="x", pady=10)
status_lbl_1 = ttk.Label(left_frame, text="Status: Ready", font=("Arial", 10, "bold")); status_lbl_1.pack()

canvas = tk.Canvas(right_frame, bg="#e0e0e0"); scrollbar = ttk.Scrollbar(right_frame, orient="vertical", command=canvas.yview)
scrollable_frame = ttk.Frame(canvas); scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw"); canvas.configure(yscrollcommand=scrollbar.set)
canvas.pack(side="left", fill="both", expand=True); scrollbar.pack(side="right", fill="y"); root.bind_all("<MouseWheel>", _on_mousewheel)

# ========== TAB 2 UI ==========
t2_center = tk.Frame(tab2_frame); t2_center.pack(pady=30)
merge_lbl = ttk.Label(t2_center, text="Add files in order (or Drag & Drop multiple here):", font=("Arial", 11, "bold")); merge_lbl.pack(anchor="w")
listbox_frame = tk.Frame(t2_center); listbox_frame.pack(pady=5); merge_listbox = tk.Listbox(listbox_frame, width=80, height=15, selectmode=tk.EXTENDED, font=("Arial", 10)); merge_listbox.pack(side=tk.LEFT, fill=tk.BOTH)
scroll_lb = tk.Scrollbar(listbox_frame, command=merge_listbox.yview); scroll_lb.pack(side=tk.RIGHT, fill=tk.Y); merge_listbox.config(yscrollcommand=scroll_lb.set)
btn_frame_2 = tk.Frame(t2_center); btn_frame_2.pack(fill="x", pady=10)
btn_add_merge = ttk.Button(btn_frame_2, text="Add PDFs", command=t2_add); btn_add_merge.grid(row=0, column=0, padx=5)
btn_rem_merge = ttk.Button(btn_frame_2, text="Remove Selected", command=t2_rem); btn_rem_merge.grid(row=0, column=1, padx=5)
btn_up_merge = ttk.Button(btn_frame_2, text="Move Up", command=t2_up); btn_up_merge.grid(row=0, column=2, padx=5)
btn_dn_merge = ttk.Button(btn_frame_2, text="Move Down", command=t2_dn); btn_dn_merge.grid(row=0, column=3, padx=5)
btn_do_merge = tk.Button(t2_center, text="MERGE PDFs", command=process_merge, bg="#28A745", fg="white", font=("Arial", 11, "bold"), width=30, pady=5); btn_do_merge.pack(pady=10)
btn_do_mix = tk.Button(t2_center, text="ALTERNATE MIX", command=process_mix, bg="#17A2B8", fg="white", font=("Arial", 11, "bold"), width=30, pady=5); btn_do_mix.pack(pady=5)
status_lbl_2 = ttk.Label(t2_center, text="Status: Ready", font=("Arial", 10, "bold")); status_lbl_2.pack(pady=10)

# ========== TAB 3 UI ==========
t3_center = tk.Frame(tab3_frame); t3_center.pack(pady=30, padx=50, fill="x")
split_file_lbl = ttk.Label(t3_center, text="Select File to Split/Extract (or Drag & Drop):", font=("Arial", 11, "bold")); split_file_lbl.pack(anchor="w")
t3_f = tk.Frame(t3_center); t3_f.pack(fill="x", pady=5); split_entry = ttk.Entry(t3_f, width=70); split_entry.pack(side="left"); split_browse_btn = ttk.Button(t3_f, text="Browse", command=t3_sel); split_browse_btn.pack(side="left", padx=10)
modes_frame = ttk.LabelFrame(t3_center, text="Action Mode"); modes_frame.pack(fill="x", pady=20, ipadx=10, ipady=10); split_mode_var = tk.StringVar(value="extract")
f_ext = tk.Frame(modes_frame); f_ext.pack(fill="x", pady=5); rb_ext = ttk.Radiobutton(f_ext, text="Extract/Duplicate Pages:", variable=split_mode_var, value="extract"); rb_ext.pack(side="left"); split_ext_val = ttk.Entry(f_ext, width=20); split_ext_val.pack(side="left", padx=10); split_ext_val.insert(0, "1-3, 5")
f_div = tk.Frame(modes_frame); f_div.pack(fill="x", pady=5); rb_div = ttk.Radiobutton(f_div, text="Split after every X pages:", variable=split_mode_var, value="div"); rb_div.pack(side="left"); split_div_val = ttk.Entry(f_div, width=10); split_div_val.pack(side="left", padx=10); split_div_val.insert(0, "5")
f_bm = tk.Frame(modes_frame); f_bm.pack(fill="x", pady=5); rb_bm = ttk.Radiobutton(f_bm, text="Split by Bookmarks", variable=split_mode_var, value="bm"); rb_bm.pack(side="left")
f_sz = tk.Frame(modes_frame); f_sz.pack(fill="x", pady=5); rb_size = ttk.Radiobutton(f_sz, text="Split by Target Size (MB):", variable=split_mode_var, value="size"); rb_size.pack(side="left"); split_sz_val = ttk.Entry(f_sz, width=10); split_sz_val.pack(side="left", padx=10); split_sz_val.insert(0, "10")
btn_do_split = tk.Button(t3_center, text="EXECUTE", command=process_split, bg="#DC3545", fg="white", font=("Arial", 11, "bold"), width=30, pady=10); btn_do_split.pack(pady=20)
status_lbl_3 = ttk.Label(t3_center, text="Status: Ready", font=("Arial", 10, "bold")); status_lbl_3.pack()

# ========== TAB 4 UI (PREMIUM) ==========
prem_lock_frame = tk.Frame(tab4_frame); prem_lock_frame.pack(expand=True)
prem_lock_lbl = tk.Label(prem_lock_frame, text="RESTRICTED ACCESS\nEnter developer access code to unlock Premium Functions:", font=("Arial", 12, "bold"), fg="#DC3545", pady=10); prem_lock_lbl.pack()
prem_pass_entry = ttk.Entry(prem_lock_frame, show="*", width=35, font=("Arial", 12)); prem_pass_entry.pack(pady=10)
prem_unlock_btn = tk.Button(prem_lock_frame, text="UNLOCK", command=unlock_premium, bg="#FFC107", font=("Arial", 11, "bold"), width=15); prem_unlock_btn.pack(pady=10)

prem_content_frame = tk.Frame(tab4_frame)
t4_f = tk.Frame(prem_content_frame); t4_f.pack(fill="x", padx=50, pady=10)
ttk.Label(t4_f, text="Select Target PDF (or Drag & Drop):", font=("Arial", 10, "bold")).pack(anchor="w")
f_br = tk.Frame(t4_f); f_br.pack(fill="x", pady=5); prem_f1_entry = ttk.Entry(f_br, width=70); prem_f1_entry.pack(side="left"); ttk.Button(f_br, text="Browse", command=t4_sel).pack(side="left", padx=10)

prem_grid = tk.Frame(prem_content_frame)
prem_grid.pack(fill="both", expand=True, padx=40, pady=10)

f1_box = ttk.LabelFrame(prem_grid, text="Function 1"); f1_box.grid(row=0, column=0, padx=10, pady=5, sticky="ew")
prem_f1_lbl = ttk.Label(f1_box, text="Remove PDF Restrictions", font=("Arial", 10, "bold")); prem_f1_lbl.pack(pady=5)
btn_do_unlock = tk.Button(f1_box, text="STRIP RESTRICTIONS", command=process_unlock, bg="#28A745", fg="white", font=("Arial", 10, "bold"), pady=5, width=25); btn_do_unlock.pack(pady=5)

f2_box = ttk.LabelFrame(prem_grid, text="Function 2"); f2_box.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
prem_f2_lbl = ttk.Label(f2_box, text="Digital PDF to Word", font=("Arial", 10, "bold")); prem_f2_lbl.pack(pady=5)
prem_f2_desc = ttk.Label(f2_box, text="*For highlightable text only.", font=("Arial", 8, "italic"), foreground="gray"); prem_f2_desc.pack(pady=2)
btn_do_word = tk.Button(f2_box, text="CONVERT TO WORD", command=process_pdf2word, bg="#17A2B8", fg="white", font=("Arial", 10, "bold"), pady=5, width=25); btn_do_word.pack(pady=5)

prem_grid.columnconfigure(0, weight=1); prem_grid.columnconfigure(1, weight=1)

f3_box = ttk.LabelFrame(prem_content_frame, text="Deep Learning OCR (Scanned to Word)"); f3_box.pack(fill="x", padx=50, pady=10)
prem_f3_lbl = ttk.Label(f3_box, text="Premium #3: SCANNED PDF to Word", font=("Arial", 11, "bold")); prem_f3_lbl.pack(pady=5)
prem_f3_desc = ttk.Label(f3_box, text="*100% Offline AI. Extracts English & Chinese from flat images.", font=("Arial", 9, "italic"), foreground="gray"); prem_f3_desc.pack()

f3_ctrl = tk.Frame(f3_box); f3_ctrl.pack(pady=10)
ttk.Label(f3_ctrl, text="Document Language:").pack(side="left", padx=5)
ocr_lang_var = tk.StringVar(value="Chinese/English (Auto)")
ttk.Combobox(f3_ctrl, textvariable=ocr_lang_var, state="readonly", values=("Chinese/English (Auto)", "English Only")).pack(side="left", padx=5)
btn_do_ocr = tk.Button(f3_ctrl, text="RUN AI OCR CONVERSION", command=process_ai_ocr, bg="#6f42c1", fg="white", font=("Arial", 10, "bold"), width=25); btn_do_ocr.pack(side="left", padx=10)

ocr_log_text = tk.Text(f3_box, height=8, bg="#f8f9fa", font=("Courier", 9))
ocr_log_text.pack(fill="x", padx=10, pady=10)

change_language()
root.mainloop()
