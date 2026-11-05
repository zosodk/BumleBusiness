def parse_logline(line):
    """
    modtager i linie fra logfilen og returnerer et dictionary med key,value pairs af log liniens indhold
    :param line:
    :return: dictionary med key, value
    """

    import shlex
    parts = shlex.split(line)
    #print(parts)

    data = {"timestamp": parts[0]}
    for item in parts[1:]:
        key, value = item.split("=", 1)
        data[key] = value

    return data

def openLogfile(filename):
    with open(filename, "r", encoding="utf-8") as fil:

        for linie in fil:
            loglinie = parse_logline(linie)
            print(loglinie)

if __name__ == '__main__':
    openLogfile("cyber_security_log_sample.txt")