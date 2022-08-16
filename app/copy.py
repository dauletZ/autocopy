
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

def prepareCopy(fullpath, remote,lampnumber, flash):
    import os, logging
    from app.Log.loggerforlamp import getLoggerForLamp
    getLoggerForLamp(remote, lampnumber)
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
    while True:
        i+=1
        if os.path.exists(newfile) == True:
            logging.info(f"File {newfile} is already exists!")
            newfile = f"{remotefile[:len(remotefile)-4]}_{i}{remotefile[len(remotefile)-4:]}"
        else:
            break
    logging.info(f"start copy {filename} from {hostname}{flash} to {ip}/{filenameArchive}/{date}/{code}/{filename}")
    os.system(f'cp {fullpath} {newfile}')
    if os.path.isfile(f"{fullpath}"):
        os.remove(f'{fullpath}')
        logging.info(f"File {filename} was copied and removed succesfully")
    else:
        if os.path.exists(flash):
            logging.error(f"Flash {flash} doesn't active!")
            return
        logging.error(f"File {filename} doesn't exist!")
    return


def CopyingMoviesFromFlash(remote, flash, isBaselevel, lampnum):
    import os, logging
    from app.Log.loggerforlamp import getLoggerForLamp
    lampnumber = lampnum
    getLoggerForLamp(remote,lampnumber)
    files = os.listdir(flash)
    for file in files:
        fullname = f"{flash}/{file}"
        if file == "logs":
            continue
        if os.path.isdir(fullname) ==True:
            CopyingMoviesFromFlash(remote, fullname, False, lampnumber)
            continue
        if file.endswith('MP4') == False:
            continue
        prepareCopy(fullname, remote, lampnumber, flash)
    if isBaselevel == True:
        if os.path.exists(flash) == False:
            return
        if os.path.isfile(f"{flash}/umount.txt") == False:
            open(f"{flash}/umount.txt", "w")
            logging.info(f"'{flash}/umount.txt' was created successfully")
        else:
            logging.error("the umount file has already been created")
        return