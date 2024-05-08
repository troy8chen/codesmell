"""
GUI is followed by the Tk Documentation:
https://docs.python.org/3/library/tk.html
"""
import tkinter as tk
import os
from tkinter import filedialog, messagebox, simpledialog
from src.code_smells.clone_detector import CloneDetector
from src.code_smells.long_method import LongMethodDetector
from src.code_smells.long_parameter_list import LongParameterListDetector


class CodeSmellGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Code Smells Checker")
        self.button_frame = tk.Frame(master)
        self.master.resizable(width=False, height=False)
        self.button_frame.pack(pady=(10, 0))
        self.gui_result_text = self.create_report_text_widget(master)
        self.upload_button = self.create_upload_button(self.button_frame)
        self.refactor_button = self.create_refactor_and_save_button(self.button_frame)  # Ensure buttons are added to button_frame
        self.create_exit_button(self.button_frame)  # Consistency in button creation
        self.set_initial_prompt()
        self.current_file_path = ''
        self.clone_detector = None  # Initialize the clone detector

    def create_upload_button(self, frame):
        upload_btn = tk.Button(frame, text="Upload Python File",
                               command=self.upload_and_analyze,
                               height=2, width=20)
        upload_btn.pack(side=tk.LEFT, padx=(0, 10))
        return upload_btn

    def create_refactor_and_save_button(self, frame):
        refactor_save_btn = tk.Button(frame, text="Refactor and Save Code",
                                      command=self.perform_refactoring_and_save_output,
                                      height=2, width=20)
        refactor_save_btn.pack(side=tk.LEFT, padx=(0, 10))
        return refactor_save_btn

    def create_exit_button(self, frame):
        exit_btn = tk.Button(frame, text="Exit App", command=self.master.quit,
                             height=2, width=20)
        exit_btn.pack(side=tk.RIGHT)
        return exit_btn

    def create_report_text_widget(self, master):
        font = ("Helvetica", 14)
        report_widget = tk.Text(master, height=20, width=120, font=font)
        report_widget.pack(pady=(5, 5))
        return report_widget

    def set_initial_prompt(self):
        self.gui_result_text.config(state=tk.NORMAL)
        self.gui_result_text.delete("1.0", tk.END)
        message = "Please use the Upload Python File button for your " \
                  "Code Smell Analysis"
        self.gui_result_text.insert(tk.END, message)
        self.gui_result_text.config(state=tk.DISABLED)

    def upload_and_analyze(self):
        file_path = filedialog.askopenfilename(
                title="Select Python File",
                filetypes=[("Python Files", "*.py"), ("All Files", "*.*")])
        if file_path:
            self.current_file_path = file_path  # Save the current file path for possible refactoring
            self.process_file_for_analysis(file_path)

    def process_file_for_analysis(self, file_path):
        report, clone_detector = self.generate_analysis_report(file_path)
        self.clone_detector = clone_detector  # Save the clone detector for later refactoring
        self.display_analysis_report(report)

    def generate_analysis_report(self, file_path):
        clone_detector = CloneDetector()
        clone_detector.read_file(file_path)
        clone_report = clone_detector.print_duplicates()
        lm_report = self.detect_long_methods(file_path)
        lp_report = self.detect_long_parameter_lists(file_path)
        return self.merge_reports(lm_report, lp_report, clone_report), clone_detector

    def detect_long_methods(self, file_path):
        detector = LongMethodDetector()
        detector.read_file(file_path)
        return detector.print_long_methods()

    def detect_long_parameter_lists(self, file_path):
        detector = LongParameterListDetector()
        detector.analyze_file(file_path)
        return detector.print_parameter_counts()

    def detect_duplicate_code(self, file_path):
        clone_detector = CloneDetector()
        clone_detector.read_file(file_path)
        return clone_detector.print_duplicates()

    def merge_reports(self, lm_report, lp_report, clone_report):
        report = f"Code Smell Analysis Report:\n\nLong Method Report:\n{lm_report}\n\n" \
                 f"Long Parameter List Report:\n{lp_report}\n\n" \
                 f"Clone Detection Report:\n{clone_report}"
        return report

    def display_analysis_report(self, report):
        self.gui_result_text.config(state=tk.NORMAL)
        self.gui_result_text.delete("1.0", tk.END)
        self.gui_result_text.insert(tk.END, report)
        self.gui_result_text.config(state=tk.DISABLED)

    def select_project_directory(self):
        project_path = filedialog.askdirectory(title="Select Project Directory")
        if not project_path:
            messagebox.showinfo("Refactoring", "Project directory not selected.")
            return None
        return project_path

    def get_refactoring_details(self):
        old_name = simpledialog.askstring("Input",
                                          "Enter the name of the function/variable to refactor:",
                                          parent=self.master)
        if not old_name:
            messagebox.showwarning("Refactoring Cancelled",
                                   "Refactoring operation was cancelled.")
            return None, None

        new_name = simpledialog.askstring("Input",
                                          "Enter the new name for the function/variable:",
                                          parent=self.master)
        if not new_name:
            messagebox.showwarning("Refactoring Cancelled",
                                   "Refactoring operation was cancelled.")
            return None, None

        return old_name, new_name

    def perform_refactoring_and_save_output(self):
        if not self.current_file_path:
            messagebox.showinfo("Refactoring", "No file selected for refactoring.")
            return

        if not self.clone_detector or not self.clone_detector.duplicates:
            messagebox.showinfo("Refactoring", "No duplicates detected for refactoring.")
            return

        # Prompt the user to confirm refactoring
        if messagebox.askyesno("Refactor", "Do you want to refactor the duplicated code?"):
            save_path = filedialog.asksaveasfilename(
                defaultextension=".py",
                filetypes=[("Python Files", "*.py")],
                initialdir=os.path.dirname(self.current_file_path),
                title="Save Refactored File As"
            )

            if save_path:
                # Perform refactoring and save the new code
                try:
                    self.clone_detector.save_refactored_code(save_path)
                    messagebox.showinfo("Refactoring", f"Refactored code saved to: {save_path}")
                except Exception as e:
                    messagebox.showerror("Refactoring Error", f"Failed to save the refactored code: {e}")
            else:
                messagebox.showinfo("Refactoring", "Refactoring was not saved.")

