import tkinter
from tkinter import messagebox
import random
import pyperclip
import json


# ---------------------------- PASSWORD LOOKUP ------------------------------- #


def search_website():
    try:
        open("password_bank.json")

    except FileNotFoundError:
        open("password_bank.json", mode="w")

    website_to_look = website_entry.get()
    with open("password_bank.json", "w") as pass_file:
        try:
            json.load(pass_file)
        except json.decoder.JSONDecodeError:
            messagebox.showerror(title="No entries", message="Add at least one entry to the application before searching")
        else:


#messagebox.showerror(title="404", message="Website not found in the database")
#messagebox.showinfo(title=website_to_look,
#message=f"User: {database_dict[website_to_look]["user"]} \nPassword: {database_dict[website_to_look]["password"]}")


# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def insert_pass():
    letters = [
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
        'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D',
        'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S',
        'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
    ]
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_list = [random.choice(letters) for letter in range(nr_letters)]
    password_list += [random.choice(numbers) for num in range(nr_numbers)]
    password_list += [random.choice(symbols) for sym in range(nr_symbols)]

    random.shuffle(password_list)
    password = ""
    for char in password_list:
        password += char

    password_entry.delete(0, 'end')
    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #

def save_info():
    website = website_entry.get()
    user = email_entry.get()
    password = password_entry.get()
    json_format = {
        website: {
            "user": user,
            "password": password
        }
    }

    if len(website) == 0 or len(user) == 0 or len(password) == 0:
        messagebox.showerror(title="Missing Inputs", message="Fill in the missing fields and try again")

    else:
        user_confirmation = messagebox.askokcancel(title="Confirm Entry",
                                                   message=f"Are you sure your details are as follows? \n website: {website} \n user: {user} \n password: {password}")

        if user_confirmation:
            try:
                open("password_bank.json")

            except FileNotFoundError:
                open("password_bank.json", mode="w")
            try:
                with open("password_bank.json", mode="r") as pass_file:
                    data = json.load(pass_file)
                    data.update(json_format)
            except json.decoder.JSONDecodeError:
                with open("password_bank.json", mode="w") as pass_file:
                    starting_entry = {
                        website: {
                            "user": user,
                            "password": password
                        }
                    }
                    json.dump(starting_entry, pass_file, indent=4)




            finally:
                with open("password_bank.json", mode="r") as pass_file:
                    data = json.load(pass_file)
                    data.update(json_format)

                with open("password_bank.json", mode="w") as pass_file:
                    json.dump(data, pass_file, indent=4)

                website_entry.delete(0, 'end')
                password_entry.delete(0, 'end')


# ---------------------------- UI SETUP ------------------------------- #


window = tkinter.Tk()
canvas = tkinter.Canvas(height=200, width=200)

window.config(padx=20, pady=20, height=240, width=240)
window.title("Password Manager")

# logo
logo = tkinter.PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo)
canvas.grid(column=2, row=1)

# website
website_label = tkinter.Label(text="Website:")
# website_label.config(padx=10, pady=10)
website_label.grid(column=1, row=2)
search_button = tkinter.Button(text="Search", command=search_website)
search_button.config(width=15)
search_button.grid(column=3, row=2)

website_entry = tkinter.Entry()
website_entry.focus()
website_entry.config(width=34)
website_entry.grid(column=2, row=2)

# email / username

email_label = tkinter.Label(text="Email/Username:")
# email_label.config(padx=10, pady=10)
email_label.grid(column=1, row=3)

email_entry = tkinter.Entry()
email_entry.insert(0, "typeyouremailhere@gmail.com")
email_entry.config(width=53)
email_entry.grid(column=2, row=3, columnspan=2)

# password

password_label = tkinter.Label(text="Password:")
# password_label.config(pady=10, padx=10)
password_label.grid(column=1, row=4)

password_entry = tkinter.Entry()
password_entry.config(width=34)
password_entry.grid(column=2, row=4)

password_button = tkinter.Button(text="Generate Password", command=insert_pass)
password_button.config(width=15)
password_button.grid(row=4, column=3)

# add
add_button = tkinter.Button(text="Add", command=save_info)
add_button.grid(column=2, row=5, columnspan=2)
add_button.config(width=45)

window.mainloop()
