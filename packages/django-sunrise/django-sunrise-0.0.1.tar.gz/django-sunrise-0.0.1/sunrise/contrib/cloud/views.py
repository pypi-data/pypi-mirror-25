# Author: Integra
# Dev: Partha(Ref)

import json
from datetime import datetime

from django.http import HttpResponse
from django.views.generic import View
from django.conf import settings

from boto.s3.connection import S3Connection
from boto.s3.key import Key

from .api import SunriseCloud


def aws_s3():
    AWS_ACCESS_KEY_ID = settings.AWS_ACCESS_KEY_ID
    AWS_SECRET_ACCESS_KEY = settings.AWS_SECRET_ACCESS_KEY
    S3_BUCKET = settings.S3_BUCKET
    conn = S3Connection(AWS_ACCESS_KEY_ID,AWS_SECRET_ACCESS_KEY)
    buck = conn.get_bucket(S3_BUCKET)
    return buck


class CloudBase(View):
    def get(self, request):
        return self.read(request)

    def post(self, request):
        return self.write(request)


class CloudView(CloudBase):

    def s3_cloud_upload(self, flag,from_file_path,from_file_name,to_file_path,to_file_name,content,replace=True, username="RECON"):
        sobj = SunriseCloud()
        if flag=='create':
            if not replace:
                result = sobj.read('root/' + to_file_path)
                if result[0]:
                    for file_ins in result[1]:
                        if to_file_name == file_ins['fields']['name']:
                            return 'File Already Exist'
            try:
                bucket = aws_s3()
                k = Key(bucket)
                k.key = to_file_path + '/' + to_file_name
                k.set_contents_from_string(content)
                sobj.build('root/'+to_file_path)
                result = sobj.write('root/'+to_file_path, to_file_name, 'File',"{0:.2f}".format(round((float(k.size)/1024)*100)/100), username)
            except:
                result = [False]
        elif flag =='move':
            result = sobj.cut('root/'+from_file_path+'/'+from_file_name,'root/'+to_file_path)
            if from_file_name != to_file_name and to_file_name is not None:
                sobj.rename('root/'+to_file_path+'/'+from_file_name, to_file_name, "File")
        elif flag == 'copy':
            result = sobj.copy('root/'+from_file_path+'/'+from_file_name, 'root/'+to_file_path)
            if from_file_name != to_file_name and to_file_name is not None:
                sobj.rename('root/'+to_file_path+'/'+from_file_name, to_file_name, "File")
        elif flag == 'delete':
            result = sobj.delete('root/' + from_file_path+'/'+from_file_name)
        elif flag == 'read':
            result = sobj.read('root/' + from_file_path)
        elif flag == 'build':
            result = sobj.build('root/' + to_file_path)
        if result[0]:
            return result[1]
        else:
            pass

    def read(self, request):
        if "q" in request.GET:
            item_path = request.GET["q"]
        else:
            item_path = 'root/'
        sobj = SunriseCloud()
        data = sobj.read(item_path)
        if data[0]:
            return HttpResponse(json.dumps(data[1]))
        else:
            return HttpResponse(data[1])

    def write(self, request):
        dir_path=request.POST['current_url'][5:]
        item_name=request.POST['file_name']
        replace=True
        prefix = request.POST['prefix']
        
        if 'file' in request.FILES:
            file_data = request.FILES['file']
            result = self.s3_cloud_upload('create',None,None,dir_path,item_name,file_data.read())
        if result =='File Already Exist':
            return HttpResponse(json.dumps({'result':result}))
        return HttpResponse(json.dumps({'time':str(datetime.now())}))

    

