import pymysql
import json
import time

con = pymysql.connect(host='5.23.51.236', user='cy55476_pechirus', password='HK6Ck1gh', database='cy55476_pechirus', charset='utf8', cursorclass=pymysql.cursors.DictCursor)

with con:
    cur = con.cursor()
    cur.execute("SELECT * FROM product")

    rows = cur.fetchall()

    with open("products/products"+'_'+str(time.time())+'.json', 'w', encoding='utf-8') as f:
        json.dump(rows, f, ensure_ascii=False, indent=4)
