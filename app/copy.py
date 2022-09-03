import logging


def getSubdirs(filename):
    import logging
    filename = filename.replace("_","")
    if len(filename) >=16:
        code = filename[:5]
        date = filename[5:13]
        return date, code
    else:
        logging.error("Failed to get date and code!")
        code = "00000"
        date = "20220101"
        return date, code

def oldestFile(path):
    import os, time
    import pathlib
    try:
        taggedrootdir = pathlib.Path(path)
        folderName = os.path.split(path)[1]
        oldFile = str(min([f for f in taggedrootdir.resolve().glob('**/*') if f.is_file()], key=os.path.getctime))
        oldFolder = os.path.dirname(oldFile)
        i = oldFile.find(folderName)
        vyvodPath = oldFile[i:]
        try:
            os.unlink(oldFile)
            logging.info(f"{vyvodPath} deleted")
        except:
            time.sleep(1)
            return
        while os.listdir(oldFolder) == []:
            vyvodPath = oldFolder[i:]
            try:
                os.rmdir(oldFolder)
                logging.info(f"{vyvodPath} deleted")
                oldFolder = os.path.dirname(oldFolder)
            except:
                time.sleep(1)
                return
        return
    except:
        return
def prepareCopy(fullpath, remote, lampnumber, flash, saveFiles, fileReplace, availableSpace, videoMaxSize, cyclicCopy,
                videoPath, SysLogPath, logDevpath):
    import os, logging, time, datetime
    from app.Log.loggerforlamp import getLoggerForLamp
    from app.Log.logger import Logger
    from pathlib import Path
    filename = os.path.split(fullpath)[1]
    date, code = getSubdirs(filename)

    filedate = datetime.datetime(year = int(date[0:4]), month = int(date[4:6]), day = int(date[6:8]))
    dictPath = {'my_hostname': os.uname()[1], 'dev_nmb': lampnumber,
                'cur_date': str(datetime.date.today()).replace("-", ""), 'file_date': date,
                'cur_year': str(datetime.date.today().year), 'cur_mounth': datetime.datetime.now().strftime("%B"),
                'cur_day': datetime.datetime.now().strftime('%d'), 'file_year': str(filedate.year), 'file_mounth': filedate.strftime("%B"),
                'file_day': filedate.strftime("%d")}

    words = videoPath.split('/')
    i = 0
    for word in words:
        if word in dictPath:
            words[i] = dictPath[word]
        i += 1
    try:
        Videopath = "/".join(words)
    except:
        logging.info("Video path specified incorrectly")
        exit()
    if Videopath[-1] == '/':
        Videopath = Videopath[:-1]

    remotefolder = f"{remote}{Videopath}"
    if not os.path.exists(remotefolder):
            os.makedirs(remotefolder, exist_ok= True)
    hostname = os.uname()[1]
    remotefile = f"{remotefolder}/{filename}"
    newfile = remotefile
    filenameArchive = os.path.split(remote)[1] # архив
    remL = os.path.dirname(remote)  # home/pi/winserver
    source = os.popen(f"findmnt {remL} -o SOURCE")
    resSource = source.readlines()
    if len(resSource) > 1:
        ip = resSource[1].splitlines()
    else:
        logging.error("Couldn't find server ip!")
        ip = newfile
    i=0
    if fileReplace == 'false':
        while True:
            i+=1
            if os.path.exists(newfile) == True:
                if i ==1:
                    logging.info(f"File {newfile} is already exists!")
                newfile = f"{remotefile[:len(remotefile)-4]}_{i}{remotefile[len(remotefile)-4:]}"
            else:
                break
    else:
        if os.path.exists(newfile) == True:
            logging.info(f"File {newfile} is already exists!")
    pth = Path(remote)
    drSpace = round(sum(f.stat().st_size for f in pth.glob('**/*') if f.is_file()) / 1024 ** 3, 2)
    if drSpace >= (availableSpace - videoMaxSize*9):
        Logger(SysLogPath)
        logging.info(f"Occupied place on the server: {drSpace} GB")
        if cyclicCopy == "false":
            logging.info("The server is full. Cyclic copying is disable. Copying has stopped")
            while drSpace>=(availableSpace- videoMaxSize*10):
                drSpace = round(sum(f.stat().st_size for f in pth.glob('**/*') if f.is_file()) / 1024 ** 3, 2)
                time.sleep(0.5)
            logging.info("")
        else:
            logging.info("The server is full. Cyclic copy is enable.")
            while drSpace>=(availableSpace- videoMaxSize*10):
                oldestFile(remote)
                drSpace = round(sum(f.stat().st_size for f in pth.glob('**/*') if f.is_file()) / 1024 ** 3, 2)
        logging.info(f"Occupied place on the server: {drSpace} GB")
        getLoggerForLamp(remote, lampnumber,logDevpath)
    try:
        logging.info(f"start copy {filename} from //{hostname}{flash} to {ip[0]}/{filenameArchive}{Videopath}/{os.path.split(newfile)[1]}")
        os.system(f'cp -a {fullpath} {newfile}')
    except:
        logging.info(f'copying {filename} failed')
        return
    if os.path.isfile(f"{fullpath}"):
        if saveFiles == 'false':
            try:
                os.remove(f'{fullpath}')
                logging.info(f"File {filename} was copied and removed succesfully")
            except:
                return
        else:
            logging.info(f"File {filename} was copied")
    else:
        if os.path.exists(flash) == False:
            return
        logging.error(f"File {filename} doesn't exist!")
    return


def CopyingMoviesFromFlash(remote, flash, isBaselevel, lampnum, saveFiles, fileReplace, availableSpace, videoMaxSize,
                           cyclicCopy, videoPath, SysLogPath, logDevpath):
    import os, logging
    from app.Log.logger import Logger
    lampnumber = lampnum
    files = os.listdir(flash)
    for file in files:
        fullname = f"{flash}/{file}"
        if file == "logs":
            continue
        if os.path.isdir(fullname) ==True:
            CopyingMoviesFromFlash(remote, fullname, False, lampnumber, saveFiles, fileReplace, availableSpace,
                                   videoMaxSize, cyclicCopy, videoPath, SysLogPath, logDevpath)
            continue
        if file.endswith('MP4') == False and file.endswith('3GP') == False:
            continue
        prepareCopy(fullname, remote, lampnumber, flash, saveFiles, fileReplace, availableSpace, videoMaxSize,
                    cyclicCopy, videoPath, SysLogPath, logDevpath)
        if os.path.exists(flash) == False:
            return
    if isBaselevel == True:
        Logger(SysLogPath)
        if os.path.exists(flash) == False:
            return
        if os.path.isfile(f"{flash}/umount") == False:
            open(f"{flash}/umount", "w")
            logging.info(f"'{flash}/umount' was created successfully")
        else:
            logging.error("the umount file has already been created")
    return
