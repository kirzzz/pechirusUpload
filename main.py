import json
import requests
from yandex_market_language import parse, convert, models
import time

def parseYML(xmlFile,filename):
    xml = requests.get(xmlFile)
    file = open('xml/'+str(filename)+'.xml', 'w')  # создаем файл для записи результатов
    file.write(xml.text)  # записываем результат
    file.close()  # закрываем файл

    feed = parse('xml/'+str(filename)+'.xml')

    print(type(feed.to_dict()))
    # with open("output/"+str(filename)+'_'+str(time.time())+'.json', 'w', encoding='utf-8') as f:
    #     json.dump(feed.to_dict(), f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    parseYML("https://lit-kom.ru/yml_get/5", "litkom")
