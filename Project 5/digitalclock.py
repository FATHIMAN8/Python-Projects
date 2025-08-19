from tkinter import *
import time

# Create main window
clk = Tk()
clk.title("Digital Clock")
clk.geometry("500x200")
clk.config(bg="#0C1E28")

# Function to update time
def update_time():
    current_time = time.strftime("%H:%M:%S")  # Hour:Minute:Second
    label.config(text=current_time)
    label.after(1000, update_time)  # update every 1 second

# Create label
label = Label(clk, font=("Times New Roman", 60, "bold"), bg="#0C1E28", fg="white")
label.pack(anchor="center", pady=50)

# Start updating time
update_time()

clk.mainloop()
