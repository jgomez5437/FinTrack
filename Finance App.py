#Jesus Gomez Martinez
#FinTrack

import pandas as pd 
import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
import sqlite3
#Initialize database connection
connection = sqlite3.connect('finance.db')
#Create ik instance and root frame
root = tk.Tk()
root.resizable(False, False)
root_frame = tk.Frame(root)
root_frame.pack(fill="both", expand=True)
root.title("FinTrack")
root.geometry("1050x600")
root.resizable(False, False)
root.configure(background="darkgreen")
root_frame.configure(background="darkgreen")
#budget frame
budget_frame = tk.Frame(root, bg="darkgreen")
budget_frame.pack(fill="both", expand=True)
#transaction frame
transaction_frame = tk.Frame(root, bg="darkgreen")
transaction_frame.pack(fill="both", expand=True)
#function to switch between frames
def raise_frame(frame):
    if frame == budget_frame:
        root_frame.pack_forget()
        transaction_frame.pack_forget()
        frame.tkraise()
        frame.pack(fill="both", expand=True)
    elif frame == transaction_frame: 
        root_frame.pack_forget()
        budget_frame.pack_forget()
        frame.tkraise()
        frame.pack(fill="both", expand=True)
    elif frame == root_frame:
        budget_frame.pack_forget()
        transaction_frame.pack_forget()
        frame.tkraise()
        frame.pack(fill="both", expand=True)
"""Home Screen """
#title label - home screen
title_label = tk.Label(root_frame, text="FinTrack", font=("Arial", 40), fg="darkblue", bg="darkgreen")
title_label.place(relx=0.5, rely=0.3, anchor=tk.CENTER)
#subtitle label
sentence_label = tk.Label(root_frame, text="Be Smart With Your Money", font=("Arial", 20), fg="darkblue", bg="darkgreen")
sentence_label.place(relx=0.5, rely=0.4, anchor=tk.CENTER)
#enter button
enter_button = tk.Button(root_frame, text="Enter Budget", font=("Arial",20), fg="darkblue", bg="white", padx=20, pady=10, command=lambda: raise_frame(budget_frame))
enter_button.place(relx=0.4, rely=0.6, anchor=tk.CENTER)
#exit button
exit_button = tk.Button(root_frame, text="Exit", font=("Arial",20), fg="darkblue", bg="white", padx=20, pady=10, command=lambda: root.quit())
exit_button.place(relx=0.6, rely=0.6, anchor=tk.CENTER)
#exit button on budget_frame
exit_button = tk.Button(budget_frame, text="Exit", font=("Arial",10), fg="darkblue", bg="white", padx=10, pady=5, command=lambda: root.quit())
exit_button.place(x=950, y=50)
"""Budget Screen"""
#title
budget_title = tk.Label(budget_frame, text="FinTrack", font=("Arial",25), fg="darkblue", bg="darkgreen")
budget_title.place(x=40, y=40, anchor="nw")
"""Income Section"""
#income
income_title = tk.Label(budget_frame, text="Current Income:", font=("Arial", 15), fg="white", bg="darkgreen")
income_title.place(x=200, y=150)
#display income
current_income_label = tk.Label(budget_frame, text="", font=("Arial", 15), fg="white",bg="darkgreen")
current_income_label.place(x=350, y=150)
#this takes the last inputted income from db and displays it in current income label
current_income = pd.read_sql('SELECT amount FROM income ORDER BY id DESC LIMIT 1', connection)
if not current_income.empty:
    income_value = current_income.iloc[0]['amount']
    current_income_label.config(text="${:.2f}".format(income_value))
else:
    current_income_label.config(text="")
#function to show error message
def show_error_message(message):
    messagebox.showerror("Error", message)
#label to display the remaining income
remaining_income_label = tk.Label(budget_frame, text="", font=("Arial", 15), fg="white", bg="darkgreen")
remaining_income_label.place(x=600, y=310)
#Function to calculate the remaining income
def save_income():
    income = income_entry.get().strip()
    if not income:
        show_error_message("Please enter an income.")
        return
    try:
        income = float(income)
    except ValueError:
        show_error_message("Please enter a valid income.")
        return
    #Save the income to the database
    income_df = pd.DataFrame({'amount': [income]})
    income_df.to_sql('income', connection, if_exists='append', index=False)
    #Update the current income label
    update_income()
    #Clear the entry field
    income_entry.delete(0, tk.END)
    #Hide the income entry field and save button
    toggle_income_entry()
