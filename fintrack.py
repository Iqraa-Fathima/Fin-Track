import tkinter as tk
from tkinter import messagebox, ttk
import csv
import os
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
FILENAME = 'data.csv'
data = {'income': [], 'expenses': []}
def load_data():
    "Loading data from the CSV file if it exists."
    if os.path.exists(FILENAME):
        with open(FILENAME, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == 'income':
                    data['income'].append(float(row[1]))
                elif row[0] == 'expense':
                    data['expenses'].append(float(row[1]))

def save_data():
    "Saving data to the CSV file."
    with open(FILENAME, mode='w', newline='') as file:
        writer = csv.writer(file)
        for amount in data['income']:
            writer.writerow(['income', amount])
        for amount in data['expenses']:
            writer.writerow(['expense', amount])

def add_income():
    """Add income to the data dictionary and update the summary."""
    try:
        amount = float(income_entry.get())
        data['income'].append(amount)
        income_entry.delete(0, tk.END)
        update_summary()
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid number for income.")

def add_expense():
    """Add expense to the data dictionary and update the summary."""
    try:
        amount = float(expense_entry.get())
        data['expenses'].append(amount)
        expense_entry.delete(0, tk.END)
        update_summary()
    except ValueError:
        messagebox.showerror("Invalid input", "Please enter a valid number for expense.")

def update_summary():
    """Update the financial summary and chart."""
    total_income = sum(data['income'])
    total_expenses = sum(data['expenses'])
    balance = total_income - total_expenses
    
    total_income_label.config(text=f"Total Income: ₹{total_income:.2f}")
    total_expenses_label.config(text=f"Total Expenses: ₹{total_expenses:.2f}")
    balance_label.config(text=f"Remaining Balance: ₹{balance:.2f}")
    
    update_chart(total_income, total_expenses)

def update_chart(income, expenses):
    """Update the bar chart to display income vs. expenses."""
    fig.clear()
    ax = fig.add_subplot(111)
    ax.bar(['Income', 'Expenses'], [income, expenses], color=['green', 'red'])
    ax.set_title('Income vs. Expenses')
    ax.set_ylabel('Amount (₹)')
    canvas.draw()

root = tk.Tk()
root.title("Fin-Tracker")
# Income input
tk.Label(root, text="Income Amount (₹):").grid(row=0, column=0, padx=10, pady=10)
income_entry = tk.Entry(root)
income_entry.grid(row=0, column=1, padx=10, pady=10)
tk.Button(root, text="Add Income", command=add_income).grid(row=0, column=2, padx=10, pady=10)
# Expense input
tk.Label(root, text="Expense Amount (₹):").grid(row=1, column=0, padx=10, pady=10)
expense_entry = tk.Entry(root)
expense_entry.grid(row=1, column=1, padx=10, pady=10)
tk.Button(root, text="Add Expense", command=add_expense).grid(row=1, column=2, padx=10, pady=10)

# Summary Labels
total_income_label = tk.Label(root, text="Total Income: ₹0.00")
total_income_label.grid(row=2, column=0, columnspan=3, pady=10)

total_expenses_label = tk.Label(root, text="Total Expenses: ₹0.00")
total_expenses_label.grid(row=3, column=0, columnspan=3, pady=10)

balance_label = tk.Label(root, text="Remaining Balance: ₹0.00")
balance_label.grid(row=4, column=0, columnspan=3, pady=10)

fig = Figure(figsize=(4, 3), dpi=100)
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(row=5, column=0, columnspan=3, pady=20)

load_data()
update_summary()

root.protocol("WM_DELETE_WINDOW", lambda: [save_data(), root.destroy()])
root.mainloop()