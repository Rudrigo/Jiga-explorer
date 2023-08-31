import json
from os.path import isfile

class JsonFiles():
    def __init__(self, parent=None):
        print("Function json")

    def consultJson(self, file, key):
        if isfile(file):
            with open(file, "r+", encoding="utf-8") as dados:
                result = json.load(dados)
                try:
                    value = result[key]
                    return value
                except:
                    return False
        else:
            return False

    def creatUpdateJson(self, file, key, value):
        if not isfile(file):
           with open(file, "w", encoding="utf-8") as dados:
                result = {key: value}
                json.dump(result, dados, ensure_ascii=False, indent=4, separators=(',', ':'), sort_keys=False)
        else:
            with open(file, "r+", encoding="utf-8") as dados:
                try:
                    result = json.load(dados)
                    result[key] = value
                    dados.seek(0)
                    json.dump(result, dados, ensure_ascii=False, indent=4, separators=(',', ':'), sort_keys=False)
                    #json.dump(result, dados, ensure_ascii=False, sort_keys=False, indent=4, separators=(',', ':'))
                    dados.truncate()
                except:
                    result = {key: value}
                    json.dump(result, dados, ensure_ascii=False, indent=4, separators=(',', ':'), sort_keys=False)


#if __name__ == '__main__':
    #jfiles = JsonFiles()
    #consulta MAC no json, retorna serie
    #print(jfiles.creatUpdateJson('registro.json', '11:11:2d:8f:dc:fd', 100006 ))

    #try:
        #verify = jfiles.consultJson('registro.json',"08:b6:1f:89:60:b0")
    #except:
        #verify = False

    #print(str(verify))

    #if not verify:
        #print(verify)
        #jfiles.creatUpdateJson('registro.json', '77:11:2d:8f:dc:fd', 100005)