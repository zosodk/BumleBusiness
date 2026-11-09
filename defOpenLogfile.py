def parse_logfile_data(path):

    # åben filen
    logfile = open_logfile(path)

    # filens indhold skal tjekkes for mangler
    # vi vil tjekke om filen indeholder et timestamp og om filen indeholder de oplysninger som vi forventer
    timestamp = has_timestamp(logfile)

    expected_content = has_expected_content(logfile)

    return timestamp and expected_content

def has_timestamp(logfile):
    return True

def has_expected_content(logfile):
    return True

def open_logfile(path):
    try:
        # hvis koden her nedenfor kører, så kan filen læses
        with open(path, "r") as logfile:
            content = logfile.read()
        return content

    # tjek først om filen eksisterer
    except FileNotFoundError:
        return "File not found."

    # tjek om brugeren har adgang til filen
    except PermissionError:
        return "You do not have permission to access this file."

    # tjek om filen kan læses
    except UnicodeDecodeError:
        return "File could not be read with UTF-8 encoding."

    # tjek for fejl relateret
    except OSError as err:
        return f"Operating system error: {err}"

    # tjek for andre tænkelige fejl
    except:
        return "An unknown error occurred."


file = parse_logfile_data("cyber_security_log_sample.txt")
print(file)