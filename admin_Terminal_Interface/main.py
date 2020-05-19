#!/usr/bin/env python3

import time, os, re, sys
from simple_term_menu import TerminalMenu
import bcrypt
from mongoengine import *

disconnect()
connect('IReNEdb', host = 'mongodb://testuser:testpassword@test.irene.uprm.edu:27017/?authSource=admin')

class bcolors:
    """
       Class that holds the color values of the text to be displayed.
       List of attributes:
            - HEADER: Color of the header text.
            - OKBLUE: Terminal text color blue.  
            - OKGREEN: Terminal text color green.
            - WARNING: Terminal text color to display a warning. 
            - FAIL: Terminal text color red to display a failure. 
            - ENDC: Value to let the terminal know the end of a color.
            - BOLD: Value to make a terminal text bold.
            - UNDERLINE: Value to make a terminal text underlined.
    """
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class admin(Document):
    """
        Document Class for Admin. 
        Admin are the users that will have access to the Admin Dashboard.
        These attributes will be the credentials of the Admins for them to enter the Admin Dashboard.
        List of attributes:
            - username: <String>  Admin's username.
                - username attribute follows this regex: r'(^[a-z](?!\.)(?!.*\.$)(?!.*?\.\.)[a-zA-Z0-9_.]{5,19})$'
            - password: <String> Admin's  password hash.   
                
    """
    username = StringField(min_length=5, max_length=20, required=True, unique=True, regex='(^[a-zA-Z](?!\.)(?!.*\.$)(?!.*?\.\.)[a-zA-Z0-9_.]{5,19})$')
    password = StringField(required=True)

#Rules to create a username
username_rules = """Username Requirements: Minimum six alphanumeric characters, must start with an alphabetic character, only valid special character is the dot. Username must not start or end with a dot and no two consecutive dots are allowed. Usernames are case insensitive.
Username examples:
dante.alighieri
donquijote
sancho.panza
sancho.panza1"""

#Rules to create a password
password_rules = "Password Requirements: Minimum 8 characters, maximum 128 characters, at least one uppercase letter, one lowercase letter and one number."


def print_admin_accounts():
    """
        Method to print the admin accounts found in the server.
        
    """
    for adminAcc in admin.objects():
        print(adminAcc.username)

def remove_admin_account(username):
    """
        Method to remove an admin accounts found in the server.
        
        Parameters
        ----------
        username : string
            username of the admin account to be removed
        
    """
    admin.objects.get(username = username.lower()).delete()

def password_match(admin_account, password):
    """
        Method to maatch the given password to the password in the admin account.
        
        Parameters
        ----------
        admin_account : string
            Admin account to be used to compare the password to
        password : string
            Password to compare
        
        Returns
        -------
        Boolean
            Returns true if the password matches, false otherwise.
    """
    return bcrypt.checkpw(password.encode('utf-8'), admin_account.password.encode('utf-8'))

def find_admin_account(username):
    """
        Method to find an admin account in the database.
        
        Parameters
        ----------
        username : string
            username of the admin account to find
        
        Returns
        -------
        admin
            Returns an admin object, or None if the admin was not found.
    """
    try:
        adminAcc = admin.objects.get(username = username.lower())
    except DoesNotExist:
        return None
    return adminAcc

def add_admin_account(username, password):
    """
        Method to add an admin account to the database.
        
        Parameters
        ----------
        username : string
            username of the admin account to be added
        password : string
            password of the admin account to be added
    """
    adminAcc = admin(username = username.lower(), password = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt()).decode('utf8'))
    try:
        adminAcc.save()
    except ValidationError:
        print("Unable to register admin account. A validation error ocurred. "+ str(ValidationError))

def username_exists(username):
    """
        Method that checks if an admin account with the given username exists
        
        Parameters
        ----------
        username : string
            username of the admin account to find
        
        Returns
        -------
        Boolean
            True if the admin account exists, false otherwise.
    """
    try:
        admin.objects.get(username = username.lower())
    except DoesNotExist:
        return False
    return True

