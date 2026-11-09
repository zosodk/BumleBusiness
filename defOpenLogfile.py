def parse_logfile_data(path):

    # åben filen
    logfile = open_logfile(path)

    # filens indhold skal tjekkes for mangler
    timestamp = has_timestamp(logfile)

    # vi vil tjekke om filen indeholder et timestamp og om filen indeholder de oplysninger som vi forventer
    expected_content = has_expected_content(logfile)

    return timestamp and expected_content

def has_timestamp(logfile):
    from datetime import datetime

    line = '2026-03-01T08:01:17 level=INFO event=LOGIN_SUCCESS user=eve src_ip=10.0.0.5 dest_host=db01 dest_port=53 status=OK msg="User authenticated successfully"'

    try:
        datetime.fromisoformat(line[:19])
    except ValueError:
        print('Not a timestamp')
    else:
        print('Found a timestamp')

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