#Function to update the current income and calculate the remaining income
def update_income():
    global current_income
    #Fetch the last entered income from the database
    current_income = pd.read_sql('SELECT amount FROM income ORDER BY id DESC LIMIT 1', connection)
    if not current_income.empty:
        income_value = current_income.iloc[0]['amount']
        current_income_label.config(text="${:.2f}".format(income_value))
        calculate_remaining_income()  #Recalculate the remaining income
    else:
        current_income_label.config(text="")
        remaining_income_label.config(text="")  #Reset the remaining income label
#Function to calculate the remaining income
def calculate_remaining_income():
    global current_income  #Declare current_income as global
    #Get the total income
    total_income = current_income.iloc[0]['amount'] if not current_income.empty else 0
    #Get the sum of the budget categories' amounts
    categories_amounts = pd.read_sql('SELECT amount FROM budget_category', connection)
    categories_sum = categories_amounts['amount'].sum()
    #Calculate the remaining income
    remaining_income = total_income - categories_sum
    #Update the remaining income label
    remaining_income_label.config(text="Left to Budget: ${:.2f}".format(remaining_income))
#save button
save_button = tk.Button(budget_frame, text="Save", font=("Arial", 10), width=6, bg="white", command=save_income)
save_button.place(x=735, y=250)
#Entry for user to enter the income
income_entry = tk.Entry(budget_frame, width=15)
income_entry.place(x=600, y=250)
income_entry.bind("<Return>", save_income)
#Function that will hide and show the income entry and save button
def toggle_income_entry():
    if income_entry.winfo_ismapped():
        income_entry.place_forget()
        save_button.place_forget()
        income_button.config(text="Edit Income")
    else:
        income_entry.place(x=600, y=250)
        save_button.place(x=735, y=250)
        income_button.config(text="Hide")
#Income save/hide button
income_button = tk.Button(budget_frame, text="Hide", font=("Arial", 10), width=8, bg="white", command=toggle_income_entry)
income_button.place(x=600, y=280)
"""Category Section"""
#Category frame
category_frame = tk.Frame(budget_frame, bg="darkgreen")
category_frame.place(x=50, y=200)
#create a list to store the category labels
category_labels = []
#Function that removes category from GUI and database
def remove_category(category_name):
    #Delete the category from the database
    query = f"DELETE FROM budget_category WHERE name = '{category_name}'"
    connection.execute(query)
    connection.commit()
    #Recalculate the remaining income after removing the category
    calculate_remaining_income()
    #Redisplay the budget categories
    display_categories()
#Function that finds the transaction amounts from each category and adds them up
def get_total_category_spending(category):
    #Fetch the transactions for the specified category from the database
    query = f"SELECT amount FROM transactions WHERE category = '{category}'"
    transactions = pd.read_sql(query, connection)
    #Calculate the total spending for the category
    total_spending = transactions['amount'].sum()
    return total_spending
#Fetch the budget categories from the database
categories = pd.read_sql('SELECT name, amount FROM budget_category', connection)
#Extract the category names from the DataFrame
category_names = categories['name'].tolist()
#Check if the category_names list is empty
if not category_names:
    #Handle the case where there are no categories
    category_names = ['No categories available']
#Set the default value for the OptionMenu
selected_category = tk.StringVar(root)
selected_category.set(category_names[0])  #Set the default value
#OptionMenu widget
category_dropdown = tk.OptionMenu(transaction_frame, selected_category, *category_names)
category_dropdown.place(x=600, y=190)
#category label for options
category_indicator = tk.Label(transaction_frame, text="Choose category:", font=("Arial", 15), fg="white", bg="darkgreen")
category_indicator.place(x=600, y=160)
#Function to update the dropdown menu options for transactions
def update_transaction_options():
    #Fetch the budget categories from the database
    categories = pd.read_sql('SELECT name FROM budget_category', connection)
    category_names = categories['name'].tolist()
    #Update the options in the dropdown menu
    menu = category_dropdown["menu"]
    menu.delete(0, "end")
    for name in category_names:
        menu.add_command(label=name, command=lambda value=name: selected_category.set(value))
        
