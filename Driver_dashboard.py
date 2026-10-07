import os
from tkinter import *
from tkinter import ttk, messagebox
import mysql.connector

class driver:

    def __init__(self, root, username):
        # Initialize the main window (driver dashboard) with root window and username passed from the login screen
        self.root = root
        self.username = username
        self.root.geometry("800x600")  # Set window size
        self.root.title("Driver Dashboard")  # Set window title
        self.root.resizable(True, True)  # Allow window resizing

        # Frame for displaying completed trips
        self.frame = Frame(self.root, bg="white", bd=2, relief=SOLID)
        self.frame.place(x=50, y=300, width=700, height=250)

        # Title for completed trips frame
        frame_title = Label(
            self.frame,
            text="Completed Trips",  # Title text
            font=("Arial", 14, "bold"),
            bg="white",
            fg="#333333"
        )
        frame_title.pack(side=TOP, fill=X, pady=10)

        # Scrollbars for the table
        scroll_x = Scrollbar(self.frame, orient=HORIZONTAL)
        scroll_y = Scrollbar(self.frame, orient=VERTICAL)
        
        # Table for displaying completed trips with columns: id, name, pickup_location, etc.
        self.user_table = ttk.Treeview(self.frame, columns=("id", "name", "pickup_location", "drop_address", "date", "time", "status"), xscrollcommand=scroll_x.set)
        scroll_x.pack(side=BOTTOM, fill=X)  # Bottom scrollbar
        scroll_y.pack(side=RIGHT, fill=Y)  # Right scrollbar
        scroll_x.config(command=self.user_table.xview)
        scroll_y.config(command=self.user_table.yview)

        # Define headers for the table
        self.user_table.heading("id", text="Id")
        self.user_table.heading("name", text="Name")
        self.user_table.heading("pickup_location", text="Pickup Location")
        self.user_table.heading("drop_address", text="Drop address")
        self.user_table.heading("date", text="Date")
        self.user_table.heading("time", text="Time")
        self.user_table.heading("status", text="Status")

        # Set columns to be displayed
        self.user_table['show'] = 'headings'
        self.user_table.column("id", width=100, anchor=CENTER)
        self.user_table.column("name", width=100, anchor=CENTER)
        self.user_table.column("pickup_location", width=100, anchor=CENTER)
        self.user_table.column("drop_address", width=100, anchor=CENTER)
        self.user_table.column("date", width=100, anchor=CENTER)
        self.user_table.column("time", width=100, anchor=CENTER)
        self.user_table.column("status", width=100, anchor=CENTER)

        self.user_table.pack(fill=BOTH, expand=3)  # Pack the table into the frame
        self.fetch_data01()  # Fetch completed trips from the database

        # Frame for displaying assigned trips
        self.frame2 = Frame(self.root, bg="white", bd=2, relief=SOLID)
        self.frame2.place(x=50, y=50, width=700, height=200)

        # Title for assigned trips frame
        frame2_title = Label(
            self.frame2,
            text="Assigned Trips",  # Title text
            font=("Arial", 14, "bold"),
            bg="white",
            fg="#333333"
        )
        frame2_title.pack(side=TOP, fill=X, pady=10)

        # Scrollbars for the table
        scroll_x = Scrollbar(self.frame2, orient=HORIZONTAL)
        scroll_y = Scrollbar(self.frame2, orient=VERTICAL)

        # Table for displaying assigned trips
        self.user_table01 = ttk.Treeview(self.frame2, columns=("id", "name", "pickup_location", "drop_address", "date", "time", "status"), xscrollcommand=scroll_x.set)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.user_table01.xview)
        scroll_y.config(command=self.user_table01.yview)

        # Define headers for the assigned trips table
        self.user_table01.heading("id", text="Id")
        self.user_table01.heading("name", text="Name")
        self.user_table01.heading("pickup_location", text="Pickup Location")
        self.user_table01.heading("drop_address", text="Drop address")
        self.user_table01.heading("date", text="Date")
        self.user_table01.heading("time", text="Time")
        self.user_table01.heading("status", text="Status")

        # Set columns to be displayed
        self.user_table01['show'] = 'headings'
        self.user_table01.column("id", width=100, anchor=CENTER)
        self.user_table01.column("name", width=100, anchor=CENTER)
        self.user_table01.column("pickup_location", width=100, anchor=CENTER)
        self.user_table01.column("drop_address", width=100, anchor=CENTER)
        self.user_table01.column("date", width=100, anchor=CENTER)
        self.user_table01.column("time", width=100, anchor=CENTER)
        self.user_table01.column("status", width=100, anchor=CENTER)

        self.user_table01.pack(fill=BOTH, expand=3)  # Pack the table into the frame
        self.fetch_data()  # Fetch assigned trips from the database

        # Back button to return to the previous screen
        self.button_back = Button(
            self.root,
            text="Back",
            font=("Arial", 10, "bold"),
            bg="#FF6347",  # Tomato color for visibility
            fg="white",
            activebackground="#FF4500",  # Darker shade on hover
            activeforeground="white",
            bd=2,
            relief=RAISED,
            command=self.cmd
        )
        self.button_back.place(x=720, y=10, width=80, height=30)

        # Trip completed button to mark a trip as completed
        self.button_complete = Button(
            self.root,
            text="Trip Completed",
            font=("Arial", 10, "bold"),
            bg="#32CD32",  # Lime green for positive action
            fg="white",
            activebackground="#228B22",  # Darker shade on hover
            activeforeground="white",
            bd=2,
            relief=RAISED,
            command=self.complete_data
        )
        self.button_complete.place(x=10, y=10, width=150, height=30)

        self.root.mainloop()

    def fetch_data(self):
        # Fetch assigned trips (status 'Active') from the database
        conn = mysql.connector.connect(host="localhost", user="root", password="123456789", database="booking")
        cursor = conn.cursor()

        cursor.execute("select * from driver where name=%s", (self.username,))  # Get driver ID based on username
        driver_id = cursor.fetchone()[0]

        cursor.execute("SELECT * FROM book_customer where driverid =%s and status ='Active'", (driver_id,))
        rows = cursor.fetchall()
        if len(rows) != 0:
            self.user_table01.delete(*self.user_table01.get_children())  # Clear previous data in the table
            for row in rows:
                self.user_table01.insert('', END, values=row)  # Insert new rows into the table
                conn.commit()
        conn.close()

    def fetch_data01(self):
        # Fetch completed trips (status 'Completed') from the database
        conn = mysql.connector.connect(host="localhost", user="root", password="123456789", database="booking")
        cursor = conn.cursor()

        cursor.execute("select * from driver where name=%s", (self.username,))  # Get driver ID based on username
        driver_id = cursor.fetchone()[0]

        cursor.execute("SELECT * FROM book_customer where driverid =%s and status ='Completed'", (driver_id,))
        rows = cursor.fetchall()
        if len(rows) != 0:
            self.user_table.delete(*self.user_table.get_children())  # Clear previous data in the table
            for row in rows:
                self.user_table.insert('', END, values=row)  # Insert new rows into the table
                conn.commit()
        conn.close()

    def complete_data(self):
        # Mark selected trip as completed
        conn = mysql.connector.connect(host="localhost", user="root", password="123456789", database="booking")
        cursor = conn.cursor()
        selected_item = self.user_table01.selection()[0]  # Get the selected row in the table
        book_id = self.user_table01.item(selected_item)['values'][0]  # Get booking ID
        cursor.execute("select * from driver where name=%s", (self.username,))  # Get driver ID based on username
        driver_id = cursor.fetchone()[0]
        
        # Update the driver's status to 'Available' and set the trip status to 'Completed'
        cursor.execute("Update driver set driver_status = 'Available' where driverid = %s", (driver_id,))
        cursor.execute("Update book_customer set driverid = %s, status='Completed' where book_id=%s", (driver_id, book_id,))
        rows = cursor.fetchall()
        conn.commit()

        self.fetch_data01()  # Refresh the completed trips table
        messagebox.showinfo("Success", "Booking Completed Successfully")  # Show success message
        conn.close()

    def cmd(self):
        # Go back to the login screen (or previous screen)
        self.root.destroy()
        # os.system("Driver_Login.py")  # Uncomment to navigate to the driver login screen
