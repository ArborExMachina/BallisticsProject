import csv
from sys import argv
from subprocess import Popen, PIPE
from pathlib import Path
from CalcResult import ResultTable

path = Path("a.out").resolve()

# TODO: find min/max range & resolution in input
fields = ["BC", "V", "SH", "ANGLE", "ZERO", "WINDSPEED", "WINDANGLE"]

kw_alias = [
    "Ballistic Coefficient",
    "Initial Velocity",
    "Sight Height",
    "Shooting Angle",
    "Zero Range",
    "Wind Speed",
    "Wind Angle"
]

input_file_name = "02 input.csv"
output_file_name = "output.csv"

rangeStart = 0
rangeEnd = 500
resolution = 1

outputs = []

with open(input_file_name) as inputfile:
    inputs = [line.strip().split(',') for line in inputfile.readlines()]

input_header = inputs[0]

positions = [input_header.index(kw) for kw in kw_alias]

inputs = inputs[1:]

# for loop goes here
args = [inputs[0][x] for x in positions] + [str(rangeStart), str(rangeEnd), str(resolution)]
x = Popen([path, *args], stdin=PIPE, stdout=PIPE, stderr=PIPE)

output, error = x.communicate()

ret_val = x.wait()
rows = [tuple(float(v) for v in line.split(',')) for line in output.decode("utf-8").split("\n")[1:] ]

result = ResultTable(rows)

for row in result.rows:
    print(row.tuple())