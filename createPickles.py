import os
import pickle

#Read card filenames (which happen to also be their ID)
cards_directory = 'downloaded_cards'

def all_cards_id_list():
    directory = os.listdir(cards_directory)
    return [x.split('.')[0] for x in directory]

#all_cards_id = all_cards_id_list()

#Read and create a dictionary for the database
def read_database(database):
    db = []

    with open(database) as f:
        for line in f.readlines():
            db.append(line.rstrip().split(','))

    dataDict = {}
    for line in db:
        key = line[0]
        tuple = (line[1], line[2], line[3])
        dataDict[key] = tuple

    return dataDict

#databaseDictionary = read_database('yugioh_databaseV8_24thMarch2022.csv')

#Create pickle files
def createPickle(output_name, variable):
    with open(f'{output_name}.pickle', 'wb') as handle:
        pickle.dump(variable, handle, protocol=pickle.HIGHEST_PROTOCOL)

#createPickle('allCardsIDPickled', all_cards_id)
#createPickle('databaseDictionary', databaseDictionary)

# #Testing purposes
def loadPickle(filename):
    with open(f'{filename}', 'rb') as handle:
        loaded_pickle = pickle.load(handle)
    return loaded_pickle

#print(loadPickle('allCardsIDPickled.pickle'))
#print(loadPickle('databaseDictionary.pickle'))