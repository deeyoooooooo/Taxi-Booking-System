from tkinter import *  # Import all classes and functions from the Tkinter library for GUI.
from tkinter import messagebox  # Import messagebox to display pop-up messages.
import os  # Import os module for interacting with the operating system (like running other Python scripts).

# Define the Admin_Dashboard class
class Admin_Dashboard:
    def __init__(self, root):  # Constructor method to initialize the Admin Dashboard window
        self.root = root  # Reference to the main window
        self.root.geometry("800x500")  # Set the size of the window (width x height).
        self.root.resizable(False, False)  # Prevent resizing the window.
        self.root.title("Admin Dashboard")  # Set the title of the window.

        # Set a background image for the admin dashboard
        self.bg = PhotoImage(file="booking.png")  # Load the image file (make sure it exists in the same directory).
        self.bg_image = Label(self.root, image=self.bg).place(x=0, y=0)  # Place the image in the background.

        # Add a heading to the dashboard
        self.label = Label(self.root, text='Welcome to Admin Dashboard', font=('Arial', 20, 'bold'))
        self.label.place(x=250, y=1)  # Position the heading in the window.

        # Add a button for managing bookings
        self.button = Button(self.root, text="Manage Booking", font=('Arial', 15, 'bold'), command=self.cmd1)
        self.button.place(x=575, y=90)  # Place the button in the window.

        # Add a Logout button
        self.button = Button(self.root, text="Logout", font=('Arial', 20, 'bold'), command=self.cmd)
        self.button.place(x=600, y=425)  # Place the Logout button at the bottom-right corner.

        # Run the main GUI loop
        self.root.mainloop()

    # Method for handling the logout action
    def cmd(self):
        self.root.destroy()  # Close the current admin dashboard window.
        os.system("Login.py")  # Run the Login page (ensure the Login.py file exists in the same directory).

    # Method for handling the "Manage Booking" button
    def cmd1(self):
        self.root.destroy()  # Close the current admin dashboard window.
        os.system("python Manage.py")  # Run the Manage booking page (ensure Manage.py exists).

# Check if this script is being run directly (not imported)
if __name__ == '__main__':
    root = Tk()  # Create the main Tkinter window.
    obj = Admin_Dashboard(root)  # Create an instance of Admin_Dashboard with the main window.
    root.mainloop()  # Start the GUI event loop.
