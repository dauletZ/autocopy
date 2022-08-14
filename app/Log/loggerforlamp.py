def getLoggerForLamp(folder, lampnumber):
    import logging,os
    from datetime import date
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    if not os.path.exists(f'{folder}/{str(date.today()).replace("-","")}/{lampnumber}/logs/'):
        os.makedirs(f'{folder}/{str(date.today()).replace("-","")}/{lampnumber}/logs/', exist_ok=True)
    return logging.basicConfig(handlers=(logging.FileHandler(f'{folder}/{str(date.today()).replace("-","")}/{lampnumber}/logs/lamp{lampnumber}.txt'), logging.StreamHandler()), level=logging.DEBUG,format=f"[{lampnumber}] %(asctime)s - %(message)s", datefmt = '%Y/%m/%d %H:%M:%S')  # логи
