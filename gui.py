"""
Tkinter GUI for selecting DSB files to proofread.
"""

import tkinter as tk
from tkinter import filedialog, messagebox


class FileSelectionGUI:
    """GUI for selecting DSB files to proofread."""

    def __init__(self):
        """Initialize the file selection GUI."""
        self.selected_file_path = None
        self.root = None

    def browse_file(self, on_start_callback):
        """Open file dialog to select .dsb file."""

        filename = filedialog.askopenfilename(
            title="Select DSB File",
            filetypes=[("DSB files", "*.dsb"), ("All files", "*.*")]
        )

        if filename:
            self.selected_file_path = filename
            # Hide the Tkinter window
            self.root.withdraw()

            try:
                # Call the callback to start visualization
                on_start_callback(self.selected_file_path)

                # Close the Tkinter window after visualization is done
                self.root.quit()
                self.root.destroy()

            except Exception as e:
                # Show the window again if there's an error
                self.root.deiconify()
                messagebox.showerror("Error", f"Failed to load or visualize file:\n{str(e)}")
                raise e

    def run(self, on_start_callback):
        """
        Run the file selection GUI.

        :param on_start_callback: Function to call when user starts visualization.
                                  Should accept file path as argument.
        """
        self.root = tk.Tk()
        self.root.title("DSB Proofreading Tool")
        self.root.geometry("400x200")

        # Create UI elements
        title_label = tk.Label(self.root, text="DSB Proofreading Tool", font=("Arial", 16, "bold"))
        title_label.pack(pady=20)

        browse_button = tk.Button(
            self.root,
            text="Browse DSB File",
            command=lambda: self.browse_file(on_start_callback),
            width=20,
            height=2
        )
        browse_button.pack(pady=10)


        # Run the Tkinter event loop
        self.root.mainloop()

        return self.selected_file_path

