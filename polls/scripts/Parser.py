import os
import csv
from collections import OrderedDict
from xml.dom.minidom import parse
import xml.dom.minidom
import codecs

# klasa parsująca dane z pliku .ccl który ma strukturę xmla i zawiera leksemy oraz informacje o nich (jaka część mowy, itp)


def parser(path):

    in_path = path+"out/"
    out_path = path+'outcsv/'

    for file in os.listdir(in_path + "."):
        dict = {}
        chunksCounter = 0
        print(file)
        print("Start Parsing...")
        fileName = os.path.splitext(file)[0]

        with codecs.open(in_path + file, "r", "utf-8") as my_file:
            doc = my_file.read()

        doc = doc.encode('utf-8')
        # Open XML document using minidom parser
        DOMTree = xml.dom.minidom.parseString(doc)
        chunkList = DOMTree.documentElement
        print("String parsed")
        # Get all the chunks in the collection
        chunks = chunkList.getElementsByTagName("chunk")
        print("got chunks")
        # Print detail of each chunk.
        for chunk in chunks:
            toks = chunk.getElementsByTagName("tok")
            chunksCounter += 1
            if chunksCounter >= 1000:
                chunksCounter = 0
                print("1000 chunks...")

            for tok in toks:
                lex = tok.getElementsByTagName('lex')[0]
                ctag = lex.getElementsByTagName('ctag')[0]
                tag = ctag.childNodes[0].data
                # ign - nazwa własna? num - liczby
                if tag == 'interp' or tag == 'conj' or tag == 'comp' or tag == 'qub' or 'prep' in tag:
                    continue

                ann = tok.getElementsByTagName("ann")
                # print (ann.length)
                if ann.length != 0:
                    ann = tok.getElementsByTagName("ann")[0]
                    annData = ann.childNodes[0].data
                    if int(annData) != 0:
                        continue

                base = lex.getElementsByTagName('base')[0]
                data = base.childNodes[0].data

                if data in dict:
                    count = dict[data]
                    count += 1
                    dict[data] = count
                else:
                    dict[data] = 1

        dict = OrderedDict(sorted(dict.items(), reverse=True, key=lambda t: t[1]))

        if not os.path.exists(out_path + "wordcounts/"):
            os.makedirs(out_path + "wordcounts/")
        try:
            with open(out_path + "wordcounts/wordcounts_" + fileName + '.csv', 'w', newline='\n', encoding='utf-8') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(["WORDCOUNTS", "WEIGHT"])
                for key, value in dict.items():
                    writer.writerow([key, value])
        except UnicodeEncodeError as e:
            print(str(e))
        #     with open(out_path + "wordcounts\wordcounts_" + fileName + '.csv', 'w', newline="\n", encoding="utf=8") as csv_file:
        #         writer = csv.writer(csv_file)
        #         writer.writerow(["WORDCOUNTS", "WEIGHT"])
        #         for key, value in dict.items():
        #             writer.writerow([key, value])


