from defDbHandler import connect_to_db
import numpy as np
import sqlite3
from sqlite3 import Error
import matplotlib.pyplot as plt

def scatterplot(conn,tabelname, xdata, ydata, parameter, xlabel, ylabel, titel):
    """
    denne funktion tager et vilkårligt table og laver
    et scatter plot ud fra 2 dataer som
    man gerne vil analysere også bruger
    den en parameter til at finde ud af
    hvad den skal søge efter i en colum
    :param conn:
    :param tabelname:
    :param xdata:
    :param ydata:
    :param parameter:
    :param xlabel:
    :param ylabel:
    :param titel:
    :return: bool
    """
    try:
        xakse = []
        yakse = []
        cursor = conn.cursor()

        #læser et table og finder hvor mange gange en bestemt ting sker
        cursor.execute(f"""
            SELECT {xdata}, COUNT(*)
            FROM {tabelname}
            WHERE {ydata} LIKE ?
            GROUP BY {xdata}
        """, (parameter,))
        data = cursor.fetchall()
        #print(data)
        for tuple in data:
            xakse.append(tuple[0])
            yakse.append(tuple[1])

        #laver selve plottet
        plt.rcParams["figure.figsize"] = [20, 5]
        plt.scatter(xakse, yakse)
        plt.title(titel)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)

        plt.show()
        return True
    except Error as e:
        print(f"Scatterplot failed: {e}")
        return False

def scatterplotMedTendensLinje(conn,tabelname, xdata, ydata, parameter, xlabel, ylabel, titel):
    """
    denne funktion tager et vilkårligt table og laver
    et scatter plot ud fra 2 dataer som
    man gerne vil analysere også bruger
    den en parameter til at finde ud af
    hvad den skal søge efter i en colum
    :param conn:
    :param tabelname:
    :param xdata:
    :param ydata:
    :param parameter:
    :param xlabel:
    :param ylabel:
    :param titel:
    :return: bool
    """
    try:
        xakse = []
        yakse = []
        cursor = conn.cursor()

        #læser et table og finder hvor mange gange en bestemt ting sker
        cursor.execute(f"""
            SELECT {xdata}, COUNT(*)
            FROM {tabelname}
            WHERE {ydata} = ?
            GROUP BY {xdata}
        """, (parameter,))
        data = cursor.fetchall()
        #print(data)
        for tuple in data:
            xakse.append(tuple[0])
            yakse.append(tuple[1])

        #laver selve plottet
        x_numeric = list(range(len(xakse)))

        a, b = np.polyfit(x_numeric, yakse, 1)

        plt.rcParams["figure.figsize"] = [20, 5]

        plt.scatter(x_numeric, yakse)
        plt.plot(x_numeric, [a * x + b for x in x_numeric])

        plt.title(titel)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)

        plt.xticks(x_numeric, xakse)

        plt.show()
        return True
    except Error as e:
        print(f"Scatterplot failed: {e}")
        return False

def piechart(conn,tabelname, coulum, titel):
    labels = []
    count = []
    cursor = conn.cursor()

    # læser et table og finder hvor mange gange en bestemt ting sker
    cursor.execute(f"""
                SELECT {coulum}, COUNT(*)
                FROM {tabelname}
                GROUP BY {coulum}
            """,)
    data = cursor.fetchall()
    # print(data)
    for tuple in data:
        labels.append(tuple[0])
        count.append(tuple[1])

    plt.pie(count, labels=labels, autopct='%1.1f%%')
    plt.title(titel)
    plt.show()
def timestamperlevel(conn,time):
    cursor = conn.cursor()
    cursor.execute(f"""
    SELECT 
        datetime((unixepoch(timestamp) / {time}) * {time}, 'unixepoch') AS interval_start,
        COUNT(*) AS total_events,
        SUM(CASE WHEN level = 'INFO' THEN 1 ELSE 0 END) AS count_info,
        SUM(CASE WHEN level = 'WARN' THEN 1 ELSE 0 END) AS count_warn,
        SUM(CASE WHEN level = 'ALERT' THEN 1 ELSE 0 END) AS count_alert,
        -- Højeste sværhedsgrad i det pågældende kvarter
        MAX(CASE UPPER(level)
            WHEN 'INFO'  THEN 1
            WHEN 'WARN'  THEN 2
            WHEN 'ALERT' THEN 3
            ELSE 0
        END) AS peak_severity
    FROM 
        logdata
    WHERE event = 'PORT_SCAN_DETECTED' OR 'MALWARE_SIGNATURE_MATCH'
    GROUP BY 
        interval_start
    ORDER BY 
        interval_start ASC;
        """)
    data = cursor.fetchall()
    return data

