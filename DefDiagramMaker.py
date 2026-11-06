from defDbHandler import connect_to_db
import numpy as np
import sqlite3
from sqlite3 import Error
import matplotlib.pyplot as plt
import numpy as np

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

def piechart(conn,tabelname, xdata, ydata, parameter, titel):
    xakse = []
    yakse = []
    cursor = conn.cursor()

    # læser et table og finder hvor mange gange en bestemt ting sker
    cursor.execute(f"""
                SELECT {xdata}, COUNT(*)
                FROM {tabelname}
                WHERE {ydata} = ?
                GROUP BY {xdata}
            """, (parameter,))
    data = cursor.fetchall()
    # print(data)
    for tuple in data:
        xakse.append(tuple[0])
        yakse.append(tuple[1])

    plt.pie(count, labels=labels, autopct='%1.1f%%')
    plt.title("zoo animals")
    plt.show()
if __name__ == "__main__":
    connection = connect_to_db()
    scatterplotMedTendensLinje(connection, "logdata", "user","level", "ALERT", "users", "amount of alerts", "alerts per user")
