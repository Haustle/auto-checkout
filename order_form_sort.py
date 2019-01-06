import xlrd


def getOrders(file_location):
    workbook = xlrd.open_workbook(file_location)
    sheet = workbook.sheet_by_index(0)
    rows = sheet.nrows
    cols = sheet.ncols
    mega_list = []
    for x in range(rows):
        if x == 0: continue
        coppin = []
        for y in range(cols):
            coppin.append((str(sheet.cell_value(x,y))).encode("utf-8"))
        mega_list.append(coppin)
    if len(mega_list) > 0:
        return mega_list
    return None
