import tkinter as tk
from tkinter import messagebox, ttk
from tkinter import Canvas, Scrollbar
import csv
import os
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkcalendar import Calendar
from datetime import datetime

# Initialize application settings
FILENAME = 'data.csv'
data = {'income': [], 'expenses': []}
options = ["Groceries", "Rent", "Bills", "Entertainment", "Miscellaneous"]

# Load and save functions for CSV data
def load_data():
    if os.path.exists(FILENAME):
        with open(FILENAME, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) == 4:
                    date, category, amount, type = row
                    if type == 'income':
                        data['income'].append((date, float(amount)))
                    elif type == 'expense':
                        data['expenses'].append((date, category, float(amount)))

def save_data():
    with open(FILENAME, mode='w', newline='') as file:
        writer = csv.writer(file)
        for date, amount in data['income']:
            writer.writerow([date, '', amount, 'income'])
        for date, category, amount in data['expenses']:
            writer.writerow([date, category, amount, 'expense'])

# Function to add income
def add_income():
    try:
        amount = float(income_entry.get())
        date = calendar.get_date()
        data['income'].append((date, amount))
        income_entry.delete(0, tk.END)
        update_summary()
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid income.")

# Function to add expense
def add_expense():
    try:
        amount = float(expense_entry.get())
        date = calendar.get_date()
        category = category_combobox.get()
        data['expenses'].append((date, category, amount))
        expense_entry.delete(0, tk.END)
        update_summary()
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid expense.")

# Function to update the summary and chart
def update_summary():
    total_income = sum(amount for _, amount in data['income'])
    total_expenses = sum(amount for _, _, amount in data['expenses'])
    balance = total_income - total_expenses
    
    total_income_label.config(text=f"Total Income: ₹{total_income:.2f}")
    total_expenses_label.config(text=f"Total Expenses: ₹{total_expenses:.2f}")
    balance_label.config(text=f"Remaining Balance: ₹{balance:.2f}")
    
    if balance < 5000:
        messagebox.showwarning("Low Savings", "Your savings are below ₹5000. Consider spending wisely!")
    
    update_chart(total_income, total_expenses)

# Function to update the bar chart for income vs expenses
def update_chart(income, expenses):
    fig.clear()
    ax = fig.add_subplot(111)
    ax.bar(['Income', 'Expenses'], [income, expenses], color=['#5cb85c', '#d9534f'])
    ax.set_title('Income vs. Expenses', fontsize=14)
    ax.set_ylabel('Amount (₹)', fontsize=12)
    ax.tick_params(axis='x', labelsize=10)
    ax.tick_params(axis='y', labelsize=10)
    canvas.draw()

# Function to calculate and display savings for the selected month
def calculate_monthly_savings():
    selected_month = month_combobox.get()
    month_number = datetime.strptime(selected_month, "%B").month
    
    income_for_month = sum(amount for date, amount in data['income'] if datetime.strptime(date, "%Y-%m-%d").month == month_number)
    expenses_for_month = sum(amount for date, _, amount in data['expenses'] if datetime.strptime(date, "%Y-%m-%d").month == month_number)
    
    savings_for_month = income_for_month - expenses_for_month
    monthly_savings_label.config(text=f"Savings for {selected_month}: ₹{savings_for_month:.2f}")

