import argparse
from zabbixbackuputils import *
from zabbixrestoreutils import *


#zabbix_restore() function calls restore functions from zabbixrestoreutils and restores either database or configuration
#or both.

def zabbix_restore(args):
    print("Stopping Zabbix Server ...")
    zabbix_server_stop()
    if args.only_database:
        zabbix_restore_database(args.file)
        print(" **** Successfully restored Zabbix Server database! **** ")
    elif args.only_config:
        zabbix_restore_config(args.file)
        print(" **** Successfully restored Zabbix Server configuration! **** ")
    else:
        zabbix_restore_database(args.file)
        zabbix_restore_config(args.file)
        print(" **** Successfully restored Zabbix Server database and configuration! **** ")
    print("Starting Zabbix Server ...")
    zabbix_server_start()


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
