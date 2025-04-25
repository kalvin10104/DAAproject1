import tkinter as tk
from tkinter import messagebox

class Item:
    def __init__(self, name, profit, weight):
        self.name = name
        self.profit = profit
        self.weight = weight

def knapsack_max_profit(capacity, items):
    items.sort(key=lambda item: item.profit, reverse=True)
    total_profit = 0.0
    remaining_capacity = capacity
    selected_items = []

    for item in items:
        if remaining_capacity >= item.weight:
            remaining_capacity -= item.weight
            total_profit += item.profit
            selected_items.append((item.name, item.weight, item.profit))
        else:
            fraction = remaining_capacity / item.weight
            total_profit += item.profit * fraction
            selected_items.append((item.name, remaining_capacity, item.profit * fraction))
            break

    return total_profit, selected_items

class KnapsackApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Fractional Knapsack Problem")
        self.root.geometry("500x600")
        self.root.configure(bg="#e8f6f3")

        self.item_entries = []
        self.profit_entries = []
        self.weight_entries = []

        self.setup_ui()

    def setup_ui(self):
        tk.Label(self.root, text="Enter number of items:", font=("Arial", 12), bg="#e8f6f3").pack(pady=5)
        self.num_items_entry = tk.Entry(self.root, font=("Arial", 12))
        self.num_items_entry.pack(pady=5)

        tk.Button(self.root, text="Next", command=self.create_input_fields, bg="#2e86c1", fg="white", font=("Arial", 12)).pack(pady=5)

    def create_input_fields(self):
        try:
            self.num_items = int(self.num_items_entry.get())
            if self.num_items <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid positive number.")
            return

        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Shopping Bag", font=("Arial", 14, "bold"), bg="#e8f6f3").pack(pady=10)

        header = tk.Frame(self.root, bg="#e8f6f3")
        header.pack()
        tk.Label(header, text="Name", width=10, font=("Arial", 12), bg="#e8f6f3").grid(row=0, column=0)
        tk.Label(header, text="Value", width=10, font=("Arial", 12), bg="#e8f6f3").grid(row=0, column=1)
        tk.Label(header, text="Weight", width=10, font=("Arial", 12), bg="#e8f6f3").grid(row=0, column=2)

        self.item_entries.clear()
        self.profit_entries.clear()
        self.weight_entries.clear()

        for i in range(self.num_items):
            row = tk.Frame(self.root, bg="#e8f6f3")
            row.pack(pady=2)

            name_entry = tk.Entry(row, width=10, font=("Arial", 12))
            profit_entry = tk.Entry(row, width=10, font=("Arial", 12))
            weight_entry = tk.Entry(row, width=10, font=("Arial", 12))

            name_entry.grid(row=0, column=0)
            profit_entry.grid(row=0, column=1)
            weight_entry.grid(row=0, column=2)

            self.item_entries.append(name_entry)
            self.profit_entries.append(profit_entry)
            self.weight_entries.append(weight_entry)

        tk.Label(self.root, text="Enter Weight Capacity:", font=("Arial", 12), bg="#e8f6f3").pack(pady=10)
        self.capacity_entry = tk.Entry(self.root, font=("Arial", 12))
        self.capacity_entry.pack(pady=5)

        tk.Button(self.root, text="Calculate", command=self.calculate_knapsack, bg="#1e8449", fg="white", font=("Arial", 12)).pack(pady=10)
        tk.Button(self.root, text="Reset", command=self.reset, bg="#c0392b", fg="white", font=("Arial", 12)).pack(pady=5)

    def calculate_knapsack(self):
        items = []
        try:
            for i in range(self.num_items):
                name = self.item_entries[i].get() or f"Item {i+1}"
                profit = float(self.profit_entries[i].get())
                weight = float(self.weight_entries[i].get())
                if profit <= 0 or weight <= 0:
                    raise ValueError
                items.append(Item(name, profit, weight))
        except ValueError:
            messagebox.showerror("Input Error", "All profits and weights must be positive numbers.")
            return

        try:
            capacity = float(self.capacity_entry.get())
            if capacity <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid positive capacity.")
            return

        max_profit, selected_items = knapsack_max_profit(capacity, items)

        result_window = tk.Toplevel(self.root)
        result_window.title("Knapsack Result")
        result_window.configure(bg="#f0f8ff")
        result_window.geometry("500x400")

        title_label = tk.Label(
            result_window,
            text=f"\U0001F3AF Maximum Value: {max_profit:.2f}$",
            font=("Helvetica", 16, "bold"),
            fg="#1e8449",
            bg="#f0f8ff"
        )
        title_label.pack(pady=10)

        subtitle_label = tk.Label(
            result_window,
            text="\U0001F9BE Selected Items:",
            font=("Helvetica", 14, "bold"),
            fg="#2e86c1",
            bg="#f0f8ff"
        )
        subtitle_label.pack()

        text_frame = tk.Frame(result_window, bg="#f0f8ff")
        text_frame.pack(pady=10, fill="both", expand=True)

        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side="right", fill="y")

        text_widget = tk.Text(
            text_frame,
            wrap="word",
            font=("Courier New", 12),
            bg="#ffffff",
            fg="#000000",
            yscrollcommand=scrollbar.set
        )
        text_widget.pack(fill="both", expand=True)
        scrollbar.config(command=text_widget.yview)

        for name, used_weight, earned_profit in selected_items:
            text_widget.insert("end", f"\u2714\ufe0f {name} — Weight: {used_weight:.2f}kg, Value: {earned_profit:.2f}$\n")

        text_widget.config(state="disabled")

    def reset(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.item_entries = []
        self.profit_entries = []
        self.weight_entries = []
        self.setup_ui()

if __name__ == "__main__":
    root = tk.Tk()
    app = KnapsackApp(root)
    root.mainloop()
