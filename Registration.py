from tkinter import *
import mysql.connector
from tkinter import messagebox
import os

class Register:
    def __init__(self):
        # Initialize the main window (root)
        self.root = Tk()
        self.root.geometry("500x400")
        self.root.resizable(False, False)  # Disable window resizing
        self.root.title("Customer Signup")

        # Background color for the main window
        self.root.configure(bg="#f0f8ff")

        # Heading Frame
        self.heading_frame = Frame(self.root, bg="#4682B4", relief=FLAT)
        self.heading_frame.place(x=0, y=0, relwidth=1, height=60)
        self.heading_label = Label(
            self.heading_frame,
            text="Welcome to Online Taxi Service",
            font=('Arial', 18, 'bold'),
            bg="#4682B4",
            fg="white"
        )
        self.heading_label.pack(pady=10)

        # Form Fields Frame
        self.form_frame = Frame(self.root, bg="#f0f8ff")
        self.form_frame.place(x=50, y=80, width=400, height=250)

        # Full Name field
        Label(self.form_frame, text="Full Name:", font=('Arial', 12), bg="#f0f8ff").grid(row=0, column=0, pady=5, sticky=W)
        self.namebox = Entry(self.form_frame, font=('Arial', 12), bg="white")
        self.namebox.grid(row=0, column=1, pady=5, padx=10, sticky=E)

        # Address field
        Label(self.form_frame, text="Address:", font=('Arial', 12), bg="#f0f8ff").grid(row=1, column=0, pady=5, sticky=W)
        self.addressbox = Entry(self.form_frame, font=('Arial', 12), bg="white")
        self.addressbox.grid(row=1, column=1, pady=5, padx=10, sticky=E)

        # Email field
        Label(self.form_frame, text="Email Address:", font=('Arial', 12), bg="#f0f8ff").grid(row=2, column=0, pady=5, sticky=W)
        self.emailbox = Entry(self.form_frame, font=('Arial', 12), bg="white")
        self.emailbox.grid(row=2, column=1, pady=5, padx=10, sticky=E)

        # Mobile Number field
        Label(self.form_frame, text="Mobile Number:", font=('Arial', 12), bg="#f0f8ff").grid(row=3, column=0, pady=5, sticky=W)
        self.mobilebox = Entry(self.form_frame, font=('Arial', 12), bg="white")
        self.mobilebox.grid(row=3, column=1, pady=5, padx=10, sticky=E)

        # Password field
        Label(self.form_frame, text="Password:", font=('Arial', 12), bg="#f0f8ff").grid(row=4, column=0, pady=5, sticky=W)
        self.passwordbox = Entry(self.form_frame, show="*", font=('Arial', 12), bg="white")
        self.passwordbox.grid(row=4, column=1, pady=5, padx=10, sticky=E)

        # Buttons Frame
        self.button_frame = Frame(self.root, bg="#f0f8ff")
        self.button_frame.place(x=150, y=350, width=200, height=50)

        # Sign Up button
        self.signup_button = Button(
            self.button_frame,
            text="Sign Up",
            font=('Arial', 12, 'bold'),
            bg="#32CD32",
            fg="white",
            cursor="hand2",
            command=self.Connect_info  # Call Connect_info() method when clicked
        )
        self.signup_button.grid(row=0, column=0, padx=5)

        # Back button
        self.back_button = Button(
            self.button_frame,
            text="Back",
            font=('Arial', 12, 'bold'),
            bg="#DC143C",
            fg="white",
            cursor="hand2",
            command=self.cmd  # Call cmd() method to go back when clicked
        )
        self.back_button.grid(row=0, column=1, padx=5)

        # Start the Tkinter mainloop to run the application
        self.root.mainloop()

    def Connect_info(self):
        # Check if all fields are filled
        if self.namebox.get() == "" or self.passwordbox.get() == "" or self.addressbox.get() == "" or self.emailbox.get() == "" or self.mobilebox.get() == "":
            messagebox.showerror("Error", "Please fill in all the information.")  # Show error if any field is empty
        else:
            try:
                # Connect to the MySQL database
                conn = mysql.connector.connect(
                    host="localhost", user="root", password="123456789", database="booking"
                )
                cursor = conn.cursor()

                # Check if the email already exists
                cursor.execute("SELECT * FROM register WHERE email = %s", (self.emailbox.get(),))
                if cursor.fetchone():
                    messagebox.showerror("Error", "Email already exists. Please try a different one.")
                else:
                    # Insert new registration details into the database
                    cursor.execute(
                        "INSERT INTO register (name, address, email, contact, password) VALUES (%s, %s, %s, %s, %s)",
                        (
                            self.namebox.get(),
                            self.addressbox.get(),
                            self.emailbox.get(),
                            self.mobilebox.get(),
                            self.passwordbox.get(),
                        ),
                    )
                    conn.commit()  # Commit the changes to the database
                    conn.close()  # Close the database connection
                    messagebox.showinfo("Success", "Registration successful!")  # Show success message
                    self.root.destroy()  # Close the current window
                    import Login  # Import the login module for the next step

            except mysql.connector.Error as err:
                # Show error message if there is a database-related error
                messagebox.showerror("Error", f"Database error: {err}")
            except Exception as e:
                # Show a generic error message if an exception occurs
                messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def cmd(self):
        # Close the current window and return to the login page
        self.root.destroy()
        os.system("Login.py")  # Open the login page

# Run the application
Register()  # Create an instance of the Register class to start the application