def timestamperevent(conn,time):
    cursor = conn.cursor()
    cursor.execute(f"""
    SELECT 
        datetime((unixepoch(timestamp) / {time}) * {time}, 'unixepoch') AS interval_start,
        COUNT(*) AS total_events,
        SUM(CASE WHEN event = 'LOGIN_FAILED' THEN 1 ELSE 0 END) AS count_LOGIN_FAILED,
        SUM(CASE WHEN event = 'FILE_ACCESS_DENIED' THEN 1 ELSE 0 END) AS count_FILE_ACCESS_DENIED,
        SUM(CASE WHEN level = 'PASSWORD_RESET' THEN 1 ELSE 0 END) AS count_PASSWORD_RESET,
        SUM(CASE WHEN level = 'PORT_SCAN_DETECTED' THEN 1 ELSE 0 END) AS count_PORT_SCAN_DETECTED,
        SUM(CASE WHEN level = 'PRIVILEGE_ESCALATION_ATTEMPT' THEN 1 ELSE 0 END) AS count_PRIVILEGE_ESCALATION_ATTEMPT,
        SUM(CASE WHEN level = 'USB_DEVICE_ATTACHED' THEN 1 ELSE 0 END) AS count_USB_DEVICE_ATTACHED,
        SUM(CASE WHEN level = 'MALWARE_SIGNATURE_MATCH' THEN 1 ELSE 0 END) AS count_MALWARE_SIGNATURE_MATCH,
        -- Højeste sværhedsgrad i det pågældende kvarter
        MAX(CASE UPPER(level)
            WHEN 'LOGIN_FAILED'  THEN 1
            WHEN 'FILE_ACCESS_DENIED'  THEN 2
            WHEN 'PASSWORD_RESET' THEN 3
            WHEN 'PORT_SCAN_DETECTED' THEN 4
            WHEN 'PRIVILEGE_ESCALATION_ATTEMPT' THEN 5
            WHEN 'USB_DEVICE_ATTACHED' THEN 6
            WHEN 'MALWARE_SIGNATURE_MATCH' THEN 7
            ELSE 0
        END) AS peak_severity
    FROM 
        logdata
    WHERE status = 'OK'
    GROUP BY 
        interval_start
    ORDER BY 
        interval_start ASC;
        """)
    data = cursor.fetchall()
    return data

def scatterplotTime(conn, titel,xlabel,ylabel ):
    levelType = int(input(f"skriv 1 for at se info\n"
                      f"skriv 2 for at se warnings\n"
                      f"skriv 3 for at se alerts"))

    tidsinterval = int(input(f"skriv dit tidsinterval i minutter"))
    tidsinterval *= 60
    xakse = []
    yakse = []
    try:
        data = timestamperevent(conn, tidsinterval)
        print(data)
        for tuple in data:
            if tuple[levelType+1] > 0:
                xakse.append(tuple[0])
                yakse.append(tuple[levelType+1])

        #laver selve plottet
        plt.rcParams["figure.figsize"] = [20, 5]
        plt.bar(xakse, yakse)
        plt.title(titel)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)

        plt.show()
        return True
    except Error as e:
        print(f"Scatterplot failed: {e}")
        return False
def barchart(conn,tabelname, xdata, ydata, parameter, xlabel, ylabel, titel):
    """
    denne funktion tager et vilkårligt table og laver
    et scatter plot ud fra 2 dataer som
    man gerne vil analysere også bruger
    den en parameter til at finde ud af
    hvad den skal søge efter i en colum
    :param conn:
    :param tabelname:
    :param xdata:
    :param ydata:
    :param parameter:
    :param xlabel:
    :param ylabel:
    :param titel:
    :return: bool
    """
    try:
        xakse = []
        yakse = []
        cursor = conn.cursor()

        #læser et table og finder hvor mange gange en bestemt ting sker
        cursor.execute(f"""
            SELECT {xdata}, COUNT(*)
            FROM {tabelname}
            WHERE {ydata} = ?
            GROUP BY {xdata}
        """, (parameter,))
        data = cursor.fetchall()
        #print(data)
        for tuple in data:
            xakse.append(tuple[0])
            yakse.append(tuple[1])

        #laver selve plottet
        plt.rcParams["figure.figsize"] = [20, 5]
        plt.bar(xakse, yakse)
        plt.title(titel)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)

        plt.show()
        return True
    except Error as e:
        print(f"Scatterplot failed: {e}")
        return False

def allUserEvents(conn, user, tabelname):
    cursor = conn.cursor()
    cursor.execute(f"""SELECT * FROM {tabelname} WHERE user = '{user}' """)
    data = cursor.fetchall()
    return data


if __name__ == "__main__":
    connection = connect_to_db()

    #print ønsked bruger
    #bruger = input(f"indtast ønsked brugers navn")
    #historik = allUserEvents(connection, bruger, 'logdata')
    #for item in historik:
    #    print(item)
    #scatterplot(connection, "logdata", 'timestamp', 'user', 'walter', "time", "events","logdata" )

    #malware per user detected
    #scatterplot(connection, "logdata", "user","event", "MALWARE_SIGNATURE_MATCH", "users", "amount of malware per user detected", "logdata")
    #barchart(connection, "logdata", "user", "event", "MALWARE_SIGNATURE_MATCH", "users",
                #"amount of malware per user detected", "logdata")

    #check walters events
    #scatterplot(connection, "logdata", "event", "user", "walter", "events",
                #"walters events", "logdata")
    #barchart(connection, "logdata", "event", "user", "walter", "events",
                #"walters events", "logdata")

    #scatterplotMedTendensLinje(connection, "logdata", "user", "level","ALERT" , "Ipadresses", "walters logins", "logdata")
    piechart(connection, "logdata", "event", "logdata")
    #timestamper(connection)
    scatterplotTime(connection,"titel", "xlabel", "ylabel")

