#SFTP Master
import os, tarfile, paramiko
from stat import S_ISDIR
from django.conf import settings
import fnmatch

class SFTApi(object):

    transport = None
    sftp = None
    zipname = None

    def __init__(self, *args, **kwargs):
        
        self.hostname = kwargs['FTP_DOMAIN'] 
        self.port = kwargs['FTP_PORT']
        self.username = kwargs['FTP_USERNAME']
        self.password = kwargs['FTP_PASSWORD']
        self.logger = kwargs['logger']
        self._connect()

    def _connect(self, *args, **kwargs):
        """ It is used to connect with remote host """
        self._get_ssh()
        self.transport = paramiko.Transport((self.hostname, self.port))
        self.transport.connect(username = self.username, password = self.password)
        
        self.sftp = paramiko.SFTPClient.from_transport(self.transport)
        try:
            self.logger.info("Connected to ", self.hostname, "as ", self.username)
        except:
            pass
        print "Connected to ", self.hostname, "as ", self.username
        return

    def setLogger(self, logger):
        self.logger = logger

    def setMessenger(self, task_request_id = None, request_id = None):
        self.task_request_id = task_request_id
        self.request_id = request_id

    def writeMessage(self, message, warning=False):
        """ Writing message to message log """
        message = str(message)
        if warning:
            msg_log(self.task_request_id,self.request_id, "Gen", "W001", **{'message':message})
        else:
            msg_log(self.task_request_id,self.request_id, "Gen", "S905", **{'message':message})            
        return 

    def _get_ssh(self, *args, **kwargs):
        """ It is used to connect as ssh """
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.hostname, username = self.username, password = self.password)
        return ssh

    
    def _zip(self, *args, **kwargs):
        """ It is used to zip folder or files """
        if "zip_type" and "path" not in kwargs:
            return None
        if kwargs["zip_type"] == "local":
            tar = tarfile.open("Tests.tar.gz", "w:gz")
            tar.add(kwargs["path"], arcname="Tests")
            tar.close()
            return "Zipped"
        if kwargs["zip_type"] == "remote":
            ssh = self._get_ssh()
            tar_name = kwargs['path'].split("/")[len(kwargs['path'].split("/")) - 2] +".tar.gz"
            print "tar -zcvf ",tar_name," ", kwargs['path']
            stdin, stdout, stderr = ssh.exec_command("tar -zcvf "+ tar_name + " " + kwargs['path'])
            return tar_name
        return 0

    def isExists(self, path):
        """ It will return whether a file/directory exists or not and return type """
        """ 1 - directory, 0 - file, -1 - Not exists """
        is_file = os.path.isfile(path)
        is_dir = os.path.isdir(path)

        if is_file or is_dir:
            if is_file:
                return 0
            else:
                return 1
        else:
            return -1

    def remove(self, path):
        self.sftp.remove(path)


    def upload(self, *args, **kwargs):
        """ It is used to upload files / folders """
        if "source" and "destination" not in kwargs:
            return
        else:
            path_type = self.isExists(kwargs['source'])
            if path_type == -1:
                return 
            if path_type == 0:
                #Copy directly
                file_name = kwargs['source'].split("/")[len(kwargs['source'].split("/")) -1]
                self.sftp.put(kwargs['source'], kwargs['destination'] + file_name)
            if path_type == 1:
                #  recursively upload a full directory
                os.chdir(os.path.split(kwargs['source'])[0])
                parent=os.path.split(kwargs['source'])[1]
                for walker in os.walk(parent):
                    try:
                        self.sftp.mkdir(os.path.join(kwargs['destination'],walker[0]))
                    except:
                        pass
                    for file in walker[2]:
                        self.sftp.put(os.path.join(walker[0],file),os.path.join(kwargs['destination'],walker[0],file))
        return 
    def sftp_walk(self,remotepath):
        # Kindof a stripped down  version of os.walk, implemented for 
        # sftp.  Tried running it flat without the yields, but it really
        # chokes on big directories.
        path = remotepath
        files = []
        folders = []
        for f in self.sftp.listdir_attr(remotepath):
            if S_ISDIR(f.st_mode):
                folders.append(f.filename)
            else:
                files.append(f.filename)
        yield path,folders,files
        for folder in folders:
            new_path=os.path.join(remotepath,folder)
            for x in self.sftp_walk(new_path):
                yield x

    def get_files_list(self, path, pattern=None):
        """ It is used to download the file / folders """
        output = []
        dirs = []
        files = []
        self.sftp.chdir(os.path.split(path)[0])
        parent=os.path.split(path)[1]
        
        for walker in self.sftp_walk(parent):
            for file in walker[2]:
                print os.path.join(walker[0],file)
                try:
                    if len(fnmatch.filter([os.path.join(walker[0],file)], pattern)) > 0 or os.path.join(walker[0],file).endswith(pattern) or fnmatch.fnmatch(file, pattern):
                        output.append(os.path.join(walker[0],file))
                        dirs.append(walker[0])
                        files.append(file)
                except:
                    pass
        return zip(output, dirs, files)

    def get_files(self, source, destination, pattern='*', keep_original=True):
        files_list = self.get_files_list(source, pattern)
        try:
            os.mkdir(destination)
        except:
            pass
        for file in files_list:
            try:
                try:
                    os.makedirs(os.path.join(destination,file[1]))
                except:
                    pass
                self.sftp.get(file[0], os.path.join(destination, file[1], file[2]))
                self.logger.info(file[0] + " Downloaded Successfully")
                self.writeMessage(file[0] + " Downloaded Successfully")
                print file[0] + " Downloaded Successfully"
                if keep_original == False:
                    try:
                        self.sftp.remove(os.path.join(file[1],file[2]))
                        self.writeMessage(file[0] + " Removed From FTPServer Successfully")
                        self.logger.info(file[0] + " Removed From FTPServer Successfully")
                        print file[0] + " Removed From FTPServer Successfully"
                    except:
                        self.writeMessage(file[0] + " Removing From FTPServer Failed", True)
                        self.logger.info(file[0] + " Removing From FTPServer Failed")
                        print file[0] + " Removing From FTPServer Failed" 
            except:
                self.writeMessage(file[0] + " Download Failed", True)
                self.logger.info(file[0] + " Download Failed")
                print file[0] + " Download Failed"
        return True

    def get_file(self, source, destination):
        """ It is used to download the single file """
        self.sftp.get(source, destination)

    def download(self, *args, **kwargs):
        """ It is used to download the file / folders """
        if "source" and "destination" not in kwargs:
            return
        else:
            if 'type' not in kwargs or kwargs['type'] == "File":
                self.sftp.get(kwargs['source'], kwargs['destination'])
            else:
                self.sftp.chdir(os.path.split(kwargs['source'])[0])
                parent=os.path.split(kwargs['source'])[1]
                try:
                    os.mkdir(kwargs['destination'])
                except:
                    pass
                for walker in self.sftp_walk(parent):
                    try:
                        os.mkdir(os.path.join(kwargs['destination'],walker[0]))
                    except:
                        pass
                    for file in walker[2]:
                        
                        try:
                            self.sftp.get(os.path.join(walker[0],file),os.path.join(kwargs['destination'],walker[0],file))
                            print "Dleteing file.....", os.path.join(walker[0],file)
                            self.sftp.remove(os.path.join(walker[0],file))
                            print os.path.join(walker[0],file),": Success"
                        except:
                            print os.path.join(walker[0],file),": Fail" 

        return

    
