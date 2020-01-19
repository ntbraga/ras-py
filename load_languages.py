import os
import shutil


def cp_dir(src, dest):
    try:
        shutil.copytree(src, dest)
    # Directories are the same
    except shutil.Error as e:
        print('Directory not copied. Error: %s' % e)
    # Any error saying that the directory doesn't exist
    except OSError as e:
        print('Directory not copied. Error: %s' % e)


def run():
    cp_dir(os.path.dirname(os.path.abspath(__file__)) + '/languages/snips_nlu_en-0.2.3', '/tmp/sls-py-req/snips_nlu'
                                                                                         '/data/en')
    cp_dir(os.path.dirname(os.path.abspath(__file__)) + '/languages/snips_nlu_pt_br-0.1.1', '/tmp/sls-py-req'
                                                                                            '/snips_nlu/data/pt_br')