# Function to create scrollable frame
def create_scrollable_frame(container):
    canvas = Canvas(container, bg="#f5f5f5")
    scrollbar = Scrollbar(container, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    return scrollable_frame

# Function to categorize expenses and visualize using a pie chart
def show_expense_pie_chart():
    categories = {}
    for _, category, amount in data['expenses']:
        if category in categories:
            categories[category] += amount
        else:
            categories[category] = amount

    if not categories:
        messagebox.showinfo("No Data", "No expenses found!")
        return

    fig_pie.clear()
    ax = fig_pie.add_subplot(111)
    ax.pie(categories.values(), labels=categories.keys(), autopct='%1.1f%%', startangle=90, colors=['#ff9999','#66b3ff','#99ff99','#ffcc99', '#ffb3e6'])
    ax.axis('equal')
    pie_canvas.draw()

    # Function to categorize expenses and visualize using a pie chart
def show_expense_pie_chart():
    categories = {}
    for _, category, amount in data['expenses']:
        if category in categories:
            categories[category] += amount
        else:
            categories[category] = amount

    if not categories:
        messagebox.showinfo("No Data", "No expenses found!")
        return

    fig_pie.clear()  # Clear previous pie chart
    ax = fig_pie.add_subplot(111)
    ax.pie(categories.values(), labels=categories.keys(), autopct='%1.1f%%', startangle=90, 
           colors=['#ff9999','#66b3ff','#99ff99','#ffcc99', '#ffb3e6'])
    ax.axis('equal')  # Ensure the pie chart is a circle
    pie_canvas.draw()  # Update the pie chart canvas

# Initialize the main window
root = tk.Tk()
root.title("Fin-Tracker")
root.configure(bg="#f5f5f5")
root.geometry("800x650")

# Create a main frame with a scrollable feature
main_frame = ttk.Frame(root)
main_frame.pack(fill="both", expand=True, padx=10, pady=10)
scrollable_frame = create_scrollable_frame(main_frame)

# Title Label
header_frame = tk.Frame(scrollable_frame, bg="#5bc0de", padx=20, pady=10)
header_frame.grid(row=0, column=0, columnspan=3, sticky="ew")
title_label = tk.Label(header_frame, text="PocketPluse", font=("Arial", 20, "bold"), bg="#5bc0de", fg="white")
title_label.grid(row=0, column=0)

# Calendar
tk.Label(scrollable_frame, text="Date:", font=("Arial", 12), bg="#f5f5f5").grid(row=1, column=0, padx=10, pady=10, sticky="w")
calendar = Calendar(scrollable_frame, selectmode='day', date_pattern="y-mm-dd", background="#e6f7ff", headersbackground="#5bc0de")
calendar.grid(row=1, column=1, columnspan=2, padx=10, pady=10)

# Income Entry
tk.Label(scrollable_frame, text="Income Amount (₹):", font=("Arial", 12), bg="#f5f5f5").grid(row=2, column=0, padx=10, pady=10, sticky="w")
income_entry = tk.Entry(scrollable_frame, font=("Arial", 12), bg="#dff0d8")
income_entry.grid(row=2, column=1, padx=10, pady=10, sticky="ew")
add_income_button = tk.Button(scrollable_frame, text="Add Income", command=add_income, bg="#5cb85c", fg="white", font=("Arial", 12, "bold"))
add_income_button.grid(row=2, column=2, padx=10, pady=10)

# Expense Entry with Categories
tk.Label(scrollable_frame, text="Expense Amount (₹):", font=("Arial", 12), bg="#f5f5f5").grid(row=3, column=0, padx=10, pady=10, sticky="w")
expense_entry = tk.Entry(scrollable_frame, font=("Arial", 12), bg="#f2dede")
expense_entry.grid(row=3, column=1, padx=10, pady=10, sticky="ew")

tk.Label(scrollable_frame, text="Category:", font=("Arial", 12), bg="#f5f5f5").grid(row=3, column=2, padx=10, pady=10, sticky="w")
category_combobox = ttk.Combobox(scrollable_frame, values=options, font=("Arial", 12))
category_combobox.grid(row=3, column=3, padx=10, pady=10, sticky="ew")
category_combobox.set(options[0])  # Set default category

add_expense_button = tk.Button(scrollable_frame, text="Add Expense", command=add_expense, bg="#d9534f", fg="white", font=("Arial", 12, "bold"))
add_expense_button.grid(row=3, column=4, padx=10, pady=10)

# Monthly Savings Calculation
tk.Label(scrollable_frame, text="Select Month:", font=("Arial", 12), bg="#f5f5f5").grid(row=4, column=0, padx=10, pady=10, sticky="w")
month_combobox = ttk.Combobox(scrollable_frame, values=[datetime(2024, m, 1).strftime('%B') for m in range(1, 13)], font=("Arial", 12))
month_combobox.grid(row=4, column=1, padx=10, pady=10, sticky="ew")
month_combobox.set(datetime.now().strftime('%B'))

calculate_savings_button = tk.Button(scrollable_frame, text="Calculate Savings", command=calculate_monthly_savings, bg="#5bc0de", fg="white", font=("Arial", 12, "bold"))
calculate_savings_button.grid(row=4, column=2, padx=10, pady=10)

monthly_savings_label = tk.Label(scrollable_frame, text="Savings for the month: ₹0.00", font=("Arial", 12), bg="#f5f5f5")
monthly_savings_label.grid(row=4, column=3, padx=10, pady=10, columnspan=2, sticky="w")

# Summary Labels
total_income_label = tk.Label(scrollable_frame, text="Total Income: ₹0.00", font=("Arial", 14), bg="#f5f5f5")
total_income_label.grid(row=5, column=0, padx=10, pady=10, columnspan=2, sticky="w")

total_expenses_label = tk.Label(scrollable_frame, text="Total Expenses: ₹0.00", font=("Arial", 14), bg="#f5f5f5")
total_expenses_label.grid(row=5, column=2, padx=10, pady=10, columnspan=2, sticky="w")

balance_label = tk.Label(scrollable_frame, text="Remaining Balance: ₹0.00", font=("Arial", 14, "bold"), bg="#f5f5f5")
balance_label.grid(row=5, column=4, padx=10, pady=10, sticky="w")

# Pie Chart Button
pie_chart_button = tk.Button(scrollable_frame, text="Show Expense Distribution", command=show_expense_pie_chart, bg="#0275d8", fg="white", font=("Arial", 12, "bold"))
pie_chart_button.grid(row=6, column=0, padx=10, pady=10, columnspan=5, sticky="ew")

#Figure for Bar Chart (Income vs Expenses)
fig = Figure(figsize=(6, 4), dpi=100)
canvas = FigureCanvasTkAgg(fig, master=scrollable_frame)
canvas.get_tk_widget().grid(row=7, column=0, columnspan=5, padx=10, pady=10)

#Figure for Pie Chart (Expense Category Distribution)
"""fig_pie = Figure(figsize=(6, 4), dpi=100)
pie_canvas = FigureCanvasTkAgg(fig_pie, master=scrollable_frame)
pie_canvas.get_tk_widget().grid(row=8, column=0, columnspan=5, padx=10, pady=10)"""

#to load data and update UI
load_data()
update_summary()

# Save data when the window is closed
def on_closing():
    save_data()
    root.destroy()
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()


# Initialize the main window
root = tk.Tk()
root.title("PocketPluse")
root.configure(bg="#f5f5f5")
root.geometry("800x650")

# Create a main frame with a scrollable feature
main_frame = ttk.Frame(root)
main_frame.pack(fill="both", expand=True, padx=10, pady=10)
scrollable_frame = create_scrollable_frame(main_frame)

# Title Label
header_frame = tk.Frame(scrollable_frame, bg="#5bc0de", padx=20, pady=10)
header_frame.grid(row=0, column=0, columnspan=3, sticky="ew")
title_label = tk.Label(header_frame, text="PocketPluse", font=("Arial", 20, "bold"), bg="#5bc0de", fg="white")
title_label.grid(row=0, column=0)

# Calendar
tk.Label(scrollable_frame, text="Date:", font=("Arial", 12), bg="#f5f5f5").grid(row=1, column=0, padx=10, pady=10, sticky="w")
calendar = Calendar(scrollable_frame, selectmode='day', date_pattern="y-mm-dd", background="#e6f7ff", headersbackground="#5bc0de")
calendar.grid(row=1, column=1, columnspan=2, padx=10, pady=10)

# Income Entry
tk.Label(scrollable_frame, text="Income Amount (₹):", font=("Arial", 12), bg="#f5f5f5").grid(row=2, column=0, padx=10, pady=10, sticky="w")
income_entry = tk.Entry(scrollable_frame, font=("Arial", 12), bg="#dff0d8")
income_entry.grid(row=2, column=1, padx=10, pady=10, sticky="ew")
add_income_button = tk.Button(scrollable_frame, text="Add Income", command=add_income, bg="#5cb85c", fg="white", font=("Arial", 12, "bold"))
add_income_button.grid(row=2, column=2, padx=10, pady=10)

# Expense Entry with Categories
tk.Label(scrollable_frame, text="Expense Amount (₹):", font=("Arial", 12), bg="#f5f5f5").grid(row=3, column=0, padx=10, pady=10, sticky="w")
expense_entry = tk.Entry(scrollable_frame, font=("Arial", 12), bg="#f2dede")
expense_entry.grid(row=3, column=1, padx=10, pady=10, sticky="ew")

tk.Label(scrollable_frame, text="Category:", font=("Arial", 12), bg="#f5f5f5").grid(row=3, column=2, padx=10, pady=10, sticky="w")
category_combobox = ttk.Combobox(scrollable_frame, values=options, font=("Arial", 12))
category_combobox.grid(row=3, column=3, padx=10, pady=10, sticky="ew")
category_combobox.set(options[0])  # Set default category

add_expense_button = tk.Button(scrollable_frame, text="Add Expense", command=add_expense, bg="#d9534f", fg="white", font=("Arial", 12, "bold"))
add_expense_button.grid(row=3, column=4, padx=10, pady=10)

# Monthly Savings Calculation
tk.Label(scrollable_frame, text="Select Month:", font=("Arial", 12), bg="#f5f5f5").grid(row=4, column=0, padx=10, pady=10, sticky="w")
month_combobox = ttk.Combobox(scrollable_frame, values=[datetime(2024, m, 1).strftime('%B') for m in range(1, 13)], font=("Arial", 12))
month_combobox.grid(row=4, column=1, padx=10, pady=10, sticky="ew")
month_combobox.set(datetime.now().strftime('%B'))

calculate_savings_button = tk.Button(scrollable_frame, text="Calculate Savings", command=calculate_monthly_savings, bg="#5bc0de", fg="white", font=("Arial", 12, "bold"))
calculate_savings_button.grid(row=4, column=2, padx=10, pady=10)

monthly_savings_label = tk.Label(scrollable_frame, text="Savings for the month: ₹0.00", font=("Arial", 12), bg="#f5f5f5")
monthly_savings_label.grid(row=4, column=3, padx=10, pady=10, columnspan=2, sticky="w")

# Summary Labels
total_income_label = tk.Label(scrollable_frame, text="Total Income: ₹0.00", font=("Arial", 14), bg="#f5f5f5")
total_income_label.grid(row=5, column=0, padx=10, pady=10, columnspan=2, sticky="w")

total_expenses_label = tk.Label(scrollable_frame, text="Total Expenses: ₹0.00", font=("Arial", 14), bg="#f5f5f5")
total_expenses_label.grid(row=5, column=2, padx=10, pady=10, columnspan=2, sticky="w")

balance_label = tk.Label(scrollable_frame, text="Remaining Balance: ₹0.00", font=("Arial", 14, "bold"), bg="#f5f5f5")
balance_label.grid(row=5, column=4, padx=10, pady=10, sticky="w")

# Pie Chart Button
pie_chart_button = tk.Button(scrollable_frame, text="Show Expense Distribution", command=show_expense_pie_chart, bg="#0275d8", fg="white", font=("Arial", 12, "bold"))
pie_chart_button.grid(row=6, column=0, padx=10, pady=10, columnspan=5, sticky="ew")

#Figure for Bar Chart (Income vs Expenses)
fig = Figure(figsize=(6, 4), dpi=100)
canvas = FigureCanvasTkAgg(fig, master=scrollable_frame)
canvas.get_tk_widget().grid(row=7, column=0, columnspan=5, padx=10, pady=10)

#Figure for Pie Chart (Expense Category Distribution)
fig_pie = Figure(figsize=(6, 4), dpi=100)
pie_canvas = FigureCanvasTkAgg(fig_pie, master=scrollable_frame)
pie_canvas.get_tk_widget().grid(row=8, column=0, columnspan=5, padx=10, pady=10)


from tkcalendar import DateEntry

# Filter by Date Range
def filter_by_date_range():
    start_date = start_date_entry.get()
    end_date = end_date_entry.get()

    filtered_expenses = [expense for expense in data['expenses'] if start_date <= expense[0] <= end_date]
    filtered_income = [income for income in data['income'] if start_date <= income[0] <= end_date]

    total_filtered_income = sum(amount for _, amount in filtered_income)
    total_filtered_expenses = sum(amount for _, _, amount in filtered_expenses)
    filtered_balance = total_filtered_income - total_filtered_expenses

    filter_result_label.config(text=f"Filtered Income: ₹{total_filtered_income:.2f}, Filtered Expenses: ₹{total_filtered_expenses:.2f}, Balance: ₹{filtered_balance:.2f}")

# UI Elements for Date Range Filter
tk.Label(scrollable_frame, text="Start Date:", font=("Arial", 12), bg="#f5f5f5").grid(row=9, column=0, padx=10, pady=10)
start_date_entry = DateEntry(scrollable_frame, date_pattern="y-mm-dd")
start_date_entry.grid(row=9, column=1, padx=10, pady=10)

tk.Label(scrollable_frame, text="End Date:", font=("Arial", 12), bg="#f5f5f5").grid(row=9, column=2, padx=10, pady=10)
end_date_entry = DateEntry(scrollable_frame, date_pattern="y-mm-dd")
end_date_entry.grid(row=9, column=3, padx=10, pady=10)

filter_button = tk.Button(scrollable_frame, text="Filter", command=filter_by_date_range, bg="#0275d8", fg="white", font=("Arial", 12, "bold"))
filter_button.grid(row=9, column=4, padx=10, pady=10)

filter_result_label = tk.Label(scrollable_frame, text="", font=("Arial", 12), bg="#f5f5f5")
filter_result_label.grid(row=10, column=0, columnspan=5, padx=10, pady=10)

#to load data and update UI
load_data()
update_summary()

# Save data when the window is closed
def on_closing():
    save_data()
    root.destroy()
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
