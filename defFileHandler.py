def parse_logfile_data(path):
    """
    Beskrivelse af funktionen:

        Funktionen starter med at åbne en log-fil af ved at kalde funktionen open_logfile().
        Forudsat at dette går som forventet, omformes data udlæst fra log-filen til en liste af strings.

        Nu hvor vi er så langt, er vi klar til at tjekke om alle elementer (strings) i vores liste indeholder et
        timestamp. Derefter omformer vi vores liste med strings til en liste bestående af dictionaries. Hver dictionary
        indeholder de samme data som vores strenge indeholdt.

        Begge disse funktioner returnerer 'true' såfremt vores lister indeholder hvad vi forventer.
        Såfremt begge funktioner returnerer 'true', returnerer funktionen vores liste med dictionaries.

    Args:
        path (str): relativ path til log-filen på brugerens system

    Returns:
        list: liste af dictionaries som indeholder data fra den originale log-fil
    """

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
    """
    Beskrivelse af funktionen:
        Funktionen tjekker om hver linje streng i listen logfile indeholder et timestamp.

    Args:
        logfile (list): liste af strenge

    Returns:
        bool: returnerer true hvis alle strenge i listen indeholder et timestamp
        ellers returneres en fejlmeddelelse eller false.
    """

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

    """
    Beskrivelse af funktionen:

        Opgaven gennemgår en liste af dictionaries og sammenholder keys i hver dictionary med indholdet i
        list_of_expected_content. Hvis alt går godt får vi 'true' retur. Ellers får vi en fejlmeddelelse.

    Args:
        logfile (list): liste med dictionaries
        list_of_expected_content (list): liste af dictionaries som strenge med keys som vi forventer at finde i hver
        linje af vores logfile liste

    Returns:
        bool: true, hvis alle dictionaries i vores streng indeholder alle de key's som vi som minimum forventer
        fremgår
        Ellers får vi en fejlmeddelelse
    """

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
    """
    Beskrivelse af funktionen:

        Funktionens eneste opgave er at omforme en liste af strenge til en liste af dictionaries.

        Vi gennemgår vores liste med strenge én linje af gangen.
        Vi bruger et bibliotek kaldet shlex for at splitte vores strenge efter mellemrum. Shlex biblioteket er ment
        til bash commands men dets plit funktion virker til vores formãl. Derfor bruger vi den.

        Det smarte ved at bruge shlex.split() funktionen er, at vi for splittet vores streng efter mellemrum uden at
        værdien af msg i hver linje også bliver splittet, idet mellemrum imellem hvert ord fremgår her.

        På nuværende tidspunkt har vi stadig en liste bestående af lister af strenge, der nu ser således ud:
        ['2026-03-01T08:01:17', 'level=INFO', 'event=LOGIN_SUCCESS', 'user=eve', ...]

        Inden at vi laver key-value pairs og omformer til en liste af dictionaries, indsætter vi 'timestamp='
        ['timestamp=2026-03-01T08:01:17', 'level=INFO', 'event=LOGIN_SUCCESS', 'user=eve', ...]

        Nu kommer vi til at vi gerne vil omforme vores inderste liste af strenge til dictionaries.

        Vi starter med at gennemgå hvert element (streng) i lister og splitte efter '='.
        Vores liste og elementer ser da sådan her ud:
        [['timestamp', '2026-03-01T08:01:17'], ['level', 'INFO'], ['event', 'LOGIN_SUCCESS'], ['user', 'eve'], ...]

        Så finder vi key, value pairs sã alt til venstre for lighedstegnene er keys og alt til venstre er value for den
        pågældende key. Der dannes en dictionary for hver linje i vores log-fil og disse dictionaries smides ind i en ny
        tom liste som vi har lavet. Nedenfor ses et eksempel på en af disse dictionaries i den endelige liste:

        {'timestamp': '2026-03-01T08:01:17', 'level': 'INFO', 'event': 'LOGIN_SUCCESS', 'user': 'eve', ...}

        Det er denne liste, som funktionen returnerer hvis alt gik godt undervejs.

    Args:
        logfile (list): liste af strenge. Hver streng svarer til en log entry i den originale log-fil

    Returns:
        list: liste af dictionaries som indeholder data fra den originale log-fil
    """
    import shlex

    # Hvis logfil ikke er en liste, så alarmer brugeren om at vi forventer en liste
    if not isinstance(logfile, list):
        raise TypeError("Expected a list.")

    # Vi skal også tjekke om hver log er en string
    if not all(isinstance(log, str) for log in logfile):
        raise TypeError("All logs in the list must be strings.")

    try:
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
    """
    Beskrivelse af funktionen:

    Funktionen åbner log-filen såfremt alt går godt. Hvis nogle af de fejl, som vi tjekker for opstår,
    så får brugeren en fejlmeddelelse i konsollen.

    Args:
        path (str): relativ path til log-filen på brugerens system

    Returns:
        str: log-filens indhold i form af strenge repareret af linjeskift
        Ellers får brugeren en fejlmeddelelse
    """
    from pathlib import Path

    # Kontroller filendelse først
    # Hvorfor? Fordi vi forventer en .txt fil med log-data
    if Path(path).suffix.lower() != ".txt":
        return "Vælg venligst en .txt fil med log-data."

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