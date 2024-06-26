import tkinter as tk
from tkinter import ttk, messagebox, filedialog, colorchooser

class ColorSetCreator:
    def __init__(self, master):
        self.master = master
        self.master.title("Color Set Creator")
        self.master.configure(bg="black")  # Set full black background

        self.color_set = {}

        # Create style for ttk widgets
        self.style = ttk.Style()

        # Configure style for buttons
        self.style.configure('TButton', foreground='black', background='#666666', font=('Arial', 12), padding=10)
        self.style.map('TButton', background=[('active', '#999999')])

        # Hex Color Code entry
        self.label_code = ttk.Label(master, text="Hex Color Code:", foreground="white", background="black")
        self.label_code.grid(row=0, column=0, padx=10, pady=10, sticky='e')
        self.color_code_entry = ttk.Entry(master, width=20, font=('Arial', 12))
        self.color_code_entry.grid(row=0, column=1, padx=10, pady=10)

        # Pick Color button
        self.pick_color_button = ttk.Button(master, text="Pick Color", command=self.pick_color)
        self.pick_color_button.grid(row=0, column=2, padx=10, pady=10)

        # Add Color button
        self.add_button = ttk.Button(master, text="Add Color", command=self.add_color)
        self.add_button.grid(row=0, column=3, padx=10, pady=10)

        # Color Display frame
        self.color_display_frame = ttk.LabelFrame(master, text="Color Display", padding=10)
        self.color_display_frame.grid(row=1, column=0, columnspan=4, padx=10, pady=10, sticky='ew')

        # Export Color Set button
        self.export_button = ttk.Button(master, text="Export Color Set", command=self.export_color_set)
        self.export_button.grid(row=2, column=0, columnspan=4, padx=10, pady=10)

    def pick_color(self):
        color_code = colorchooser.askcolor()[1]  # Ask for a color and get its hex code
        if color_code:
            self.color_code_entry.delete(0, tk.END)
            self.color_code_entry.insert(0, color_code)

    def add_color(self):
        color_code = self.color_code_entry.get()

        if not color_code:
            messagebox.showwarning("Error", "Please enter a Hex Color Code.")
            return

        # Validate hex color code
        if not self.is_valid_hex_color(color_code):
            messagebox.showwarning("Error", "Please enter a valid Hex Color Code (e.g., #RRGGBB).")
            return

        # Generate a unique color ID
        color_id = f"Color {len(self.color_set) + 1}"

        self.color_set[color_id] = color_code
        self.update_color_display()

        self.color_code_entry.delete(0, tk.END)

    def is_valid_hex_color(self, color_code):
        if len(color_code) != 7:
            return False
        if not color_code.startswith('#'):
            return False
        try:
            int(color_code[1:], 16)
            return True
        except ValueError:
            return False

    def update_color_display(self):
        # Clear existing widgets in color display frame
        for widget in self.color_display_frame.winfo_children():
            widget.destroy()

        # Re-populate color display frame with updated color set
        row = 0
        for color_id, color_code in self.color_set.items():
            color_label = tk.Label(self.color_display_frame, text=color_id, foreground='white', background=color_code, font=('Arial', 12), padx=5, pady=5)
            color_label.grid(row=row, column=0, padx=5, pady=5, sticky='ew')
            color_label.bind('<Button-1>', lambda event, id=color_id: self.edit_color(event, id))

            row += 1

    def edit_color(self, event, color_id=None):
        if color_id:
            current_color_code = self.color_set[color_id]

            # Create a popup window for editing the color
            edit_window = tk.Toplevel(self.master)
            edit_window.title(f"Edit Color - {color_id}")
            edit_window.configure(bg="black")

            # Hex Color Code entry in edit window
            label_code_edit = ttk.Label(edit_window, text="Hex Color Code:", foreground="white", background="black")
            label_code_edit.grid(row=0, column=0, padx=10, pady=10, sticky='e')
            color_code_entry_edit = ttk.Entry(edit_window, width=20, font=('Arial', 12))
            color_code_entry_edit.insert(0, current_color_code)
            color_code_entry_edit.grid(row=0, column=1, padx=10, pady=10)

            # Update Color button in edit window
            update_button = ttk.Button(edit_window, text="Update Color", command=lambda: self.update_color(color_id, color_code_entry_edit.get(), edit_window))
            update_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

            # Delete Color button in edit window
            delete_button = ttk.Button(edit_window, text="Delete Color", command=lambda: self.delete_color(color_id, edit_window))
            delete_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    def update_color(self, color_id, new_color_code, edit_window):
        if not self.is_valid_hex_color(new_color_code):
            messagebox.showwarning("Error", "Please enter a valid Hex Color Code (e.g., #RRGGBB).")
            return

        self.color_set[color_id] = new_color_code
        edit_window.destroy()  # Close edit window
        self.update_color_display()

    def delete_color(self, color_id, edit_window):
        del self.color_set[color_id]
        edit_window.destroy()  # Close edit window
        self.update_color_display()

    def export_color_set(self):
        if not self.color_set:
            messagebox.showwarning("Error", "No colors to export.")
            return

        filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if filename:
            try:
                with open(filename, 'w') as f:
                    for color_code in self.color_set.values():
                        f.write(color_code + "\n")
                messagebox.showinfo("Success", "Color set exported successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Error exporting color set:\n{str(e)}")

def main():
    root = tk.Tk()
    app = ColorSetCreator(root)
    root.mainloop()

if __name__ == "__main__":
    main()