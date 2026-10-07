import os
from tkinter import *
from tkinter import messagebox
from tkinter import PhotoImage
import mysql.connector

# LoginPage class handles the driver login functionality
class LoginPage:
    def __init__(self):
        self.root = Tk()
        self.root.geometry("600x400")  # Set the window size to 600x400
        self.root.resizable(False, False)  # Disable resizing
        self.root.title("Driver Login")  # Set the window title
        self.root.configure(background="light blue")  # Set background color

        # **Heading Section**
        self.label = Label(self.root, text="DRIVE SAFE", font=("Arial", 24, "bold"), bg="#F44336", fg="white")
        self.label.pack(pady=20)

        # **Username Entry**
        self.label_username = Label(self.root, text="Username (License Number)", font=("Arial", 12), bg="light gray")
        self.label_username.pack(pady=10)

        # Entry field for the username
        self.userbox = Entry(self.root, font=("Arial", 12), width=30, bd=2, relief=GROOVE)
        self.userbox.pack()

        # **Password Entry**
        self.label_password = Label(self.root, text="Password", font=("Arial", 12), bg="light gray")
        self.label_password.pack(pady=10)

        # Frame to hold password field and "Show Password" button
        password_frame = Frame(self.root, bg="#FFFFFF")
        password_frame.pack(pady=5)

        self.passwordbox = Entry(password_frame, font=("Arial", 12), show="*", width=25, bd=2, relief=GROOVE)
        self.passwordbox.grid(row=0, column=0, padx=5)

        # **Show Password Button**
        self.btn_show = Button(password_frame, text="Show Password", font=("Arial", 10), bg="#0288D1", fg="white",
                               activebackground="#03A9F4", activeforeground="white", cursor="hand2")
        self.btn_show.grid(row=0, column=1)

        # Event binding for "Show Password" button
        def showpwd(event):
            self.passwordbox.config(show="")  # Show the password text

        def hidepwd(event):
            self.passwordbox.config(show="*")  # Hide the password text

        # Bind mouse events to toggle password visibility
        self.btn_show.bind('<Button-1>', showpwd)  # Show password on press
        self.btn_show.bind('<ButtonRelease-1>', hidepwd)  # Hide password on release

        # **Sign In Button**
        self.button_signin = Button(self.root, text="Sign In", font=("Arial", 12), bg="#388E3C", fg="white",
                                    activebackground="#4CAF50", activeforeground="white", cursor="hand2",
                                    command=self.validinfo, width=15)
        self.button_signin.pack(pady=10)

        # **Back Button**
        self.button_back = Button(self.root, text="Back", font=("Arial", 12), bg="#F44336", fg="white",
                                  activebackground="#FF5252", activeforeground="white", cursor="hand2",
                                  command=self.cmd, width=15)
        self.button_back.pack(pady=10)

        self.root.mainloop()  # Start the Tkinter main loop

    # Validate login credentials
    def validinfo(self):
        username = self.userbox.get()  # Get the entered username
        passwd = self.passwordbox.get()  # Get the entered password

        # Check if either username or password is empty
        if username == "" or passwd == "":
            messagebox.showerror("Error", "Please enter both username (license number) and password.")
            return

        try:
            # Connect to the database
            conn = mysql.connector.connect(host="localhost",
                                           user="root",
                                           password="123456789",
                                           database="booking")
            cursor = conn.cursor()

            # Query to check if the username and password exist
            cursor.execute("SELECT * FROM driver WHERE name = %s AND password = %s", (username, passwd))
            data = cursor.fetchone()  # Fetch one record

            if data is None:  # If no matching record is found
                messagebox.showerror("Error", "Incorrect username or password.", parent=self.root)
            else:  # If login is successful
                messagebox.showinfo("Welcome", f"Welcome {username}", parent=self.root)
                self.Driver_dashboard(username)  # Redirect to the driver dashboard

            conn.close()  # Close the database connection

        # Handle database-related errors
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        # Handle other exceptions
        except Exception as es:
            messagebox.showerror("Error", f"An error occurred: {str(es)}")

    # Open the driver dashboard after successful login
    def Driver_dashboard(self, username):
        self.root.destroy()  # Close the login window
        import Driver_dashboard  # Import the driver dashboard module
        self.new = Tk()
        reg = Driver_dashboard.driver(self.new, username)  # Pass the username to the dashboard

    # Return to the main menu (or previous screen)
    def cmd(self):
        self.root.destroy()  # Close the current window
        os.system("Login.py")  # Open the main login page

# Initialize and run the LoginPage
LoginPage()
