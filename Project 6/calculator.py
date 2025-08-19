from tkinter import *

def click(event):
    global sc_value
    text = event.widget.cget("text")
    if text == "=":
        try:
            result = eval(sc_value.get())
            sc_value.set(result)
        except Exception:
            sc_value.set("Error")
    elif text == "C":
        sc_value.set("")
    else:
        sc_value.set(sc_value.get() + text)

root = Tk()
root.geometry("400x600")
root.title("Calculator")

sc_value = StringVar()
sc_value.set("")
screen = Entry(root, textvar=sc_value, font="lucida 20 bold")
screen.pack(fill=X, ipadx=8, pady=10, padx=10)

buttons = [
    ["7", "8", "9", "/"],
    ["4", "5", "6", "*"],
    ["1", "2", "3", "-"],
    ["0", "C", "=", "+"]
]

for row in buttons:
    f = Frame(root)
    f.pack()
    for btn in row:
        b = Button(f, text=btn, padx=20, pady=20, font="lucida 15 bold")
        b.pack(side=LEFT, padx=5, pady=5)
        b.bind("<Button-1>", click)

root.mainloop()
