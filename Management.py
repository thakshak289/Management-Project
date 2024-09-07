import mysql.connector
import tkinter as tk
from tkinter import messagebox, scrolledtext
import tkinter.font as tkFont


def connect_to_db():
    return mysql.connector.connect(
        host="localhost",       
        user="root",    
        password="Thakshak@1234",
        database="thakshak_server"    
    )


def submit_data():
    
    name = name_entry.get()      
    symptoms = symptoms_entry.get()  
    tablets = tablets_entry.get()    

    
    if not name or not symptoms or not tablets:
        messagebox.showwarning("Input Error", "All fields must be filled!")
        return

    
    db = connect_to_db()
    cursor = db.cursor()
    
    
    query = "INSERT INTO Med (name, symptoms, tablets) VALUES (%s, %s, %s)"
    values = (name, symptoms, tablets)

    try:
        cursor.execute(query, values)  
        db.commit() 
        update_table_display()                    
        messagebox.showinfo("Success", "Record added successfully!")
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
    finally:
        cursor.close()  
        db.close() 

def update_table_display():
    db = connect_to_db()
    cursor = db.cursor()
    
    query = "SELECT * FROM med"
    cursor.execute(query)
    rows = cursor.fetchall()

    # Clear the current contents of the text widget
    table_display.delete(1.0, tk.END)

    # Display the data in the text widget
    for row in rows:
        table_display.insert(tk.END, f"{row}\n")

    cursor.close()
    db.close()    


root = tk.Tk()

root.title("Patient Record Submission")
heading_font = tkFont.Font(family="Helvetica", size=16, weight="bold")


heading_label = tk.Label(root, text="Patient Record Submission Form", font=heading_font, bg="lightblue")
heading_label.grid(row=0, column=0, columnspan=2, padx=0, pady=0,sticky="ew")



tk.Label(root, text="Name:",font=("Times New Roman",15)).grid(row=1, column=0, padx=10, pady=10)
name_entry = tk.Entry(root)   
name_entry.grid(row=1, column=1)


tk.Label(root, text="Symptoms:",font=("Times New Roman",15)).grid(row=2, column=0, padx=10, pady=10)
symptoms_entry = tk.Entry(root)   
symptoms_entry.grid(row=2, column=1)


tk.Label(root, text="Tablets:",font=("Times New Roman",15)).grid(row=3, column=0, padx=10, pady=10)
tablets_entry = tk.Entry(root)    
tablets_entry.grid(row=3, column=1)

submit_button = tk.Button(root, text="Submit",font=("Times New Roman",15), command=submit_data)
submit_button.grid(row=4, column=1, pady=20)

table_display = scrolledtext.ScrolledText(root, width=60, height=10, wrap=tk.WORD)
table_display.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

# Update the table display initially
update_table_display()

root.mainloop()
