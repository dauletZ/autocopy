#!/usr/bin/env python

import multiprocessing
import signal
import sys, os
import datetime
import yaml, logging,time, pathlib
from app.flashdetector import *
from app.lampnumber import *
from app.Log.logger import Logger
from app.mount import MountRemoteServer
from app.copy import CopyingMoviesFromFlash
from app.logs import CopyingLogs

def handle_exit(seg, frame):
    print(seg, frame)   # заглушка, чтобы не было предупреждения
    raise SystemExit

def checkSize(path, availableSpace, videoMaxSize, SysLogPath, cyclicCopy):
    import os, time
    import pathlib
    from app.Log.logger import Logger
    pth = pathlib.Path(path)
    drSpace = round(sum(f.stat().st_size for f in pth.glob('**/*') if f.is_file()) / 1024 ** 3, 2)
    while True:
        while True:
            if drSpace <= (availableSpace - videoMaxSize * 9):
                time.sleep(5)
            else:
                break
        if drSpace >= (availableSpace - videoMaxSize*9):
            Logger(SysLogPath)
            logging.info(f"Occupied place on the server: {drSpace} GB")
            if cyclicCopy == "false":
                logging.info("The server is full. Cyclic copying is disable. Copying has stopped")
                while drSpace>=(availableSpace- videoMaxSize*10):
                    drSpace = round(sum(f.stat().st_size for f in pth.glob('**/*') if f.is_file()) / 1024 ** 3, 2)
                    time.sleep(0.5)
                logging.info("Сopying resumed")
            else:
                logging.info("The server is full. Cyclic copy is enable.")
                while drSpace>=(availableSpace- videoMaxSize*10):
                    drSpace = round(sum(f.stat().st_size for f in pth.glob('**/*') if f.is_file()) / 1024 ** 3, 2)
                    taggedrootdir = pathlib.Path(path)
                    folderName = os.path.split(path)[1]
                    oldFile = str(min([f for f in taggedrootdir.resolve().glob('**/*') if f.is_file()], key=os.path.getctime))
                    oldFolder = os.path.dirname(oldFile)
                    i = oldFile.find(folderName)
                    vyvodPath = oldFile[i:]
                    try:
                        os.unlink(oldFile)
                        logging.info(f"{vyvodPath} delete")
                    except:
                        time.sleep(1)
                        logging.info(f"f{vyvodPath} delete error")
                    while os.listdir(oldFolder) == []:
                        vyvodPath = oldFolder[i:]
                        os.rmdir(oldFolder)
                        logging.info(f"{vyvodPath} deleted")
                        oldFolder = os.path.dirname(oldFolder)
                    drSpace = round(sum(f.stat().st_size for f in pth.glob('**/*') if f.is_file()) / 1024 ** 3, 2)
            logging.info(f"Occupied place on the server: {drSpace} GB")


def get_mount(newFlashes):
    with open('settings.yml', encoding='utf-8') as ymlfile:  # чтение конфига
        cfg = yaml.safe_load(ymlfile)
    mountOn = cfg["mountOn"]

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
    videoMaxSize = cfg['options']["video_file_max_size"].replace(',', '.')
    if videoMaxSize.replace('.', '', 1).isdigit() == True:
        videoMaxSize = float(videoMaxSize)
    else:
        videoMaxSize = 1.8
    cyclicCopy = cfg['options']['cyclic_copy']
    if cyclicCopy !='true' and cyclicCopy != 'false':
        cyclicCopy = 'false'
    lampnumber = GetLampNumber(f'{mountOn}{newFlashes}')
    if lampnumber == "false":
        return
    dictPath = {'my_hostname': os.uname()[1], 'dev_nmb': lampnumber, 'cur_date': str(datetime.date.today()).replace("-",""), 'file_date':'fileDate','cur_year':str(datetime.date.today().year), 'cur_mounth': datetime.datetime.now().strftime("%B"), 'cur_day': datetime.datetime.now().strftime('%d'), 'file_year': 'fileYear', 'file_mounth': 'fileMounth', 'file_day': 'fileDay'}
    SysLogDevPath = cfg['options']['sys_log_dev_path']
    videoPath = cfg['options']['video_path']
    DevLogPath = cfg['options']['dev_log_path']
    pathMainLog = cfg['options']["sys_log_path"]
    words = pathMainLog.split('/')
    i = 0
    for word in words:
        if word in dictPath:
            words[i] = dictPath[word]
        i += 1
    try:
        SysLogPath = "/".join(words)
    except:
        logging.error("sys_log_path specified incorrectly")
        exit()
    if SysLogPath[-1] == '/':
        SysLogPath = SysLogPath[:-1]

    words = SysLogDevPath.split('/')
    i = 0
    for word in words:
        if word in dictPath:
            words[i] = dictPath[word]
        i += 1
    logDevpath = "/".join(words)
    if logDevpath[-1] == '/':
        logDevpath = logDevpath[:-1]

    logging.info(f"Mounted a new flash drive {mountOn}{newFlashes} for copy to {folder}")
    CopyingLogs(folder, f"{mountOn}{newFlashes}", lampnumber, saveFiles, logDevpath, DevLogPath, SysLogPath)
    CopyingMoviesFromFlash(folder, f"{mountOn}{newFlashes}", True, lampnumber, saveFiles, fileReplace, availableSpace,
                           videoMaxSize, videoPath, SysLogPath, logDevpath)
    return


