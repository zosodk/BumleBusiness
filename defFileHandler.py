def parse_logfile_data(path):
    try:
        # åben filen
        logfile = open_logfile(path)

        # lad os formatere log-filen så vi har at gøre med en liste af strings
        logfile_as_list_of_strings = logfile.split("\n")

        # filens indhold skal tjekkes for mangler
        timestamp = has_timestamps(logfile_as_list_of_strings)

        # lad os formatere filen inden vi kontrollerer dens indhold yderligere for de forventede søjler
        logfile_as_list_of_directories = format_logfile(logfile_as_list_of_strings)

        # vi vil tjekke om filen indeholder et timestamp og om filen indeholder de oplysninger som vi forventer
        # vi forventer følgende indhold:
        expected_content = ["level", "user", "src_ip", "dest_host", "dest_port", "status", "msg"]

        has_content = has_expected_content(logfile_as_list_of_directories, expected_content)

        if timestamp and has_content:
            return logfile_as_list_of_directories

    except FileNotFoundError:
        return "File not found."

    except:
        return "An unknown error occurred."


def has_timestamps(logfile):

    # Hvis log-filen ikke er en liste, så alarmer brugeren om at vi forventer en liste
    if not isinstance(logfile, list):
        raise TypeError("Expected a list.")

    # Vi skal også tjekke om hver log er en string
    if not all(isinstance(log, str) for log in logfile):
        raise TypeError("All logs in the list must be strings.")

    from datetime import datetime
    import shlex

    for line in logfile:

        tokens = shlex.split(line)

        if not tokens:
            return False

        try:
            datetime.fromisoformat(tokens[0])

        # Vi kan tjekke for ValueError og IndexError
        except ValueError:
            return "Methods calls do not fit value type."

        except IndexError:
            return "Token can not be indexed."

    return True

def has_expected_content(logfile, list_of_expected_content):

    # Logfile should be a list of dictionaries
    if not isinstance(logfile, list):
        raise TypeError("For logfile we expect a list.")

    # Vi skal tjekke om indholdet i logfile er dictionaries, som vi forventer
    if not all(isinstance(log, dict) for log in logfile):
        raise TypeError("All items in logfile must be dictionaries.")

    # Hvis list_of_expected_content ikke er en liste, alarmér brugeren herom
    if not isinstance(list_of_expected_content, list):
        raise TypeError("For list_of_expected_content we expected a list.")

    # Vi skal tjekke om indholdet i list_of_expected_content er strings, ligesom vi forventer
    if not all(isinstance(prop, str) for prop in list_of_expected_content):
        raise TypeError("All items in the list_of_expected_content must be strings.")

    try:
        modified_logfile = logfile.copy()
        length_original_logfile = len(logfile)
        counter = 0

        for log_entry in modified_logfile:
            if set(list_of_expected_content).issubset(log_entry.keys()):
                counter +=1

        return counter == length_original_logfile

    except:
        return 'Something else went wrong.'

def format_logfile(logfile):

    # Hvis logfil ikke er en liste, så alarmer brugeren om at vi forventer en liste
    if not isinstance(logfile, list):
        raise TypeError("Expected a list.")

    # Vi skal også tjekke om hver log er en string
    if not all(isinstance(log, str) for log in logfile):
        raise TypeError("All logs in the list must be strings.")

    try:
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

        return modified_logfile
    except ValueError:
        return "Log indeholder ikke et lighedstegn ('=')."
    except IndexError:
        return "FEJL: Den valgte liste er tom."

def open_logfile(path):
    from pathlib import Path

    # Kontroller filendelse først
    # Hvorfor? Fordi vi forventer en .txt fil med logdata
    if Path(path).suffix.lower() != ".txt":
        return "Vælg venligst en .txt fil med logdata."

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

    # tjek for fejl relateret til styresystemet
    except OSError as err:
        return f"Operating system error: {err}"

    # tjek for andre tænkelige fejl
    except:
        return "An unknown error occurred."

if __name__ == '__main__':
    file = parse_logfile_data("cyber_security_log_sample.txt")