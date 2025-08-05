import tkinter as tk
from tkinter import messagebox, simpledialog
from datetime import datetime
import json

class HotelManagement:
    def __init__(self, root):
        self.root = root
        self.root.title("🏨 Hotel Management System")
        self.root.geometry("600x700")
        
        # Color Palette
        self.colors = {
            'primary': '#2C3E50',       # Dark blue-gray (primary color)
            'secondary': '#34495E',     # Slightly lighter blue-gray
            'accent': '#3498DB',        # Bright blue (for buttons)
            'light_bg': '#ECF0F1',      # Light gray (background)
            'highlight': '#E74C3C',     # Red (for important buttons)
            'text': '#2C3E50',          # Dark text
            'success': '#27AE60',       # Green (for success messages)
            'warning': '#F39C12'        # Orange (for warnings)
        }
        
        self.root.config(bg=self.colors['light_bg'])
        self.guests = []
        self.load_data()

        # Title Frame
        title_frame = tk.Frame(root, bg=self.colors['primary'])
        title_frame.pack(pady=10, fill="x")
        tk.Label(title_frame, text="Hotel Management System", font=("Helvetica", 20, "bold"), 
                bg=self.colors['primary'], fg="white").pack(pady=10)

        # Input Frame
        input_frame = tk.Frame(root, bg=self.colors['light_bg'])
        input_frame.pack(pady=10)

        # Guest Info
        self.name_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        self.room_var = tk.StringVar()
        self.room_num_var = tk.StringVar()

        label_style = {'font': ("Helvetica", 12), 'bg': self.colors['light_bg'], 'fg': self.colors['text']}
        entry_style = {'font': ("Helvetica", 12), 'highlightthickness': 1, 'highlightbackground': self.colors['secondary']}

        tk.Label(input_frame, text="Guest Name:", **label_style).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        tk.Entry(input_frame, textvariable=self.name_var, **entry_style).grid(row=0, column=1, padx=5, pady=5)

        tk.Label(input_frame, text="Phone Number:", **label_style).grid(row=1, column=0, sticky="w", padx=5, pady=5)
        tk.Entry(input_frame, textvariable=self.phone_var, **entry_style).grid(row=1, column=1, padx=5, pady=5)

        tk.Label(input_frame, text="Room Type:", **label_style).grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.room_menu = tk.OptionMenu(input_frame, self.room_var, "Single", "Double", "Deluxe", "Suite")
        self.room_menu.config(font=("Helvetica", 11), bg=self.colors['light_bg'], 
                            activebackground=self.colors['accent'], highlightthickness=0)
        self.room_var.set("Single")
        self.room_menu.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        tk.Label(input_frame, text="Room Number:", **label_style).grid(row=3, column=0, sticky="w", padx=5, pady=5)
        tk.Entry(input_frame, textvariable=self.room_num_var, **entry_style).grid(row=3, column=1, padx=5, pady=5)

        # Button Frame
        button_frame = tk.Frame(root, bg=self.colors['light_bg'])
        button_frame.pack(pady=10)

        button_style = {
            'font': ("Helvetica", 11, "bold"),
            'width': 12,
            'border': 0,
            'highlightthickness': 0,
            'activebackground': self.colors['secondary'],
            'fg': 'white'
        }

        tk.Button(button_frame, text="Check-In", command=self.check_in, 
                 bg=self.colors['success'], **button_style).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="Show Guests", command=self.show_guests, 
                 bg=self.colors['accent'], **button_style).grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="Check-Out", command=self.check_out, 
                 bg=self.colors['highlight'], **button_style).grid(row=0, column=2, padx=5)
        tk.Button(button_frame, text="Search", command=self.search_guest, 
                 bg=self.colors['warning'], **button_style).grid(row=1, column=0, pady=5)
        tk.Button(button_frame, text="Save Data", command=self.save_data, 
                 bg=self.colors['primary'], **button_style).grid(row=1, column=1, pady=5)
        tk.Button(button_frame, text="Clear", command=self.clear_fields, 
                 bg=self.colors['secondary'], **button_style).grid(row=1, column=2, pady=5)

        # Output Frame
        output_frame = tk.Frame(root, bg=self.colors['light_bg'])
        output_frame.pack(pady=10)

        self.output = tk.Text(output_frame, height=15, width=70, font=("Helvetica", 11),
                            bg='white', fg=self.colors['text'], relief='flat',
                            highlightbackground=self.colors['secondary'], highlightthickness=1)
        scrollbar = tk.Scrollbar(output_frame, command=self.output.yview)
        self.output.configure(yscrollcommand=scrollbar.set)
        
        self.output.grid(row=0, column=0)
        scrollbar.grid(row=0, column=1, sticky="ns")

    # [Rest of your methods remain exactly the same...]
    def check_in(self):
        name = self.name_var.get().strip()
        phone = self.phone_var.get().strip()
        room_type = self.room_var.get()
        room_num = self.room_num_var.get().strip()

        if not name:
            messagebox.showwarning("Invalid Input", "Please enter a valid name.")
            return
        if not phone.isdigit() or len(phone) < 10:
            messagebox.showwarning("Invalid Input", "Please enter a valid phone number (at least 10 digits).")
            return
        if not room_num:
            messagebox.showwarning("Invalid Input", "Please enter a room number.")
            return

        check_in_date = datetime.now().strftime("%Y-%m-%d %H:%M")
        guest = {
            "Name": name,
            "Phone": phone,
            "Room Type": room_type,
            "Room Number": room_num,
            "Check-in Date": check_in_date,
            "Check-out Date": ""
        }

        # Check if room is already occupied
        for g in self.guests:
            if g["Room Number"] == room_num and not g["Check-out Date"]:
                messagebox.showwarning("Room Occupied", f"Room {room_num} is already occupied by {g['Name']}.")
                return

        self.guests.append(guest)
        messagebox.showinfo("Success", f"{name} checked into {room_type} room {room_num}.")
        self.clear_fields()
        self.show_guests()

    def show_guests(self):
        self.output.delete(1.0, tk.END)
        if not self.guests:
            self.output.insert(tk.END, "No guests currently checked in.\n")
        else:
            self.output.insert(tk.END, "Current Guests:\n")
            self.output.insert(tk.END, "-"*70 + "\n")
            for i, g in enumerate(self.guests, 1):
                if not g["Check-out Date"]:  # Only show guests who haven't checked out
                    self.output.insert(tk.END, 
                        f"{i}. {g['Name']} | Phone: {g['Phone']}\n"
                        f"   Room: {g['Room Type']} ({g['Room Number']}) | Checked in: {g['Check-in Date']}\n"
                        f"{'-'*70}\n")

    def check_out(self):
        name = self.name_var.get().strip()
        if not name:
            messagebox.showwarning("Missing Info", "Please enter guest name to check out.")
            return
            
        for g in self.guests:
            if g["Name"].lower() == name.lower() and not g["Check-out Date"]:
                if messagebox.askyesno("Confirm", f"Check out {g['Name']} from {g['Room Type']} room {g['Room Number']}?"):
                    g["Check-out Date"] = datetime.now().strftime("%Y-%m-%d %H:%M")
                    messagebox.showinfo("Checked Out", f"{name} has been checked out.")
                    self.clear_fields()
                    self.show_guests()
                return
        
        messagebox.showwarning("Not Found", f"{name} not found in guest list or already checked out.")

    def search_guest(self):
        search_term = simpledialog.askstring("Search", "Enter guest name or phone number:")
        if search_term:
            self.output.delete(1.0, tk.END)
            found = False
            for g in self.guests:
                if (search_term.lower() in g['Name'].lower() or 
                    search_term in g['Phone']):
                    status = "Checked in" if not g["Check-out Date"] else "Checked out"
                    self.output.insert(tk.END, 
                        f"Name: {g['Name']} | Phone: {g['Phone']}\n"
                        f"Room: {g['Room Type']} ({g['Room Number']})\n"
                        f"Check-in: {g['Check-in Date']} | Status: {status}\n"
                        f"{'-'*70}\n")
                    found = True
            if not found:
                self.output.insert(tk.END, f"No guests found matching '{search_term}'.\n")

    def clear_fields(self):
        self.name_var.set("")
        self.phone_var.set("")
        self.room_var.set("Single")
        self.room_num_var.set("")

    def save_data(self):
        with open('guests.json', 'w') as f:
            json.dump(self.guests, f)
        messagebox.showinfo("Success", "Guest data saved successfully.")

    def load_data(self):
        try:
            with open('guests.json', 'r') as f:
                self.guests = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.guests = []

# Run the App
if __name__ == "__main__":
    root = tk.Tk()
    app = HotelManagement(root)
    root.mainloop()