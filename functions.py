import menu
import os
import time
import pprint
import boto3

clear = lambda: os.system('clear')
pp = pprint.PrettyPrinter(width=41, compact=True)


##############################
# Gets the workspaces client #
##############################
def get_workspaces_client(profile, region):
    """
    Connect to AWS APIs
    :return: workspaces client
    """

    # Setup a session with AWS
    boto3.setup_default_session(profile_name=profile)

    # Use the session and get the workspaces boto3 client
    return boto3.client("workspaces", region_name=region)


#####################################
# Function to execute aws functions #
#####################################
def aws_function(_aws_function, **kwargs):
    return _aws_function(**kwargs)

##################################
# function to get all workspaces #
##################################
def get_workspaces(client):
    """
    Returns existing workspaces details
    :param client: a boto3 workspaces client
    :return flat_list:  list of workspaces with relevant details
    """

    # Initialize variable
    _all_workspaces = []

    # AWS may throttle the connection, this will retry unless the error is due to an expired token
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

    # Profile a list of workspaces and include selected attributes below
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
                    ],
                    "State" : workspace['State']
                }
            )
        if "NextToken" not in res_workspaces:
            break

        # AWS may throttle the connection, at this point, there should be no errors that should kill this attempt
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

#################################
# Function to restart workspace #
#################################
def restart_workspace(client, ws_id):

    #TODO Create a dynamic switch for cases where users have more than one workspace
    # response = client.reboot_workspaces(
    #     RebootWorkspaceRequests=[
    #     {
    #         'WorkspaceId': ws_id
    #         },
    #     ]
    # )

    response = "currently not in use"

    return response

############################################################
# Function to get the client profile to be used in the app #
############################################################
def get_client_profile(client_profile, region):

    # Initialize variable
    client = client_profile
    clear()

    # If client is not provided, get the client profile to use
    if not client:
        while True:
            print("Client Profile Required")
            print("-----------------------\n")
            print("Please enter Client Profile")
            print("A client profile is required so the app knows what aws account to use.")
            print("Example: runcmd-test")
            print("\ntype 4 to exit...")
            client = input("Enter Client Profile:   ")

            # if 4, go back to the menu
            if client == "4":
                menu.menu()

            # if client entered
            elif client:

                # confirm the profile exists
                try:
                    get_workspaces_client(client, region)
                    break

                # Print error if the profile doesn't exist
                except Exception as e:
                    clear()
                    print(e)
                    print("\n\n")
                    time.sleep(2)
            else:
                clear()
    return client

#################################################################
# function to get all workspaces and print them to the terminal #
#################################################################
def get_workspaces_list(client):

    # Get list of workspaces
    workspaces = get_workspaces(client)

    clear()

    # Print the list of users who have workspaces
    for workspace in workspaces:
        pp.pprint("Workspace User: {}".format(workspace['UserName']))

    # Print the total count of all workspaces
    pp.pprint("Total Workspaces: {}".format(len(workspaces)))



###############################
# Function to search for user #
###############################
def get_user(client_profile,region, user_id):

    # initialize variables
    client = client_profile

    # If client isn't provided, get the client
    if not client:
        client_profile = get_client_profile(client, region)

    # Get the boto3 workspaces client
    client = get_workspaces_client(client_profile, region)

    clear()

    # If user_id not provided
    if not user_id:

        # Get the client profile
        user_id = input("Enter User ID:  ")
    

    # Get all workspaces
    workspaces = get_workspaces(client)
    ws = ""
    for workspace in workspaces:

        # if the workspace's username is equal to the username being searched, save the details to print after
        if workspace['UserName'] in user_id:
            ws += "Username:     {}\n".format(workspace['UserName'])
            ws += "ComputerName: {}\n".format(workspace['ComputerName'])
            ws += "DirectoryId:  {}\n".format(workspace['DirectoryId'])
            ws += "State:        {}\n".format(workspace['State'])

    # If a workspace was found, print the details
    if ws:
        clear()
        print(ws)
        exit()

    # If no workspaces are found, print error
    else:
        clear()
        print("User Not Found")
        exit()