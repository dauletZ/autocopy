import time


def GetLampNumber(newFlash):
    import logging, os
    lampNumber = "00000"
    try:
        files = os.listdir(newFlash)
    except:
        if os.path.exists(newFlash) == True:
            time.sleep(1.5)
            files = os.listdir(newFlash)
        else:
            return "00000"
    for file in files:
        if file.startswith("CMC15_") and file.endswith("txt"):
            if len(newFlash) > 6:
                if newFlash[len(newFlash)-5:].isnumeric() == True:
                    lampNumber = newFlash[len(newFlash) - 5:]
    logging.info(f"Using next lamp number {lampNumber} for {newFlash}")
    return lampNumber