import multiprocessing

import yaml, logging
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
    mountOn = cfg["mountOn"]
    logging.info(f"Mounted a new flash drive {mountOn}{newFlashes} for copy to {folder}")
    lampnumber = GetLampNumber(f'{mountOn}{newFlashes}')
    CopyingMoviesFromFlash(folder, f"{mountOn}{newFlashes}", True, lampnumber)
    CopyingLogs(folder,f"{mountOn}{newFlashes}",lampnumber)

with open('settings.yml', encoding='utf-8') as ymlfile: # чтение конфига
    cfg = yaml.safe_load(ymlfile)
mountOn = cfg["mountOn"]

MountRemoteServer(cfg["server"]["local_endpoint"])
Logger()
logging.info("Running ETP AutoCopyPy v0.1.01")
logging.info("Using next configuration:")
logging.info("Poll interval:"+ str((cfg["timeouts"])["poll_interval"]))
logging.info("Endpoint for flash drives:" + cfg["mountOn"])
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




