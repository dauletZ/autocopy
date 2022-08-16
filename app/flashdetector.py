def FlashDetector(pref, mountedFlash): #pref - путь к флешкам,
    import os, time, logging
    from app.Log.logger import Logger
    Logger()
    mountDir = os.listdir(pref)
    newFlashes = []
    for f in mountedFlash:
        if f not in mountDir:
            mountedFlash.remove(f)
            logging.info(f"flash {f} isn't active")
    while mountDir == mountedFlash:
        mountDir = os.listdir(pref)
        time.sleep(0.5)
    for dir in mountDir:
        findmnt = os.popen(f"findmnt {pref}{dir}")
        res = findmnt.readlines()
        if len(res) == 0:
            mountedFlash.append(dir)
    for flash in mountDir:
        if flash not in mountedFlash:
            newFlashes.append(flash)
            mountedFlash.append(flash)
            logging.info(f"Found a new flash! Endpoint:{pref}{flash}")
    return mountedFlash, newFlashes
