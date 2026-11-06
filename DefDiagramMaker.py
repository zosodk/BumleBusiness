from defDbHandler import connect_to_db
import numpy as np
import sqlite3
from sqlite3 import Error
import matplotlib.pyplot as plt
def scatterplot(conn,tabelname, xdata, ydata, xlabel, ylabel, titel):
    xliste = []
    yliste = []
    cursor = conn.cursor()

    cursor.execute(f"""SELECT {xdata} FROM {tabelname}""")
    xakse = cursor.fetchall()

    cursor.execute(f"""SELECT {ydata} FROM {tabelname}""")
    yakse = cursor.fetchall()
    for x,y in zip(xakse, yakse):
        xliste.append(x)
        yliste.append(y)
    print(xliste)
    print(yliste)

    #plt.rcParams["figure.figsize"] = [20, 5]
    #plt.scatter(xakse, yakse)
    #plt.title(titel)
    #plt.xlabel(xlabel)
    #plt.ylabel(ylabel)

    plt.show()
if __name__ == "__main__":
    connection = connect_to_db()
    scatterplot(connection, "logdata", "user","level", "user", "Level", "what user has most warnings")