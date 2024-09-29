import tkinter as tk
from tkinter import filedialog, messagebox
import os

# Function to read and format the input text
def format_text(file_path, lines_per_paragraph=15):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        paragraphs = []
        current_paragraph = []

        # Create paragraphs with a specified number of lines
        for i, line in enumerate(lines):
            current_paragraph.append(line.strip())
            if (i + 1) % lines_per_paragraph == 0 or line == '\n':
                paragraphs.append(' '.join(current_paragraph))
                current_paragraph = []

        # Append any remaining lines
        if current_paragraph:
            paragraphs.append(' '.join(current_paragraph))

        return '\n\n'.join(paragraphs)
    except Exception as e:
        return f"[Error] Could not format the file: {e}"

# Function to save formatted text
def save_formatted_text(formatted_text, output_path):
    try:
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(formatted_text)
        messagebox.showinfo("Success", "File saved successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save the file: {e}")

# Function to handle file processing
def process_file():
    input_path = filedialog.askopenfilename(title="Select Input File", filetypes=[("Text files", "*.txt")])
    if not input_path:
        return

    output_path = filedialog.asksaveasfilename(title="Save Output File", defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if not output_path:
        return

    formatted_text = format_text(input_path)
    if "[Error]" in formatted_text:
        messagebox.showerror("Error", formatted_text)
    else:
        save_formatted_text(formatted_text, output_path)

# Setting up the Tkinter window
def create_gui():
    root = tk.Tk()
    root.title("Text Formatter")

    frame = tk.Frame(root, padx=20, pady=20)
    frame.pack()

    label = tk.Label(frame, text="Format a Text File into Paragraphs", font=('Arial', 14))
    label.pack(pady=10)

    format_button = tk.Button(frame, text="Select File and Format", command=process_file, font=('Arial', 12))
    format_button.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
