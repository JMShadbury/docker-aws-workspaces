import argparse
import sys
import menu
import workspace_functions


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


    # If the -c is provided with "list_workspaces"
    if args.command == "list_workspaces":
        workspace_functions.get_workspaces_list(args.profile)

    # If the -c is provided with "get_user"
    if args.command == "get_user":
        workspace_functions.get_user(args.profile,args.region,args.argument)
        exit()


    #display menu
    menu.menu(args.profile,args.region, args.argument)