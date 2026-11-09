def open_logfile(path):
    try:
        # hvis koden her nedenfor kører, så kan filen læses
        with open(path, "r") as logfile:
            content = logfile.read()
        return content
    except FileNotFoundError:
        print("File not found")
        return None


file = open_logfile("cyber_security_log_sample.txt")
print(file)