def password_isvalid(password):
    """
        Method that checks if the given password is valid
        
        Parameters
        ----------
        password : string
            password to be evaluated
        
        Returns
        -------
        Boolean
            True if the password is valid, false otherwise.
    """
    if(len(password)>128):
        return False
    match = re.search(r"(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d\w].{8,}", password)
    if(match is None):
        return False
    else:
        return True

def username_isvalid(username):
    """
        Method that checks if the given username is valid
        
        Parameters
        ----------
        username : string
            username to be evaluated
        
        Returns
        -------
        Boolean
            True if the username is valid, false otherwise.
    """
    try:
        match = re.search(r'(^[a-zA-Z](?!\.)(?!.*\.$)(?!.*?\.\.)[a-zA-Z0-9_.]{5,19})$',username)
    except:
        return False
    if(match is None):
        return False
    else:
        return True

def print_admin_rules():
    """
        Method that prints the rules to add an admin account
    """
    print(f"{bcolors.UNDERLINE}Add Admin{bcolors.ENDC}")
    print("\n"+username_rules)
    print(password_rules)
    print()

def add_admin():
    """
        Method that performs the procedure to add an admin account to the database
    """
    print_admin_rules()
    count = 0
    while(count < 3):
        username = str(input("Username: "))
        if(not username_isvalid(username)):
            print(f"{bcolors.FAIL}Invalid Username{bcolors.ENDC}")
            count = count + 1
            if(count >=3):
                print(f"{bcolors.FAIL}Could not add admin{bcolors.ENDC}")
            continue
        else:
            if(username_exists(username)):
                print(f"{bcolors.FAIL}Username already exists{bcolors.ENDC}")
                count = count + 1
                if(count >=3):
                    print(f"{bcolors.FAIL}Could not add admin{bcolors.ENDC}")
                continue
        password = str(input("Password: "))
        count = 0
        while(not password_isvalid(password) and count <2):
            print(f"{bcolors.FAIL}Invalid Password{bcolors.ENDC}")
            password = str(input("Password: "))
            count = count + 1
        
        if(not password_isvalid(password) or count >=2):
            print(f"{bcolors.FAIL}Could not add admin{bcolors.ENDC}")
            count = 3
        else:
            add_admin_account(username, password)
            print(f"{bcolors.OKGREEN}Admin account successfully added.{bcolors.ENDC}")
            count = 3

def update_admin_username():
    """
        Method that performs the procedures to update an admin account username in the database
    """
    print(f"{bcolors.UNDERLINE}Update Admin Username{bcolors.ENDC}")
    print()
    print(username_rules+"\n")
    admin_to_update = str(input("Admin username to update: "))
    admin_account = find_admin_account(admin_to_update)
    if(admin_account is None):
        print(f"{bcolors.FAIL}Admin account not found{bcolors.ENDC}")
    else:
        count = 0
        new_username = str(input("New admin username: "))
        while(not username_isvalid(new_username) and count < 2):
            print(f"{bcolors.FAIL}Invalid Username{bcolors.ENDC}")
            new_username = str(input("New admin username: "))
            count = count + 1
            if(count >=2):
                print(f"{bcolors.FAIL}Could not update admin username{bcolors.ENDC}")
        if(count>=2):
            return
        else:
            try:
                admin_account.username = new_username
                admin_account.save()
                print(f"{bcolors.OKGREEN}Admin account successfully updated.{bcolors.ENDC}")
            except:
                print(f"{bcolors.FAIL}Database username validation error{bcolors.ENDC}")

