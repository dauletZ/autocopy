def CopyingLogs(folder,flash,lampnumber, saveFiles, logDevpath):
    import logging, os
    from app.Log.loggerforlamp import getLoggerForLamp
    getLoggerForLamp(folder,lampnumber, logDevpath)
    logging.info(f"Copying logs from {flash} to {folder}")
    if not os.path.exists(f"{flash}/logs"):
        logging.error("couldn't find logs folder")
        return
    files = os.listdir(f"{flash}/logs")
    for file in files:
        fullname = f"{flash}/logs/{file}"
        if os.path.isdir(fullname):
            continue
        if file.endswith("txt") == False:
            continue
        logfolder = (f"{folder}/20{os.path.splitext(file)[0]}/{lampnumber}")
        if not os.path.exists(logfolder):
            os.makedirs(logfolder, exist_ok=True)
        logfile = f"{flash}/logs/{file}"
        f = open(logfile, encoding='cp1251').read()
        logging.info(f"Reading log file {file} ")
        if not os.path.exists(f"{logfolder}"):
            os.makedirs(f"{logfolder}", exist_ok=True)
        srfile = f"{logfolder}/{file}"
        serverfile = open(f"{srfile}", "w")
        logging.info(f"open remote log file {file}")
        serverfile.write(f)
        logging.info(f"write remote log file {file}")
        if saveFiles == 'false':
            os.remove(logfile)
            logging.info(f"remove log file {logfile}")
            logging.info(f"log {file} was copied {logfolder} and removed")
        else:
            logging.info(f"log {file} was copied {logfolder}")
        return
