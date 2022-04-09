import time
import cv2 as cv
from concurrent.futures import ThreadPoolExecutor, as_completed
import createPickles
import PySimpleGUI as sg
from PIL import Image, ImageTk
import io
import os

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

#Threaded execution (cuts time by up to 75%)
def threadedMatch():

    values_for_each_image = []

    with ThreadPoolExecutor(20) as executor:

        results = {executor.submit(match_and_id, one_card, deck_img, read_card(one_card, user_width, user_height)) for one_card in all_cards_ID}

        for result in as_completed(results):
            values_for_each_image.append(result.result())

    return values_for_each_image

#Card ID's become the card name
def translate_id_to_names(list_of_ids):
    card_names = []
    for id in list_of_ids:
        card_names.append((id, database[id][0]))

    return card_names

#Main function
def execute(threshold):
    id_and_score = threadedMatch()
    matched_ids = get_matched_ids(id_and_score, threshold)
    card_names = translate_id_to_names(matched_ids)
    return card_names

##GUI##

sg.theme('DarkGrey6')

#Left column, where all the input will be
left_column =[

    [sg.Text("Deck image"), sg.Input(size=(25, 1), key="path"), sg.FileBrowse(key="chosen_deck_img"),
     sg.Button("Load deck")],
    [sg.Image(key="deck_img")],

    [sg.Text("Card dimensions on the image (width x height) [if default, put 0 in both]")], [sg.Input(key="width", size=(10,10))],
    [sg.Input(key="height", size=(10,10))],
    [sg.Button("Confirm dimensions")],

    [sg.Text("Accuracy coefficient (between 0 and 1) [recommended: 0.60 to 0.90]")], [sg.Input(key="coeff", size=(10,10))],
    [sg.Button("Confirm coeff")],
    [sg.Button("Identify cards")],
    [sg.Output(key="deck_list")],

]

#Right column of the GUI, where the card viewer will be
right_column =[
    [sg.Combo([''], key='dropdown', size=(30,0)), sg.Button("Show card")],

    [sg.Image(key="card_img")]
]

#Main layout (merges left and right column)
layout = [
    [sg.Column(left_column, vertical_alignment='top'), sg.VSeparator(), sg.Column(right_column, vertical_alignment='top')],
]

window = sg.Window("Card identifier", layout)

while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break

    #Load the deck and show a preview of the deck chosen in a 300x300 format
    if event == "Load deck":
        filename = values["path"]
        if os.path.exists(filename):
            image = Image.open(values["path"])
            image.thumbnail((300, 300))
            bio = io.BytesIO()
            image.save(bio, format="PNG")
            window["deck_img"].update(data=bio.getvalue())
            deck_img = read_deck(filename)

    #Default values = Master Duel format for a 1920x1080 picture
    if event == "Confirm dimensions":
        if int(values['width']) == 0 or int(values['height']) == 0:
            user_width = 64
            user_height = 94
            print(f"Dimensions confirmed: {user_width} x {user_height}")

        else:
            user_width = int(values['width'])
            user_height = int(values['height'])
            print(f"Dimensions confirmed: {user_width} x {user_height}")

    #Coefficient of accuracy for the image recognition
    if event == "Confirm coeff":
        user_coeff = float(values['coeff'])
        print(f"Coefficient confirmed: {user_coeff}")

    #Activates the algorithm
    if event == "Identify cards":
        print("Please wait, this may take a few minutes...")

        all_cards = all_cards_ID
        db = database

        cards_names = execute(threshold=user_coeff)

        window['dropdown'].update(values=[card[1] for card in cards_names])

        print(f"Execution time: {time.time() - start_time} seconds")

    #Select a card from a dropdown and show the card in full size
    if event == "Show card":
        chosen_card_name = values['dropdown']
        dict_cards= {w:n for n, w in cards_names}
        card_id = dict_cards[chosen_card_name]
        card_img = Image.open(f"./downloaded_cards/{card_id}.jpg")
        window["card_img"].update(data=ImageTk.PhotoImage(card_img))
