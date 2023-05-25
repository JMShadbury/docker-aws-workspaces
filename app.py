import argparse
import sys
import pprint
import workspaces_functions
import client_functions


if __name__ == "__main__":

    # Arguments provided to the app

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


    # initialize variables
    args = parser.parse_args(sys.argv[1:])

    # get workspaces client
    client = workspaces_functions.get_workspaces_client(args.profile, args.region)


    # If the -c is provided with "list_workspaces"
    if args.command == "list_workspaces":
        client_functions.get_workspaces_list()

    # If the -c is provided with "get_user"
    if args.command == "get_user":
        client_functions.get_user(args.argument)


    #display menu
    client_functions.menu()