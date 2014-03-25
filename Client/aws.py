__author__ = 'harry'
import login
import argparse
import getpass

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="start AWS.")
    parser.add_argument('--username', '-u', help='Username for GUI-less login')
    parser.add_argument('--password', '-p', help='Password for GUI-less login')
    args = vars(parser.parse_args())
    if args['username'] == None:
        login.startLogin()
    elif args['password'] == None:
        args['password'] = getpass.getpass()
