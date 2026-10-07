from tkinter import *
from tkinter import messagebox, ttk
import os
import mysql.connector

# Class to display and manage available drivers
class avilable:
    def __init__(self, root):
        # Initialize the main window for the 'Available Drivers' functionality
        self.root = root
        self.root.geometry("750x300")  # Set window size
        self.root.title("Available Drivers")  # Set window title
        self.root.resizable(False, False)  # Disable resizing of the window

        # Frame for holding the table of available drivers
        self.frame = Frame(self.root, width=700, height=200, bg="red")
        self.frame.place(x=25, y=50)

        # Frame for future buttons or additional UI (currently not used)
        self.tbl_frm = Frame(self.root, width=800, height=500)
        self.tbl_frm.place(x=100, y=300, width=900)

        # Scrollbars for horizontal and vertical scrolling
        scroll_x = Scrollbar(self.frame, orient=HORIZONTAL)
        scroll_y = Scrollbar(self.frame, orient=VERTICAL)

        # Treeview widget to display driver details in a tabular format
        self.user_table = ttk.Treeview(self.frame, columns=(
            "driverid", "name", "citizen", "license", "contact", "driver_status"),
            xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

        # Configure scrollbars
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.user_table.xview)
        scroll_y.config(command=self.user_table.yview)

        # Define the headers (columns) for the Treeview
        self.user_table.heading("driverid", text="Id")
        self.user_table.heading("name", text="Name")
        self.user_table.heading("citizen", text="Citizen")
        self.user_table.heading("license", text="License")
        self.user_table.heading("contact", text="Contact")
        self.user_table.heading("driver_status", text="Status")

        # Configure column widths and alignment
        self.user_table['show'] = 'headings'  # Display only headings, no default column
        self.user_table.column("driverid", width=100, anchor=CENTER)
        self.user_table.column("name", width=100, anchor=CENTER)
        self.user_table.column("citizen", width=100, anchor=CENTER)
        self.user_table.column("license", width=100, anchor=CENTER)
        self.user_table.column("contact", width=100, anchor=CENTER)
        self.user_table.column("driver_status", width=100, anchor=CENTER)

        # Pack the table into the frame
        self.user_table.pack(fill=BOTH, expand=3)

        # Fetch and display data from the database
        self.fetch_data()

        # Start the main event loop for the window
        self.root.mainloop()

    # Function to fetch driver data from the database and display it in the Treeview
    def fetch_data(self):
        conn = mysql.connector.connect(host="localhost", user="root", password="123456789", database="booking")
        cursor = conn.cursor()

        # SQL query to retrieve relevant driver information
        cursor.execute("SELECT driverid, name, citizen, license, contact, driver_status FROM driver")
        rows = cursor.fetchall()  # Fetch all rows from the query result

        # If rows exist, clear the table and insert new rows
        if len(rows) != 0:
            self.user_table.delete(*self.user_table.get_children())  # Clear existing data in the Treeview
            for row in rows:
                self.user_table.insert('', END, values=row)  # Insert each row into the Treeview
                conn.commit()  # Commit any changes to the database (not necessary for SELECT queries)

        conn.close()  # Close the database connection

    # Function to cancel a booking (not used in this context)
    def cancel_data(self):
        conn = mysql.connector.connect(host="localhost", user="root", password="123456789", database="booking")
        cursor = conn.cursor()

        # Retrieve the selected booking ID from the Treeview
        selected_item = self.user_table.selection()[0]
        book_id = self.user_table.item(selected_item)['values'][0]

        # Update the booking status to 'Cancelled'
        cursor.execute("UPDATE book_customer SET status='Cancelled' WHERE book_id=%s", (book_id,))
        conn.commit()  # Commit the update to the database

        self.fetch_data()  # Refresh the displayed data
        messagebox.showinfo("Success", "Booking Cancelled Successfully")  # Display success message


# Uncomment the following block to test the functionality independently
# if __name__ == '__main__':
#     root = Tk()
#     obj = avilable(root)
#     root.mainloop()
