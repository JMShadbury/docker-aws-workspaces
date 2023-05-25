import boto3



# Gets the workspaces client
def get_workspaces_client(profile, region):
    """
    Connect to AWS APIs
    :return: workspaces client
    """

    boto3.setup_default_session(profile_name=profile)
    return boto3.client("workspaces", region_name=region)

# Function to execute aws functions
def aws_function(_aws_function, **kwargs):
    return _aws_function(**kwargs)


# function to get all workspaces 
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


# Function to restart workspace
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