import datetime
import argparse
from zabbixbackuputils import *


#zabbix_backup_archive() function calls backup functions from zabbixbackuputils and creates timestamped backup archive

def zabbix_backup_archive(args):
    backup_files = "config databases httpd" #defines directories to backup
    cmd = "tar cvfz zabbix_backup_{0}.tar.gz {1} && /usr/bin/rm -rf {1}" #archiving command
    time = str(datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")) #timestamp
    print("Stopping Zabbix Server ...")
    zabbix_server_stop()
    zabbix_database_backup(args.backup_path)
    zabbix_config_backup(args.backup_path)
    zabbix_httpd_backup(args.backup_path)
    print("Starting Zabbix Server ...")
    zabbix_server_start()
    p = subprocess.Popen(cmd.format(time, backup_files), stdout=subprocess.PIPE, shell=True, cwd=args.backup_path)
    p.communicate()
    p.wait()
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

