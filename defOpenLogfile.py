def parse_logfile_data(path):

    # åben filen
    logfile = open_logfile(path)

    # lad os formatere logfilen så vi har at gøre med en liste af strings
    logfile_as_list = logfile.split("\n")

    # filens indhold skal tjekkes for mangler
    timestamp = has_timestamps(logfile_as_list)

    # vi vil tjekke om filen indeholder et timestamp og om filen indeholder de oplysninger som vi forventer
    # vi forventer følgende indhold:
    expected_content = ["level", "user", "src_ip", "dest_host", "dest_port", "status", "msg"]

    has_content = has_expected_content(logfile_as_list, expected_content)

    return timestamp and has_content

def has_timestamps(logfile):
    from datetime import datetime
    count = 0

    while count < len(logfile):
        for line in logfile:
            try:
                datetime.fromisoformat(line[:19])
            except:
                print('No timestamp found!')
                break
            else:
                count += 1

    if count == len(logfile):
        return True
    else:
        return False

def has_expected_content(logfile, list_of_expected_content):
    print("Logfile content:", logfile)
    print("Expected content:", list_of_expected_content)

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