import string
from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json



# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def password_generator():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
               'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_letters = [random.choice(letters) for _ in range(nr_letters)]
    password_symbols = [random.choice(symbols) for _ in range(nr_symbols)]
    password_numbers = [random.choice(numbers) for _ in range(nr_numbers)]

    password_list = password_numbers + password_symbols + password_letters
    random.shuffle(password_list)
    password = "".join(password_list)
    password_input.delete(0, END)
    password_input.insert(0, password)
    pyperclip.copy(password)


# for char in password_list:
#     password += char
# ---------------------------- SAVE PASSWORD ------------------------------- #

# ---------------------------- UI SETUP ------------------------------- #
frame = Tk()
frame.title("Password Generator")
frame.config(padx=20, pady=10, height=200, width=200)

# WORKING WITH CANVAS
img = PhotoImage(file="logo.png", name="demo")
canvas = Canvas(relief="groove")
canvas.create_image(220, 120, image=img)

# WORKING WITH INPUT AND LAYOUT WIDGET
web_label = Label(text="Website: ", font=('calibre', 12, 'bold'))
email_label = Label(text="Email: ", font=('calibre', 12, 'bold'))
password_label = Label(text="Password: ", font=('calibre', 12, 'bold'))
web_input = Entry(frame, font=('calibre', 12, 'normal'), width=21)
print(web_input)
web_input.focus()
email_input = Entry(frame, font=('calibre', 12, 'normal'), width=40)
password_input = Entry(frame, font=('calibre', 12, 'normal'), width=21)


# COMMAND TO STORE SAVED PASSWORD
def on_add_click():
    web_text = web_input.get().capitalize()
    email_text = email_input.get()
    password_text = password_input.get()
    new_data = {
        web_text: {
            "email": email_text,
            "password": password_text
        }
    }

    if len(web_text) == 0 or len(email_text) == 0 or len(password_text) == 0:
        messagebox.showerror(title=web_text, message="You should not left the field empty.")
        return
    else:
        is_ok = messagebox.askokcancel(title=web_text,
                                       message=f"These are the details entered. website = {web_text}, email = {email_text}, password = {password_text}.Is it fine?")
        if is_ok:
            try:
                with open("saved_password.json", "r") as file:
                    data = json.load(file)
                    data.update(new_data)
                    with open("saved_password.json", "w") as data_file:
                        json.dump(data, data_file, indent=4)
                    # file.write(f"\n {web_text} | {email_text} | {password_text}")
                    # CLEAR INPUT FIELD
            except FileNotFoundError:
                with open("saved_password.json", "w") as file:
                    json.dump(new_data, file, indent=4)
            finally:
                web_input.delete(0, END)
                email_input.delete(0, END)
                password_input.delete(0, END)


def search_details():
    try:
        with open("saved_password.json") as file:
            data = json.load(file)
    except FileNotFoundError:
        messagebox.showerror(message="No details saved for above website.")

    else:
        if web_input.get().capitalize() in data:
            searched_data = data[web_input.get().capitalize()]
            email = searched_data["email"]
            password = searched_data["password"]
            messagebox.showinfo(title=web_input.get().capitalize(), message=f"Email: {email} \n Password: {password}")
        else:
            messagebox.showerror(title="Error", message="No details saved for above website.")


# WORKING WITH BUTTON
btn_add = Button(frame, text="Add", font=('calibre', 12, 'bold'), justify="center", width=36, command=on_add_click)
btn_generate_password = Button(frame, text="Generate Password", font=('calibre', 10, 'bold'), justify="center",
                               width=20, command=password_generator)
btn_search = Button(frame, text="Search", font=("calibre", 10, "bold"), justify="center", width=20,
                    command=search_details, bg="green", border=2)
# WORKING WITH LAYOUT
canvas.grid(row=0, column=1)
web_label.grid(row=1, column=0)
email_label.grid(row=2, column=0)
password_label.grid(row=3, column=0)
web_input.grid(row=1, column=1)
email_input.grid(row=2, column=1, columnspan=2)
password_input.grid(row=3, column=1)
btn_generate_password.grid(row=3, column=2)
btn_add.grid(row=4, column=1, columnspan=2)
btn_search.grid(row=1, column=2)
frame.mainloop()
