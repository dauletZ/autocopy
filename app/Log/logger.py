def Logger(path):
    import yaml, logging, os
    from datetime import date
    with open('settings.yml', encoding='utf-8') as ymlfile: # чтение конфига
        cfg = yaml.safe_load(ymlfile)
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    folder = "{}{}".format(cfg["server"]["local_endpoint"], cfg["server"]["folder"])
    if not os.path.exists(f'{folder}{path}'):
        os.makedirs(f'{folder}{path}')
    logging.basicConfig(handlers=(logging.FileHandler(f'{folder}{path}/sys_{str(date.today()).replace("-","")}.txt'), logging.StreamHandler()),level=logging.DEBUG, format= "%(asctime)s - %(message)s", datefmt = '%Y/%m/%d %H:%M:%S') #логи
    return