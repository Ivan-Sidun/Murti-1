import pandas as pd 
import tkinter as tk
from tkinter import filedialog, messagebox

root = tk.Tk()
root.withdraw()

way = filedialog.askopenfilename(
    defaultextension=".csv",
    filetypes=[("CSV files", "*.csv")],
    title="Обрати файл з чинниками"    
)
way_save = filedialog.asksaveasfilename(
    defaultextension=".xslx",
    filetypes=[("Excel files", "*.xlsx")],
    title="Обрати файл з чинниками"    
)

data = pd.read_csv(way)
data.to_excel(way_save, index=False)
messagebox.showinfo('inf', f'file saved as {way_save}')
root.destroy()


root.mainloop()