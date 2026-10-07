# Import necessary libraries
from tkinter import *             # For creating GUI
from tkinter import messagebox    # For showing pop-up messages
from tkinter import ttk           # For advanced widgets like Treeview
import mysql.connector            # For connecting and interacting with MySQL databases
import os                         # For interacting with the operating system (like running other Python scripts)

# Booking class handles the Booking System GUI and backend logic
class Booking:
    def __init__(self, root):  # Constructor method
        self.root = root  # Main window
        self.root.geometry("1000x600")  # Set window dimensions
        self.root.title("Booking System")  # Window title
        self.root.resizable(False, False)  # Disable resizing
        self.root.config(bg="#f0f0f0")  # Background color

        # Variables to store booking details
        self.Bookingid = StringVar()
        self.name = StringVar()
        self.pickuplocation = StringVar()
        self.droplocation = StringVar()
        self.pickupdate = StringVar()
        self.pickuptime = StringVar()

        # ------------------- Input Frame -------------------
        # Frame to contain the input fields
        input_frame = Frame(self.root, bg="#ffffff", bd=5, relief=RIDGE)
        input_frame.place(x=200, y=10, width=600, height=350)

        # Title of the input section
        Label(input_frame, text="Booking Details", font=("Arial", 15, "bold"), bg="#ffffff").place(x=220, y=10)

        # Labels and Entry fields for booking details
        Label(input_frame, text="Booking ID:", font=("Arial", 10, "bold"), bg="#ffffff").place(x=50, y=50)
        self.bookid = Entry(input_frame, textvariable=self.Bookingid, font=("Arial", 10))
        self.bookid.place(x=200, y=50, width=200)

        Label(input_frame, text="Name of Customer:", font=("Arial", 10, "bold"), bg="#ffffff").place(x=50, y=90)
        self.cust_name = Entry(input_frame, textvariable=self.name, font=("Arial", 10))
        self.cust_name.place(x=200, y=90, width=200)

        Label(input_frame, text="Pick-up Address:", font=("Arial", 10, "bold"), bg="#ffffff").place(x=50, y=130)
        self.address = Entry(input_frame, textvariable=self.pickuplocation, font=("Arial", 10))
        self.address.place(x=200, y=130, width=200)

        Label(input_frame, text="Drop-off Location:", font=("Arial", 10, "bold"), bg="#ffffff").place(x=50, y=170)
        self.drop = Entry(input_frame, textvariable=self.droplocation, font=("Arial", 10))
        self.drop.place(x=200, y=170, width=200)

        Label(input_frame, text="Pick-up Date:", font=("Arial", 10, "bold"), bg="#ffffff").place(x=50, y=210)
        self.date = Entry(input_frame, textvariable=self.pickupdate, font=("Arial", 10))
        self.date.place(x=200, y=210, width=200)

        Label(input_frame, text="Pick-up Time:", font=("Arial", 10, "bold"), bg="#ffffff").place(x=50, y=250)
        self.time = Entry(input_frame, textvariable=self.pickuptime, font=("Arial", 10))
        self.time.place(x=200, y=250, width=200)

        Label(input_frame, text="Driver's Name:", font=("Arial", 10, "bold"), bg="#ffffff").place(x=50, y=290)
        self.driver_name = Entry(input_frame, font=("Arial", 10))
        self.driver_name.place(x=200, y=290, width=200)

        # ------------------- Button Frame -------------------
        # Frame to contain action buttons
        button_frame = Frame(self.root, bg="#f0f0f0")
        button_frame.place(x=200, y=370, width=600, height=60)

        # Buttons for different actions
        assign_btn = Button(button_frame, text="Assign Driver", command=self.assign_data, font=("Arial", 10, "bold"), bg="#4CAF50", fg="white", padx=20)
        assign_btn.grid(row=0, column=0, padx=20)

        available_driver_btn = Button(button_frame, text="Available Drivers", command=self.cmd1, font=("Arial", 10, "bold"), bg="#2196F3", fg="white", padx=20)
        available_driver_btn.grid(row=0, column=1, padx=20)

        back_btn = Button(button_frame, text="Back", command=self.cmd, font=("Arial", 10, "bold"), bg="#f44336", fg="white", padx=20)
        back_btn.grid(row=0, column=2, padx=20)

        # ------------------- Data Table -------------------
        # Frame to display booking data in a table format
        self.frm = Frame(self.root, bg="#ffffff", bd=5, relief=RIDGE)
        self.frm.place(x=50, y=420, width=900, height=130)

        # MySQL connection to fetch booking data
        mydb = mysql.connector.connect(host="localhost", user="root", password="123456789", database="booking")
        cursor = mydb.cursor()
        sql = "SELECT * FROM book_customer"
        cursor.execute(sql)
        rows = cursor.fetchall()
        total = cursor.rowcount
        print("Total Data Entries: " + str(total))

        # Scrollbars for the data table
        scroll_x = Scrollbar(self.frm, orient=HORIZONTAL)
        scroll_y = Scrollbar(self.frm, orient=VERTICAL)

        # Treeview widget for displaying data in tabular form
        self.user_table = ttk.Treeview(self.frm, columns=("id", "name", "pickup_location", "drop_address", "date", "time", "status"), xscrollcommand=scroll_x.set)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.user_table.xview)
        scroll_y.config(command=self.user_table.yview)

        # Configure table columns
        self.user_table.heading("id", text="Id")
        self.user_table.heading("name", text="Name")
        self.user_table.heading("pickup_location", text="Pickup Location")
        self.user_table.heading("drop_address", text="Drop address")
        self.user_table.heading("date", text="Date")
        self.user_table.heading("time", text="Time")
        self.user_table.heading("status", text="Status")
        self.user_table['show'] = 'headings'
        self.user_table.column("id", width=100, anchor=CENTER)
        self.user_table.column("name", width=100, anchor=CENTER)
        self.user_table.column("pickup_location", width=100, anchor=CENTER)
        self.user_table.column("drop_address", width=100, anchor=CENTER)
        self.user_table.column("date", width=100, anchor=CENTER)
        self.user_table.column("time", width=100, anchor=CENTER)
        self.user_table.column("status", width=100, anchor=CENTER)
        self.user_table.pack(fill=BOTH, expand=3)
        self.user_table.bind("<ButtonRelease-1>", self.get_cursor)

        self.fetch_data()  # Fetch and populate data into the table

        self.root.mainloop()  # Start the Tkinter main loop

    # ------------------- Function Definitions -------------------
    def fetch_data(self):
        """Fetch data from MySQL database and display it in the table."""
        conn = mysql.connector.connect(host="localhost", user="root", password="123456789", database="booking")
        cursor = conn.cursor()
        sql = "SELECT * FROM book_customer"
        cursor.execute(sql)
        rows = cursor.fetchall()
        if len(rows) != 0:
            self.user_table.delete(*self.user_table.get_children())
            for row in rows:
                self.user_table.insert('', END, values=row)
                conn.commit()
        conn.close()

    def assign_data(self):
        """Assign a driver to a booking and update database records."""
        conn = mysql.connector.connect(host="localhost", user="root", password="123456789", database="booking")
        cursor = conn.cursor()
        selected_item = self.user_table.selection()[0]
        book_id = self.user_table.item(selected_item)['values'][0]
        cursor.execute("SELECT driverid FROM driver WHERE name = %s", (self.driver_name.get(),))
        driver_id = cursor.fetchone()[0]
        cursor.execute("UPDATE driver SET driver_status = 'not Available' WHERE driverid = %s", (driver_id,))
        cursor.execute("UPDATE book_customer SET driverid = %s, status='Active' WHERE book_id=%s", (driver_id, book_id,))
        conn.commit()
        self.fetch_data()
        messagebox.showinfo("Success", "Booking Assigned Successfully")

    def get_cursor(self, ev):
        """Fetch data from selected row in the table."""
        f = self.user_table.focus()
        content = self.user_table.item(f)
        row = content['values']
        self.Bookingid.set(row[0])
        self.name.set(row[1])
        self.pickuplocation.set(row[2])
        self.droplocation.set(row[3])
        self.pickupdate.set(row[4])
        self.pickuptime.set(row[5])

    def cmd(self):
        """Go back to the Admin dashboard."""
        self.root.destroy()
        os.system("Admin.py")

    def cmd1(self):
        """Show available drivers."""
        import Avilabe
        self.new = Tk()
        reg = Avilabe.avilable(self.new)


# Function to run the Booking page
def page():
    root = Tk()
    Booking(root)
    root.mainloop()


# Run the program
if __name__ == '__main__':
    page()
