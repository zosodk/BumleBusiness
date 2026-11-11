import matplotlib.pyplot as plt
import pandas as pd
import sqlite3
conn = sqlite3.connect('bumlebusiness.db')


query = "SELECT * FROM logdata WHERE src_ip = '198.51.100.23'"
df = pd.read_sql(query, conn)

# Luk forbindelsen
conn.close()

# Tjek om der er data
if df.empty:
  print('Ingen data fundet for denne IP-adresse.')
else:
  # Konverter tidskolonnen til datetime-objekter
  #
  df['timestamp'] = pd.to_datetime(df['timestamp'])

  # Opsætning af Scatter Plot
  plt.figure(figsize=(12, 6))

  # Plot tidspunkt (X-akse) mod f.eks. statuskode (Y-akse)
  # Erstat 'status_code' med den kolonne derskal analyseres på Y-aksen
  plt.scatter(
      df['timestamp'],
      df['event'],
      alpha=0.7,
      edgecolors='k',
      s=50,
      color='royalblue',
  )

  plt.title(
      'Aktivitet for IP: 198.51.100.23 (Udtrukket fra database)', fontsize=14
  )
  plt.xlabel('Tidspunkt', fontsize=12)
  plt.ylabel('HTTP Statuskode / Værdi', fontsize=12)

  # Gør datoerne på X-aksen læsevenlige
  plt.gcf().autofmt_xdate()

  plt.grid(True, linestyle='--', alpha=0.5)
  plt.tight_layout()

  # Vis plottet
  plt.show()