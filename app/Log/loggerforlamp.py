def getLoggerForLamp(folder, lampnumber, logDevPath):
    import logging,os
    from datetime import date
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    if not os.path.exists(f'{folder}{logDevPath}'):
        os.makedirs(f'{folder}{logDevPath}', exist_ok=True)
    return logging.basicConfig(handlers=(logging.FileHandler(f'{folder}/{logDevPath}/lamp_{str(date.today()).replace("-","")}.txt'), logging.StreamHandler()), level=logging.DEBUG,format=f"[{lampnumber}] %(asctime)s - %(message)s", datefmt = '%Y/%m/%d %H:%M:%S')  # логи
