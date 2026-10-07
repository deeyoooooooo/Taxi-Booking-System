from tkinter import *
from tkinter import messagebox
import mysql.connector
import os

# Driver class handles the Driver Registration form
class Driver:
    def __init__(self):
        # Initialize the main window for the Driver Signup form
        self.root = Tk()
        self.root.geometry("600x450")  # Set window size to 600x450
        self.root.resizable(False, False)  # Disable resizing
        self.root.title("Driver Signup")  # Set the window title

        # Background Color
        self.root.configure(bg="#f7f7f7")  # Set background color to light gray

        # Header Label
        # A label with "Driver Registration" text is created for the top header.
        self.header = Label(self.root, text="Driver Registration", font=("Arial", 18, "bold"), bg="#007BFF", fg="white")
        self.header.place(x=0, y=0, relwidth=1, height=50)  # Place header at the top of the window

        # Full Name Label and Input Field
        Label(self.root, text="Full Name:", font=("Arial", 12), bg="#f7f7f7").place(x=50, y=80)  # Label for Name field
        self.namebox = Entry(self.root, font=("Arial", 12), bd=2, relief=GROOVE)  # Input field for Name
        self.namebox.place(x=250, y=80, width=250)  # Position the name input field

        # Citizenship Number Label and Input Field
        Label(self.root, text="Citizenship Number:", font=("Arial", 12), bg="#f7f7f7").place(x=50, y=130)  # Label for Citizenship field
        self.citizenbox = Entry(self.root, font=("Arial", 12), bd=2, relief=GROOVE)  # Input field for Citizenship Number
        self.citizenbox.place(x=250, y=130, width=250)  # Position the citizenship input field

        # License Number Label and Input Field
        Label(self.root, text="License Number:", font=("Arial", 12), bg="#f7f7f7").place(x=50, y=180)  # Label for License field
        self.licensebox = Entry(self.root, font=("Arial", 12), bd=2, relief=GROOVE)  # Input field for License Number
        self.licensebox.place(x=250, y=180, width=250)  # Position the license input field

        # Password Label and Input Field
        Label(self.root, text="Password:", font=("Arial", 12), bg="#f7f7f7").place(x=50, y=230)  # Label for Password field
        self.passwordbox = Entry(self.root, font=("Arial", 12), bd=2, relief=GROOVE, show="*")  # Input field for Password (hidden text)
        self.passwordbox.place(x=250, y=230, width=250)  # Position the password input field

        # Contact Number Label and Input Field
        Label(self.root, text="Contact Number:", font=("Arial", 12), bg="#f7f7f7").place(x=50, y=280)  # Label for Contact field
        self.contactbox = Entry(self.root, font=("Arial", 12), bd=2, relief=GROOVE)  # Input field for Contact Number
        self.contactbox.place(x=250, y=280, width=250)  # Position the contact input field

        # Register Button
        # The Register button triggers the Connect_info method to handle registration
        self.register_button = Button(self.root, text="Register", font=("Arial", 12, "bold"), bg="#28a745", fg="white",
                                      cursor="hand2", command=self.Connect_info)  # Register button with green background
        self.register_button.place(x=150, y=350, width=100)  # Position the button on the window

        # Back Button
        # The Back button takes the user back to the Login page
        self.back_button = Button(self.root, text="Back", font=("Arial", 12, "bold"), bg="#dc3545", fg="white",
                                   cursor="hand2", command=self.cmd)  # Back button with red background
        self.back_button.place(x=300, y=350, width=100)  # Position the back button on the window

        # Mainloop to run the Tkinter application
        self.root.mainloop()

    def Connect_info(self):
        # Validate if all the fields are filled before submitting
        if (
            self.namebox.get() == ""
            or self.passwordbox.get() == ""
            or self.citizenbox.get() == ""
            or self.licensebox.get() == ""
            or self.contactbox.get() == ""
        ):
            # If any field is empty, show an error message
            messagebox.showerror("Error", "Please fill in all the information.")
        else:
            try:
                # Connect to the MySQL database
                conn = mysql.connector.connect(
                    host="localhost", user="root", password="123456789", database="booking"
                )
                cursor = conn.cursor()  # Create a cursor to interact with the database

                # SQL query to insert driver information into the 'driver' table
                cursor.execute(
                    "INSERT INTO driver (name, citizen, license, password, contact, driver_status) VALUES (%s, %s, %s, %s, %s, %s)",
                    (
                        self.namebox.get(),  # Name from the input field
                        self.citizenbox.get(),  # Citizenship Number from the input field
                        self.licensebox.get(),  # License Number from the input field
                        self.passwordbox.get(),  # Password from the input field
                        self.contactbox.get(),  # Contact Number from the input field
                        "Available",  # Default driver status is "Available"
                    ),
                )

                # Commit the transaction to save the data in the database
                conn.commit()
                conn.close()  # Close the database connection
                messagebox.showinfo("Success", "Driver registered successfully!")  # Show success message
                self.root.destroy()  # Close the registration window
                import Driver_Login  # Import the driver login page

            except mysql.connector.Error as err:
                # Handle any database connection errors
                messagebox.showerror("Database Error", f"Error: {err}")
            except Exception as e:
                # Handle any other exceptions
                messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def cmd(self):
        # The cmd method is called when the "Back" button is pressed
        import Login  # Import the Login script
        os.system("Login.py")  # Open the Login window
        self.root.destroy()  # Close the Driver Signup window

# Create an instance of the Driver class to run the program
Driver()
