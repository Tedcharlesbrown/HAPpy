import tkinter as tk

def ask_confirmation():
    def on_submit():
        if var.get():
            print("Checkbox is checked")
        else:
            print("Checkbox is not checked")
        if response_var.get() == "Yes":
            print("User clicked Yes")
        else:
            print("User clicked No")
        popup.destroy()

    popup = tk.Toplevel(root)
    popup.title("Confirmation")

    label = tk.Label(popup, text="Do you want to continue?")
    label.pack(pady=20)

    var = tk.IntVar()
    checkbox = tk.Checkbutton(popup, text="Do this for all", variable=var)
    checkbox.pack(pady=10)

    response_var = tk.StringVar()
    yes_btn = tk.Button(popup, text="Yes", command=lambda: response_var.set("Yes"), width=10)
    no_btn = tk.Button(popup, text="No", command=lambda: response_var.set("No"), width=10)
    submit_btn = tk.Button(popup, text="Submit", command=on_submit, width=10)

    yes_btn.pack(side="left", padx=10)
    no_btn.pack(side="right", padx=10)
    submit_btn.pack(pady=20)

root = tk.Tk()
btn = tk.Button(root, text="Ask Confirmation", command=ask_confirmation)
btn.pack(pady=20)

root.mainloop()
