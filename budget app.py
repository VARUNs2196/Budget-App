import tkinter as tk
from tkinter import messagebox
import pandas as pd

data = pd.DataFrame(columns=["Type", "Amount", "Description"])
refresh_data = False

def add_entry(type_entry, amount_entry, desc_entry):
    global data

    etype = type_entry.get()
    amount = amount_entry.get()
    description = desc_entry.get()

    if etype not in ["Income", "Expense"]:
        messagebox.showerror("Error", "Type must be 'Income' or 'Expense'")
        return

    try:
        amount = float(amount)
        if amount <= 0:
            raise ValueError("Amount must be greater than zero.")
    except ValueError as e:
        messagebox.showerror("Error", str(e))
        return

    new_entry = pd.DataFrame([[etype, amount, description]], columns=["Type", "Amount", "Description"])
    data = pd.concat([data, new_entry], ignore_index=True)

    type_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)
    desc_entry.delete(0, tk.END)

    messagebox.showinfo("Success", "Entry added successfully")

    if refresh_data:
        update_data_display()

def update_data_display():
    for widget in dframe.winfo_children():
        widget.destroy()

    if data.empty:
        label = tk.Label(dframe, text="No data available.")
        label.pack()
        return

    for index, row in data.iterrows():
        entry_frame = tk.Frame(dframe)
        entry_frame.pack(pady=2)

        label = tk.Label(entry_frame, text=f"{row['Type']} - ₹{row['Amount']} - {row['Description']}")
        label.pack(side=tk.LEFT)

        remove_button = tk.Button(entry_frame, text="Remove", command=lambda idx=index: remove_entry(idx))
        remove_button.pack(side=tk.RIGHT)

def show_data():
    global refresh_data
    if show_button["text"] == "Show Data":
        refresh_data = True
        update_data_display()
        show_button["text"] = "Hide Data"
    else:
        for widget in dframe.winfo_children():
            widget.destroy()
        refresh_data = False
        show_button["text"] = "Show Data"

def remove_entry(index):
    global data
    data = data.drop(index).reset_index(drop=True)
    messagebox.showinfo("Removed", "Entry removed successfully.")
    
    if refresh_data:
        update_data_display()

def calculate_loss():
    if data.empty:
        messagebox.showinfo("Info", "No data available to calculate loss.")
        return

    income = data[data["Type"] == "Income"]["Amount"].sum()
    expense = data[data["Type"] == "Expense"]["Amount"].sum()

    if expense > income:
        loss = expense - income
        messagebox.showinfo("Loss Calculation", f"You are in a loss of: ₹{loss:.2f}")
    else:
        profit = income - expense
        messagebox.showinfo("Profit Calculation", f"You are in profit of: ₹{profit:.2f}")

def clear_entries():
    global data
    data = pd.DataFrame(columns=["Type", "Amount", "Description"])
    messagebox.showinfo("Cleared", "All entries cleared.")
    
    if refresh_data:
        update_data_display()

def create_widgets(root):
    frame = tk.Frame(root)
    frame.pack(padx=10, pady=10)

    tk.Label(frame, text="Type (Income/Expense):").grid(row=0, column=0)
    
    type_entry = tk.Entry(frame)
    type_entry.grid(row=0, column=1)

    tk.Label(frame, text="Amount:").grid(row=1, column=0)
    
    amount_entry = tk.Entry(frame)
    amount_entry.grid(row=1, column=1)

    tk.Label(frame, text="Description:").grid(row=2, column=0)
    
    desc_entry = tk.Entry(frame)
    desc_entry.grid(row=2, column=1)

    tk.Button(frame, text="Add", command=lambda: add_entry(type_entry, amount_entry, desc_entry)).grid(row=3, column=0)

    global show_button
    show_button = tk.Button(frame, text="Show Data", command=show_data)
    show_button.grid(row=3, column=1)

    tk.Button(frame, text="Calculate Loss/Profit", command=calculate_loss).grid(row=4, column=0)

    tk.Button(frame, text="Clear All Entries", command=clear_entries).grid(row=4, column=1)

    global dframe
    dframe = tk.Frame(root)
    dframe.pack(padx=10, pady=(10, 0))

def main():
    root = tk.Tk()
    root.title("Budget App")
    
    create_widgets(root)
    
    root.mainloop()

if __name__ == "__main__":
    main()