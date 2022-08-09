def GetLampNumber(newFlash):
    import logging
    from app.Log.logger import Logger
    Logger()
    lampNumber = "00000"
    if newFlash.startswith("CMC15_"):
        if len(newFlash) > 6:
            if newFlash[len(newFlash)-5:].isnumeric() == True:
                lampNumber = newFlash[len(newFlash) - 5:]
    logging.info(f"Using next lamp number {lampNumber} for {newFlash}")
    return lampNumber