def GetLampNumber(newFlash):
    import logging, os
    from app.Log.logger import Logger
    Logger()
    lampNumber = "00000"
    files = os.listdir(newFlash)
    for file in files:
        if file.startswith("CMC15_") and file.endswith("txt"):
            if len(newFlash) > 6:
                if newFlash[len(newFlash)-5:].isnumeric() == True:
                    lampNumber = newFlash[len(newFlash) - 5:]
    logging.info(f"Using next lamp number {lampNumber} for {newFlash}")
    return lampNumber