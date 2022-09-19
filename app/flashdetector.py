def FlashDetector(pref, mountedFlash): #pref - путь к флешкам,
    import os, time, logging, pathlib
    mountDir = os.listdir(pref)
    newFlashes = []
    while mountDir == mountedFlash:
        mountDir = os.listdir(pref)
        time.sleep(0.5)
    for f in mountedFlash:
        if f not in mountDir:
            mountedFlash.remove(f)
            logging.info(f"Flash {f} isn't active")
    for dir in mountDir:
        if pathlib.Path(f"{pref}{dir}").is_mount() == False:
            if dir not in mountedFlash:
                time.sleep(1)
                if pathlib.Path(f"{pref}{dir}").is_mount() == False:
                    mountedFlash.append(dir)
    for flash in mountDir:
        if flash not in mountedFlash:
            newFlashes.append(flash)
            mountedFlash.append(flash)
            logging.info(f"Found a new flash! Endpoint:{pref}{flash}")
    return (mountedFlash, newFlashes)
