import os
from xml.dom.minidom import parse
import xml.dom.minidom
import codecs
from xlutils.copy import copy # http://pypi.python.org/pypi/xlutils
from xlrd import open_workbook # http://pypi.python.org/pypi/xlrd
import datetime

# parser do plików xml, które dostaliśmy z Racjonalisty. Robi z nich pliki txt z tekstem
# i odczytuje dane, zeby stworzyć automatycznie plik citations


def parser(path,excel_name):

    excel_path_empty = path+"citations_empty.xlsx"
    excel_path = path + str(excel_name)
    current_row = 1
    column_id = 0
    column_title = 2
    column_author = 3
    column_journal = 4
    column_date = 7

    in_path = path+"corpus/"
    out_path = path+'in/'

    citations_empty = open_workbook(excel_path_empty)
    wb = copy(citations_empty)  # a writable copy (I can't read values out of this, only write to it)
    citations = wb.get_sheet(0)  # the sheet to write to within the writable copy
    counter = 0;
    for file in os.listdir(in_path + "."):
        fileName = os.path.splitext(file)[0]

        with codecs.open(in_path + file, "r", "utf-8") as my_file:
            doc = my_file.read()

        try:
            # Open XML document using minidom parser
            DOMTree = xml.dom.minidom.parseString(doc)
            chunkList = DOMTree.childNodes
            body = chunkList[0].getElementsByTagName("body")[0]
            metadata = chunkList[0].getElementsByTagName("metadata")[0]
            entries = metadata.getElementsByTagName("entry")
            if body.childNodes.length != 0:
                citations.write(current_row, column_id, fileName)
                citations.write(current_row, column_journal, "Racjonalista")
                for entry in entries:
                    key = entry.getElementsByTagName("key")
                    value = entry.getElementsByTagName("value")
                    if key.length != 0 and value.length != 0:
                        if key[0].childNodes[0].data == "author" and value[0].childNodes.length != 0:
                            citations.write(current_row, column_author, value[0].childNodes[0].data)
                        if key[0].childNodes[0].data == "date" and value[0].childNodes.length != 0:
                            date = value[0].childNodes[0].data
                            if valid_date(date):
                                date_tab = date.split("-");
                                date_new = date_tab[2] + "-" + date_tab[1] + "-" + date_tab[0];
                                citations.write(current_row, column_date, date_new)

                title = chunkList[0].getElementsByTagName("title")[0]
                if title.childNodes.length != 0:
                    citations.write(current_row, column_title, title.childNodes[0].data)

                #data = body.childNodes[0].data

                # odkomentuj poniższe jeśli chcesz STWORZYĆ nowe pliki txt (nie ma potrzeby, bo już są zrobione)

                #if not os.path.exists(out_path):
                #    os.makedirs(out_path)
                #with open(out_path + fileName + '.txt', 'w', newline="\n", encoding="utf-8") as in_file:
                #    in_file.write(data)
                #    in_file.close()
                current_row += 1
                print(counter)
                counter += 1
        except xml.parsers.expat.ExpatError as e:
            s = str(e)
            print(s)
        wb.save(excel_path)


def valid_date(datestring):
    try:
        datetime.datetime.strptime(datestring, '%d-%m-%Y')
        return True
    except ValueError:
        #try:
            #datetime.datetime.strptime(datestring, '%d-%m-%Y')
            #return True
        #except ValueError:
        return False
