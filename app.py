import argparse
import boto3
import sys
import pprint
import os
import time

clear = lambda: os.system('clear')


def aws_function(_aws_function, **kwargs):
    return _aws_function(**kwargs)

def get_workspaces(client):
    """
    Returns existing workspaces details
    :param client: a boto3 workspaces client
    :return flat_list:  list of workspaces with relevant details
    """
    _all_workspaces = []
    throttle = True
    while(throttle):
        try:
            res_workspaces = aws_function(client.describe_workspaces)
            throttle = False
        except Exception as e:
            print(e)
            throttle = True
            if "ExpiredToken" in str(e):
                exit()
    while True:
        for workspace in res_workspaces["Workspaces"]:
            _all_workspaces.append(
                {
                    "WorkspaceId": workspace["WorkspaceId"],
                    "ComputerName": workspace.get("ComputerName", "Unknown"),
                    "UserName": workspace["UserName"],
                    "DirectoryId": workspace["DirectoryId"],
                    "RunningMode": workspace["WorkspaceProperties"]["RunningMode"],
                    "ComputeTypeName": workspace["WorkspaceProperties"][
                        "ComputeTypeName"
                    ]
                }
            )
        if "NextToken" not in res_workspaces:
            break
        throttle = True
        while(throttle):
            try:
                res_workspaces = aws_function(
                    client.describe_workspaces, NextToken=res_workspaces["NextToken"]
                )
                throttle = False
            except:
                throttle = True
    return _all_workspaces





def get_workspaces_client(profile, region):
    """
    Connect to AWS APIs
    :return: workspaces client
    """

    boto3.setup_default_session(profile_name=profile)
    return boto3.client("workspaces", region_name=region)

def restart_workspace(client, ws_id):


    # response = client.reboot_workspaces(
    #     RebootWorkspaceRequests=[
    #     {
    #         'WorkspaceId': ws_id
    #         },
    #     ]
    # )

    response = "currently not in use"

    return response

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
                get_workspaces_client(client, args.region)
                break
            except Exception as e:
                clear()
                print(e)
                print("\n\n")
                time.sleep(2)
        else:
            clear()
    return client

def get_user():

    if not args.profile: 
        client = get_client_profile()
    else:
        client = args.profile
    client = get_workspaces_client(client, args.region)

    # IF User ID is stil required
    user_id = ""
    if not args.argument: 
        while True:
            if not args.argument:
                clear()
                user_id = input("Enter User ID:  ")
            if user_id:
                break
    else:
        user_id = args.argument

    
    workspaces = get_workspaces(client)
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
        
def get_workspaces_list(client):

    workspaces = get_workspaces(client)

    clear()
    for workspace in workspaces:
        pp.pprint("Workspace User: {}".format(workspace['UserName']))
    pp.pprint("Total Workspaces: {}".format(len(workspaces)))


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
        workspaces_client = get_workspaces_client(client, args.region)
        get_workspaces_list(workspaces_client)
    if selection == "2":
        get_user()
    if selection == "3":
        print("This is currently not in use")
        exit()
    if selection == "4":
        exit()

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-p",
        "--profile",
        help="Client name.  This needs to be set under your .aws/config file",
        required=False,
    )

    parser.add_argument(
        "-c",
        "--command",
        help="provide a command to run. Current_Commands: list_workspaces, get_user and reboot_workspaces",
        required=False,
    )

    parser.add_argument(
        "-r",
        "--region",
        help="Region, provides a region for the application to run in",
        default="ap-southeast-2",
        required=False,
    )

    parser.add_argument(
        "-a",
        "--argument",
        help="Argument, this is extra arguments to provide to the app (like the username)",
        required=False,
    )


    args = parser.parse_args(sys.argv[1:])
    pp = pprint.PrettyPrinter(width=41, compact=True)

    client = get_workspaces_client(args.profile, args.region)

    menu()

    if args.command == "list_workspaces":
        workspaces = get_workspaces(client)

        clean = ""

        for workspace in workspaces:

            clean += "Username:     {}\n".format(workspace['UserName'])
            clean += "ComputerName: {}\n".format(workspace['ComputerName'])
            clean += "DirectoryId:  {}\n".format(workspace['DirectoryId'])
            clean += "------------------\n"

        print(clean)
        print("total workspaces: {}".format(len(workspaces)))

    if args.command == "get_user":
        if not args.argument:
            print("ERROR: -a needs to be defined to search for a user \nExample: workspaces -p stockland-prod -c get_user -a a_joelh")
        else:
            workspaces = get_workspaces(client)
            ws = ""

            for workspace in workspaces:
                if workspace['UserName'] == args.argument:
                    ws += "Username:     {}\n".format(workspace['UserName'])
                    ws += "ComputerName: {}\n".format(workspace['ComputerName'])
                    ws += "DirectoryId:  {}\n".format(workspace['DirectoryId'])

            if ws:
                print(ws)
            else:
                print("User Not Found")

    if args.command == "restart_workspace":
        if not args.argument:
            print("ERROR: -a needs to be defined to search for a user's workspace to reboot \nExample: workspaces -p stockland-prod -c restart_workspace -a a_joelh")
        else:
            workspaces = get_workspaces(client)
            ws_id = ""
            ws = ""

            for workspace in workspaces:
                if workspace['UserName'] == args.argument:
                    ws_id += workspace["WorkspaceId"] 
                    ws += "Username:     {}\n".format(workspace['UserName'])
                    ws += "ComputerName: {}\n".format(workspace['ComputerName'])
                    ws += "DirectoryId:  {}\n".format(workspace['DirectoryId'])
                    ws += "WorkspaceID:  {}\n".format(ws_id)
            
            response = ""
            
            while True:
                print("\n\n\nselected workspace")
                print("------------------\n")
                print(ws)
                print("\n")
                confirm = input('[y]Yes or [n]No: ')
                if confirm.strip().lower() in ('y'):
                    response = restart_workspace(client, ws_id)
                    break
                if confirm.strip().lower() in ('n'):
                    response = "reboot cancelled"
                    break
                print("\n Invalid Option. Please Enter a Valid Option.")
                

            print(response)