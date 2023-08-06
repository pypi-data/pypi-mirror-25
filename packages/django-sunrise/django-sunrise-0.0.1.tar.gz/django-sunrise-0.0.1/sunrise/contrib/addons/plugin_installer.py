
import tempfile
from sunrise.contrib.addons.models import Plugin
from django.conf import settings
from sunrise.contrib.cloud.views import aws_s3
from django.core import management


import zipfile,os.path
def unzip(source_filename, dest_dir):
    with zipfile.ZipFile(source_filename) as zf:
        for member in zf.infolist():
            words = member.filename.split('/')
            path = dest_dir
            for word in words[:-1]:
                while True:
                    drive, word = os.path.splitdrive(word)
                    head, word = os.path.split(word)
                    if not drive:
                        break
                if word in (os.curdir, os.pardir, ''):
                    continue
                #path = os.path.join(path, word)
            zf.extract(member, path)

def install():
    #1. Get plugins list to be installed
    plugins = Plugin.objects.all()

    #2. Install every plugin
    bucket = aws_s3()    
    PLUGIN_APPS = []
    for plugin in plugins:
        plugin_location = plugin.location + "/" + plugin.zip_location
        #Get PluginZip from S3 to local
        k = bucket.get_key(plugin_location)
        #Write to temparory location
        egg_file_location = tempfile.mkdtemp() + "/" + plugin.zip_location
        k.get_contents_to_filename(egg_file_location)
        #Unzip
        unzip(egg_file_location, (settings.PROJECT_ROOT + "/plugins/").__str__())
        #Delete the egg file
        os.remove(egg_file_location)

        #build string to be added in settings
        app_label = ".".join(plugin.zip_location.split(".")[:-1])
        PLUGIN_APPS.append("'plugins.%s'"%(app_label))
    #Build plugin apps
    plugin_str = "PLUGIN_APPS = (\n\t"
    for idx, item in enumerate(PLUGIN_APPS):
        plugin_str = plugin_str + "%s"%item + ",\n"
        if idx != len(PLUGIN_APPS) - 1:
            plugin_str = plugin_str + "\t"
    plugin_str = plugin_str + ")"
    #Write plugin apps
    f = open(settings.PROJECT_ROOT + "/sunrisebilling/settings/plugin_config.py", "w")
    f.write(plugin_str)
    f.close()
    #Reload the module

    #Do makemigrations
    #Need to invoke from the external

    