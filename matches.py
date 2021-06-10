import json
import time
from fuzzywuzzy import fuzz
import re
import pandas as pd
from fuzzywuzzy import process

with open('products/products_1623209381.2105181.json', encoding='utf-8') as json_file:
    pechirus = json.load(json_file)
with open('output/litkom1623207802.678594.json', encoding='utf-8') as json_file:
    vezuvii = json.load(json_file)
    categories = vezuvii['shop']['categories']
    vezuvii = vezuvii['shop']['offers']

output = []
index = 0
len_obj = (len(pechirus)*len(vezuvii))
for pech_i in pechirus:
    for vez_i in vezuvii:
        index += 1
        k = fuzz.token_sort_ratio(pech_i['name'], vez_i['name'])
        if k > 80:  # and (len(output) == 0 or pech_i['id'] not in [out.get('id_1') for out in output])
            num_1 = ''.join(re.findall(r'\d+', pech_i['name']))
            num_2 = ''.join(re.findall(r'\d+', vez_i['name']))

            desc_1 = re.sub('<[^>]*>|&nbsp;', '', pech_i['description'])
            desc_2 = re.sub('<[^>]*>|&nbsp;', '', str(vez_i['description']))
            k_desc = fuzz.token_sort_ratio(desc_1, desc_2)

            price_series = pd.Series([pech_i['price'], int(vez_i['price']['value'])])
            k_price = price_series.pct_change()

            try:
                properties_1 = ';\n'.join([(i['name'] + ': ' + i['value']) for i in json.loads(pech_i['property'])['myrows']]) if pech_i['property'] is not None else ''
            except:
                properties_1 = ''
            properties_2 = ';\n'.join([(i['name'] + ': ' + i['value']) for i in vez_i['parameters']])
            k_property = fuzz.token_sort_ratio(properties_1, properties_2)

            output.append({
                'koef': (k*50 + k_desc*25 + k_property*25)/300,
                'id_1': pech_i['id'],
                'id_2': vez_i['offer_id'],
                'name': {
                    'koef': k,
                    'numbers': num_1 == num_2,
                    'shop_1': {
                        'data': pech_i['name'],
                        'num': num_1,
                    },
                    'shop_2': {
                        'data': vez_i['name'],
                        'num': num_2,
                    }
                },
                'desc': {
                    'koef': k_desc,
                    'shop_1': {
                        'data': desc_1,
                    },
                    'shop_2': {
                        'data': desc_2,
                    }
                },
                'price': {
                    'koef': k_price[1],
                    'shop_1': {
                        'data': pech_i['price'],
                    },
                    'shop_2': {
                        'data': int(vez_i['price']['value']),
                    }
                },
                'property': {
                    'koef': k_property,
                    'shop_1': {
                        'data': properties_1,
                    },
                    'shop_2': {
                        'data': properties_2,
                    }
                }
            })
            print(str((index/len_obj)*100) + '_' + str(pech_i['id']) + '_' + vez_i['offer_id'])


with open("matches/pechirus_vezuvii"+'_'+str(time.time())+'.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=4)






