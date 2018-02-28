import datetime
import argparse
from zabbixbackuputils import *


#zabbix_backup_archive() function calls backup functions from zabbixbackuputils and creates timestamped backup archive

def zabbix_backup_archive(args):
    backup_files = "config databases httpd" #defines directories to backup
    cmd = "tar cvfz zabbix_backup_{0}.tar.gz {1} && rm -rf {1}" #archiving command
    time = str(datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")) #timestamp
    print("Stopping Zabbix Server ...")
    zabbix_server_stop()
    print("Stopped ..." + "\n" + "Starting Zabbix Server Database backup ...")
    zabbix_database_backup(args.backup_path)
    print("Finished Database backup ..." + "\n" + "Starting Zabbix Server configuration backup ...")
    zabbix_config_backup(args.backup_path)
    print("Finished Configuration backup ..." + "\n" + "Starting Zabbix Server HTTPD Configuration backup ...")
    zabbix_httpd_backup(args.backup_path)
    print("Zabbix Server backup completed ..." + "\n" + "Starting Zabbix Server ...")
    zabbix_server_start()
    print("Started ..." + "\n" + "Archiving backup files ...")
    p = subprocess.Popen(cmd.format(time, backup_files), stdout=subprocess.PIPE, shell=True, cwd=args.backup_path)
    p.communicate()
    p.wait()
    print("Archiving completed ..." + "\n" + "Removing old backup archives ...")
    zabbix_backups_rotate(args.backup_path, args.number_of_copies) #deletes old backup archives
    print(" **** Successfully finished Zabbix Server backup and archiving! **** ")


#create cli argument parser using python argparse framework

parser = argparse.ArgumentParser()
parser.add_argument("-v", "--version", action="version", version="1.0.0") #add --version option
parser.add_argument("-b", "--backup_path", help="absolute path to backup folder", required=True) #add --backup-path option
parser.add_argument("-n", "--number_of_copies", help="number of backup copies to keep", type=int, required=True) #add --number-of-copies option
parser.set_defaults(func=zabbix_backup_archive) #set default function for zabbix server backup


#main function for zabbix-backup entry point

def backupfunc():
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    backupfunc()
