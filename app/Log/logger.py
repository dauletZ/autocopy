def Logger():
    import yaml, logging, os
    from datetime import date
    with open('settings.yml', encoding='utf-8') as ymlfile: # чтение конфига
        cfg = yaml.safe_load(ymlfile)
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    hostname = os.uname()[1]
    folder = "{}{}".format(cfg["server"]["local_endpoint"], cfg["server"]["folder"])
    if not os.path.exists(f'{folder}/+logs/{hostname}'):
        os.makedirs(f'{folder}/+logs/{hostname}')
    logging.basicConfig(handlers=(logging.FileHandler(f'{folder}/+logs/{hostname}/sys_{str(date.today()).replace("-","")}.txt'), logging.StreamHandler()),level=logging.DEBUG, format= "%(asctime)s - %(message)s", datefmt = '%Y/%m/%d %H:%M:%S') #логи
    return