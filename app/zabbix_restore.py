import argparse
from zabbixbackuputils import *
from zabbixrestoreutils import *
import sys


#zabbix_restore() function calls restore functions from zabbixrestoreutils and restores either database or configuration
#or both.

def zabbix_restore(args):
    if not (args.file.endswith(".sql") or args.file.endswith(".tar.gz")):
        print(" Unsupported file type!!! ")
        sys.exit()
    else:
        if args.only_database:
            print("Stopping Zabbix Server ...")
            zabbix_server_stop()
            print("Stopped ..." + "\n" + "Starting Zabbix Server Database restore ...")
            zabbix_restore_database(args.file)
            print(" **** Successfully restored Zabbix Server database! **** ")
            print("Starting Zabbix Server ...")
            zabbix_server_start()
            print("Started!!!")
        elif args.only_config:
            if args.file.endswith(".sql"):
                print("Please, provide archive file with .tar.gz extension ...")
                sys.exit()
            else:
                print("Stopping Zabbix Server ...")
                zabbix_server_stop()
                print("Stopped ..." + "\n" + "Starting Zabbix Server configuration restore ...")
                zabbix_restore_config(args.file)
                print(" **** Successfully restored Zabbix Server configuration! **** ")
                print("Starting Zabbix Server ...")
                zabbix_server_start()
                print("Started!!!")
        else:
            if args.file.endswith(".sql"):
                print("Please, provide archive file with .tar.gz extension ...")
                sys.exit()
            else:
                print("Stopping Zabbix Server ...")
                zabbix_server_stop()
                print("Stopped ..." + "\n" + "Starting Zabbix Server Database restore ...")
                zabbix_restore_database(args.file)
                print(" **** Successfully restored Zabbix Server database! **** ")
                print("Starting Zabbix Server configuration restore ...")
                zabbix_restore_config(args.file)
                print(" **** Successfully restored Zabbix Server configuration! **** ")
                print("Starting Zabbix Server ...")
                zabbix_server_start()
                print("Started!!!")



#create cli argument parser using python argparse framework

parser = argparse.ArgumentParser()
parser.add_argument("-v", "--version", action="version", version="1.0.0") #add --version option
parser.add_argument("-f", "--file", help="absolute path to backup file", required=True) #add --file option
parserGroup = parser.add_mutually_exclusive_group()
parserGroup.add_argument("-d", "--only_database", action="store_true", help="restore only database")
parserGroup.add_argument("-c", "--only_config", action="store_true", help="restore only configuration")
parser.set_defaults(func=zabbix_restore) #set default function for zabbix restore


#main function for zabbix-restore entry point

def restorefunc():
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    restorefunc()
