from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import mysql.connector
from tkcalendar import DateEntry
from datetime import datetime

class TBS:
    # Constructor to initialize the booking page
    def __init__(self, root, username):
        self.root = root  # Main window (root) passed as parameter
        self.username = username  # Username passed as parameter
        self.root.geometry("700x450")  # Set window size
        self.root.title("Booking")  # Set window title
        self.root.resizable(False, False)  # Disable window resizing

        # Title label at the top of the window
        self.title = Label(self.root, text="Taxi Booking System", font=("Arial", 24, "bold"), bg="lightblue", fg="white")
        self.title.place(x=0, y=0, relwidth=1, height=50)  # Position the title label

        # Frame to contain the form fields
        self.frame = Frame(self.root, bg="white", bd=2, relief=RIDGE)
        self.frame.place(x=150, y=80, width=400, height=350)  # Position the frame

        # Customer Name Entry
        self.name_label = Label(self.frame, text='Name of Customer', font=('Arial', 12), bg="white")
        self.name_label.grid(row=0, column=0, padx=10, pady=10, sticky=W)  # Position label
        self.tf_name = Entry(self.frame, font=('Arial', 12))  # Input field for name
        self.tf_name.grid(row=0, column=1, padx=10, pady=10)  # Position input field

        # Pickup Location Entry
        self.pickup_label = Label(self.frame, text='Pick up location', font=('Arial', 12), bg="white")
        self.pickup_label.grid(row=1, column=0, padx=10, pady=10, sticky=W)  # Position label
        self.tf_pick = Entry(self.frame, font=('Arial', 12))  # Input field for pickup location
        self.tf_pick.grid(row=1, column=1, padx=10, pady=10)  # Position input field

        # Drop Location Entry
        self.drop_label = Label(self.frame, text='Drop location', font=('Arial', 12), bg="white")
        self.drop_label.grid(row=2, column=0, padx=10, pady=10, sticky=W)  # Position label
        self.tf_drop = Entry(self.frame, font=('Arial', 12))  # Input field for drop location
        self.tf_drop.grid(row=2, column=1, padx=10, pady=10)  # Position input field

        # Pickup Date Entry (using DateEntry widget from tkcalendar)
        self.date_label = Label(self.frame, text='Pick up date', font=('Arial', 12), bg="white")
        self.date_label.grid(row=3, column=0, padx=10, pady=10, sticky=W)  # Position label
        self.tf_date = DateEntry(self.frame, width=16, background="blue", foreground="white", bd=2, font=('Arial', 12))  # Date picker widget
        self.tf_date.grid(row=3, column=1, padx=10, pady=10)  # Position date picker widget

        # Pickup Time Entry
        self.time_label = Label(self.frame, text='Pick up time', font=('Arial', 12), bg="white")
        self.time_label.grid(row=4, column=0, padx=10, pady=10, sticky=W)  # Position label
        self.tf_time = Entry(self.frame, font=('Arial', 12))  # Input field for pickup time
        self.tf_time.grid(row=4, column=1, padx=10, pady=10)  # Position input field

        # Booking Button (to request a booking)
        self.book_button = Button(self.frame, text="Request Booking", command=self.valid__info, font=("Arial", 12),
                                  bg="green", fg="white", cursor="hand2")  # Button to initiate booking
        self.book_button.grid(row=5, column=0, columnspan=2, pady=10, ipadx=5)  # Position button

        # Back Button (to go back to the home page)
        self.back_button = Button(self.frame, text="Back", command=self.cmd, font=("Arial", 12),
                                  bg="red", fg="white", cursor="hand2")  # Button to go back to the home page
        self.back_button.grid(row=6, column=0, columnspan=2, pady=10, ipadx=5)  # Position button

    # Method to validate the user input and proceed with booking
    def valid__info(self):
        # Get the values from the input fields
        name = self.tf_name.get()
        pickuplocation = self.tf_pick.get()
        droplocation = self.tf_drop.get()
        date = self.tf_date.get_date()
        time = self.tf_time.get()

        # Check if any required fields are empty
        if not all([name, pickuplocation, droplocation, time]):
            messagebox.showerror("Error", "All fields must be filled!")  # Show error message
            return

        # Get the current date and time to compare against the user's selected date and time
        current_datetime = datetime.now()

        # Combine the selected date and time into a single datetime object
        pickup_datetime_str = f"{date.strftime('%Y-%m-%d')} {time}"
        try:
            pickup_datetime = datetime.strptime(pickup_datetime_str, "%Y-%m-%d %H:%M")  # Convert string to datetime object
        except ValueError:
            messagebox.showerror("Error", "Invalid time format! Please enter a valid time.")  # Handle invalid time format
            return

        # Check if the selected time is in the past
        if pickup_datetime < current_datetime:
            messagebox.showerror("Error", "Cannot book for a past date or time!")  # Show error if time is in the past
            return

        # Proceed with booking if all checks pass
        try:
            formatted_date = date.strftime('%Y-%m-%d')  # Format the date for database insertion
            # Connect to MySQL database
            conn = mysql.connector.connect(host="localhost", user="root", password="123456789", database="booking")
            cursor = conn.cursor()

            # Fetch the customer ID based on the provided username
            cursor.execute("SELECT id FROM register WHERE email=%s", (self.username,))
            result = cursor.fetchone()

            # If no user found, show error
            if not result:
                messagebox.showerror("Error", "User not found!")
                return

            cust_id = result[0]  # Extract the customer ID from the result

            # Insert the booking information into the database
            cursor.execute(
                "INSERT INTO book_customer (name, pickbox, dropbox, datebox, timebox, status, id) VALUES (%s, %s, %s, %s, %s, 'Pending', %s)",
                (name, pickuplocation, droplocation, formatted_date, time, cust_id))  # Insert data into the database
            conn.commit()  # Commit the transaction
            conn.close()  # Close the database connection

            # Show success message after booking is completed
            messagebox.showinfo("Success", "Booking successful!")
        except Exception as e:
            # Handle any errors during the booking process
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    # Method to navigate back to the home page
    def cmd(self):
        self.root.destroy()  # Close the current window
        import Home  # Import the Home module
        self.new = Tk()  # Create a new Tkinter window
        reg = Home.Home_Page(self.new, username=self.username)  # Create an instance of the Home_Page class

# Example usage
if __name__ == "__main__":
    root = Tk()  # Create the main Tkinter window
    app = TBS(root, username="test@example.com")  # Create an instance of the TBS class
    root.mainloop()  # Run the Tkinter mainloop to keep the application running
