import os
from tkinter import *
from tkinter import messagebox
import mysql.connector

# Class for Login Page
class Login_page:
    def __init__(self, root):
        # Initialize the root window
        self.root = root
        self.root.geometry("970x600")  # Set the window size
        self.root.title("Login Page")  # Set the title of the window
        self.root.resizable(False, False)  # Disable window resizing

        # Heading
        self.label = Label(self.root, text="ALWAYS FOR YOUR SERVICE", font=("Arial", 28, "bold"))
        self.label.pack(pady=20)  # Add padding above the heading

        # Background image
        self.bg = PhotoImage(file="booking.png")  # Load the background image
        self.bg_image = Label(self.root, image=self.bg).place(x=400, y=80)  # Set the position of the background

        # Create a frame for all form elements (left-aligned)
        button_frame = Frame(self.root)
        button_frame.pack(side="left", padx=20, pady=20)

        # Username label and entry field
        self.label_username = Label(button_frame, text="Username", font=("Arial", 12))
        self.label_username.pack(anchor="w")  # Align to the left
        self.userbox = Entry(button_frame, font=("Arial", 12), width=30)
        self.userbox.pack(pady=5, anchor="w")  # Add some padding

        # Password label and entry field
        self.label_password = Label(button_frame, text="Password", font=("Arial", 12))
        self.label_password.pack(anchor="w")

        # Create a frame for password entry and "Show Password" button
        password_frame = Frame(button_frame)
        password_frame.pack(pady=5, anchor="w")

        self.passwordbox = Entry(password_frame, font=("Arial", 12), show="*", width=30)  # Hide password input
        self.passwordbox.grid(row=0, column=0, padx=5)

        self.btn_show = Button(password_frame, text="Show Password", font=("Arial", 10))  # Button to toggle password visibility
        self.btn_show.grid(row=0, column=1)

        # Function to show and hide password
        def showpwd(event):
            self.passwordbox.config(show="")  # Show password
        def hidepwd(event):
            self.passwordbox.config(show="*")  # Hide password again

        # Bind button events for toggling password visibility
        self.btn_show.bind('<Button-1>', showpwd)
        self.btn_show.bind('<ButtonRelease-1>', hidepwd)

        # Login button
        self.button_signin = Button(button_frame, text="Log In", font=("Arial", 12), command=self.validinfo, width=15)
        self.button_signin.pack(pady=5, anchor="w")

        # Login as Driver button
        self.button_driver_signin = Button(button_frame, text="Log In as Driver", font=("Arial", 12), command=self.cmd, width=15)
        self.button_driver_signin.pack(pady=5, anchor="w")

        # Separator
        self.label_or = Label(button_frame, text="OR", font=("Arial", 12))
        self.label_or.pack(pady=10, anchor="w")

        # Sign-up section
        self.label_signup = Label(button_frame, text="Don't have an account? Sign up as:", font=("Arial", 12))
        self.label_signup.pack(pady=10, anchor="w")

        # Customer sign-up button
        self.button_customer_signup = Button(button_frame, text="Customer", font=("Arial", 12), command=self.nextPage, width=15)
        self.button_customer_signup.pack(pady=5, anchor="w")

        # Driver sign-up button
        self.button_driver_signup = Button(button_frame, text="Driver", font=("Arial", 12), command=self.next_page, width=15)
        self.button_driver_signup.pack(pady=5, anchor="w")

    # Admin login handling
    def admin(self):
        import Admin  # Import the Admin module
        self.root.withdraw()  # Hide the current window
        self.new = Toplevel()  # Create a new window
        self.obj = Admin.Admin_Dashboard(self.new)  # Open the admin dashboard

    # Validate user credentials
    def validinfo(self):
        username = self.userbox.get()
        passwd = self.passwordbox.get()

        # Ensure both username and password are provided
        if username == "" or passwd == "":
            messagebox.showerror("Error", "Please enter username and password.")
        # Admin credentials for demonstration
        elif username == "admin" and passwd == "admin":
            messagebox.showinfo("Welcome", "Welcome to the admin dashboard")
            self.admin()  # Open admin dashboard
        else:
            # Check database for user credentials
            try:
                conn = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="123456789",
                    database="booking"
                )
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM register WHERE email = %s AND password = %s", (username, passwd))
                data = cursor.fetchone()
                if data is None:  # No matching record found
                    messagebox.showerror("Error", "Incorrect username or password")
                else:  # Successful login
                    messagebox.showinfo("Welcome", f"Welcome {username}")
                    self.home_page(username)  # Navigate to the home page
                conn.close()
            except Exception as es:  # Handle database connection errors
                messagebox.showerror("Error", f"Error due to: {str(es)}")

    # Navigate to home page
    def home_page(self, username):
        self.root.destroy()  # Close the current window
        import Home  # Import the Home module
        self.new = Tk()
        reg = Home.Home_Page(self.new, username)  # Open the home page with user info

    # Navigate to customer sign-up page
    def nextPage(self):
        import Registration  # Import the Registration module
        os.system("Registration.py")  # Run the registration script
        self.root.destroy()  # Close the current window

    # Navigate to driver sign-up page
    def next_page(self):
        import Driver_Signup  # Import the Driver_Signup module
        os.system("Driver_signup.py")  # Run the driver sign-up script
        self.root.destroy()  # Close the current window

    # Navigate to driver login page
    def cmd(self):
        import Driver_Login  # Import the Driver_Login module
        os.system("Driver_Login.py")  # Run the driver login script
        # self.root.destroy()  # Uncomment if needed to close the current window


# Main execution starts here
if __name__ == "__main__":
    root = Tk()  # Create the main application window
    obj = Login_page(root)  # Initialize the login page
    root.mainloop()  # Run the application
