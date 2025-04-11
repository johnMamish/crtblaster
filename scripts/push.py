#!/usr/bin/env python3

import argparse
import os
import subprocess
import sys

def find_proj_root(dirname):
    # Start from the directory of this script
    current = os.path.abspath(os.path.dirname(__file__))

    while True:
        if (os.path.basename(current) == dirname):
            return current
        parent = os.path.dirname(current)

        # If there's nowhere else to go (reached root), fail
        if (parent == current):
            return None

        current = parent

def main():
    parser = argparse.ArgumentParser(
        description="Push a local folder to a remote host and run a command in the background."
    )
    parser.add_argument("username", help="User name on remote host.")
    parser.add_argument("host", help="Hostname or IP address.")
    parser.add_argument(
        "remote_path",
        nargs="?",
        default="~",
        help="Path on the remote host (default: user’s home)."
    )

    args = parser.parse_args()

    folder = find_proj_root("crtblaster")
    user = args.username
    host = args.host
    remote_path = args.remote_path

    if (folder is None):
        print(f"Couldn't find root dir, make sure you're executing from within crtblaster project")
        sys.exit(-1)

    print(f"Pushing '{folder}' to {user}@{host}:{remote_path} ...")
    try:
        subprocess.run(
            ["rsync", "-av", "--exclude", ".git", folder, f"{user}@{host}:{remote_path}"],
            check=True
        )
    except subprocess.CalledProcessError:
        print(f"Failed to push {folder} to {user}@{host}:{remote_path}.")
        sys.exit(-1)

    sys.exit(0)

    print(f"Running 'foo.py' on {user}@{host} in the background ...")
    # Use nohup so it keeps running after SSH disconnects; redirect output to /dev/null
    try:
        subprocess.run(
            ["ssh", f"{user}@{host}", "nohup foo.py > /dev/null 2>&1 &"],
            check=True
        )
    except subprocess.CalledProcessError:
        print(f"Failed to run foo.py on {user}@{host}.")
        return

    print("Done. foo.py is running in the background on the remote host.")

if __name__ == "__main__":
    main()