#Function to display the budget categories
def display_categories():
    #Remove any existing category labels and buttons
    for label, budget_label, spending_label, remove_button in category_labels:
        label.destroy()
        budget_label.destroy()
        spending_label.destroy()
        remove_button.destroy()
    category_labels.clear()
    #Fetch the budget categories from the database
    categories = pd.read_sql('SELECT name, amount FROM budget_category', connection)
    #Create labels for each category
    for i, row in categories.iterrows():
        category_name = row['name']
        label = tk.Label(category_frame, text=category_name, font=("Arial", 15), fg="white", bg="darkgreen", width=10, wraplength=100)
        label.grid(column=0, row=i, padx=10, pady=10)
        #Create a label for the budget amount
        budget_label = tk.Label(category_frame, text="Budget: ${:.2f}".format(row['amount']), font=("Arial", 12), fg="white", bg="darkgreen")
        budget_label.grid(column=1, row=i, padx=10, pady=10)
        #Calculate the total spending for the category
        total_spending = get_total_category_spending(category_name)
        #Calculate the remaining budget for the category
        remaining_budget = row['amount'] - total_spending
        #Create a separate label to display the spending and remaining budget for each category
        remaining_budget_var = tk.StringVar()
        spending_label = tk.Label(category_frame,textvariable=remaining_budget_var,font=("Arial", 12), fg="white", bg="darkgreen")
        spending_label.grid(column=2, row=i, padx=10, pady=10)
        # Calculate the remaining budget for the category
        remaining_budget_var.set("Remaining: ${:.2f}".format(remaining_budget))
        #Create a remove button for each category
        remove_button = tk.Button(category_frame, text="Remove", font=("Arial", 10), width=6, bg="white", command=lambda name=category_name: remove_category(name))
        remove_button.grid(column=4, row=i, padx=10, pady=10)
        #Adds the information tot he category_labels list
        category_labels.append((label, budget_label, spending_label, remove_button))
    #Update the dropdown menu options for transactions
    update_transaction_options()
#display the budget categories when the program starts
display_categories()

#Function that saves the category and adds to the database
def save_category(category, amount_entry, category_label, amount_label):
    amount = amount_entry.get().strip()
    amount_entry.grid_remove()
    if not amount:
        show_error_message("Please enter an amount.")
        return
    try:
        amount = float(amount)
    except ValueError:
        show_error_message("Please enter a valid amount.")
        return
    category_df = pd.DataFrame({'name': [category], 'amount': [amount]})
    category_df.to_sql('budget_category', connection, if_exists='append', index=False)
    category_label.config(text=category)
    amount_label.config(text="$" + str(amount))  #Convert amount to string
    amount_entry.delete(0, tk.END)
    calculate_remaining_income()  #Update the remaining income
    display_categories()  #Redisplay the budget categories
    
#Function that adds a new category name
def add_category():
    global category_entry, category_label, category_entry_row
    category_label = tk.Label(category_frame, text="Category:", font=("Arial", 15), fg="white", bg="darkgreen")
    category_label.grid(column=0, row=category_frame.grid_size()[1], padx=10, pady=10)
    category_entry_row = category_frame.grid_size()[1] - 1
    category_entry = tk.Entry(category_frame, font=("Arial", 13))
    category_entry.grid(column=1, row=category_entry_row, padx=10, pady=10)
    category_entry.bind("<Return>", lambda event: add_category_amount())
    calculate_remaining_income()  #Update the remaining income
    
#Function that adds a new category amount
def add_category_amount():
    global amount_entry, amount_label
    category = category_entry.get().strip()  #Store the value before destroying the entry widget
    category_entry.grid_remove()
    amount_label = tk.Label(category_frame, text="Amount:", font=("Arial", 15), fg="white", bg="darkgreen")
    amount_label.grid(column=2, row=category_entry_row, padx=10, pady=10)
    amount_entry = tk.Entry(category_frame, font=("Arial", 15))
    amount_entry.focus_set()
    amount_entry.grid(column=3, row=category_entry_row, padx=10, pady=10)
    amount_entry.bind("<Return>", lambda event: save_category(category, amount_entry, category_label, amount_label))
#create the "Add Category" button
add_category_button = tk.Button(budget_frame, text="Add Category", font=("Arial", 10), width=10, bg="white", command=add_category)
add_category_button.place(x=90, y=150)
"""Transactions Section"""
#Transaction name label
transaction_name_label = tk.Label(transaction_frame, text="Transaction Name:", font=("Arial", 15), fg="white", bg="darkgreen")
transaction_name_label.place(x=600, y=220)
#Transaction name entry
transaction_name_entry = tk.Entry(transaction_frame, font=("Arial", 13))
transaction_name_entry.place(x=600, y=250)
#Amount label
transaction_amount_label = tk.Label(transaction_frame, text="Amount:", font=("Arial", 15), fg="white", bg="darkgreen")
transaction_amount_label.place(x=600, y=280)
#Transaction amount entry
transaction_amount_entry = tk.Entry(transaction_frame, font=("Arial", 13))
transaction_amount_entry.place(x=600, y=310)
#Empty list to store the transaction labels
transaction_labels = []
#Transactions label
transactions_label = tk.Label(transaction_frame, text="Transactions:", font=("Arial", 15), fg="white", bg="darkgreen")
transactions_label.place(x=100, y=50)

