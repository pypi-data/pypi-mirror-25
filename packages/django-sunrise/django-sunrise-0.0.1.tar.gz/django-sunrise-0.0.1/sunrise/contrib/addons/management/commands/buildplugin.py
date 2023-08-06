"""
Management utility to sync s3 and cloud with FtpServer.
"""
import os, shutil
from django.core.management.base import BaseCommand
from django.db import connection
from django.apps import apps
from django.conf import settings

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

        # self.option_list = BaseCommand.option_list

    # option_list = BaseCommand.option_list
    help = 'Used to create views in db for models with managed = False'

    def add_arguments(self, parser):
        parser.add_argument('args', metavar='plugin', nargs='*',
            help='Specify Json file path to create migrations for.')

    def handle(self, *args, **options):
        for appname in args:
            shutil.make_archive(appname, 'zip', settings.PROJECT_ROOT + "/plugins/%s"%appname)
            shutil.copyfile(settings.PROJECT_ROOT + "/" + "%s.zip"%appname, settings.PROJECT_ROOT + "/eggs/%s.zip"%appname)
            os.remove(settings.PROJECT_ROOT + "/" + "%s.zip"%appname)
            print "Buildng plugin"
        



