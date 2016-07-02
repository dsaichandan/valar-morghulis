import urllib
import data_cleaner as dc
import pandas as pd
import time


class ImageRetriever(object):
    def __init__(self):
        pass

    @staticmethod
    def load_images_from_api():
        start = time.time()
        print("Loading from JSON...")
        data_cleaner = dc.DataCleaner()
        data_cleaner.load_data()
        print("Loading finished.")
        end = time.time()
        total = end - start
        print("Loading time: " + str(total))

        start = time.time()
        print("Retrieving images [characters] from API...")
        retrieved = 0
        not_retrieved = 0
        for index, row in data_cleaner.characters_json.iterrows():
            if pd.notnull(row['imageLink']):
                link = str(row['imageLink'])
                url = 'https://api.got.show' + link
                filename = link.split('/')[4]
                urllib.urlretrieve(url, "view/images/characters/" + filename)
                retrieved += 1
            else:
                not_retrieved += 1
        print("Retrieving images from API finished.")
        print("Total images retrieved: " + str(retrieved))
        print("Characters without image: " + str(not_retrieved))
        end = time.time()
        total = end - start
        print("Retrieving time: " + str(total))

        start = time.time()
        print("Retrieving images [houses] from API...")
        retrieved = 0
        not_retrieved = 0
        for index, row in data_cleaner.houses_json.iterrows():
            if pd.notnull(row['imageLink']):
                link = str(row['imageLink'])
                url = 'https://api.got.show' + link
                filename = link.split('/')[4]
                urllib.urlretrieve(url, "view/images/houses/" + filename)
                retrieved += 1
            else:
                not_retrieved += 1
        print("Retrieving images from API finished.")
        print("Total images retrieved: " + str(retrieved))
        print("Characters without image: " + str(not_retrieved))
        end = time.time()
        total = end - start
        print("Retrieving time: " + str(total))


if __name__ == '__main__':
    ImageRetriever.load_images_from_api()
