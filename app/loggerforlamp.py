def getLoggerForLamp(folder, lampNumber):
    import logging
    from datetime import date
    now = str(date.today()).replace("-","")
    dir = f"{folder}/{now}/{lampNumber}/logs"
    logging.basicConfig(level=logging.DEBUG, filename=f"{dir}/lamp_{now}.txt",format="%(asctime)s - %(message)s")  # логи
    return 0