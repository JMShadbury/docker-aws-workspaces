import menu
import os
import time
import pprint
import boto3

clear = lambda: os.system('clear')
pp = pprint.PrettyPrinter(width=41, compact=True)

# Get a report of all workspaces, the report will provide a list of alwayson vs auto stop workspaces and the cost of upgrading them to a different compute type
def report(client_profile, region):
    '''
    This function will get a report of all workspaces, the report will provide a list of alwayson vs auto stop workspaces and the cost of upgrading them to a different compute type
    :param client_profile: the client profile to use
    :param region: the region to use
    :return: the report
    '''

    # initialize variables
    client = client_profile
    region = region

    # If client isn't provided, get the client
    if not client:
        client_profile = get_client_profile(client, region)

    # Get the boto3 workspaces client
    client = get_workspaces_client(client_profile, region)

    # Get all workspaces
    workspaces = get_workspaces(client)

    # Initialize variables
    always_on = []
    auto_stop = []
    always_on_cost = 0
    auto_stop_cost = 0

    # Get the cost of each workspace
    for workspace in workspaces:
            
            # If the workspace is always on, add it to the always on list
            if workspace['RunningMode'] == "ALWAYS_ON":
                always_on.append(workspace)
    
            # If the workspace is auto stop, add it to the auto stop list
            elif workspace['RunningMode'] == "AUTO_STOP":
                auto_stop.append(workspace)

    # Get the cost of each workspace
    for workspace in always_on:
        if workspace['ComputeTypeName'] == "VALUE":
            always_on_cost += 23.20
        elif workspace['ComputeTypeName'] == "STANDARD":
            always_on_cost += 30.40
        elif workspace['ComputeTypeName'] == "PERFORMANCE":
            always_on_cost += 41.60
        elif workspace['ComputeTypeName'] == "POWER":
            always_on_cost += 79.20
        elif workspace['ComputeTypeName'] == "GRAPHICS":
            always_on_cost += 117.60

    # Get the cost of each workspace
    for workspace in auto_stop:
        if workspace['ComputeTypeName'] == "VALUE":
            auto_stop_cost += (0.18*83) + 8
        elif workspace['ComputeTypeName'] == "STANDARD":
            auto_stop_cost += (0.26*83) + 8
        elif workspace['ComputeTypeName'] == "PERFORMANCE":
            auto_stop_cost += (0.42*83) + 8
        elif workspace['ComputeTypeName'] == "POWER":
            auto_stop_cost += (0.68*83) + 8
        elif workspace['ComputeTypeName'] == "GRAPHICS":
            auto_stop_cost += (1.34*83) + 8

    
    # float to 2 decimal places
    always_on_cost = "{:.2f}".format(always_on_cost)
    auto_stop_cost = "{:.2f}".format(auto_stop_cost)

    total_cost = float(always_on_cost) + float(auto_stop_cost)

    # Print the report
    clear()
    print("Always On Workspaces: {}".format(len(always_on)))
    print("Auto Stop Workspaces: {}".format(len(auto_stop)))
    print("\n")
    print("Always On Cost: ${}".format(always_on_cost))
    print("Auto Stop Cost: ${}".format(auto_stop_cost))
    print("\n")
    print("Total Workspaces: {}".format(len(workspaces)))
    print("Total Cost: ${}".format(total_cost))
    exit()


def get_workspaces_client(profile, region):
    """
    Connect to AWS APIs
    :return: workspaces client
    """

    # Setup a session with AWS
    boto3.setup_default_session(profile_name=profile)

    # Use the session and get the workspaces boto3 client
    return boto3.client("workspaces", region_name=region)


def aws_function(_aws_function, **kwargs):
    '''
    This function will attempt to run the provided function and return the response
    If the function fails, it will retry the function until it succeeds
    :param _aws_function: the function to run
    :param kwargs: the arguments to pass to the function
    :return: the response from the function
    '''

    return _aws_function(**kwargs)


def get_workspaces(client):
    '''
    This function will get all workspaces in the account
    :param client: the workspaces client
    :return: a list of all workspaces
    '''

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
            elif "AccessDenied" in str(e):
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


def restart_workspace(client, ws_id):
    '''
    This function will restart a workspace
    :param client: the workspaces client
    :param ws_id: the workspace id to restart
    :return: the response from the restart
    '''

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

def get_client_profile(client_profile, region):
    '''
    This function will get the client profile to use
    :param client_profile: the client profile to use
    :param region: the region to use
    :return: the client profile to use
    '''

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


def get_workspaces_list(client):
    '''
    This function will get the list of workspaces
    :param client: the workspaces client
    :return: the list of workspaces
    '''

    # Get list of workspaces
    workspaces = get_workspaces(client)

    clear()

    # Print the list of users who have workspaces
    for workspace in workspaces:
        pp.pprint("Workspace User: {}".format(workspace['UserName']))

    # Print the total count of all workspaces
    pp.pprint("Total Workspaces: {}".format(len(workspaces)))



def get_user(client_profile,region, user_id):
    '''
    This function will get the user's workspace details
    :param client_profile: the client profile to use
    :param region: the region to use
    :param user_id: the user id to search for
    :return: the user's workspace details
    '''

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
            ws += "\nUsername:     {}\n".format(workspace['UserName'])
            ws += "ComputerName: {}\n".format(workspace['ComputerName'])
            ws += "DirectoryId:  {}\n".format(workspace['DirectoryId'])
            ws += "State:        {}\n".format(workspace['State'])
            ws += "----------------------\n"

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