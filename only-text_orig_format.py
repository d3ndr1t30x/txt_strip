import fitz  # PyMuPDF
import tkinter as tk
from tkinter import filedialog, messagebox

def strip_pdf(input_file, output_file):
    """Strip non-text elements from the PDF and save as a text file, preserving formatting."""
    try:
        # Open the PDF file
        pdf_document = fitz.open(input_file)
        text = ""
        
        # Iterate through each page
        for page_num in range(len(pdf_document)):
            page = pdf_document[page_num]
            blocks = page.get_text("blocks")  # Extract content in blocks
            for block in blocks:
                # Check if the block contains text (block[6] = block type, 0 for text)
                if block[6] == 0:
                    text += block[4]  # block[4] contains the text of the block
            text += "\n"  # Add a newline after each page to preserve pagination

        # Write the text to the output file
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(text.strip())
        pdf_document.close()
        return True
    except Exception as e:
        print(f"[Error] {e}")
        return False

def select_input_file():
    """Open a file dialog to select the input PDF file."""
    input_file = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    input_entry.delete(0, tk.END)
    input_entry.insert(0, input_file)

def select_output_file():
    """Open a file dialog to select the output text file."""
    output_file = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    output_entry.delete(0, tk.END)
    output_entry.insert(0, output_file)

def process_pdf():
    """Process the PDF file and generate the output text file."""
    input_file = input_entry.get()
    output_file = output_entry.get()
    
    if not input_file or not output_file:
        messagebox.showerror("Error", "Please specify both input and output files.")
        return

    if strip_pdf(input_file, output_file):
        messagebox.showinfo("Success", "PDF processed successfully!")
    else:
        messagebox.showerror("Error", "Failed to process the PDF.")

# Create the main application window
root = tk.Tk()
root.title("PDF to Text Converter")

# Input file selection
tk.Label(root, text="Input PDF File:").grid(row=0, column=0, padx=10, pady=10)
input_entry = tk.Entry(root, width=50)
input_entry.grid(row=0, column=1, padx=10, pady=10)
tk.Button(root, text="Browse", command=select_input_file).grid(row=0, column=2, padx=10, pady=10)

# Output file selection
tk.Label(root, text="Output Text File:").grid(row=1, column=0, padx=10, pady=10)
output_entry = tk.Entry(root, width=50)
output_entry.grid(row=1, column=1, padx=10, pady=10)
tk.Button(root, text="Browse", command=select_output_file).grid(row=1, column=2, padx=10, pady=10)

# Process button
tk.Button(root, text="Process PDF", command=process_pdf).grid(row=2, column=1, padx=10, pady=20)

# Start the Tkinter main loop
root.mainloop()
