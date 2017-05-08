import xlrd
import codecs

# robi plik .tsv z wejściowego .xls (testowo .xls, bo taki plik moglam stworzyć w TestCorpusParser, potem moze być .xlsx)


def make(path):
    current_row = 0
    current_col = 0

    # path to the file you want to extract data from
    out_path = path+'outcsv/'

    src = 'citations.xls'

    book = xlrd.open_workbook(src)

    # select the sheet that the data resides in
    work_sheet = book.sheet_by_index(0)

    # get the total number of rows
    num_rows = work_sheet.nrows
    num_cols = work_sheet.ncols

    f = codecs.open(out_path + "citations.tsv", 'w', "utf-8")

    row = ""

    while current_row < num_rows:
        while current_col < num_cols:
            row_header = work_sheet.cell_value(current_row, current_col)
            if type(row_header) is float:
                row_header = repr(row_header).split(".")[0]
            row += str(row_header)
            row += "\t"
            if current_row == 0 and current_col == num_cols - 1:
                row = row[:-1]
            current_col += 1

        row += "\n"
        f.write(row)
        row = ""
        current_row += 1
        current_col = 0

    f.close()
