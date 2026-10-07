import os
from tkinter import *
from tkinter import messagebox


class Home_Page:
    # Constructor to initialize the homepage
    def __init__(self, root, username):
        self.root = root  # Main window (root) passed as parameter
        self.username = username  # Username passed as parameter
        self.root.geometry("600x400")  # Set the window size
        self.root.resizable(False, False)  # Disable window resizing
        self.root.title("Customer Dashboard")  # Set window title

        # Gradient-like Background (top and bottom sections)
        self.bg_top = Label(self.root, bg="#4A90E2", width=600, height=15)  # Top background
        self.bg_top.place(x=0, y=0)  # Positioning top background
        self.bg_bottom = Label(self.root, bg="#50E3C2", width=600, height=25)  # Bottom background
        self.bg_bottom.place(x=0, y=200)  # Positioning bottom background

        # Title Label (Header)
        self.title = Label(self.root, text="Welcome to the Customer Dashboard", font=("Arial", 16, "bold"),
                           bg="#4A90E2", fg="white")  # Set font, background, and foreground colors
        self.title.place(x=0, y=10, relwidth=1, height=40)  # Position title at the top of the window

        # Buttons Frame (Containing all buttons)
        self.button_frame = Frame(self.root, bg="#FFFFFF", bd=2, relief=GROOVE)  # A frame for buttons
        self.button_frame.place(x=200, y=100, width=200, height=180)  # Position the frame

        # View Booking Button
        self.view_booking_button = Button(self.button_frame, text="View Booking", font=('Arial', 12, 'bold'),
                                          bg="#44BD32", fg="white", cursor="hand2", command=self.cmd2)  # Button to view booking
        self.view_booking_button.pack(fill=X, pady=10, padx=10)  # Pack the button in the frame

        # Book a Ride Button
        self.booking_button = Button(self.button_frame, text="Book a Ride", font=('Arial', 12, 'bold'),
                                     bg="#F39C12", fg="white", cursor="hand2", command=self.cmd1)  # Button to book a ride
        self.booking_button.pack(fill=X, pady=10, padx=10)  # Pack the button in the frame

        # Back Button (to go back to the login page)
        self.back_button = Button(self.button_frame, text="Back", font=('Arial', 12, 'bold'),
                                  bg="#E74C3C", fg="white", cursor="hand2", command=self.cmd)  # Button to go back
        self.back_button.pack(fill=X, pady=10, padx=10)  # Pack the button in the frame

        # Footer Label
        self.footer = Label(self.root, text="Thank you for using our service!", font=("Arial", 10),
                            bg="#50E3C2", fg="white")  # Footer text
        self.footer.place(x=0, y=370, relwidth=1, height=30)  # Position footer at the bottom of the window

        # Start the Tkinter mainloop to run the application
        self.root.mainloop()

    # Command to go back to the login page
    def cmd(self):
        self.root.destroy()  # Close the current window
        os.system("Login.py")  # Run the Login.py script

    # Command to open the booking page
    def cmd1(self):
        self.root.destroy()  # Close the current window
        import Booking  # Import the Booking module
        self.new = Tk()  # Create a new Tkinter window
        obj = Booking.TBS(self.new, username=self.username)  # Create an instance of the Booking class

    # Command to view existing bookings
    def cmd2(self):
        self.root.destroy()  # Close the current window
        import demo  # Import the demo module
        self.new = Tk()  # Create a new Tkinter window
        obj = demo.Booking(self.new, username=self.username)  # Create an instance of the demo.Booking class

    # Command to go back to the login page (duplicate of the first cmd method)
    def cmd(self):
        self.root.destroy()  # Close the current window
        import Login  # Import the Login module
        self.new = Tk()  # Create a new Tkinter window
        reg = Login.Login_page(self.new)  # Create an instance of the Login_page class


# Example usage (to run the program)
if __name__ == "__main__":
    root = Tk()  # Create the main Tkinter window
    app = Home_Page(root, username="test@example.com")  # Create an instance of Home_Page
    root.mainloop()  # Run the Tkinter mainloop to keep the application running
