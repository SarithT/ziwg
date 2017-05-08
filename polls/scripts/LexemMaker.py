import json
import urllib.request
import urllib.parse
import os
import time
import codecs
from docx import Document


# klasa zajmująca się uploadem plików na serwer a a następnie odpalaniem na nich odpowiedniego narzędzia, aby otrzymać pliki .ccl
url = "http://ws.clarin-pl.eu/nlprest2/base"


def upload(file):

        # jeśli plik jest dokumentem .docx
        if os.path.splitext(file)[1] == ".docx":
            document = Document(file)
            fullText = []
            for para in document.paragraphs:
                fullText.append(para.text)
            doc = str(fullText)
            print(doc)
        else:
            try:
                # spróbuj otworzyć plik z kodowaniem utf-8
                with codecs.open(file, "r", "utf-8") as myfile:
                    doc = myfile.read()
                    print("utf-8")
            except:
                print("not utf-8")
                try:
                    # spróbuj otworzyć plik z kodowaniem ansi
                    with codecs.open(file, "r", "ansi") as myfile:
                        # with open(file, "rb") as myfile:
                        doc = myfile.read()
                        # print(doc)
                        print("ansi")
                except:
                    print("just nope")

        doc = doc.replace(u'xa0', u' ').encode('utf-8')

        header = {'Content-Type': 'binary/octet-stream'}
        req = urllib.request.Request(url+'/upload', doc, header)
        print("Uploading!")
        return urllib.request.urlopen(req).read().decode("utf-8")

def tool(lpmn, user):

        data = {}
        data['lpmn'] = lpmn
        data['user'] = user

        doc = json.dumps(data)
        doc = doc.encode("utf-8")
        header = {'Content-Type': 'application/json'}
        req = urllib.request.Request(url+'/startTask/', doc, header)
        taskid = urllib.request.urlopen(req).read().decode("utf-8")

        print(taskid)

        time.sleep(0.1)
        resp = urllib.request.urlopen(urllib.request.Request(url+'/getStatus/'+taskid))
        data = json.load(resp)

        print(data)

        while data["status"] == "QUEUE" or data["status"] == "PROCESSING":
            time.sleep(0.1)
            resp = urllib.request.urlopen(urllib.request.Request(url+'/getStatus/'+taskid))
            data = json.load(resp)

        if data["status"] == "ERROR":
            print("Error "+data["value"])
            return None
        return data["value"]


def main():

    in_path = "in/"
    out_path = 'out/'
    global_time = time.time()

    for file in os.listdir(in_path + "."):
        print(file)
        fileName = os.path.splitext(file)[0]
        file = in_path + file
        start_time = time.time()
        data = upload(file)

        print("Uploaded to: " + data)
        print("Processing: " + file)

        data = tool('file('+data+')|any2txt|wcrft2|liner2({\"model\":\"names\"})','agrybicka@gmail.com')

        if data is None:
            continue

        print(data)
        data = data[0]["fileID"]
        content = urllib.request.urlopen(urllib.request.Request(url+'/download'+data)).read().decode("utf-8")

        with codecs.open(out_path + fileName + '.ccl', "w", "utf-8") as outfile:
                outfile.write(content)

        print("--- %s seconds ---" % (time.time() - start_time))

    print("GLOBAL %s seconds ---" % (time.time() - global_time))
