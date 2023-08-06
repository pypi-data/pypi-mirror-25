#Author: Integra
#Dev: Partha

import os, shutil
from sftp_api import SFTApi
from boto.s3.connection import S3Connection,Key
from sunrise.contrib.cloud.views import aws_s3
from sunrise_cloud_api import SunriseCloud
from django.conf import settings
from celery import shared_task
from celery.contrib import rdb
from sync_master import connect_to_ftp_server, sync_ftp_with_s3_and_cloud
from datetime import datetime
from sunrise.contrib.jobs.signals import message_logger,process_logger,close_process


def FTPScheduler(**kwargs): 
    if 'request_id' not in kwargs.keys() and 'id' not in kwargs.keys():
        raise Exception("Redirect to Failure")  
    assert('process_number' in kwargs.keys()), "Process Error need Process ID"
    assert('process_name' in kwargs.keys()), "Process Error need Process Name"    
    from setup.models import FtpSyncDtl, FtpSyncRules
    dtl = FtpSyncDtl.objects.get(job_id_id=kwargs['id'])          
    request_id = kwargs['request_id']
    process_id = kwargs['process_number']
    process_name = kwargs['process_name']
    sync_rules = FtpSyncRules.objects.filter(sync_id=kwargs['id'])
    logger = kwargs['logger']
    #Preparing connector
    connector = {
        'FTP_DOMAIN': dtl.ftp_domain,
        'FTP_PORT': int(dtl.ftp_port),
        'FTP_USERNAME': dtl.ftp_username,
        'FTP_PASSWORD': dtl.ftp_password,
        'logger':logger
    }

    #Initiating connection
    connected_to_ftp_server, sftpObj, connection_status_message = connect_to_ftp_server(connector)
    
    if not connected_to_ftp_server is True:
        #Log here
        print "CLose here"
        close_process(False,process_name,request_id) ##Exit on connection failure
    else:
        print "log here"
        message_logger(process_id,request_id, "Gen", "S905", logger,**{'message':'Successfully connected to FTP Server'})            
    #Proceed on successfull connection
    #Syncing rules
    for rule in sync_rules:
        if rule.status == True:
            if rule.ftp_blank_files_path == "":
                blank_files_path = None
            else:
                blank_files_path = rule.ftp_blank_files_path
            sync_ftp_with_s3_and_cloud(
                        connection = sftpObj, 
                        source = rule.source, #FTP Path 
                        destination = rule.cloud_ftp_container, #Cloud path
                        pattern = rule.file_pattern, 
                        delete_from_ftp = rule.keep_original, 
                        blank_files_path = blank_files_path,
                        prefix = str(rule.prefix) if rule.prefix is not None else None, 
                        append_date = rule.append_date,
                        logger = logger,
                        process_id = process_id,
                        request_id = request_id)
    close_process(False,process_name,request_id)
