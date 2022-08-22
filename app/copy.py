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
        date = "00000000"
        return date, code

def oldestFile(path, contCopy,drSpace):
    import os
    import pathlib
    taggedrootdir = pathlib.Path(path)
    folderName = os.path.split(path)[1]
    oldFile = str(min([f for f in taggedrootdir.resolve().glob('**/*') if f.is_file()], key=os.path.getctime))
    oldFolder = os.path.dirname(oldFile)
    i = oldFile.find(folderName)
    vyvodPath = oldFile[i:]
    logging.info("The server is full. Cyclic copy is enable.")
    logging.info(f"{vyvodPath} deleted")
    os.remove(oldFile)
    while os.listdir(oldFolder) == []:
        vyvodPath = oldFolder[i:]
        logging.info(f"{vyvodPath} deleted")
        os.rmdir(oldFolder)
        oldFolder = os.path.dirname(oldFolder)
    return
def prepareCopy(fullpath, remote,lampnumber, flash, saveFiles, fileReplace, availableSpace, videoMaxSize,cyclicCopy):
    import os, logging, time
    from pathlib import Path
    filename = os.path.split(fullpath)[1]
    date, code = getSubdirs(filename)
    remotefolder = f"{remote}/{date}/{code}"
    if not os.path.exists(remotefolder):
        os.makedirs(remotefolder)
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
                logging.info(f"File {newfile} is already exists!")
                newfile = f"{remotefile[:len(remotefile)-4]}_{i}{remotefile[len(remotefile)-4:]}"
            else:
                break
    fileSize = round(os.path.getsize(fullpath) / 1024**3,2)
    if fileSize <= videoMaxSize:
        pth = Path(remote)
        drSpace = round(sum(f.stat().st_size for f in pth.glob('**/*') if f.is_file()) / 1024 ** 3, 2)
        logging.info(f"Occupied place on the server: {drSpace} GB")
        logging.info(f"start copy {filename} from {hostname}{flash} to {ip[0]}/{filenameArchive}/{date}/{code}/{filename}")
        if drSpace >= (availableSpace - videoMaxSize*9):
            if cyclicCopy == "false":
                logging.info("The server is full. Cyclic copying is disable. Copying has stopped")
                while drSpace<=(availableSpace- videoMaxSize*10):
                    drSpace = round(sum(f.stat().st_size for f in pth.glob('**/*') if f.is_file()) / 1024 ** 3, 2)
                    time.sleep(0.5)
            else:
                contCopy = availableSpace - videoMaxSize*10
                oldestFile(remote,contCopy, drSpace)
        os.system(f'cp {fullpath} {newfile}')
        if os.path.isfile(f"{fullpath}"):
            if saveFiles == 'false':
                os.remove(f'{fullpath}')
                logging.info(f"File {filename} was copied and removed succesfully")
            else:
                logging.info(f"File {filename} was copied")
        else:
            if os.path.exists(flash):
                logging.error(f"Flash {flash} doesn't active!")
                return
            logging.error(f"File {filename} doesn't exist!")
    else:
        logging.info(f"The {filename} size exceeds max value!")
        logging.info(f"{filename} size:{fileSize} GB")
    return


def CopyingMoviesFromFlash(remote, flash, isBaselevel, lampnum, saveFiles, fileReplace, availableSpace, videoMaxSize,cyclicCopy ):
    import os, logging
    lampnumber = lampnum
    files = os.listdir(flash)
    for file in files:
        fullname = f"{flash}/{file}"
        if file == "logs":
            continue
        if os.path.isdir(fullname) ==True:
            CopyingMoviesFromFlash(remote, fullname, False, lampnumber, saveFiles, fileReplace, availableSpace, videoMaxSize,cyclicCopy )
            continue
        if file.endswith('MP4') == False and file.endswith('3GP') == False:
            continue
        prepareCopy(fullname, remote, lampnumber, flash,saveFiles, fileReplace, availableSpace, videoMaxSize,cyclicCopy)
    if isBaselevel == True:
        if os.path.exists(flash) == False:
            return
        if os.path.isfile(f"{flash}/umount") == False:
            open(f"{flash}/umount", "w")
            logging.info(f"'{flash}/umount' was created successfully")
        else:
            logging.error("the umount file has already been created")
        return