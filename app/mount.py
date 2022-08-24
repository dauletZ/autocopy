def IsMounted(localfolder):
    import os
    com = os.popen("sh -c mount | grep /home/pi/winserver")
    res = com.readlines()
    com.close()
    if len(res) > 0:
        return True
    return False

def MountRemoteServer(localfolder):
    import os, logging, time
    if IsMounted(localfolder) == False:
        os.popen(f"mount {localfolder}")
        time.sleep(0.2)
        if IsMounted(localfolder) == True:
            logging.info(f"MS server mounted to {localfolder}")
        else:
            logging.error(f"Failed mounted server to {localfolder}")
    return
