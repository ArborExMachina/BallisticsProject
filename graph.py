import sqlite3

from matplotlib import pyplot as plt
from sys import argv

# Usage:
#                   [name of database]    [bc] [mv] [z] [me]
# python graph.py "Sample BC + Velocity" 0.212 1700 101 1.5
db_name = argv[1] # name of the data base
bc = argv[2] 
mv = argv[3] # muzzle velocity
zero = argv[4]
max_elev = argv[5]

db = sqlite3.connect(db_name)
c = db.cursor()

c.execute(f"SELECT range, elevation FROM Dump WHERE bc = {bc} AND muzzle_velocity = {mv} AND zero = {zero} AND elevation <= {max_elev}")

data = c.fetchall()
data.sort(key=lambda x: x[0])
x_axis = [pair[0] for pair in data]
y_axis = [pair[1] for pair in data]

plt.plot(x_axis, y_axis)
plt.show()