#Function that displays transactions
def display_transactions():
    #Clears existing transactions
    transaction_display.delete('1.0', tk.END)
    #Fetch all transactions from the database
    query = "SELECT category, name, amount FROM transactions"
    transactions = pd.read_sql(query, connection)
    #Sort transactions by category name
    transactions = transactions.sort_values('category')
    #Display transactions in the scrolledtext widget
    for _, row in transactions.iterrows():
        category = row['category']
        name = row['name']
        amount = row['amount']
        transaction_display.insert(tk.END, "Category: {} | Name: {} | Amount: {:.2f}".format(category, name, amount))
        #Create a remove button for each transaction
        remove_button = tk.Button(transaction_frame, text="Remove", font=("Arial", 8), width=6, bg="white", command=lambda c=category, n=name, a=amount: remove_transaction(c, n, a))
        transaction_display.window_create(tk.END, window=remove_button)
        transaction_display.insert(tk.END, "\n")
#Function that adds transactions to GUI and database

def add_transaction(category):
    name = transaction_name_entry.get().strip()
    amount = transaction_amount_entry.get().strip()
    if not name or not amount:
        show_error_message("Please enter a name and amount.")
        return
    try:
        amount = float(amount)
    except ValueError:
        show_error_message("Please enter a valid amount.")
        return
    #Insert the transaction into the database with the selected category
    transaction_df = pd.DataFrame({'category': [category], 'name': [name], 'amount': [amount]})
    transaction_df.to_sql('transactions', connection, if_exists='append', index=False)
    #Updates the spending and remaining labels for the corresponding category
    for label in category_labels:
        if label[0] == category:
            budget_label = label[1]
            spending_label = label[2]
            current_budget = float(budget_label.cget("text").split("$")[1])
            current_spending = float(spending_label.cget("text").split("$")[1])
            #Calculates new amounts
            new_spending = current_spending + amount
            new_remaining = current_budget - new_spending
            #Updates remaining label
            spending_label.config(text="Remaining: ${:.2f}".format(new_remaining))
            break
    #Clear the entry fields
    transaction_name_entry.delete(0, tk.END)
    transaction_amount_entry.delete(0, tk.END)
    display_categories()
#Scroll box for the transactions
transaction_display = scrolledtext.ScrolledText(transaction_frame, font=("Arial", 12), fg="white", bg="darkgreen", width=45, height=24)
transaction_display.place(x=100, y=80)
#Button to move to transactions frame
transaction_frame_b = tk.Button(budget_frame, text="Transactions", font=("Arial", 10), width=10, bg="white", command=lambda: raise_frame(transaction_frame))
transaction_frame_b.place(x=600, y=410)
#Function to remove transactions
def remove_transaction(category, name, amount):
    #Delete the transaction from the database
    query = "DELETE FROM transactions WHERE category = ? AND name = ? AND amount = ?"
    connection.execute(query, (category, name, amount))
    connection.commit()
    #Update the spending and remaining labels for the corresponding category
    for label in category_labels:
        if label[0] == category:
            budget_label = label[1]
            spending_label = label[2]
            current_budget = float(budget_label.cget("text").split("$")[1])
            current_spending = float(spending_label.cget("text").split("$")[1])
            #Calculates math
            new_remaining = current_spending + amount
            #Updates the remaining label
            spending_label.config(text="Remaining: ${:.2f}".format(new_remaining))
            break
    #Redisplay the transactions
    display_transactions()
    display_categories()
#Function to handle the button click event to add a transaction
def handle_add_transaction():
    category = selected_category.get()  #Retrieve the selected category value
    add_transaction(category)
    display_transactions()
add_transaction_button = tk.Button(transaction_frame, text="Add Transaction", font=("Arial", 10), width=11, bg="white", command=handle_add_transaction)
add_transaction_button.place(x=600, y=340)
#back button for the transaction screen
trans_back_button = tk.Button(transaction_frame, text="Back To Budget", font=("Arial", 10), width=11, bg="white", command=lambda: raise_frame(budget_frame))
trans_back_button.place(x=600, y=100)
#will initially update the remaining income
calculate_remaining_income()
#Display all transactions for each category
display_transactions()
#starts program at root frame - home screen
raise_frame(root_frame)
#starts GUI
root.mainloop()
