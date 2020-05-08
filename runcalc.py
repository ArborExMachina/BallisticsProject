from sys import argv
from configparser import ConfigParser
from subprocess import Popen, PIPE
from pathlib import Path

from CalcResult import ResultTable
from parse import Parser
from goodzero import good_zero

path = Path("a.out").resolve()

# TODO: find min/max range & resolution in input
#fields = ["BC", "V", "SH", "ANGLE", "ZERO", "WINDSPEED", "WINDANGLE"]
fields = ["sight_height", "shooting_angle", "wind_speed", "wind_angle"]


input_file_name = argv[1]
output_file_name = "output.csv"

# get configs
config = ConfigParser()
config.read(argv[2])

fixed_params = [config['params'][p] for p in fields]

rangeStart = config['yardage_range']['start']
rangeEnd = config['yardage_range']['end']
resolution = config['yardage_range']['res']

zero_start = int(config['zero_range']['start'])
zero_end = int(config['zero_range']['end'])
zero_res = int(config['zero_range']['res'])

ideal_min = float(config['ideal']['min'])
ideal_max = float(config['ideal']['max'])

yardage_range = [rangeStart, rangeEnd, resolution]
zero_range = [zero_start, zero_end, zero_res]

outputs = []

table = Parser(input_file_name, 'Abbreviated')
next(table) # skip the header

filter_func = good_zero(ideal_min, ideal_max)

count = 0
for row in table:
    bc = row[0]
    range_args = list(map(int, row[1:]))
    range_args[1] += range_args[2]

    for vi in range(*range_args):
        calc_group = []
        for zero in range(zero_start, zero_end+zero_res, zero_res):
            count += 1
            print(count)
            args = [path, bc, str(vi), *fixed_params, str(zero), *yardage_range]
            x = Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
            output, error = x.communicate()
            ret_val = x.wait()
            rows = [tuple(float(v) for v in line.split(',')) for line in output.decode("utf-8").split("\n")[1:] ]

            result = ResultTable([bc, vi, zero, argv[2]], rows)
            calc_group.append(result)
        
        maximal = max([ (table.params, table.find_maximal_peak(ideal_max)) for table in calc_group],
                key=lambda row: row[1].range if row[1] != None else -99999999999999
            )
        outputs.append(maximal)


print("Calculations done")
# for num,table in enumerate(outputs):
#     print(num + 1, table.params, "\n" + "-" * 20)
#     for row in table.rows:
#         print(row.tuple())
#     print("Max:", table.find_maximal_peak().tuple())
#     print("\n")


for result in outputs:
    print(result[0], result[1].tuple() if result[1] != None else "\b, no results")
