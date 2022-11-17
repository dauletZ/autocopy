
def CopyingLogs(folder, flash, lampnumber, saveFiles, logDevpath, DevLogPath, SysLogPath):
    import logging, os, datetime
    from app.Log.loggerforlamp import getLoggerForLamp
    getLoggerForLamp(folder,lampnumber, logDevpath)
    logging.info(f"Copying logs from {flash} to {folder}")
    if not os.path.exists(f"{flash}/logs"):
        logging.error("couldn't find logs folder")
        return
    try:
        files = os.listdir(f"{flash}/logs")
        for file in files:
            fullname = f"{flash}/logs/{file}"
            if os.path.isdir(fullname):
                continue
            if file.endswith("txt") == False:
                continue
            date = f"20{os.path.splitext(file)[0]}"
            if len(date) == 8:
                filedate = datetime.datetime(year=int(date[0:4]), month=int(date[4:6]), day=int(date[6:8]))
                dictPath = {'my_hostname': os.uname()[1], 'dev_nmb': lampnumber,
                            'cur_date': str(datetime.date.today()).replace("-", ""), 'file_date': date,
                            'cur_year': str(datetime.date.today().year), 'cur_mounth': datetime.datetime.now().strftime("%B"),
                            'cur_day': datetime.datetime.now().strftime('%d'), 'file_year': str(filedate.year),
                            'file_mounth': filedate.strftime("%B"),
                            'file_day': filedate.strftime("%d")}

                words = DevLogPath.split('/')
                i = 0
                for word in words:
                    if word in dictPath:
                        words[i] = dictPath[word]
                    i += 1
                Logpath = "/".join(words)
                if Logpath[-1] == '/':
                    Logpath = Logpath[:-1]
                logfolder = (f"{folder}{Logpath}")
                if not os.path.exists(logfolder):
                    os.makedirs(logfolder, exist_ok=True)
                logfile = f"{flash}/logs/{file}"
                f = open(logfile, encoding='cp1251').read()
                if not os.path.exists(f"{logfolder}"):
                    os.makedirs(f"{logfolder}", exist_ok=True)
                srfile = f"{logfolder}/{file}"
                serverfile = open(f"{srfile}", "w")
                serverfile.write(f)
                if saveFiles == 'false':
                    os.remove(logfile)
                    logging.info(f"remove log file {logfile}")
                    logging.info(f"log {file} was copied {logfolder} and removed")
                else:
                    logging.info(f"log {file} was copied {logfolder}")
        return
    except:
        logging.error(f"loging fatal error")
        return
