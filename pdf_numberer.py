import tkinter as tk
from tkinter import filedialog, messagebox
import fitz  # PyMuPDF library
import os

def select_input_file():
    filepath = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if filepath:
        input_entry.delete(0, tk.END)
        input_entry.insert(0, filepath)

def process_pdf():
    input_pdf = input_entry.get()
    
    if not input_pdf or not os.path.exists(input_pdf):
        messagebox.showerror("Error", "Please select a valid PDF file.")
        return

    # Ask user where to save the new numbered PDF
    output_pdf = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("PDF files", "*.pdf")],
        title="Save Numbered PDF As..."
    )
    
    if not output_pdf:
        return # User cancelled the save dialog

    status_label.config(text="Status: Processing... Please wait.", fg="blue")
    root.update() # Force UI update

    try:
        # Open the PDF
        doc = fitz.open(input_pdf)
        total_pages = len(doc)
        
        # Loop through every page
        for page_num in range(total_pages):
            page = doc[page_num]
            text = f"Page {page_num + 1} of {total_pages}"
            
            # Calculate position (Bottom Center)
            page_rect = page.rect
            x = (page_rect.width / 2) - 30 # Adjust horizontally
            y = page_rect.height - 30      # 30 pixels from the bottom
            
            # Insert the page number
            page.insert_text(
                (x, y), 
                text, 
                fontsize=11, 
                fontname="helv", 
                color=(0, 0, 0) # Black color
            )
            
        # Save the new PDF
        doc.save(output_pdf)
        doc.close()
        
        status_label.config(text="Status: Finished successfully!", fg="green")
        messagebox.showinfo("Success", f"PDF saved successfully!\nTotal Pages: {total_pages}")
        
    except Exception as e:
        status_label.config(text="Status: Error occurred.", fg="red")
        messagebox.showerror("Error", f"An error occurred:\n{str(e)}")

# --- GUI Setup ---
root = tk.Tk()
root.title("Portable PDF Page Numberer")
root.geometry("500x200")
root.eval('tk::PlaceWindow . center')

# Instructions
instruction_label = tk.Label(root, text="Select a PDF to automatically add 'Page X of Y' to the bottom center.")
instruction_label.pack(pady=10)

# Input selection frame
frame = tk.Frame(root)
frame.pack(pady=5)

input_entry = tk.Entry(frame, width=50)
input_entry.pack(side=tk.LEFT, padx=5)

browse_btn = tk.Button(frame, text="Browse", command=select_input_file)
browse_btn.pack(side=tk.LEFT)

# Process Button
process_btn = tk.Button(root, text="Add Page Numbers", command=process_pdf, bg="#4CAF50", fg="black", font=("Arial", 10, "bold"))
process_btn.pack(pady=15)

# Status Label
status_label = tk.Label(root, text="Status: Ready")
status_label.pack()

root.mainloop()
