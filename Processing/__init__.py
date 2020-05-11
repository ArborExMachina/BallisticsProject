import sqlite3
import os

from configparser import ConfigParser
from subprocess import Popen, PIPE
from pathlib import Path
from matplotlib import pyplot

from CalcResult import ResultTable
from parse import Parser
from analyze import good_zero, maximal

def do_all(input_file_name, sheet_name, config_path):
    path = Path("a.out").resolve()

    # TODO: find min/max range & resolution in input
    #fields = ["BC", "V", "SH", "ANGLE", "ZERO", "WINDSPEED", "WINDANGLE"]
    fields = ["sight_height", "shooting_angle", "wind_speed", "wind_angle"]

    output_file_name = ".".join(input_file_name.split('.')[:-1]) + ".db"

    if os.path.exists(output_file_name):
        os.remove(output_file_name)
    db = sqlite3.connect(output_file_name)
    c = db.cursor()

    # setup table
    c.execute('''CREATE TABLE "Dump" (
        "id"    INTEGER PRIMARY KEY,
        "bc"	REAL,
        "muzzle_velocity"	REAL,
        "zero"	INTEGER,
        "range"	REAL,
        "elevation"	REAL
    )''')

    # get configs
    config = ConfigParser()
    config.read(config_path)

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

    outputs = {}

    table = Parser(input_file_name, sheet_name)
    next(table) # skip the header

    count = 0
    for row in table:
        print(row)
        bc = row[0]
        range_args = list(map(int, row[1:]))
        range_args[1] += range_args[2]

        for vi in range(*range_args):
            calc_group = {}
            for zero in range(zero_start, zero_end+zero_res, zero_res):
                count += 1
                # print(count)
                args = [path, bc, str(vi), *fixed_params, str(zero), *yardage_range]
                x = Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
                output, error = x.communicate()
                ret_val = x.wait()
                # rows = [tuple(float(v) for v in line.split(',')) for line in output.decode("utf-8").split("\n")[1:] ]
                rows = []
                id = 0
                for line in output.decode("utf-8").split("\n")[1:]:
                    vals = [float(v) for v in line.split(',')]
                    id += 1
                    rows.append(f"({bc},{vi},{zero},{vals[0]},{vals[1]})")
                # TEMP
                # strrow = [f"({bc},{vi},{zero},{x[0]},{x[1]})" for x in rows]
                q = "INSERT INTO Dump(bc, muzzle_velocity, zero, range, elevation) VALUES " + ", ".join(rows) + ";"
                c.execute(q)
                ##

                # result = ResultTable([bc, vi, zero, argv[2]], rows)
                # calc_group[zero] = result
            
            
            # outputs[(bc, vi)] = calc_group


    print("Calculations done")

    db.commit()
    c.close()
    db.close()
