import tkinter as tk
from gui import CodeSmellGUI


def main():
    root = tk.Tk()
    app = CodeSmellGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
