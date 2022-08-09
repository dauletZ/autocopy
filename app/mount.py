def IsMounted(localfolder):
    import os
    com = os.popen("sh -c mount | grep /home/pi/winserver")
    res = com.readlines()
    if len(res) > 0:
        return True
    return False

def MountRemoteServer(path, localfolder):
    import os, logging
    if IsMounted(localfolder) == False:
        os.popen(f"mount.cifs {path} {localfolder}")
        from app.Log.logger import Logger
        Logger()
        logging.info(f"MS server mounted to {localfolder}")
    return
