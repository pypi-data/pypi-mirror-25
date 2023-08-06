#Author: Integra
#Dev: Partha
#Description: This module will download the files from ftp and then sync to s3 and then to cloud.
#Note: wait, if you're trying to modify the code, please give me a call.

import os, tarfile, paramiko, tempfile
from stat import S_ISDIR
from django.conf import settings
from sunrise.contrib.jobs.signals import message_logger,process_logger,close_process
from boto.s3.connection import S3Connection,Key
from sunrise.contrib.cloud.views import aws_s3
from datetime import datetime
import fnmatch
from celery.contrib import rdb
from sunrise_cloud_api import SunriseCloud

BACKUP_S3_LOCATION = settings.FTP_BACKUP_S3_BUCKET

def log_success(process_id, request_id, logger, message):
    message_logger(process_id,request_id, "Gen", "S905", logger,**{'message':message})            


def log_warning(process_id, request_id, logger, message):
    message_logger(process_id,request_id, "Gen", "S905", logger,**{'message':message})           
    #msg_log(process_id,request_id, "Gen", "W001", **{'message':message})


def log_error(process_id, request_id, logger, message):
    message_logger(process_id,request_id, "Gen", "S905", logger,**{'message':message})            
    
    #msg_log(process_id,request_id, "Gen", "W001", **{'message':message})
    #msg_log(process_id,request_id, "Gen", "E900", **{'message':message})


def connect_to_backup_bucket():
    """ This is used to connect to the backup bucket """
    AWS_ACCESS_KEY_ID = settings.AWS_ACCESS_KEY_ID
    AWS_SECRET_ACCESS_KEY = settings.AWS_SECRET_ACCESS_KEY
    S3_BUCKET = BACKUP_S3_LOCATION
    conn = S3Connection(AWS_ACCESS_KEY_ID,AWS_SECRET_ACCESS_KEY)
    buck = conn.get_bucket(S3_BUCKET)
    return buck

def connect_to_ftp_server(connector):
    """ This is used to connect to ftp serve
        @output: (True/False, sftpObj, message)
    """
    # 1. Parameter Check
    assert('FTP_DOMAIN' in connector.keys()), "Please provide keyword arg FTP_DOMAIN"
    assert('FTP_USERNAME' in connector.keys()), "Please provide keyword arg FTP_USERNAME"
    assert('FTP_PASSWORD' in connector.keys()), "Please provide keyword arg FTP_PASSWORD"
    assert('FTP_PORT' in connector.keys()), "Please provide keyword arg FTP_PORT"
    
    # 2. Connecting to FTP Server
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(connector['FTP_DOMAIN'], username = connector['FTP_USERNAME'], password = connector['FTP_PASSWORD'])
        transport = paramiko.Transport((connector['FTP_DOMAIN'], int(connector['FTP_PORT'])))
        transport.connect(username = connector['FTP_USERNAME'], password = connector['FTP_PASSWORD'])
        sftp = paramiko.SFTPClient.from_transport(transport)
    except Exception, e: 
        return (False, None, str(e))
    return (True, sftp, "Connected Successfully")

def all_files(sftpObj, remotepath):
    # Kindof a stripped down  version of os.walk, implemented for 
    # sftp.  Tried running it flat without the yields, but it really
    # chokes on big directories.
    path = remotepath
    files = []
    folders = []
    for f in sftpObj.listdir_attr(remotepath):
        if S_ISDIR(f.st_mode):
            folders.append(f.filename)
        else:
            files.append(f.filename)
    yield path,folders,files
    for folder in folders:
        new_path = os.path.join(remotepath, folder)
        for x in all_files(sftpObj, new_path):
            yield x

def report_via_email(subject, message):
    to_list = ["sagar@aptuz.com", "partha@aptuz.com"]
    domain = ""
    

def create_location(filename):
    """ This will create a directory recursively"""
    try:
        folder=os.path.dirname(filename)  
        if not os.path.exists(folder):  
            os.makedirs(folder)
        return True
    except:
        return False

