import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Database setup
def setup_database():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS students (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        father_name TEXT,
                        mother_name TEXT,
                        contact TEXT,
                        address TEXT,
                        class TEXT,
                        group_type TEXT,
                        roll TEXT UNIQUE,
                        reg_no TEXT UNIQUE)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS payments (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        reg_no TEXT,
                        amount INTEGER,
                        type TEXT)''')
    conn.commit()
    conn.close()

# Tkinter App
class StudentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Management System")
        self.root.geometry("800x600")
        self.root.configure(bg="#003366")  # Dark blue background
        
        self.create_main_menu()
    
    def create_main_menu(self):
        # Top Image Placeholder
        self.image_label = tk.Label(self.root, text="Image", bg="white", font=("Arial", 20, "bold"), width=40, height=5)
        self.image_label.pack(pady=10)
        
        # Buttons Container
        self.button_frame = tk.Frame(self.root, bg="#003366")
        self.button_frame.pack()
        
        # Main Menu Buttons
        self.add_new_btn = tk.Button(self.button_frame, text="Add New", command=self.show_add_new, bg="#FFFFFF", fg="#003366", width=15, height=2)
        self.payment_btn = tk.Button(self.button_frame, text="Payment", command=self.show_payment, bg="#FFFFFF", fg="#003366", width=15, height=2)
        self.performance_btn = tk.Button(self.button_frame, text="Performance", command=self.show_performance, bg="#FFFFFF", fg="#003366", width=15, height=2)
        self.edit_btn = tk.Button(self.button_frame, text="Edit", command=self.show_edit, bg="#FFFFFF", fg="#003366", width=15, height=2)
        
        self.add_new_btn.grid(row=0, column=0, padx=10, pady=10)
        self.payment_btn.grid(row=0, column=1, padx=10, pady=10)
        self.performance_btn.grid(row=0, column=2, padx=10, pady=10)
        self.edit_btn.grid(row=0, column=3, padx=10, pady=10)
        
        # Home Button (Initially Hidden)
        self.home_btn = tk.Button(self.root, text="Home", command=self.show_main_menu, bg="#00509E", fg="white", width=10)
    
    def show_main_menu(self):
        self.clear_frame()
        self.create_main_menu()
    
    def show_add_new(self):
        self.clear_frame()
        self.home_btn.pack(anchor='nw', padx=10, pady=10)
        tk.Label(self.root, text="Add New Student", font=("Arial", 20), bg="#003366", fg="white").pack(pady=20)
        
        form_frame = tk.Frame(self.root, bg="#003366")
        form_frame.pack()
        
        labels = ["Name", "Father Name", "Mother Name", "Contact", "Address", "Class", "Group"]
        self.entries = {}
        
        for idx, label in enumerate(labels):
            tk.Label(form_frame, text=label, bg="#003366", fg="white", font=("Arial", 12)).grid(row=idx, column=0, padx=10, pady=5, sticky='w')
            entry = tk.Entry(form_frame, width=30)
            entry.grid(row=idx, column=1, padx=10, pady=5)
            self.entries[label] = entry
        
        self.class_var = tk.StringVar()
        self.class_var.set("Select Class")
        class_options = [str(i) for i in range(1, 11)] + ["SSC", "HSC"]
        class_menu = ttk.Combobox(form_frame, textvariable=self.class_var, values=class_options, state="readonly")
        class_menu.grid(row=5, column=1, padx=10, pady=5)
        
        self.group_var = tk.StringVar()
        self.group_var.set("Select Group")
        group_menu = ttk.Combobox(form_frame, textvariable=self.group_var, values=["General", "Science"], state="readonly")
        group_menu.grid(row=6, column=1, padx=10, pady=5)
        
        tk.Button(form_frame, text="Save", command=self.save_student, bg="#00509E", fg="white", width=15).grid(row=7, column=1, pady=10)
    
    def save_student(self):
        name = self.entries["Name"].get()
        father = self.entries["Father Name"].get()
        mother = self.entries["Mother Name"].get()
        contact = self.entries["Contact"].get()
        address = self.entries["Address"].get()
        class_selected = self.class_var.get()
        group_selected = self.group_var.get()
        
        if class_selected in ["SSC", "HSC"]:
            prefix = "2511" if class_selected == "SSC" else "2512"
        else:
            prefix = f"25{class_selected}"
        
        conn = sqlite3.connect("students.db")
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(id) FROM students")
        last_id = cursor.fetchone()[0]
        last_id = 1 if last_id is None else last_id + 1
        
        roll = f"{prefix}{str(last_id).zfill(3)}"
        reg_no = f"25{str(last_id).zfill(3)}"
        
        cursor.execute("INSERT INTO students (name, father_name, mother_name, contact, address, class, group_type, roll, reg_no) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                       (name, father, mother, contact, address, class_selected, group_selected, roll, reg_no))
        conn.commit()
        conn.close()
        
        messagebox.showinfo("Success", "Student added successfully!")
        self.show_main_menu()
    
    #start payment ##
    def show_payment(self):
        self.clear_frame()
        self.home_btn.pack(anchor='nw', padx=10, pady=10)
        
        tk.Label(self.root, text="Payment", font=("Arial", 20), bg="#003366", fg="white").pack(pady=20)
        
        # Search bar for student registration number
        search_frame = tk.Frame(self.root, bg="#003366")
        search_frame.pack(pady=10)

        tk.Label(search_frame, text="Search by Reg No:", bg="#003366", fg="white", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
        self.payment_search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=self.payment_search_var, width=20)
        search_entry.pack(side=tk.LEFT, padx=5)
        
        search_entry.bind("<KeyRelease>", self.search_student_payment)

        # Listbox to display matching student results
        self.payment_listbox = tk.Listbox(self.root, width=40, height=5)
        self.payment_listbox.pack(pady=10)
        self.payment_listbox.bind("<<ListboxSelect>>", self.display_student_payment)

        # Payment details display area
        self.payment_frame = tk.Frame(self.root, bg="#003366")
        self.payment_frame.pack(pady=20)

    def search_student_payment(self, event):
        search_term = self.payment_search_var.get()
        self.payment_listbox.delete(0, tk.END)

        conn = sqlite3.connect("students.db")
        cursor = conn.cursor()
        cursor.execute("SELECT reg_no, name FROM students WHERE reg_no LIKE ?", (f"%{search_term}%",))
        results = cursor.fetchall()
        conn.close()

        for reg_no, name in results:
            self.payment_listbox.insert(tk.END, f"{reg_no} - {name}")

    def display_student_payment(self, event):
        selected_index = self.payment_listbox.curselection()
        if not selected_index:
            return

        selected_text = self.payment_listbox.get(selected_index)
        reg_no = selected_text.split(" - ")[0]

        for widget in self.payment_frame.winfo_children():
            widget.destroy()

        conn = sqlite3.connect("students.db")
        cursor = conn.cursor()
        
        # Fetch student info
        cursor.execute("SELECT name, class FROM students WHERE reg_no = ?", (reg_no,))
        student_data = cursor.fetchone()

        # Fetch class price (assuming a default of 1000 if not set)
        cursor.execute("SELECT amount FROM payments WHERE reg_no = ?", (reg_no,))
        total_paid = cursor.fetchone()
        total_paid = total_paid[0] if total_paid else 0

        conn.close()

        if student_data:
            name, class_selected = student_data
            tk.Label(self.payment_frame, text=f"Student: {name}", bg="#003366", fg="white", font=("Arial", 14, "bold")).pack(pady=5)
            tk.Label(self.payment_frame, text=f"Class: {class_selected}", bg="#003366", fg="white", font=("Arial", 12)).pack(pady=5)
            tk.Label(self.payment_frame, text=f"Total Paid: ${total_paid}", bg="#003366", fg="white", font=("Arial", 12)).pack(pady=5)

            tk.Label(self.payment_frame, text="Payment Type:", bg="#003366", fg="white", font=("Arial", 12)).pack(pady=5)

            self.payment_type = tk.StringVar()
            self.payment_type.set("Monthly")

            monthly_radio = tk.Radiobutton(self.payment_frame, text="Monthly", variable=self.payment_type, value="Monthly", bg="#003366", fg="white")
            yearly_radio = tk.Radiobutton(self.payment_frame, text="Yearly", variable=self.payment_type, value="Yearly", bg="#003366", fg="white")
            
            monthly_radio.pack()
            yearly_radio.pack()

            tk.Button(self.payment_frame, text="Make Payment", command=lambda: self.make_payment(reg_no, class_selected), bg="#00509E", fg="white", width=15).pack(pady=10)

    def make_payment(self, reg_no, class_selected):
        payment_type = self.payment_type.get()
        
        # Define class price (default: 1000)
        class_price = 1000
        payment_amount = class_price if payment_type == "Monthly" else class_price * 12

        conn = sqlite3.connect("students.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO payments (reg_no, amount, type) VALUES (?, ?, ?)", (reg_no, payment_amount, payment_type))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", f"{payment_type} payment of ${payment_amount} made successfully!")
        self.show_payment()


    #end payment ##
    def show_performance(self):
        self.clear_frame()
        self.home_btn.pack(anchor='nw', padx=10, pady=10)
        
        tk.Label(self.root, text="Performance", font=("Arial", 20), bg="#003366", fg="white").pack(pady=20)
        
        # Search bar for student registration number
        search_frame = tk.Frame(self.root, bg="#003366")
        search_frame.pack(pady=10)

        tk.Label(search_frame, text="Search by Reg No:", bg="#003366", fg="white", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=self.search_var, width=20)
        search_entry.pack(side=tk.LEFT, padx=5)
        
        search_entry.bind("<KeyRelease>", self.search_student_performance)

        # Listbox to display matching student results
        self.result_listbox = tk.Listbox(self.root, width=40, height=5)
        self.result_listbox.pack(pady=10)
        self.result_listbox.bind("<<ListboxSelect>>", self.display_student_performance)

        # Student information display area
        self.info_frame = tk.Frame(self.root, bg="#003366")
        self.info_frame.pack(pady=20)


    def search_student_performance(self, event):
        search_term = self.search_var.get()
        self.result_listbox.delete(0, tk.END)

        conn = sqlite3.connect("students.db")
        cursor = conn.cursor()
        cursor.execute("SELECT reg_no, name FROM students WHERE reg_no LIKE ?", (f"%{search_term}%",))
        results = cursor.fetchall()
        conn.close()

        for reg_no, name in results:
            self.result_listbox.insert(tk.END, f"{reg_no} - {name}")

    def display_student_performance(self, event):
        selected_index = self.result_listbox.curselection()
        if not selected_index:
            return

        selected_text = self.result_listbox.get(selected_index)
        reg_no = selected_text.split(" - ")[0]

        for widget in self.info_frame.winfo_children():
            widget.destroy()

        conn = sqlite3.connect("students.db")
        cursor = conn.cursor()
        
        # Fetch student info
        cursor.execute("SELECT * FROM students WHERE reg_no = ?", (reg_no,))
        student_data = cursor.fetchone()
        
        # Fetch payment info
        cursor.execute("SELECT SUM(amount) FROM payments WHERE reg_no = ?", (reg_no,))
        total_paid = cursor.fetchone()[0]
        total_paid = total_paid if total_paid else 0
        
        conn.close()

        if student_data:
            labels = ["Name:", "Father Name:", "Mother Name:", "Contact:", "Address:", "Class:", "Group:", "Roll No:", "Reg No:", "Total Payment:"]
            values = list(student_data[1:]) + [f"${total_paid}"]
            
            for i in range(len(labels)):
                tk.Label(self.info_frame, text=labels[i], bg="#003366", fg="white", font=("Arial", 12, "bold")).grid(row=i, column=0, sticky="w", padx=10, pady=2)
                tk.Label(self.info_frame, text=values[i], bg="#003366", fg="white", font=("Arial", 12)).grid(row=i, column=1, sticky="w", padx=10, pady=2)

    #Edit Starting ___
    def show_edit(self):
        self.clear_frame()
        self.home_btn.pack(anchor='nw', padx=10, pady=10)

        tk.Label(self.root, text="Edit", font=("Arial", 20), bg="#003366", fg="white").pack(pady=20)

        # Options frame
        edit_frame = tk.Frame(self.root, bg="#003366")
        edit_frame.pack(pady=20)

        tk.Button(edit_frame, text="Edit Course Price", command=self.edit_course_price, bg="#00509E", fg="white", width=20).grid(row=0, column=0, padx=10, pady=10)
        tk.Button(edit_frame, text="Edit Student Info", command=self.edit_student_info, bg="#00509E", fg="white", width=20).grid(row=1, column=0, padx=10, pady=10)

    def edit_course_price(self):
        self.clear_frame()
        self.home_btn.pack(anchor='nw', padx=10, pady=10)

        tk.Label(self.root, text="Edit Course Price", font=("Arial", 20), bg="#003366", fg="white").pack(pady=20)

        tk.Label(self.root, text="Set New Course Price:", bg="#003366", fg="white", font=("Arial", 12)).pack(pady=5)
        self.new_price_var = tk.StringVar()
        price_entry = tk.Entry(self.root, textvariable=self.new_price_var, width=20)
        price_entry.pack(pady=5)

        tk.Button(self.root, text="Save", command=self.save_new_price, bg="#00509E", fg="white", width=15).pack(pady=10)

    def save_new_price(self):
        new_price = self.new_price_var.get()

        if not new_price.isdigit():
            messagebox.showerror("Error", "Please enter a valid number.")
            return

        conn = sqlite3.connect("students.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM payments")  # Reset payments
        cursor.execute("INSERT INTO payments (reg_no, amount, type) VALUES ('default', ?, 'monthly')", (new_price,))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Course price updated successfully!")
        self.show_edit()

    def edit_student_info(self):
        self.clear_frame()
        self.home_btn.pack(anchor='nw', padx=10, pady=10)

        tk.Label(self.root, text="Edit Student Info", font=("Arial", 20), bg="#003366", fg="white").pack(pady=20)

        # Search student by reg number
        search_frame = tk.Frame(self.root, bg="#003366")
        search_frame.pack(pady=10)

        tk.Label(search_frame, text="Search by Reg No:", bg="#003366", fg="white", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
        self.edit_search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=self.edit_search_var, width=20)
        search_entry.pack(side=tk.LEFT, padx=5)
        search_entry.bind("<KeyRelease>", self.search_student_edit)

        # Listbox to display matching student results
        self.edit_listbox = tk.Listbox(self.root, width=40, height=5)
        self.edit_listbox.pack(pady=10)
        self.edit_listbox.bind("<<ListboxSelect>>", self.display_student_edit)

        # Student info frame
        self.student_edit_frame = tk.Frame(self.root, bg="#003366")
        self.student_edit_frame.pack(pady=20)

    def search_student_edit(self, event):
        search_term = self.edit_search_var.get()
        self.edit_listbox.delete(0, tk.END)

        conn = sqlite3.connect("students.db")
        cursor = conn.cursor()
        cursor.execute("SELECT reg_no, name FROM students WHERE reg_no LIKE ?", (f"%{search_term}%",))
        results = cursor.fetchall()
        conn.close()

        for reg_no, name in results:
            self.edit_listbox.insert(tk.END, f"{reg_no} - {name}")

    def display_student_edit(self, event):
        selected_index = self.edit_listbox.curselection()
        if not selected_index:
            return

        selected_text = self.edit_listbox.get(selected_index)
        reg_no = selected_text.split(" - ")[0]

        for widget in self.student_edit_frame.winfo_children():
            widget.destroy()

        conn = sqlite3.connect("students.db")
        cursor = conn.cursor()
        cursor.execute("SELECT name, father_name, mother_name, contact, address, class, group_type FROM students WHERE reg_no = ?", (reg_no,))
        student_data = cursor.fetchone()
        conn.close()

        if student_data:
            labels = ["Name", "Father Name", "Mother Name", "Contact", "Address", "Class", "Group"]
            self.edit_entries = {}

            for idx, (label, value) in enumerate(zip(labels, student_data)):
                tk.Label(self.student_edit_frame, text=label, bg="#003366", fg="white", font=("Arial", 12)).grid(row=idx, column=0, padx=10, pady=5, sticky='w')
                entry = tk.Entry(self.student_edit_frame, width=30)
                entry.grid(row=idx, column=1, padx=10, pady=5)
                entry.insert(0, value)
                self.edit_entries[label] = entry

            tk.Button(self.student_edit_frame, text="Update", command=lambda: self.update_student_info(reg_no), bg="#00509E", fg="white", width=15).grid(row=len(labels), column=1, pady=10)

            # Add result and attendance entry
            tk.Label(self.student_edit_frame, text="Result:", bg="#003366", fg="white", font=("Arial", 12)).grid(row=len(labels)+1, column=0, padx=10, pady=5, sticky='w')
            self.result_var = tk.StringVar()
            result_entry = tk.Entry(self.student_edit_frame, textvariable=self.result_var, width=30)
            result_entry.grid(row=len(labels)+1, column=1, padx=10, pady=5)

            tk.Label(self.student_edit_frame, text="Attendance (%):", bg="#003366", fg="white", font=("Arial", 12)).grid(row=len(labels)+2, column=0, padx=10, pady=5, sticky='w')
            self.attendance_var = tk.StringVar()
            attendance_entry = tk.Entry(self.student_edit_frame, textvariable=self.attendance_var, width=30)
            attendance_entry.grid(row=len(labels)+2, column=1, padx=10, pady=5)

            tk.Button(self.student_edit_frame, text="Save Result & Attendance", command=lambda: self.save_result_attendance(reg_no), bg="#00509E", fg="white", width=20).grid(row=len(labels)+3, column=1, pady=10)

    def update_student_info(self, reg_no):
        updated_values = {label: entry.get() for label, entry in self.edit_entries.items()}

        conn = sqlite3.connect("students.db")
        cursor = conn.cursor()
        cursor.execute("""UPDATE students SET name=?, father_name=?, mother_name=?, contact=?, address=?, class=?, group_type=? WHERE reg_no=?""",
                    (updated_values["Name"], updated_values["Father Name"], updated_values["Mother Name"], updated_values["Contact"], updated_values["Address"], updated_values["Class"], updated_values["Group"], reg_no))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Student information updated successfully!")
        self.show_edit()

    def save_result_attendance(self, reg_no):
        result = self.result_var.get()
        attendance = self.attendance_var.get()

        conn = sqlite3.connect("students.db")
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS performance (reg_no TEXT PRIMARY KEY, result TEXT, attendance TEXT)")
        cursor.execute("INSERT OR REPLACE INTO performance (reg_no, result, attendance) VALUES (?, ?, ?)", (reg_no, result, attendance))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Result and Attendance saved successfully!")
        self.show_edit()

    #Edit End
    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.pack_forget()
    
if __name__ == "__main__":
    setup_database()
    root = tk.Tk()
    app = StudentApp(root)
    root.mainloop()
