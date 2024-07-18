import calendar
import tkinter as tk
from tkinter import messagebox, simpledialog
from tkcalendar import Calendar
from datetime import datetime

# Reminder Manager Class
class ReminderManager:
    def __init__(self, filename):
        self.filename = filename
        self.reminders = self.load_reminders()

    def load_reminders(self):
        try:
            with open(self.filename, 'r') as file:
                return [line.strip().split(',') for line in file.readlines()]
        except FileNotFoundError:
            return []

    def save_reminders(self):
        with open(self.filename, 'w') as file:
            for reminder in self.reminders:
                file.write(','.join(reminder) + '\n')

    def add_reminder(self, date, description):
        self.reminders.append([date, description])
        self.save_reminders()

    def get_reminders(self):
        return self.reminders

    def edit_reminder(self, index, date, description):
        if 0 <= index < len(self.reminders):
            self.reminders[index] = [date, description]
            self.save_reminders()

# GUI Application Class
class CalendarApp:
    def __init__(self, root, reminder_manager):
        self.root = root
        self.reminder_manager = reminder_manager
        self.root.title("Calendar Reminder App")
        
        # Display the calendar
        self.calendar_label = tk.Label(root, text="", font=("Courier", 12))
        self.calendar_label.pack()
        
        # Date picker
        tk.Label(root, text="Select Date").pack()
        self.cal = Calendar(root, selectmode='day', year=datetime.now().year, month=datetime.now().month)
        self.cal.pack()
        
        # Add reminder section
        tk.Label(root, text="Description").pack()
        self.description_entry = tk.Entry(root)
        self.description_entry.pack()
        
        add_button = tk.Button(root, text="Add Reminder", command=self.add_reminder)
        add_button.pack()
        
        # Reminder list section
        self.reminder_frame = tk.Frame(root)
        self.reminder_frame.pack()
        
        # Display calendar and reminders
        self.display_calendar(datetime.now().year, datetime.now().month)
        self.list_reminders()

    def display_calendar(self, year, month):
        cal_str = calendar.month(year, month)
        self.calendar_label.config(text=cal_str)

    def list_reminders(self):
        for widget in self.reminder_frame.winfo_children():
            widget.destroy()
            
        tk.Label(self.reminder_frame, text="Upcoming Reminders").pack()
        
        for i, (date, description) in enumerate(self.reminder_manager.get_reminders()):
            reminder_container = tk.Frame(self.reminder_frame)
            reminder_container.pack(fill='x', expand=True)
            
            reminder_label = tk.Label(reminder_container, text=f"{date}: {description}")
            reminder_label.pack(side=tk.LEFT)
            
            edit_button = tk.Button(reminder_container, text="Edit", command=lambda i=i: self.edit_reminder(i))
            edit_button.pack(side=tk.RIGHT)
    def add_reminder(self):
        date = self.cal.get_date()
        
        # Convert date to YYYY-MM-DD format
        formatted_date = datetime.strptime(date, '%m/%d/%y').strftime('%Y-%m-%d')
        
        description = self.description_entry.get()
        
        if description:
            self.reminder_manager.add_reminder(formatted_date, description)
            messagebox.showinfo("Success", "Reminder added successfully!")
            self.description_entry.delete(0, tk.END)
            self.list_reminders()
        else:
            messagebox.showerror("Error", "Please enter a description for the reminder.")

    def edit_reminder(self, index):
        current_date, current_description = self.reminder_manager.get_reminders()[index]
        new_date = simpledialog.askstring("Edit Date", "Enter new date (YYYY-MM-DD):", initialvalue=current_date)
        new_description = simpledialog.askstring("Edit Description", "Enter new description:", initialvalue=current_description)

        if new_date and new_description:
            try:
                # Validate and format the date
                datetime.strptime(new_date, '%Y-%m-%d')
                self.reminder_manager.edit_reminder(index, new_date, new_description)
                messagebox.showinfo("Success", "Reminder updated successfully!")
                self.list_reminders()
            except ValueError:
                messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD.")

# Main function to run the application
def main():
    filename = "reminders.txt"
    reminder_manager = ReminderManager(filename)
    
    root = tk.Tk()
    app = CalendarApp(root, reminder_manager)
    root.mainloop()

if __name__ == "__main__":
    main()

        