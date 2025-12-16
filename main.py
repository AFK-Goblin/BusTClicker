import tkinter as tk
from app import AutoClickerApp

def main():
    root = tk.Tk()
    # Theme is handled inside AutoClickerApp -> AutoClickerUI
    app = AutoClickerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()