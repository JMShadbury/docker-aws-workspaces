import workspaces_functions
import os
import time
import pprint

clear = lambda: os.system('clear')
pp = pprint.PrettyPrinter(width=41, compact=True)


# Function to display the menu
def menu():
    menu = {}
    clear()
    menu[1]="1 - List Workspaces" 
    menu[2]="2 - Find Workspace."
    menu[3]="3 - Restart Workspace."
    menu[4]="4 - Exit"

    for keys, value in menu.items():
        print(value)
    selection= input("Please Select:") 
    if selection == "1":
        client = get_client_profile()
        workspaces_client = workspaces_functions.get_workspaces_client(client, "ap-southeast-2")
        get_workspaces_list(workspaces_client)
    if selection == "2":
        get_user()
    if selection == "3":
        print("This is currently not in use")
        exit()
    if selection == "4":
        exit()

# Function to get the client profile to be used in the app
def get_client_profile():

    client = ""
    clear()

    while True:
        print("Client Profile Required")
        print("-----------------------\n")
        print("Please enter Client Profile")
        print("A client profile is required so the app knows what aws account to use.")
        print("Example: runcmd-test")
        print("\ntype 4 to exit...")
        client = input("Enter Client Profile:   ")
        if client == "4":
            menu()
        elif client:
            try:
                workspaces_functions.get_workspaces_client(client, "ap-southeast-2")
                break
            except Exception as e:
                clear()
                print(e)
                print("\n\n")
                time.sleep(2)
        else:
            clear()
    return client


# function to get all workspaces and print them to the terminal
def get_workspaces_list(client):

    workspaces = workspaces_functions.get_workspaces(client)

    clear()
    for workspace in workspaces:
        pp.pprint("Workspace User: {}".format(workspace['UserName']))
    pp.pprint("Total Workspaces: {}".format(len(workspaces)))


# Function to search for user
def get_user():

    client_profile = get_client_profile()

    client = workspaces_functions.get_workspaces_client(client_profile, "ap-southeast-2")

    clear()
    user_id = input("Enter User ID:  ")
    
    workspaces = workspaces_functions.get_workspaces(client)
    ws = ""
    for workspace in workspaces:
        if workspace['UserName'] in user_id:
            ws += "Username:     {}\n".format(workspace['UserName'])
            ws += "ComputerName: {}\n".format(workspace['ComputerName'])
            ws += "DirectoryId:  {}\n".format(workspace['DirectoryId'])
    if ws:
        clear()
        print(ws)
        exit()
    else:
        clear()
        print("User Not Found")
        exit()