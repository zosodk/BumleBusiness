def parse_logline(line):
    """
    modtager i linie fra logfilen og returnerer et dictionary med key,value pairs af log liniens indhold
    :param line:
    :return: dictionary med key, value
    """
    #shlex er en package vi fandt som kan  læse separerede ord i en linie (tab, komma, liniemellemrum osv)
    # den returnerer en linie som et dictionary.
    #Dvs - vi læser en linie og smider den over i en dictionary og returnerer denne - bliver brugt i et andet gennemlæb.
    import shlex
    parts = shlex.split(line)
    #print(parts)

    data = {"timestamp": parts[0]}
    for item in parts[1:]:
        key, value = item.split("=", 1)
        data[key] = value

    return data

def openLogfile(filename):
    """
    Viser indholdet af en fil, der parses igennem parse_logline(line) funktionen...brugt i starten til test.
    Bruges også i hovedprogrammet til at vise indholdet direkte fra filen i konsollen.
    """
    with open(filename, "r", encoding="utf-8") as fil:

        for linie in fil:
            loglinie = parse_logline(linie)
            print(loglinie)

if __name__ == '__main__':
    openLogfile("cyber_security_log_sample.txt")