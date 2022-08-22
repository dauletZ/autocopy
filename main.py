import multiprocessing
import sys, os
import datetime

import yaml, logging,time
from app.flashdetector import *
from app.lampnumber import *
from app.Log.logger import Logger
from app.mount import MountRemoteServer
from app.copy import CopyingMoviesFromFlash
from app.logs import CopyingLogs
from multiprocessing import Pool


def get_mount(newFlashes):
    with open('settings.yml', encoding='utf-8') as ymlfile:  # чтение конфига
        cfg = yaml.safe_load(ymlfile)
    folder = "{}{}".format(cfg["server"]["local_endpoint"], cfg["server"]["folder"])
    fileReplace = cfg["options"]["same_named_files_replace"]
    if fileReplace != 'true' and fileReplace !='false':
        fileReplace = 'false'
    saveFiles = cfg["options"]["save_files_on_device"]
    if saveFiles != 'true' and 'false':
        saveFiles = 'false'
    if cfg['options']['available_space'].isdigit() ==True:
        availableSpace = int(cfg['options']['available_space'])
    else:
        availableSpace = 2250
    if cfg['options']['video_file_max_size'].isdigit() == True:
        videoMaxSize = int(cfg['options']['video_file_max_size'])
    else:
        videoMaxSize = 1.8

    cyclicCopy = cfg['options']['cyclic_copy']
    mountOn = cfg["mountOn"]
    lampnumber = GetLampNumber(f'{mountOn}{newFlashes}')
    dictPath = {'my_hostname': os.uname()[1], 'dev_nmb': lampnumber, 'cur_date': str(datetime.date.today()).replace("-",""), 'file_date':'fileDate','cur_year':datetime.date.today().year, 'cur_mounth': datetime.datetime.now().strftime("%B"), 'cur_day': datetime.datetime.now().strftime('%d'), 'file_year': 'fileYear', 'file_mounth': 'fileMounth', 'file_day': 'fileDay'}
    SysLogDevPath = cfg['options']['sys_log_dev_path']
    videoPath = cfg['options']['video_path']
    DevLogPath = cfg['options']['dev_log_path']

    words = SysLogDevPath.split('/')
    i = 0
    for word in words:
        if word in dictPath:
            words[i] = dictPath[word]
        i += 1
    logDevpath = "/".join(words)
    logging.info(f"Mounted a new flash drive {mountOn}{newFlashes} for copy to {folder}")
    CopyingLogs(folder,f"{mountOn}{newFlashes}",lampnumber, saveFiles, logDevpath, DevLogPath)
    CopyingMoviesFromFlash(folder, f"{mountOn}{newFlashes}", True, lampnumber, saveFiles, fileReplace, availableSpace, videoMaxSize,cyclicCopy, videoPath)

    return
with open('settings.yml', encoding='utf-8') as ymlfile: # чтение конфига
    cfg = yaml.safe_load(ymlfile)
mountOn = cfg["mountOn"]

pathMainLog = cfg['options']["sys_log_path"]
words = pathMainLog.split('/')
dictPath = {'my_hostname': os.uname()[1], 'cur_date': str(datetime.date.today()).replace("-", ""),
            'file_date': 'fileDate', 'cur_year': datetime.date.today().year,
            'cur_mounth': datetime.datetime.now().strftime("%B"), 'cur_day': datetime.datetime.now().strftime('%d')}
i=0
for word in words:
    if word in dictPath:
        words[i] = dictPath[word]
    i+=1
path = "/".join(words)

MountRemoteServer(cfg["server"]["local_endpoint"])
Logger(path)
logging.info("Running ETP AutoCopyPy v0.1.01")
logging.info("Using next configuration:")
logging.info("Endpoint for flash drives:" + cfg["mountOn"])
fileReplace = cfg["options"]["same_named_files_replace"]
if fileReplace == 'true' or 'false':
    logging.info("Same named files replace:" + fileReplace)
else:
    fileReplace = 'false'
    logging.error("Same named files replace takes the value only 'true' or 'false'")
    logging.info("Same named files replace:" + fileReplace)
saveFiles = cfg["options"]["save_files_on_device"]
if saveFiles == 'true' or 'false':
    logging.info("Save files on device:" + saveFiles)
else:
    saveFiles = 'false'
    logging.error("Save files on device takes the value only 'true' or 'false'")
    logging.info("Save files on device:" + saveFiles)
logging.info(f"Available space:" + cfg['options']['available_space']+"GB")
if cfg['options']['available_space'].isdigit() == False:
    logging.error("Available space take only number value!")
logging.info ("Video file max size:" + cfg['options']['video_file_max_size'] + "GB")
if cfg['options']["video_file_max_size"].isdigit() ==False:
    logging.error("Video file max size take only number value")
logging.info ("Cyclic copy:" + cfg['options']['cyclic_copy'])
logging.info("Start listening a new USB flashes")

mountedFlash = []
while True:
    mountedFlash, newFlashes = FlashDetector(mountOn, mountedFlash)
    if newFlashes != []:
        if __name__ == "__main__":
            with multiprocessing.Pool(multiprocessing.cpu_count()*3) as p:
                p.map(get_mount, newFlashes)
                p.close()
                p.join()



