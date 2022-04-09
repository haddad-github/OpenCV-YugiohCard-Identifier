import time
import cv2 as cv
from concurrent.futures import ThreadPoolExecutor, as_completed
import createPickles

start_time = time.time()
########################

#Card directory
cards_folder = 'downloaded_cards'

#Load the card ID list and the database (format: {'id': ('name', 'type', 'image link')})
all_cards_ID = createPickles.loadPickle('pickle_files/allCardsIDPickled.pickle')
database = createPickles.loadPickle('pickle_files/databaseDictionary.pickle')

#Read deck image
def read_deck(deck_img):
    deck_read = cv.imread(deck_img, cv.IMREAD_UNCHANGED)
    return deck_read

#Read a card and resize it
def read_card(img, width, height):
    read_card = cv.imread(f"{cards_folder}/{img}.jpg", cv.IMREAD_UNCHANGED)
    if read_card is None:
        pass
    else:
        read_card = cv.resize(read_card, (width, height))
    return read_card

#Template matching
def match(deck_img, card_img):
    return cv.minMaxLoc(cv.matchTemplate(deck_img, card_img, cv.TM_CCOEFF_NORMED))[1]

#Create a tuple of the (id, templateMatching)
def match_and_id(id, deck_img, card_img):
    return (id, match(deck_img,card_img))

#Extracting the card ID's that match above a certain threshold (ex: 0.9)
def get_matched_ids(id_and_score, coeff_threshold):
    matched_ids = []

    for tup in id_and_score:
        if tup[1] > coeff_threshold:
            matched_ids.append(tup[0])

    return matched_ids

#Threaded execution (cuts time by 75%)
def threadedMatch():

    values_for_each_image = []

    with ThreadPoolExecutor(20) as executor:

        results = {executor.submit(match_and_id, one_card, deck_img, read_card(one_card, 81, 119)) for one_card in all_cards_ID}

        for result in as_completed(results):
            values_for_each_image.append(result.result())

    return values_for_each_image

#Main function
def execute(threshold):
    id_and_score = threadedMatch()
    matched_ids = get_matched_ids(id_and_score, threshold)

    card_names = []
    for id in matched_ids:
        card_names.append(database[id][0])

    print(card_names)

#Load the deck image (reference image)
deck_img = read_deck('deck.jpg')
execute(threshold=0.9)
print("--- %s seconds ---" % (time.time() - start_time))