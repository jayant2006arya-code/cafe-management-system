import tkinter as tk
from tkinter import messagebox
import random
from datetime import datetime

# Menu items with prices
menu = {
    'Coffee': 10,
    'Tea': 10,
    'Sandwich': 25,
    'Cake': 120,
    'Juice': 20,
    'Pasta':100
}

order = {}

def add_item(item):
    if item in order:
        order[item] += 1
    else:
        order[item] = 1
    update_bill_preview()

def update_bill_preview():
    """Shows a live preview of items added, without total or discount."""
    bill_text.delete("1.0", tk.END)
    total = 0
    for item, qty in order.items():
        price = menu[item] * qty
        bill_text.insert(tk.END, f"{item} x{qty} = ${price:.2f}\n")
        total += price
    bill_text.insert(tk.END, f"\n[Click 'Generate Bill' to apply discount]")

def generate_receipt_id():
    return f"R{random.randint(1000, 9999)}"

def generate_bill():
    customer_name = name_entry.get().strip()
    if not customer_name:
        messagebox.showwarning("Missing Info", "Please enter customer name.")
        return
    if not order:
        messagebox.showwarning("Empty Order", "No items in order.")
        return

    bill_text.delete("1.0", tk.END)
    total = 0
    receipt_id = generate_receipt_id()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    bill_text.insert(tk.END, f"Customer: {customer_name}\n")
    bill_text.insert(tk.END, f"Receipt ID: {receipt_id}\n")
    bill_text.insert(tk.END, f"Date & Time: {current_time}\n")
    bill_text.insert(tk.END, "-"*35 + "\n")

    order_lines = []
    for item, qty in order.items():
        price = menu[item] * qty
        order_lines.append(f"{item} x{qty} = ${price:.2f}")
        total += price

    for line in order_lines:
        bill_text.insert(tk.END, line + "\n")

    discount_percent = discount_entry.get()
    discount_amount = 0
    final_total = total

    # Apply discount
    if discount_percent:
        try:
            discount = float(discount_percent)
            if discount < 0 or discount > 100:
                raise ValueError
            discount_amount = total * (discount / 100)
            final_total = total - discount_amount
            bill_text.insert(tk.END, f"\nSubtotal: ${total:.2f}")
            bill_text.insert(tk.END, f"\nDiscount: {discount:.1f}% (-${discount_amount:.2f})")
            bill_text.insert(tk.END, f"\nTotal After Discount: ${final_total:.2f}")
        except ValueError:
            bill_text.insert(tk.END, f"\n[Invalid discount % entered!]")
            return
    else:
        bill_text.insert(tk.END, f"\nTotal: ${total:.2f}")

    save_to_history(customer_name, receipt_id, current_time, order_lines, total, discount_percent, discount_amount, final_total)

def save_to_history(name, receipt_id, time, items, total, discount_percent, discount_amount, final_total):
    try:
        with open("order_history.txt", "a") as file:
            file.write(f"Customer: {name}\n")
            file.write(f"Receipt ID: {receipt_id}\n")
            file.write(f"Date & Time: {time}\n")
            file.write("-" * 40 + "\n")
            for line in items:
                file.write(line + "\n")
            file.write(f"Subtotal: ${total:.2f}\n")
            if discount_percent:
                file.write(f"Discount: {discount_percent}% (-${discount_amount:.2f})\n")
            file.write(f"Total Paid: ${final_total:.2f}\n")
            file.write("=" * 40 + "\n\n")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save order history.\n{e}")

def clear_order():
    order.clear()
    bill_text.delete("1.0", tk.END)
    discount_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)

def exit_app():
    if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
        root.destroy()

# Tkinter window setup
root = tk.Tk()
root.title("Café Management System")
root.geometry("500x600")
root.config(bg="dodgerblue")

# Title
title = tk.Label(root, text="Café Algorithm", font=("Arial", 18, "bold"), bg="grey")
title.pack(pady=10)

# Customer name input
name_frame = tk.Frame(root, bg="grey")
name_frame.pack(pady=5)

name_label = tk.Label(name_frame, text="Customer Name:", font=("Arial", 11), bg="grey")
name_label.grid(row=0, column=0, padx=5)

name_entry = tk.Entry(name_frame, width=25)
name_entry.grid(row=0, column=1)

# Menu buttons
menu_frame = tk.Frame(root, bg="grey")
menu_frame.pack(pady=5)

for item in menu:
    btn = tk.Button(menu_frame, text=f"{item} (${menu[item]:.2f})", width=25, command=lambda i=item: add_item(i))
    btn.pack(pady=3)

# Discount input
discount_frame = tk.Frame(root, bg="grey")
discount_frame.pack(pady=10)

discount_label = tk.Label(discount_frame, text="Discount (%):", font=("Arial", 12), bg="yellow")
discount_label.grid(row=0, column=0, padx=5)

discount_entry = tk.Entry(discount_frame, width=10)
discount_entry.grid(row=0, column=1)

# Bill display
bill_label = tk.Label(root, text="Order Summary:", font=("Arial", 12), bg="grey")
bill_label.pack()

bill_text = tk.Text(root, height=15, width=50)
bill_text.pack(pady=5)

# Buttons
btn_frame = tk.Frame(root, bg="white")
btn_frame.pack(pady=9)

generate_btn = tk.Button(btn_frame, text="Generate Bill", width=15, bg="grey", fg="white", command=generate_bill)
generate_btn.grid(row=0, column=0, padx=1)

clear_btn = tk.Button(btn_frame, text="Clear Order", width=15, bg="grey",fg="white",command=clear_order)
clear_btn.grid(row=0, column=1, padx=1)

exit_btn = tk.Button(btn_frame, text="Exit", width=15, bg="grey",fg="white", command=exit_app)
exit_btn.grid(row=0, column=2, padx=1)

# Start the app
root.mainloop()
