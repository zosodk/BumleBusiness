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
    import shlex
    temp_logfile = logfile.copy()
    modified_logfile = []

    for line in temp_logfile:
        temp_line = shlex.split(line)

        save_initial_value = temp_line[0]
        temp_line[0] = f"timestamp={save_initial_value}"

        log_entry = {
            key: value
            for key, value in (item.split("=", 1) for item in temp_line)
        }

        modified_logfile.append(log_entry)

    length_original_logfile = len(logfile)
    counter = 0

    for log_entry in modified_logfile:
        if set(list_of_expected_content).issubset(log_entry.keys()):
            counter +=1

    return counter == length_original_logfile

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