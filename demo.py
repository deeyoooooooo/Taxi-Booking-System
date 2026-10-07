from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import mysql.connector
import os
from tkcalendar import DateEntry

class Booking:
    def __init__(self, root, username):
        # Initialize the window properties
        self.root = root
        self.username = username
        self.root.geometry("1000x600")  # Set the window size
        self.root.resizable(False, False)  # Disable resizing
        self.root.title("Taxi Booking System")  # Window title
        self.root.config(bg="#f0f0f0")  # Set the background color

        # Styling variables for consistent design
        self.entry_bg = "#f5f5f5"  # Light gray background for text entries
        self.button_bg = "#4CAF50"  # Green background for buttons
        self.button_fg = "white"  # White text for buttons
        self.label_font = ('Helvetica', 12, 'bold')  # Label font
        self.entry_font = ('Arial', 12)  # Entry font

        # Variables for data binding with entry fields
        self.Bookingid = StringVar()
        self.name = StringVar()
        self.pickuplocation = StringVar()
        self.droplocation = StringVar()
        self.pickupdate = StringVar()
        self.pickuptime = StringVar()

        # Label and entry for Booking ID
        self.label = Label(self.root, text='Booking ID', font=self.label_font, bg="#f0f0f0")
        self.label.place(x=250, y=70)  # Positioning
        self.box = Entry(self.root, textvariable=self.Bookingid, font=self.entry_font, bg=self.entry_bg)
        self.box.place(x=390, y=70, width=200)

        # Label and entry for Customer Name
        self.label = Label(self.root, text='Name of Customer', font=self.label_font, bg="#f0f0f0")
        self.label.place(x=250, y=110)
        self.box = Entry(self.root, textvariable=self.name, font=self.entry_font, bg=self.entry_bg)
        self.box.place(x=390, y=110, width=200)

        # Label and entry for Pickup Location
        self.label = Label(self.root, text='Pick up Address', font=self.label_font, bg="#f0f0f0")
        self.label.place(x=250, y=150)
        self.box01 = Entry(self.root, textvariable=self.pickuplocation, font=self.entry_font, bg=self.entry_bg)
        self.box01.place(x=390, y=150, width=200)

        # Label and entry for Drop Location
        self.label = Label(self.root, text='Drop Location', font=self.label_font, bg="#f0f0f0")
        self.label.place(x=250, y=190)
        self.box02 = Entry(self.root, textvariable=self.droplocation, font=self.entry_font, bg=self.entry_bg)
        self.box02.place(x=390, y=190, width=200)

        # Label and entry for Pick Up Date
        self.label = Label(self.root, text='Pick Up Date', font=self.label_font, bg="#f0f0f0")
        self.label.place(x=250, y=230)
        self.box03 = DateEntry(self.root, textvariable=self.pickupdate, font=self.entry_font, bg=self.entry_bg, width=18)
        self.box03.place(x=390, y=230)

        # Label and entry for Pick Up Time
        self.label = Label(self.root, text='Pick Up Time', font=self.label_font, bg="#f0f0f0")
        self.label.place(x=250, y=270)
        self.box04 = Entry(self.root, textvariable=self.pickuptime, font=self.entry_font, bg=self.entry_bg)
        self.box04.place(x=390, y=270, width=200)

        # Buttons for editing, cancelling, and going back
        self.button = Button(self.root, command=self.edit_data, text="Edit", font=('Arial', 12, 'bold'), bg=self.button_bg, fg=self.button_fg)
        self.button.place(x=50, y=320, width=100, height=35)

        self.button = Button(self.root, command=self.cancel_data, text="Cancel", font=('Arial', 12, 'bold'), bg="#f44336", fg="white")
        self.button.place(x=200, y=320, width=100, height=35)

        self.button = Button(self.root, text="Back", font=('Arial', 12, 'bold'), command=self.cmd, bg="#2196F3", fg="white")
        self.button.place(x=925, y=10, width=60, height=30)

        # Table Frame for displaying booking data
        self.tbl_frm = Frame(self.root, width=900, height=250, bg="#ffffff", bd=3, relief=SOLID)
        self.tbl_frm.place(x=50, y=370, width=900)

        # Scrollbars for the table
        scroll_x = Scrollbar(self.tbl_frm, orient=HORIZONTAL)
        scroll_y = Scrollbar(self.tbl_frm, orient=VERTICAL)
        self.user_table = ttk.Treeview(self.tbl_frm, columns=("id", "name", "pickup_location", "drop_address", "date", "time", "status"),
                                       xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.user_table.xview)
        scroll_y.config(command=self.user_table.yview)

        # Treeview Column Headings and Styling
        self.user_table.heading("id", text="Id")
        self.user_table.heading("name", text="Name")
        self.user_table.heading("pickup_location", text="Pickup Location")
        self.user_table.heading("drop_address", text="Drop Address")
        self.user_table.heading("date", text="Date")
        self.user_table.heading("time", text="Time")
        self.user_table.heading("status", text="Status")
        
        self.user_table['show'] = 'headings'
        for col in self.user_table["columns"]:
            self.user_table.column(col, width=120, anchor=CENTER)
        
        self.user_table.pack(fill=BOTH, expand=True)  # Display the table
        self.user_table.bind("<ButtonRelease-1>", self.get_cursor)  # Bind selection event to get data
        self.fetch_data()  # Fetch data to populate the table

    def fetch_data(self):
        """Fetch data from the database and populate the table"""
        conn = mysql.connector.connect(host="localhost", user="root", password="123456789", database="booking")
        cursor = conn.cursor()

        cursor.execute("select * from register where email=%s", (self.username,))  # Get customer ID based on email
        cust_id = cursor.fetchone()[0]

        cursor.execute("SELECT * FROM book_customer where id=%s", (cust_id,))  # Get all bookings for the customer
        rows = cursor.fetchall()

        if len(rows) != 0:
            self.user_table.delete(*self.user_table.get_children())  # Clear the table before inserting new data
            for row in rows:
                self.user_table.insert('', END, values=row)  # Insert the fetched data into the table
                conn.commit()

        conn.close()

    def cancel_data(self):
        """Cancel the selected booking by changing its status to 'Cancelled'"""
        conn = mysql.connector.connect(host="localhost", user="root", password="123456789", database="booking")
        cursor = conn.cursor()
        selected_item = self.user_table.selection()[0]  # Get the selected booking
        book_id = self.user_table.item(selected_item)['values'][0]  # Get the booking ID
        cursor.execute("UPDATE book_customer SET status='Cancelled' WHERE book_id=%s", (book_id,))  # Update the status
        conn.commit()
        self.fetch_data()  # Refresh the table with updated data
        messagebox.showinfo("Success", "Booking Cancelled Successfully")  # Show success message

    def edit_data(self):
        """Edit the selected booking's details"""
        conn = mysql.connector.connect(host="localhost", user="root", password="123456789", database="booking")
        cursor = conn.cursor()
        selected_item = self.user_table.selection()[0]  # Get the selected booking
        book_id = self.user_table.item(selected_item)['values'][0]  # Get the booking ID
        # Update the selected booking with new details
        cursor.execute("UPDATE book_customer SET pickbox=%s, dropbox=%s, datebox=%s, timebox=%s WHERE book_id=%s", 
                       (self.box01.get(), self.box02.get(), self.box03.get(), self.box04.get(), book_id))
        conn.commit()
        self.fetch_data()  # Refresh the table with updated data
        messagebox.showinfo("Success", "Booking Edited Successfully")  # Show success message

    def get_cursor(self, ev):
        """Get the selected booking details from the table and display in the entry fields"""
        f = self.user_table.focus()
        content = self.user_table.item(f)
        row = content['values']

        self.Bookingid.set(row[0])  # Set the booking ID in the entry
        self.name.set(row[1])  # Set the customer name in the entry
        self.pickuplocation.set(row[2])  # Set the pickup location
        self.droplocation.set(row[3])  # Set the drop location
        self.pickupdate.set(row[4])  # Set the pick up date
        self.pickuptime.set(row[5])  # Set the pick up time

    def cmd(self):
        """Go back to the home page"""
        self.root.destroy()  # Close the current window
        import Home  # Import the Home module
        self.new = Tk()  # Create a new window
        reg = Home.Home_Page(self.new, username=self.username)  # Create an instance of the home page

# Uncomment to run the page
# def page():
#     root = Tk()
#     Booking(root)
#     root.mainloop()

# if __name__ == '__main__':
#     page()
