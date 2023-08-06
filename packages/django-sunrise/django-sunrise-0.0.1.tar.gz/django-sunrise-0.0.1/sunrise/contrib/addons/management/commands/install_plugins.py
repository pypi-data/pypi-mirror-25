"""
Management utility to sync s3 and cloud with FtpServer.
"""
import os, shutil
import zipfile,os.path

from django.core.management.base import BaseCommand
from django.db import connection
from django.apps import apps
from django.conf import settings

from sunrise.contrib.addons.models import Addon
from sunrise.contrib.cloud.views import aws_s3


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Command(BaseCommand):

    def __init__(self, *args, **kwargs):
        # Options are defined in an __init__ method to support swapping out
        # custom user models in tests.
        super(Command, self).__init__(*args, **kwargs)

        self.option_list = BaseCommand.option_list

    option_list = BaseCommand.option_list
    help = 'Used to create views in db for models with managed = False'

    def add_arguments(self, parser):
        parser.add_argument('args', metavar='plugin', nargs='*',
            help='Specify Json file path to create migrations for.')

    def create_unzip(self, path_to_zip_file, directory_to_extract_to):
        import zipfile
        zip_ref = zipfile.ZipFile(path_to_zip_file, 'r')
        zip_ref.extractall(directory_to_extract_to)
        zip_ref.close()
        return True

    def _install(self):
        PLUGIN_APPS = os.walk(settings.PROJECT_ROOT + "/plugins/").next()[1]
        plugin_str = "PLUGIN_APPS = (\n\t"
        for idx, item in enumerate(PLUGIN_APPS):
            plugin_str = plugin_str + "'plugins.%s'"%item + ",\n"
            if idx != len(PLUGIN_APPS) - 1:
                plugin_str = plugin_str + "\t"
        plugin_str = plugin_str + ")"
        #Write plugin apps
        f = open(settings.PROJECT_ROOT + "/sunrisebilling/settings/plugin_config.py", "w")
        f.write(plugin_str)
        f.close()
        print bcolors.OKGREEN + "OK:%s Plugin Installed, Please runserver to make sure plugin working fine."%PLUGIN_APPS[0] + bcolors.ENDC
        

    def handle(self, *args, **options):
        #1. Get All Installed Addons
        ads = Addon.objects.filter(status = "Installed")
        bucket = aws_s3()
        
        #2. Download the Addon
        for ad in ads:
            print "Found: ", ad.name
            #Get PluginZip from S3 to local
            print "Downloading addon: ",ad.name
            k = bucket.get_key(ad.location)
            file_name = ad.location.split("/")[-1]
            egg_location = settings.PROJECT_ROOT + "/eggs/" + file_name
            plugin_location = settings.PROJECT_ROOT + "/plugins/%s/"%ad.name
            k.get_contents_to_filename(egg_location)
            print "Downloaded the addon: ", ad.name , " to ", egg_location

            #Unzip
            try:
                shutil.rmtree(plugin_location)
            except:
                pass
            try:
                if not os.path.exists(plugin_location):
                    os.makedirs(plugin_location)
            except:
                pass
            
            self.create_unzip(egg_location, plugin_location)
        if len(ads) > 0:
            self._install()
        else:
            print "No Addons Detected"