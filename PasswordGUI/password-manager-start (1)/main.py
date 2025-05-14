import json  # For reading/writing JSON data
from tkinter import *  # GUI library
from tkinter import messagebox  # For pop-up messages
import random  # For generating random characters
import pyperclip  # To copy password to clipboard


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    # Character pools
    letters = list('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
    numbers = list('0123456789')
    symbols = list('!#$%&()*+')

    # Randomly choosing number of characters from each pool
    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    # Creating random selections
    password_letters = [random.choice(letters) for _ in range(nr_letters)]
    password_symbols = [random.choice(symbols) for _ in range(nr_symbols)]
    password_numbers = [random.choice(numbers) for _ in range(nr_numbers)]

    # Combine and shuffle
    password_list = password_letters + password_symbols + password_numbers
    random.shuffle(password_list)

    # Join to form final password string
    password = "".join(password_list)

    # Display password in the password entry box
    password_entry.delete(0, END)
    password_entry.insert(0, password)

    # Copy password to clipboard
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()

    # Data format to save
    new_data = {
        website: {
            "email": email,
            "password": password
        }
    }

    # Check if any field is empty
    if len(website) == 0 or len(email) == 0 or len(password) == 0:
        messagebox.showerror("Error", "Please enter all fields")
    else:
        try:
            # Try to open and load existing data
            with open("data_file.json", "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            # If file doesn't exist, start with empty dictionary
            data = {}

        # Update old data with new entry
        data.update(new_data)

        # Save back to file
        with open("data_file.json", "w") as file:
            json.dump(data, file, indent=4)

        # Clear input fields after saving
        website_entry.delete(0, END)
        email_entry.delete(0, END)
        password_entry.delete(0, END)


# ---------------------------- FIND PASSWORD ------------------------------- #
def search():
    website = website_entry.get()
    try:
        with open("data_file.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message='Data file not found.')
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo("Search Result", f"Website: {website}\nEmail: {email}\nPassword: {password}")
        else:
            messagebox.showerror(title="Error", message=f"No details for '{website}' found.")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

# Add app logo
canvas = Canvas(width=200, height=200)
logo_img = PhotoImage(file="logo.png")  # Logo image file (must be in same directory)
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)

# ---------------------------- LABELS ------------------------------- #
website_label = Label(text="Website:")
website_label.grid(row=1, column=0)

email_label = Label(text="Email/Username:")
email_label.grid(row=2, column=0)

password_label = Label(text="Password:")
password_label.grid(row=3, column=0)

# ---------------------------- ENTRY FIELDS ------------------------------- #
website_entry = Entry(width=21)
website_entry.grid(row=1, column=1)
website_entry.focus()  # Automatically focus this field

email_entry = Entry(width=35)
email_entry.grid(row=2, column=1, columnspan=2)
email_entry.insert(0, "sathvika@gmail.com")  # Default email

password_entry = Entry(width=21)
password_entry.grid(row=3, column=1)

# ---------------------------- BUTTONS ------------------------------- #
generate_password_button = Button(text="Generate Password", command=generate_password)
generate_password_button.grid(row=3, column=2)

search_button = Button(text="Search", command=search)
search_button.grid(row=1, column=2)

add_button = Button(text="Add", width=36, command=save)
add_button.grid(row=4, column=1, columnspan=2)

# Run the app
window.mainloop()