signal.signal(signal.SIGTERM, handle_exit)
with open('settings.yml', encoding='utf-8') as ymlfile: # чтение конфига
    cfg = yaml.safe_load(ymlfile)
mountOn = cfg["mountOn"]

pathMainLog = cfg['options']["sys_log_path"]
words = pathMainLog.split('/')
dictPath = {'my_hostname': os.uname()[1],
            'cur_date': str(datetime.date.today()).replace("-", ""),
            'cur_year': str(datetime.date.today().year), 'cur_mounth': datetime.datetime.now().strftime('%m'),
            'cur_day': datetime.datetime.now().strftime('%d')}
i=0
for word in words:
    if word in dictPath:
        words[i] = dictPath[word]
    i+=1
try:
    path = "/".join(words)
except:
    logging.error("sys_log_path specified incorrectly")
    exit()
if path[-1] == '/':
    path = path[:-1]

local = cfg["server"]["local_endpoint"]
archive = cfg["server"]["folder"]
MountRemoteServer(f"{local}")
Logger(path)
logging.info("Running ETP AutoCopyPy v0.1.07")
pth = pathlib.Path(f"{local}/{archive}")
drSpace = round(sum(f.stat().st_size for f in pth.glob('**/*') if f.is_file()) / 1024 ** 3, 2)
logging.info(f"Occupied place on the server: {drSpace} GB")
logging.info("Using next configuration:")
logging.info("Endpoint for flash drives:" + cfg["mountOn"])
fileReplace = cfg["options"]["same_named_files_replace"]
folder = "{}{}".format(cfg["server"]["local_endpoint"], cfg["server"]["folder"])
if fileReplace == 'true' or fileReplace == 'false':
    logging.info("Same named files replace:" + fileReplace)
else:
    fileReplace = 'false'
    logging.error("Same named files replace takes the value only 'true' or 'false'")
    logging.info("Same named files replace:" + fileReplace)
saveFiles = cfg["options"]["save_files_on_device"]
if saveFiles == 'true' or saveFiles == 'false':
    logging.info("Save files on device:" + saveFiles)
else:
    saveFiles = 'false'
    logging.error("Save files on device takes the value only 'true' or 'false'")
    logging.info("Save files on device:" + saveFiles)
if cfg['options']['available_space'].isdigit() == False:
    logging.error("Available space take only number value!")
    logging.error("Aviailable space uses default options")
    logging.info("Avialable space: 2250")
else:
    logging.info(f"Available space:" + cfg['options']['available_space'] + "GB")
video = cfg['options']["video_file_max_size"].replace(',', '.')
if video.replace('.','',1).isdigit()==False:
    logging.error("Video file max size take only number value")
    logging.error("Video file max size uses default options")
    logging.info("Video file max size: 1,8 GB")
else:
    logging.info("Video file max size:" + cfg['options']['video_file_max_size'] + "GB")

CyclicCopy = cfg['options']['cyclic_copy']
if CyclicCopy == 'false' or CyclicCopy == 'true':
    logging.info ("Cyclic copy:" + cfg['options']['cyclic_copy'])
else:
    logging.info("Cyclic copy takes the value only 'true' or 'false'")
    logging.info ("Cyclic copy: false")
logging.info("Start listening a new USB flashes")
mountedFlash = []
if __name__ == "__main__":
    try:
        jobs = []
        p = multiprocessing.Process(target=checkSize, args=(folder, float(cfg['options']['available_space']), float(video),path, cfg['options']['cyclic_copy']))
        p.start()
        jobs.append(p)
        while True:
            mountedFlash, newFlashes = FlashDetector(mountOn, mountedFlash)
            if newFlashes != []:
                for i in range(0,len(newFlashes)):
                    enought = newFlashes[i]
                    p = multiprocessing.Process(target = get_mount, args = (enought,))
                    jobs.append(p)
                    p.start()
                time.sleep(5)
            for proc in jobs:
                if not proc.is_alive():
                    p = proc.exitcode
                    if p == 0:
                        proc.kill()
        for proc in jobs:
            proc.join()
    except(KeyboardInterrupt, SystemExit):
        exit()




