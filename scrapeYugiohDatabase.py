import requests
import json
import csv
import urllib.request

#Write Yugioh database as a CSV: [card id], [card name], [card type], [image url]
def createDatabase():
    #Parse the JSON
    url = 'https://db.ygoprodeck.com/api/v8/cardinfo.php'
    response = requests.post(url)
    data = json.loads(response.text)

    data = data['data']

    #Write in the format card_id, card_name, card_tpe, card_image_url
    with open('yugioh_databaseV8_24thMarch2022.csv', 'w', encoding='utf-8', newline='') as file:
        write = csv.writer(file)

        for card in range(len(data)):
            the_id = data[card]['id']
            name = data[card]['name'].replace(',', '')
            the_type = data[card]['type']
            image_url = data[card]['card_images'][0]['image_url']
            write.writerow([the_id, name, the_type, image_url])

#createDatabase()

#Download all images directly from the image url stored in the database previously
def downloadCardImages():
    db_list = []
    with open('yugioh_databaseV8_24thMarch2022.csv', 'r') as file:
            for line in file.readlines():
                db_list.append(line.rstrip().split(',')) # using rstrip to remove the \n

    for line in db_list:
        the_id = line[0]
        img_link = line[3]
        urllib.request.urlretrieve(img_link, f"downloaded_cards/{the_id}.jpg") #create a downloaded_cards folder first

#downloadCardImages()
