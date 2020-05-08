from openpyxl import load_workbook

def Parser(spreadsheet,sheet_name):
    wb = load_workbook(filename=spreadsheet)

    sheet = wb[sheet_name]
    for row in sheet:
        yield [str(pair.value) for pair in row]


# x = Parser("Sample BC + Velocity.xlsx", "Abbreviated")

# for row in x:
#     print(row)