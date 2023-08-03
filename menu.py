from workspace_functions import get_client_profile, get_workspaces_client, get_workspaces_list, get_user, clear, report


# Function to display the menu
def menu(client_profile, region, user_id):

    # Setup Menu Items
    menu = {}
    clear()
    menu[1]="1 - List Workspaces" 
    menu[2]="2 - Find Workspace."
    menu[3]="3 - Restart Workspace."
    menu[4]="4 - Monthly Cost Estimate."
    menu[5]="5 - Exit"

    # Print Menu to screen
    for keys, value in menu.items():
        print(value)

    # Get input from user
    selection= input("Please Select:") 


    # If the selection is 1, get list of users
    if selection == "1":

        # Get the customer profile (runcmd-test)
        customer = get_client_profile(client_profile, region)

        # get workspaces client for boto3 functions
        workspaces_client = get_workspaces_client(customer, region)

        # Get workspaces list and print to screen
        get_workspaces_list(workspaces_client)

    # If the selection is 2, search for a user's workspace
    if selection == "2":

        # search for a users workspace and print the details
        get_user(client_profile, region, user_id)

    # If the selection is 3, reboot a workspace
    if selection == "3":

        # Placeholder, will update this after extensive testing
        print("This is currently not in use")
        exit()

    if selection == "4":

        report(client_profile, region)

    # If the selection is 5, exit the application
    if selection == "5":
        exit()