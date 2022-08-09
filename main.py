import yaml, logging
from app.flashdetector import *
from app.lampnumber import *
from app.Log.logger import Logger
from app.mount import MountRemoteServer
from app.copy import CopyingMoviesFromFlash

with open('settings.yml', encoding='utf-8') as ymlfile: # чтение конфига
    cfg = yaml.safe_load(ymlfile)
ServerPath = cfg["server"]["path"]
folder = "{}{}".format(cfg["server"]["local_endpoint"], cfg["server"]["folder"])
mountOn = cfg["mountOn"]
poll_interval = cfg["timeouts"]

MountRemoteServer(ServerPath, cfg["server"]["local_endpoint"])
Logger()
logging.info("Using next configuration:")
logging.info("Path for upload:"+ cfg["server"]["path"])
logging.info("Poll interval:"+ str((cfg["timeouts"])["poll_interval"]))
logging.info("Endpoint for flash drives:" + cfg["mountOn"])
logging.info("Start listening a new USB flashes")

mountedFlash = []
while True:
    mountedFlash, newFlash = FlashDetector(mountOn, mountedFlash)
    if newFlash !="":
        logging.info(f"Mounted a new flash drive {mountOn}{newFlash} for copy to {folder}")
        lampnumber = GetLampNumber(newFlash)
        CopyingMoviesFromFlash(folder,f"{mountOn}{newFlash}",True)