def update_admin_password():
    """
        Method that performs the procedure to update an admin account password in the database
    """
    print(f"{bcolors.UNDERLINE}Update Admin Password{bcolors.ENDC}")
    print()
    print(password_rules+"\n")
    admin_to_update = str(input("Admin username to update: "))
    admin_account = find_admin_account(admin_to_update)
    if(admin_account is None):
        print(f"{bcolors.FAIL}Admin account not found{bcolors.ENDC}")
    else:
        count = 0
        old_password = str(input("Old Password: "))
        while(not password_match(admin_account, old_password) and count < 2):
            print(f"{bcolors.FAIL}Invalid Password{bcolors.ENDC}")
            old_password = str(input("Old Password: "))
            count = count + 1
            if(count >=2):
                print(f"{bcolors.FAIL}Could not update admin password{bcolors.ENDC}")
        if(count>=2):
            return
        count = 0
        new_password = str(input("New Password: "))
        while(not password_isvalid(new_password) and count < 2):
            print(f"{bcolors.FAIL}Invalid Password{bcolors.ENDC}")
            new_password = str(input("New Password: "))
            count = count + 1
            if(count >=2):
                print(f"{bcolors.FAIL}Could not update admin password{bcolors.ENDC}")
        if(count>=2):
            return
        admin_account.password = bcrypt.hashpw(new_password.encode('utf8'), bcrypt.gensalt()).decode('utf8')
        try:
            admin_account.save()
            print(f"{bcolors.OKGREEN}Admin account successfully updated.{bcolors.ENDC}")
        except:
            print(f"{bcolors.FAIL}Unexpected error{bcolors.ENDC}")

def remove_admin():
    """
        Method that performs the procedure to remove an admin account in the database
    """
    print(f"{bcolors.UNDERLINE}Remove Admin Account{bcolors.ENDC}")
    print()
    admin_to_update = str(input("Admin username to remove: "))
    admin_account = find_admin_account(admin_to_update)
    if(admin_account is None):
        print(f"{bcolors.FAIL}Admin account not found{bcolors.ENDC}")
    else:
        print(f"{bcolors.WARNING}Are you sure you want to remove this admin? [y/n]{bcolors.ENDC}")
        if(str(input()) == "y"):
            remove_admin_account(admin_account.username)
            print(f"{bcolors.OKGREEN}Admin account successfully removed.{bcolors.ENDC}")
        else:
            print(f"{bcolors.FAIL}Admin account not removed{bcolors.ENDC}")

def get_all_admins():
    """
        Method that returns all admins in the database and prints them
    """
    print(f"{bcolors.UNDERLINE}All Admin Accounts{bcolors.ENDC}")
    print()
    print_admin_accounts()

def main():
    """
        Main method in charge of displaying the menu of the application as well as delegating the tasks to be
        performed.
    """
    main_menu_title = "  Admin Main Menu\n"
    main_menu_items = ["Add Admin", "Remove Admin", "Update Admin", "See all Admins" ,"Quit"]
    main_menu_cursor = "> "
    main_menu_cursor_style = ("fg_red", "bold")
    main_menu_style = ("bg_red", "fg_yellow")
    main_menu_exit = False

    main_menu = TerminalMenu(menu_entries=main_menu_items,
                             title=main_menu_title,
                             menu_cursor=main_menu_cursor,
                             menu_cursor_style=main_menu_cursor_style,
                             menu_highlight_style=main_menu_style,
                             cycle_cursor=True)

    update_menu_title = "  Update Admin Account\n"
    update_menu_items = ["Update Username", "Update Password", "Back to Main Menu"]
    update_menu_back = False
    update_menu = TerminalMenu(update_menu_items,
                             update_menu_title,
                             main_menu_cursor,
                             main_menu_cursor_style,
                             main_menu_style)

    while not main_menu_exit:
        os.system('clear')
        main_sel = main_menu.show()

        if main_sel == 0:
            os.system('clear')
            add_admin()
            time.sleep(2)
            
        elif main_sel == 1:
            os.system('clear')
            remove_admin()
            time.sleep(2)

        elif main_sel == 2:
            while not update_menu_back:
                os.system('clear')
                update_sel = update_menu.show()
                if update_sel == 0:
                    os.system('clear')
                    update_admin_username()
                    time.sleep(2)
                elif update_sel == 1:
                    os.system('clear')
                    update_admin_password()
                    time.sleep(2)
                elif update_sel == 2:
                    update_menu_back = True
            update_menu_back = False

        elif main_sel == 3:
            os.system('clear')
            get_all_admins()
            print(f"{bcolors.OKGREEN}\n\nAdmin account successfully printed.{bcolors.ENDC}")
            print(f"{bcolors.UNDERLINE}Press Enter to exit.\n{bcolors.ENDC}")
            input()

        elif main_sel == 4:
            main_menu_exit = True
            os.system('clear')

if __name__ == "__main__":
    main()