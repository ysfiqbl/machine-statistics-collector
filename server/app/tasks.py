"""
This file contains the celery task that executes the client script, writes the result
to the database and sends the email to the client.
"""

from __future__ import absolute_import

import time
import traceback
import os
import smtplib
import calendar
import json
import paramiko

from email.mime.text import MIMEText
from app.celery import celery_app
from app.models.statistic import Statistic
from app.models.email import Email
from app.remote_script import AESCipher, key
from app.settings import (
    APP_HOME, 
    CLIENT_COMPILED_SCRIPT_NAME, 
    MAIL_DEFAULT_SENDER,
    MAIL_SERVER, MAIL_PORT, MAIL_USE_TLS, MAIL_USE_SSL,
    MAIL_USERNAME, MAIL_PASSWORD,
    MAIL_TO_SEND, MAIL_SENDING, MAIL_SENT, MAIL_FAILED,
)



@celery_app.task()
def collect_statistics(client):
    """
    Celery task that does the following
    1. Establishes an SSH connection to the client
    2. Creates a temp directory on the client machine
    2. Uploads the script that needs to be executed on the client to the temp directory
    3. Executes the scripts
    4. Decrypt's the returned value of the script
    5. Writes the decrypted result to the database
    6. Sends an email to the email confingured in config.xml for the client 

    :param client: json representation of the XML object of the client defined in the config.xml file
    :return: decrypted result of the statistics collected from the client
    """

    sftp_client = None
    statistics = None
    decrypted_result = None

    try:
        tmp_dir ='{0}_mstats'.format(calendar.timegm(time.gmtime()))
        src_script_path = os.path.join(APP_HOME, CLIENT_COMPILED_SCRIPT_NAME)
        dst_script_path = os.path.join(tmp_dir, CLIENT_COMPILED_SCRIPT_NAME)


        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        ssh_client.connect(hostname=client['ip'], username=client['username'], password=client['password'])


        sftp_client = ssh_client.open_sftp()
        dirs = sftp_client.listdir('.')
        if dir_exists(dirs, tmp_dir) is False:
            sftp_client.mkdir(tmp_dir)
            
        sftp_client.put(src_script_path, dst_script_path)
        stdin, stdout, stderr = ssh_client.exec_command('python {0}'.format(dst_script_path))
        encrypted_result = stdout.readlines()

        encrypted_result = encrypted_result[0].strip('\n')
        print('\n[Encrypted Result from {0}]: {1}\n\n'.format(client['ip'], encrypted_result))

        decryptor = AESCipher(key)
        decrypted_result = decryptor.decrypt(encrypted_result)
        print('\n[Decrypted Result from {0}]: {1}\n\n'.format(client['ip'], decrypted_result))
        
        print(sftp_client.listdir('.'))
        files = sftp_client.listdir(tmp_dir)

        for f in files:
            sftp_client.remove(os.path.join(tmp_dir, f))

        sftp_client.rmdir(tmp_dir)
        sftp_client.close()

        statistic = Statistic(ip=client['ip'], response=decrypted_result)
        statistic = statistic.save()
        
        message = get_message(client, decrypted_result)
        send_email(client['mail'], '[Statistics for {0}]'.format(client['ip']), message)
    except IOError, e:
        traceback.print_exc()
    finally:
        if sftp_client is not None:
            sftp_client.close()
        if statistics is not None:
            statistic.close_session()

    return decrypted_result


def dir_exists(dirs, dir):
    """
    Check whether a given string exists in a list.

    :param dirs: list of directory names
    :param dir: name directory to find in dirs
    :param message: email message body
    """
    for d in dirs:
        if dir == d:
            return True
    
    return False


def send_email(to, subject, message):
    """
    Send email alert to email specified in the settings file.

    :param to: email recipient
    :param subject: email subject
    :param message: email message body
    """
    email = Email(to=to, sender=MAIL_DEFAULT_SENDER, message=message, status=1)
    email = email.save()
    email.status = MAIL_SENDING
    email = email.save()
    server = None
    try:        
        server = smtplib.SMTP(MAIL_SERVER, MAIL_PORT)
        server.ehlo()
        if MAIL_USE_TLS:
            server.starttls()
        
        server.ehlo()
        
        server.login(MAIL_USERNAME, MAIL_PASSWORD)
        
        msg = MIMEText(email.message)
        msg['Subject'] = subject
        msg['To'] = email.to
        msg['From'] = email.sender

        server.sendmail(email.sender,email.to, msg.as_string())
        email.status = MAIL_SENT
        email.save()

    except:
        email.status = MAIL_FAILED
        email = email.save()
    finally:
        if server is not None:
            server.close()

    return None


def get_message(client, statistics):
    """
    Construct email body. If the machine statistics limits are reached
    these statistics will be included in the message body

    :param client: json representation of the XML object of the client defined in the config.xml file
    :param statistics: decrypted result of the script executed on the client
    :return message: email body
    """
    statistics = json.loads(statistics)
    alerts = get_alerts(client, statistics)
    message = 'Machine with IP ' + client['ip']
    if len(alerts) > 0:
        message += ' has the alerts below\n'
        alert_message = '\n'.join(alerts)
        message += alert_message
    else:
        message += ' has no alerts'

    message += '\nTotal uptime for the machine is ' + statistics['uptime']

    return message


def get_alerts(client, statistics):
    """
    :param client: json representation of the XML object of the client defined in the config.xml file
    :param statistics: json object of the script executed on the client
    :return alerts: list of alerts
    """
    alert_configs = client['alerts']
    alerts = []
    
    for alert_config in alert_configs:
        alert_limit = float(alert_config['limit'].strip('%'))
        alert_type = alert_config['type']
        if statistics[alert_type] > alert_limit:
            alerts.append('{0} : {1}%'.format(alert_type, statistics[alert_type]))
        
    return alerts