
def FlashDetector(pref, mountedFlash): #pref - путь к флешкам, endpoint к серверу
    import os, time, logging
    from app.Log.logger import Logger
    Logger()
    mountDir = os.listdir(pref)
    key = 0
    newFlashes = []
    for f in mountedFlash:
        if f not in mountDir:
            logging.info(f"flash {f} isn't active")
            mountedFlash.remove(f)
    while mountDir == mountedFlash:
        mountDir = os.listdir(pref)
        time.sleep(0.5)
        key+=1
    for flash in mountDir:
        if flash not in mountedFlash:
            newFlashes.append(flash)
            mountedFlash.append(flash)
            logging.info(f"Found a new flash! Endpoint:{pref}{flash}")
    return mountedFlash, newFlashes
