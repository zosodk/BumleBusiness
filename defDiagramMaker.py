from defDbHandler import connect_to_db
import numpy as np
import sqlite3
from sqlite3 import Error
import matplotlib.pyplot as plt

def scatterplot(conn,tabelname, xdata, ydata, parameter):
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
        plt.title(f"{xdata} in {parameter}")
        plt.xlabel(xdata)
        plt.ylabel(parameter)

        plt.show()
        return True
    except Error as e:
        print(f"Scatterplot failed: {e}")
        return False

def scatterplotMedTendensLinje(conn,tabelname, xdata, ydata, parameter):
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
        print(data)
        for tuple in data:
            xakse.append(tuple[0])
            yakse.append(tuple[1])

        #laver selve plottet
        x_numeric = list(range(len(xakse)))

        a, b = np.polyfit(x_numeric, yakse, 1)

        plt.rcParams["figure.figsize"] = [20, 5]

        plt.scatter(x_numeric, yakse)
        plt.plot(x_numeric, [a * x + b for x in x_numeric])

        plt.title(f'{xdata} sat med {parameter}')
        plt.xlabel(xdata)
        plt.ylabel(parameter)

        plt.xticks(x_numeric, xakse)

        plt.show()
        return True
    except Error as e:
        print(f"Scatterplot failed: {e}")
        return False

def piechart(conn,tabelname, coulum, titel):
    try:
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
        return True
    except Error as e:
        print(f"Scatterplot failed: {e}")
        return False

def piechartspecefic(conn,tabelname, coulum, titel, coulum2,parameter):
    try:
        labels = []
        count = []
        cursor = conn.cursor()
        # læser et table og finder hvor mange gange en bestemt ting sker
        cursor.execute(f"""
                    SELECT {coulum}, COUNT(*)
                    FROM {tabelname}
                    WHERE {coulum2} = ?
                    GROUP BY {coulum}
                """,(parameter,))
        data = cursor.fetchall()
        # print(data)
        for tuple in data:
            labels.append(tuple[0])
            count.append(tuple[1])

        plt.pie(count, labels=labels, autopct='%1.1f%%')
        plt.title(titel)
        plt.show()
        return True
    except Error as e:
        print(f"Scatterplot failed: {e}")
        return False

def barchart(conn,tabelname, xdata, ydata, parameter):
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
        plt.title(f"{xdata} in {parameter}")
        plt.xlabel(xdata)
        plt.ylabel(parameter)

        plt.show()
        return True
    except Error as e:
        print(f"Barchart failed: {e}")
        return False

def historyCreater(conn,tabelname, coulum, valueInCoulum, parameter):
    try:
        cur = conn.cursor()
        timestamp = []
        searchList = []

        cur.execute(f"SELECT * FROM {tabelname} WHERE {coulum} = ?", (valueInCoulum,))
        df = cur.fetchall()
        # Luk forbindelsen
        conn.close()

        # Tjek om der er data
        if len(df) <= 0:
          print('Ingen data fundet for denne IP-adresse.')
        else:
          # Konverter tidskolonnen til datetime-objekter
          #
            if parameter == "level":
                paramIndex = 2
            elif parameter == "event":
                paramIndex = 3
            elif parameter == "user":
                paramIndex = 4
            elif parameter == "src_ip":
                paramIndex = 5
            elif parameter == "dest_host":
                paramIndex = 6
            elif parameter == "dest_port":
                paramIndex = 7
            elif parameter == "msg":
                paramIndex = 8
            for tuple in df:
                timestamp.append(tuple[1])
                searchList.append(tuple[paramIndex])


            # Opsætning af Scatter Plot
            plt.figure(figsize=(20, 6))

            # Plot tidspunkt (X-akse) mod f.eks. statuskode (Y-akse)
            # Erstat 'status_code' med den kolonne derskal analyseres på Y-aksen
            plt.scatter(
                timestamp,
                searchList,
                alpha=0.7,
                edgecolors='k',
                s=50,
                color='royalblue',
            )

            plt.title(
              f'{parameter} for {coulum} : {valueInCoulum} (taken from database)', fontsize=14
            )

            plt.xlabel('timestamp', fontsize=12)
            plt.ylabel('values', fontsize=12)

            # Gør datoerne på X-aksen læsevenlige
            plt.gcf().autofmt_xdate()

            plt.grid(True, linestyle='--', alpha=0.5)
            plt.tight_layout()

            # Vis plottet
            plt.show()
            return True
    except Error as e:
        print(f"historik failed: {e}")

if __name__ == "__main__":
    connection = connect_to_db()

    #scatterplot(connection, "logdata", 'timestamp', 'user', 'walter', "time", "events","logdata" )

    #malware per user detected
    #scatterplot(connection, "logdata", "event","src_ip", "198.51.100.23", "users", "amount of malware per user detected", "logdata")
    #barchart(connection, "logdata", "user", "event", "MALWARE_SIGNATURE_MATCH", "users",
                #"amount of malware per user detected", "logdata")

    #check walters events
    #scatterplot(connection, "logdata", "event", "user", "walter", "events",
                #"walters events", "logdata")
    #barchart(connection, "logdata", "event", "user", "walter", "events",
                #"walters events", "logdata")

    #scatterplotMedTendensLinje(connection, "logdata", "user", "level","ALERT")
    #piechartspecefic(connection, "logdata", "event", "walters events", "src_ip", "198.51.100.23")
    #timestamper(connection)
    #scatterplotTime(connection, "titel", "xlabel", "ylabel")

