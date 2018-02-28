import subprocess
import os

#stops  Zabbix Server

def zabbix_server_stop():
    cmd = "systemctl stop zabbix-server.service"
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    p.communicate()
    p.wait()


#starts Zabbix Server

def zabbix_server_start():
    cmd = "systemctl start zabbix-server.service"
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    p_status = p.wait()
    output = str(output.decode('utf-8'))
    return output


#backes up Zabbix Server database

def zabbix_database_backup(backup_path):
    cmd = "mysqldump --all-databases > {0}/dump.sql"
    backup_folder = "{0}/databases".format(backup_path)
    if not os.path.isdir(backup_folder):
        os.makedirs(backup_folder)
    p = subprocess.Popen(cmd.format(backup_folder), stdout=subprocess.PIPE, shell=True)
    p.communicate()
    p.wait()

#backes up Zabbix Server config

def zabbix_config_backup(backup_path):
    cmd = "cp -r /etc/zabbix {0}"
    backup_folder = "{0}/config/".format(backup_path)
    if not os.path.isdir(backup_folder):
        os.makedirs(backup_folder)
    p = subprocess.Popen(cmd.format(backup_folder), stdout=subprocess.PIPE, shell=True)
    p.communicate()
    p.wait()


#backes up Zabbix httpd config

def zabbix_httpd_backup(backup_path):
    cmd = "cp /etc/httpd/conf.d/zabbix.conf {0}"
    backup_folder = "{0}/httpd/".format(backup_path)
    if not os.path.isdir(backup_folder):
        os.makedirs(backup_folder)
    p = subprocess.Popen(cmd.format(backup_folder), stdout=subprocess.PIPE, shell=True)
    p.communicate()
    p.wait()


#removs old backup files to save storage space

def zabbix_backups_rotate(backup_path, num_of_copies):
    files = os.listdir(backup_path)
    backupFiles = [f for f in files if f.endswith(".tar.gz")]
    preserve = sorted(backupFiles)[-num_of_copies:]
    for file in backupFiles:
        if file not in preserve:
            os.remove(os.path.join(backup_path, file))
