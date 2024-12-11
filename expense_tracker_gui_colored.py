import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import csv
from collections import defaultdict

class Expense:
    def __init__(self, name, category, amount):
        self.name = name
        self.category = category
        self.amount = amount

    def __str__(self):
        return f"{self.name} - {self.category} - ${self.amount:.2f}"

class ExpenseTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.root.geometry("400x600")
        self.root.minsize(400, 600)
        self.root.configure(bg="#f0f0f0")

        self.create_widgets()
        self.load_budget()
        self.blink_title()

    def create_widgets(self):
        # Title Label
        self.title_label = tk.Label(self.root, text="📊 Expense Tracker", font=("Helvetica", 24, "bold"), bg="#f0f0f0", fg="#333")
        self.title_label.pack(pady=20)

        # Icon Image
        self.icon_label = tk.Label(self.root)
        self.icon_label.pack()
        self.load_icon()

        # Colorful Message
        self.message_label = tk.Label(self.root, text="!!!SAVE MONEY AND MONEY WILL SAVE YOU!!!", font=("Helvetica", 14, "bold"), bg="#f0f0f0", fg="blue")
        self.message_label.pack(pady=10)

        # Main Content Frame
        self.content_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.content_frame.pack(pady=10, padx=10, fill="both", expand=True)

        # Entry Frame
        self.entry_frame = tk.Frame(self.content_frame, bg="#ffffff", borderwidth=1, relief="solid")
        self.entry_frame.pack(pady=10, padx=10, fill="x")

        # Expense Name
        tk.Label(self.entry_frame, text="Expense Name:", bg="#ffffff", font=("Helvetica", 12)).grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.name_entry = tk.Entry(self.entry_frame, font=("Helvetica", 12))
        self.name_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
        self.apply_hover_effect(self.name_entry)

        # Expense Amount
        tk.Label(self.entry_frame, text="Amount ($):", bg="#ffffff", font=("Helvetica", 12)).grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.amount_entry = tk.Entry(self.entry_frame, font=("Helvetica", 12))
        self.amount_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        self.apply_hover_effect(self.amount_entry)

        # Category
        tk.Label(self.entry_frame, text="Category:", bg="#ffffff", font=("Helvetica", 12)).grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.category_combobox = ttk.Combobox(self.entry_frame, values=[
            "🍔 Food",
            "🏠 Home",
            "💼 Work",
            "🎉 Fun",
            "✨ Misc"
        ], state="readonly", font=("Helvetica", 12))
        self.category_combobox.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
        self.apply_hover_effect(self.category_combobox)

        # Budget Amount
        tk.Label(self.entry_frame, text="Budget ($):", bg="#ffffff", font=("Helvetica", 12)).grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.budget_entry = tk.Entry(self.entry_frame, font=("Helvetica", 12))
        self.budget_entry.grid(row=3, column=1, padx=10, pady=5, sticky="ew")
        self.apply_hover_effect(self.budget_entry)

        # Add Button
        self.add_button = tk.Button(self.content_frame, text="Add Expense", command=self.add_expense, bg="#4CAF50", fg="#ffffff", font=("Helvetica", 12, "bold"), relief="flat")
        self.add_button.pack(pady=5, fill="x")
        self.apply_hover_effect(self.add_button)

        # Expenses Listbox
        self.expenses_listbox = tk.Listbox(self.content_frame, height=10, borderwidth=1, relief="solid", bg="#ffffff", fg="#333", font=("Helvetica", 12))
        self.expenses_listbox.pack(pady=10, fill="both", expand=True)

        # Buttons Frame
        self.buttons_frame = tk.Frame(self.content_frame, bg="#f0f0f0")
        self.buttons_frame.pack(pady=10, fill="x")

        # Load Button
        self.load_button = tk.Button(self.buttons_frame, text="Load Expenses", command=self.load_expenses, bg="#2196F3", fg="#ffffff", font=("Helvetica", 12, "bold"), relief="flat")
        self.load_button.pack(side="left", padx=5, fill="x", expand=True)
        self.apply_hover_effect(self.load_button)

        # Summary Button
        self.summary_button = tk.Button(self.buttons_frame, text="Show Summary", command=self.show_summary, bg="#FFC107", fg="#ffffff", font=("Helvetica", 12, "bold"), relief="flat")
        self.summary_button.pack(side="left", padx=5, fill="x", expand=True)
        self.apply_hover_effect(self.summary_button)

        # Reset Button
        self.reset_button = tk.Button(self.buttons_frame, text="Reset All", command=self.reset_all, bg="#F44336", fg="#ffffff", font=("Helvetica", 12, "bold"), relief="flat")
        self.reset_button.pack(side="left", padx=5, fill="x", expand=True)
        self.apply_hover_effect(self.reset_button)

        # Budget and Total Spent Labels
        self.stats_frame = tk.Frame(self.content_frame, bg="#f0f0f0")
        self.stats_frame.pack(pady=10, fill="x")

        self.budget_label = tk.Label(self.stats_frame, text="Budget: $0.00", font=("Helvetica", 14), bg="#f0f0f0")
        self.budget_label.pack(pady=2)

        self.total_spent_label = tk.Label(self.stats_frame, text="Total Spent: $0.00", font=("Helvetica", 14), bg="#f0f0f0")
        self.total_spent_label.pack(pady=2)

        self.remaining_label = tk.Label(self.stats_frame, text="Remaining: $0.00", font=("Helvetica", 14), bg="#f0f0f0")
        self.remaining_label.pack(pady=2)

        # Summary Text Widget
        self.summary_text = tk.Text(self.content_frame, height=10, wrap="word", bg="#ffffff", font=("Helvetica", 12))
        self.summary_text.pack(pady=10, fill="both", expand=True)
        self.summary_text.config(state=tk.DISABLED)

        # Apply hover effects
        self.apply_hover_effects()

    def apply_hover_effect(self, widget):
        widget.bind("<Enter>", lambda e: self.on_hover(widget, True))
        widget.bind("<Leave>", lambda e: self.on_hover(widget, False))

    def apply_hover_effects(self):
        widgets = [
            self.add_button, self.load_button, self.summary_button, self.reset_button,
            self.name_entry, self.amount_entry, self.category_combobox, self.budget_entry
        ]
        for widget in widgets:
            self.apply_hover_effect(widget)

    def on_hover(self, widget, hover):
        if isinstance(widget, tk.Entry) or isinstance(widget, ttk.Combobox):
            if hover:
                widget.config(bg="#e0f7fa")
            else:
                widget.config(bg="#ffffff")
        elif isinstance(widget, tk.Button):
            if hover:
                widget.config(bg="#333", fg="#fff")
            else:
                if widget == self.add_button:
                    widget.config(bg="#4CAF50", fg="#ffffff")
                elif widget == self.load_button:
                    widget.config(bg="#2196F3", fg="#ffffff")
                elif widget == self.summary_button:
                    widget.config(bg="#FFC107", fg="#ffffff")
                elif widget == self.reset_button:
                    widget.config(bg="#F44336", fg="#ffffff")

    def add_expense(self):
        name = self.name_entry.get().strip()
        amount_str = self.amount_entry.get().strip()
        category = self.category_combobox.get()
        budget_str = self.budget_entry.get().strip()

        if not name or not amount_str or not category or not budget_str:
            messagebox.showwarning("Input Error", "Please fill in all fields.")
            return

        try:
            amount = float(amount_str)
            if amount <= 0:
                raise ValueError("Amount must be positive.")
            budget = float(budget_str)
            if budget <= 0:
                raise ValueError("Budget must be positive.")
        except ValueError as e:
            messagebox.showwarning("Input Error", f"Invalid value: {e}")
            return

        expense = Expense(name, category, amount)
        self.expenses_listbox.insert(tk.END, str(expense))
        self.save_expense_to_file(expense, budget)
        self.clear_entries()
        self.update_totals()

    def clear_entries(self):
        self.name_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        self.category_combobox.set('')
        self.budget_entry.delete(0, tk.END)

    def save_expense_to_file(self, expense, budget):
        try:
            with open("expenses.csv", "a", newline="", encoding="utf-8-sig") as file:
                writer = csv.writer(file)
                writer.writerow([expense.name, expense.category, expense.amount, budget])
        except Exception as e:
            messagebox.showerror("File Error", f"An error occurred while saving the expense: {e}")

    def load_expenses(self):
        self.expenses_listbox.delete(0, tk.END)
        self.budget_label.config(text="Budget: $0.00")
        self.total_spent_label.config(text="Total Spent: $0.00")
        self.remaining_label.config(text="Remaining: $0.00")
        try:
            with open("expenses.csv", "r", encoding="utf-8-sig") as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) == 4:
                        name, category, amount_str, budget_str = row
                        try:
                            amount = float(amount_str)
                            budget = float(budget_str)
                            expense = Expense(name, category, amount)
                            self.expenses_listbox.insert(tk.END, str(expense))
                        except ValueError:
                            continue
            self.update_totals()
        except FileNotFoundError:
            messagebox.showwarning("File Not Found", "No expenses found. Start by adding some expenses.")
        except Exception as e:
            messagebox.showerror("File Error", f"An error occurred while loading the expenses: {e}")

    def update_totals(self):
        total_spent = 0
        budget = 0
        try:
            with open("expenses.csv", "r", encoding="utf-8-sig") as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) == 4:
                        amount_str = row[2]
                        try:
                            amount = float(amount_str)
                            total_spent += amount
                            budget = float(row[3])  # Assuming budget is the same for all entries
                        except ValueError:
                            continue
        except FileNotFoundError:
            pass

        remaining = budget - total_spent

        self.total_spent_label.config(text=f"Total Spent: ${total_spent:.2f}")
        self.budget_label.config(text=f"Budget: ${budget:.2f}")
        self.remaining_label.config(text=f"Remaining: ${remaining:.2f}")

        # Apply burst effect for positive remaining budget
        if remaining > 0:
            self.apply_burst_effect()
        # Apply sad effect for loss
        elif remaining < 0:
            self.apply_sad_effect()

    def show_summary(self):
        self.summary_text.config(state=tk.NORMAL)
        self.summary_text.delete(1.0, tk.END)
        summary = defaultdict(float)
        try:
            with open("expenses.csv", "r", encoding="utf-8-sig") as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) == 4:
                        category = row[1]
                        amount_str = row[2]
                        try:
                            amount = float(amount_str)
                            summary[category] += amount
                        except ValueError:
                            continue
        except Exception as e:
            messagebox.showerror("File Error", f"An error occurred while showing summary: {e}")

        for category, total in summary.items():
            self.summary_text.insert(tk.END, f"{category}: ${total:.2f}\n")

        self.summary_text.config(state=tk.DISABLED)

    def reset_all(self):
        if messagebox.askyesno("Reset Confirmation", "Are you sure you want to reset all expenses? This action cannot be undone."):
            try:
                # Clear the CSV file
                open("expenses.csv", "w", encoding="utf-8-sig").close()
                # Clear the Listbox and reset labels
                self.expenses_listbox.delete(0, tk.END)
                self.budget_label.config(text="Budget: $0.00")
                self.total_spent_label.config(text="Total Spent: $0.00")
                self.remaining_label.config(text="Remaining: $0.00")
                self.summary_text.config(state=tk.NORMAL)
                self.summary_text.delete(1.0, tk.END)
                self.summary_text.config(state=tk.DISABLED)
                self.clear_entries()
                messagebox.showinfo("Reset Successful", "All expenses have been cleared. You can start fresh.")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while resetting: {e}")

    def apply_burst_effect(self):
        self.root.configure(bg="#ffeb3b")  # Change background to yellow for burst effect
        self.root.after(1000, lambda: self.root.configure(bg="#f0f0f0"))  # Revert background after 1 second

    def apply_sad_effect(self):
        self.root.configure(bg="#f44336")  # Change background to red for sad effect
        self.root.after(1000, lambda: self.root.configure(bg="#f0f0f0"))  # Revert background after 1 second

    def load_budget(self):
        self.budget_entry.delete(0, tk.END)
        try:
            with open("expenses.csv", "r", encoding="utf-8-sig") as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) == 4:
                        try:
                            budget = float(row[3])
                            self.budget_entry.insert(0, f"{budget:.2f}")
                        except ValueError:
                            continue
        except FileNotFoundError:
            pass

    def load_icon(self):
        try:
            img = Image.open("icon.png")  # Replace with your image file path
            img = img.resize((50, 50))  # Resize if necessary
            img_tk = ImageTk.PhotoImage(img)
            self.icon_label.config(image=img_tk)
            self.icon_label.image = img_tk  # Keep a reference to prevent garbage collection
        except FileNotFoundError:
            print("Error loading icon.")
        except Exception as e:
            print(f"Error loading icon: {e}")

    def blink_title(self):
        current_color = self.title_label.cget("fg")
        new_color = "#FF5733" if current_color == "#333" else "#333"
        self.title_label.config(fg=new_color)
        self.root.after(500, self.blink_title)  # Change color every 500ms

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    root.mainloop()




