def sync_ftp_with_s3_and_cloud(connection = None, source = None, destination = None, pattern = None, blank_files_path = None, prefix = None, append_date = False, delete_from_ftp = False, logger=None, process_id=None, request_id=None):
    """ @connector: This is dictionary used to specify the FTP connection information
        @source: This is the FTP source location from where files need to get downloaded (required: String)
        @destination: This is the cloud path to where these downloaded files need to get placed (required: String)
        @pattern: This is the patten which needs to get matched with the file
        @blank_files_path: This is the Path where we need to place these blank files (if size == 0bytes) (optional:String)
        @prefix: This is the prefix that will be append added first to every filename(optional:String) 
        @append_date: This is boolean value which is used to append datetime after the file name based on its value(default = False)(optional: Boolean)
        @delete_from_ftp: This is boolean value which is used to make decision whether to delete the file from FTP or not (default =False)(optional: Boolean)
        
        @output: return (True/False, message)
    """
    #import pdb;pdb.set_trace()
    # rdb.set_trace()
    #1. Parameter check
    assert(connection is not None), "Please provide the FTP Creds"
    assert(source is not None), "Please provide the FTP Creds"
    assert(destination is not None), "Please provide the FTP Creds"
    assert(type(append_date) is bool), "Please provide the append_date is either True or False"
    assert(type(delete_from_ftp) is bool), "Please provide delete_from_ftp is either True or False"
    assert(logger is not None), "Please provide logger Obj"
    
    if blank_files_path is not None:
        assert(type(blank_files_path) is str or type(blank_files_path) is unicode), "Please provide the blank_files_path as string"
    if prefix is not None:
        assert(type(prefix) is str or type(blank_files_path) is unicode), "Please provide the prefix as string"        
    
    sftpObj = connection

    #4. Initialize necessary tracking parameters
    total_files_list = [] #To maintain all files list
    pattern_matched_files_list = [] #To maintain only pattern matched count
    downloaded_files_success_list = []
    downloaded_files_fail_list = [] #To track downloaded files status
    s3_uploaded_files_success_list = []
    s3_uploaded_files_fail_list  = [] #To track s3 upload status
    cloud_uploaded_files_success_list = []
    cloud_uploaded_files_fail_list = [] #To track cloud upload status
    backup_locations = {}
    cloud_destination = destination
    
    #5. Try to connect to source path
    try:
        sftpObj.chdir(os.path.split(source)[0])
    except Exception, e:
        return (False, str(e)) ##Exit on specified path doesn't exists

    parent = os.path.split(source)[1]

    #6. Try to connect to source sub path
    try:
        sftpObj.stat(parent)
    except Exception, e:
        return (False, str(e)) ##Exit on Specified sub directory not exists

    #7. Create a temparory directory
    today_date_str = "_" + datetime.now().strftime("%Y%m%d")
    temparory_location = tempfile.mkdtemp(suffix= today_date_str)

    #8. Iterate over directory
    for parent_path, subdirectory_names, file_names in all_files(sftpObj, parent):
        for file_name in file_names:
            destination = cloud_destination
            total_files_list.append(os.path.join(parent_path, file_name))
            #8. Check for pattern
            if len(fnmatch.filter([file_name], pattern)) > 0 or file_name == pattern or fnmatch.fnmatch(file_name, pattern):
                #9. Try to download the file to temparory location
                pattern_matched_files_list.append(os.path.join(parent_path, file_name))
                try:
                    temp = parent_path.replace(parent, "", 1)
                    temp = temp[1:] if temp.startswith("/") else temp
                    to_locate = os.path.join(temparory_location, temp, file_name)
                    create_location(to_locate)
                    
                    #Try to download the file
                    is_downloaded = False
                    try:
                        sftpObj.get(os.path.join(parent_path, file_name), to_locate)
                        downloaded_files_success_list.append(os.path.join(parent_path, file_name))    
                        is_downloaded = True
                        log_warning(process_id, request_id, logger,os.path.join(parent_path, file_name) + " Downloaded Successfully")
                    except Exception, e:
                        #Log here
                        log_warning(process_id, request_id, logger,str(e))
                        downloaded_files_fail_list.append(os.path.join(parent_path, file_name))
                        is_downloaded = False 
                    
                    if is_downloaded is not True:
                        continue ## To next file
                    print temparory_location
                    to_file_name = file_name #Preserve original file name
                    
                    #10. Check for prefix                    
                    if prefix is not None:
                        to_file_name = prefix
                    
                    #11. Check for append_date
                    if append_date:
                        if len(to_file_name.split(".")) == 1:
                            to_file_name = to_file_name + "_" + datetime.now().strftime("%Y%m%d")
                        else:
                            to_file_name = ".".join(to_file_name.split(".")[:-1])+"_"+datetime.now().strftime("%Y%m%d")+"."+to_file_name.split(".")[-1]
                    
                    #12. Check for blank file path
                    is_blank_file = False
                    if blank_files_path is not None:
                        if sftpObj.stat(os.path.join(parent_path, file_name)).st_size == 0:
                            if destination.startswith("/") is True:
                                destination = destination[1:]
                            destination = "root/" + destination + "/" + blank_files_path
                            log_success(process_id, request_id, logger,os.path.join(parent_path, file_name) + "is a blank file")
                            is_blank_file = True
                    
                    if is_blank_file is False:
                        to_file_path = parent_path
                        to_file_path = parent_path.replace(parent, "", 1)
                        if to_file_path.startswith("/") is True:
                            to_file_path = to_file_path[1:]
                        destination = "root/" + destination + "/" + to_file_path
                    
                    if destination.endswith("/") is False:
                        destination = destination + "/"
                    
                    #13. try to Connect to s3
                    uploaded_to_s3 = False
                    try:
                        bucket = aws_s3()
                        k = Key(bucket)
                        cloud_location = destination if destination.startswith("root/") is not True else destination.replace("root/", "", 1)
                        k.key = cloud_location + to_file_name
                        print k.key
                        f = open(to_locate, 'r')
                        k.set_contents_from_string(f.read())
                        f.close()
                        s3_uploaded_files_success_list.append(os.path.join(parent_path, file_name))
                        uploaded_to_s3 = True
                        #Log here
                        logger.info(os.path.join(parent_path, file_name) + " S3 upload succeed")
                    except:
                        uploaded_to_s3 = False
                        s3_uploaded_files_fail_list.append(os.path.join(parent_path, file_name))
                        #Log here
                        logger.info(os.path.join(parent_path, file_name) + " S3 upload failed")
                        
                    
                    #14. try to connect to cloud
                    uploaded_to_cloud = False
                    if uploaded_to_s3:
                        try:
                            destination = destination[:-1] if destination.endswith("/") is True else destination #Removing last slash
                            sobj = SunriseCloud()
                            sobj.build(destination)
                            
                            result = sobj.write(destination, to_file_name, 'File',"{0:.2f}".format(round((float(k.size)/1024)*100)/100), "FTP")            
                            if result[0] == True:
                                uploaded_to_cloud = True
                                cloud_uploaded_files_success_list.append(os.path.join(parent_path, file_name))
                                #Log here
                                logger.info(os.path.join(parent_path, file_name) + " Cloud upload succeed") 
                            else:
                                cloud_uploaded_files_fail_list(os.path.join(parent_path, file_name))
                                uploaded_to_cloud = False
                                #Log here
                                logger.info(os.path.join(parent_path, file_name) + " Cloud upload failed")
                                
                        except:
                            cloud_uploaded_files_fail_list(os.path.join(parent_path, file_name))
                            uploaded_to_cloud = False
                            #Log here
                            logger.info(os.path.join(parent_path, file_name) + " Cloud upload failed")
                    
                    #logging status
                    if uploaded_to_s3 is True and uploaded_to_cloud is True:        
                        log_success(process_id, request_id, logger,os.path.join(parent_path, file_name) + " Cloud upload Success")
                    else:
                        log_error(process_id, request_id, logger,os.path.join(parent_path, file_name) + " Cloud upload Failed")
                        
                    #15. backup the file to s3 backup location and don't delete it on remote and also in temparory location'
                    is_file_backup = False
                    if uploaded_to_s3 is not True or uploaded_to_cloud is not True:
                        try:
                            backup_bucket = connect_to_backup_bucket()
                            k = Key(backup_bucket)
                            k.key = file_name + "_" + datetime.now().strftime("%Y%m%d")
                            f = open(to_locate, 'r')
                            k.set_contents_from_string(f.read())
                            f.close()
                            is_file_backup = True
                            backup_locations.update({os.path.join(parent_path, file_name): k.key})
                            #Log here
                            log_success(process_id, request_id, logger,os.path.join(parent_path, file_name) + " Backup done")
                        except:
                            is_file_backup = False
                            #Log here
                            log_warning(process_id, request_id, logger,os.path.join(parent_path, file_name) + " Backup failed")
                    if delete_from_ftp:
                        log_success(process_id, request_id, logger,"Found delete from FTP marker")                                        
                        if uploaded_to_s3 is True and uploaded_to_cloud is True:
                            #16. Remove at remote (remove on successfull upload to s3 and cloud)
                            sftpObj.remove(os.path.join(parent_path, file_name))
                            #Log here
                            log_success(process_id, request_id, logger,"Deleted from FTP server")                                                
                        else:
                            #Log here
                            log_success(process_id, request_id, logger,"Delete from FTP server not attempted")                    
                            
                    #17. Remove locally
                    log_success(process_id, request_id, logger,"Trying to delete at server")                                        
                    # Delete on successfull upload only otherwise keep calm
                    if uploaded_to_s3 is True and uploaded_to_cloud is True:
                        try:
                            os.remove(to_locate)
                        except Exception, e:
                            logger.info("Error in deleting file in server :%s"%str(e))

                        log_success(process_id, request_id, logger,"delete from server Done")                                            
                    else:
                        log_success(process_id, request_id, logger,"delete from local server not attempted due to s3/cloud upload failure")                    
                        log_success(process_id, request_id, logger,"Backup Path: %s"%to_locate)
                except Exception, e:
                    #Log here
                    downloaded_files_fail_list.append(os.path.join(parent_path, file_name))
                    print str(e)
    
    log_success(process_id, request_id, logger,"------------------>REPORT<------------------")
    #Log the sync status
    message = ""
    for item in pattern_matched_files_list:
        log_content = "(%s) - "%item

        if item in downloaded_files_success_list:
            log_content = log_content + "Downloaded: Success "
        else:
            log_content = log_content + "Downloaded: Fail "
            
        if item in s3_uploaded_files_success_list:
            log_content = log_content + "S3 Uploaded: Success "
        else:
            log_content = log_content + "S3 Uploaded: Fail "

        if item in cloud_uploaded_files_success_list:
            log_content = log_content + "Cloud Uploaded: Success "
        else:
            log_content = log_content + "Cloud Uploaded: Fail "
        message = message + log_content
        #Log here
        logger.info(log_content)                    
        print log_content

    logger.info("Failed to Download:%s"%str(len(downloaded_files_fail_list)))
    message = message + "<br /> Failed to Download:" + str(len(downloaded_files_fail_list))
    message = message + "<br />"
    if len(downloaded_files_fail_list) > 0:
        for item in downloaded_files_fail_list:
            #Log here
            log_error(process_id, request_id, logger,str(item))
            message = message + str(item) + "<br />"
            print item
    
    logger.info("Failed to S3 Upload:%s"%str(len(s3_uploaded_files_fail_list)))    
    message = message + "<br /> Failed to S3 Upload:" + str(len(s3_uploaded_files_fail_list))    
    if len(s3_uploaded_files_fail_list) > 0:
        for item in s3_uploaded_files_fail_list:
            #Log here
            log_error(process_id, request_id, logger,str(item)) 
            message = message + str(item) + "<br />"                       
            print item
    
    logger.info("Failed to Cloud Upload:%s"%str(len(cloud_uploaded_files_fail_list)))    
    message = message + "<br /> Failed to Cloud Upload:" + str(len(cloud_uploaded_files_fail_list))    
    if len(cloud_uploaded_files_fail_list) > 0:
        for item in cloud_uploaded_files_fail_list:
            #Log here
            log_error(process_id, request_id, logger,str(item))   
            message = message + str(item) + "<br />"                     
            print item
    
    log_success(process_id, request_id, logger,"Toal files Found:" + str(len(total_files_list)))
    log_success(process_id, request_id, logger,"Pattern Matched:" + str(len(pattern_matched_files_list)))
    log_success(process_id, request_id, logger,"Toal files Downloaded:" + str(len(downloaded_files_success_list)))
    log_success(process_id, request_id, logger,"Toal files S3 Uploaded:" + str(len(s3_uploaded_files_success_list)))
    log_success(process_id, request_id, logger,"Toal files Cloud Uploaded:" + str(len(cloud_uploaded_files_success_list)))
    
    if len(pattern_matched_files_list) == len(downloaded_files_success_list) == len(s3_uploaded_files_success_list) == len(cloud_uploaded_files_success_list):
        log_success(process_id, request_id, logger,"Sync Status: Success")
    else:
        log_error(process_id, request, logger,"Sync Status: Failure")
    #Return the sync status
    return (True, "Synced Successfully") ##Exit on Success
    