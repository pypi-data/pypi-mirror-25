# coding=utf-8
import os
from shutil import copy

from bgmi.config import IS_WINDOWS, BGMI_PATH
from bgmi.config import SAVE_PATH, FRONT_STATIC_PATH, DOWNLOAD_DELEGATE, TMP_PATH, SCRIPT_PATH
from bgmi.download import get_download_class
from bgmi.utils import print_success, print_warning, print_info, print_error


def install_crontab():
    if IS_WINDOWS:
        copy(os.path.join(os.path.dirname(__file__), 'cron.vbs'), BGMI_PATH)
        print_info('cron.vbs is located as {}'.format(os.path.join(BGMI_PATH, 'cron.vbs')))
        print_warning('if you want to enable bgmi autoupdate, see https://github.com/BGmi/BGmi/blob/master/README.windows.md for next step')
    else:
        print_info('Installing crontab job')
        path = os.path.join(os.path.dirname(__file__), 'crontab.sh')
        os.system('sh \'%s\'' % path)


def create_dir():
    if not os.environ.get('HOME', ''):
        print_warning('$HOME not set, use \'/tmp/\'')

    tools_path = os.path.join(BGMI_PATH, 'tools')
    # bgmi home dir
    path_to_create = (BGMI_PATH, SAVE_PATH, TMP_PATH,
                      SCRIPT_PATH, tools_path, FRONT_STATIC_PATH)

    try:
        for path in path_to_create:
            if not os.path.exists(path):
                print_success('%s created successfully' % path)
                os.mkdir(path)
            else:
                print_warning('%s already exists' % path)
    except OSError as e:
        print_error('Error: {0}'.format(str(e)))


def install():
    get_download_class(DOWNLOAD_DELEGATE, instance=False).install()
