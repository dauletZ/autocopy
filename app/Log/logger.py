def Logger():
    import yaml, logging, os
    from datetime import date
    with open('settings.yml', encoding='utf-8') as ymlfile: # чтение конфига
        cfg = yaml.safe_load(ymlfile)
    hostname = os.uname()[1]
    folder = "{}{}".format(cfg["server"]["local_endpoint"], cfg["server"]["folder"])
    logging.basicConfig(level=logging.DEBUG,filename=f'{folder}/+logs/{hostname}/sys_{str(date.today()).replace("-","")}.txt', format= "%(asctime)s - %(message)s") #логи
    return