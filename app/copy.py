
def getSubdirs(filename):
    if len(filename) >=16:
        code = filename[:5]
        date = filename[7:15]
    return date, code

def prepareCopy(fullpath, remote):
    import os, logging
    from app.Log.logger import Logger
    Logger()
    filename = os.path.split(fullpath)[1]
    date, code = getSubdirs(filename)
    remotefolder = f"{remote}/{date}/{code}"
    if not os.path.exists(remotefolder):
        os.makedirs(remotefolder)
    hostname = os.uname()[1]
    remotefile = f"{remotefolder}/{filename}"
    newfile = remotefile
    i=0
    while True:
        i+=1
        if os.path.exists(newfile) == True:
            logging.info(f"File {newfile} is already exists!")
            newfile = f"{remotefile[:len(filename)-4]}{i}{remotefile[len(filename)-4:]}"
        else:
            break
    logging.info(f"start copy {filename} from {hostname}//{fullpath} to {newfile}")
    os.system(f'cp {fullpath} {newfile}')
    logging.info(f"Copy file {fullpath} to {newfile}")
    if os.path.isfile(f"{fullpath}"):
        os.remove(f'{fullpath}')
        logging.info(f"File {filename} was copied and removed succesfully")
    else:
        logging.error(f"File {filename} doesn't exist!")
    return 


def CopyingMoviesFromFlash(remote, flash, isBaselevel):
    import os, logging
    from app.Log.logger import Logger
    Logger()
    files = os.listdir(flash)
    for file in files:
        fullname = f"{flash}/{file}"
        if file == "logs":
            continue
        if os.path.isdir(fullname) ==True:
            CopyingMoviesFromFlash(remote, fullname, False)
            continue
        if file.endswith('MP4') == False:
            continue
        prepareCopy(fullname, remote)
    if isBaselevel == True:
        if os.path.exists(f"{flash}/umount") == False:
            fileUmount = os.mkdir(f"{flash}/umount")
            logging.info(f"'{flash}/umount' was created successfully")
        else:
            logging.error("the umount folder has already been created")
        return