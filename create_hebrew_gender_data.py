from copy import copy

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
import pandas as pd
from tqdm import tqdm
import json
import random


def create_hebrew_gender_csv():
    words = [
        "יד",
        "רגל",
        "בקבוק",
        "מעטפה",
        "ראש",
        "טלוויזיה",
        "מקרר",
        "מזגן",
        "מכונת כביסה",
        "מאוורר",
        "מחשב",
        "מטבע",
        "דרך",
        "גרב",
        "סכין",
        "בוהן",
        "אף",
        "חולצה",
        "שטיח",
        "כובע",
        "כף",
        "כפפה",
        "מטען",
        "מכשיר",
        "שולחן",
        "כיסא",
        "כרית",
        "וילון",
        "שמיכה",
        "תיק",
        "הר",
        "כפר",
        "פח",
        "נר",
        "כורסה",
        "פקק",
        "נייר",
        "ארנק",
        "חלון",
        "רכבת",
        "מכונית",
        "שקית",
        "אבן",
        "קנקן",
        "כפתור",
        "דף",
        "מראה",
        "פעמון",
        "סוכרייה",
        "טבעת",
        "מזוודה",
        "שרשרת",
        "עגיל",
        "קיר",
        "תקרה",
        "חדר",
        "מטוס",
        "מנעול",
        "מפתח",
        "טלפון",
        "כפית",
        "צלחת",
        "קערה",
        "דשא",
        "ים",
        "נהר",
        "נחל",
        "כביש",
        "פרה",
        "כלב",
        "חתול",
        "דביבון",
        "ציפורן",
        "עניבה",
        "שיער",
        "פצע",
        "צוואר",
        "כתף",
        "קומקום",
        "רחוב",
        "מקלדת",
        "מעקה",
        "וידאו",
        "מסך",
        "משאבה",
        "צעצוע",
        "קלף",
        "תיאטרון",
        "בית ספר",
        "נענע",
        "קופסה",
        "לשון",
        "מטריה",
        "שלולית",
        "כלי נגינה",
        "קייטנה",
        "שן",
        "עור",
        "סדין",
        "מנורה"
    ]
    word_gender_dict = dict.fromkeys(words)

    for word in tqdm(words):
        grammatical_gender = selenium_get_gender_mapping(word)
        word_gender_dict[word] = grammatical_gender

    print("Finish!")
    return word_gender_dict


def selenium_get_gender_mapping(word):
    gender_mapping = {
        "זכר": "Masculine",
        "נקבה": "Feminine",
        "זכר ונקבה": "Both",
        "UNKNOWN": "UNKNOWN",
    }
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=options)
    driver.get(f"https://he.wiktionary.org/wiki/{word}")

    # Try with two selectors. If none of them works, assign as "UNKNOWN" (to be fixed manually)
    css_selector1 = "#mw-content-text > div.mw-parser-output > table:nth-child(3) > tbody > tr:nth-child(5) > td:nth-child(2)"
    css_selector2 = "#mw-content-text > div.mw-parser-output > table:nth-child(4) > tbody > tr:nth-child(5) > td:nth-child(2)"

    try:
        hebrew_gender = driver.find_element(By.CSS_SELECTOR, css_selector1).accessible_name
    except NoSuchElementException:
        try:
            hebrew_gender = driver.find_element(By.CSS_SELECTOR, css_selector2).accessible_name
        except NoSuchElementException:
            hebrew_gender = "UNKNOWN"

    driver.close()
    return gender_mapping[hebrew_gender]


def print_data_as_samples_jsonl(word_gender_csv: pd.DataFrame):
    prompt = "You will be given a noun in Hebrew. Your role is to classify the word's grammatical gender to " \
             "\"Feminine\" or \"Masculine\". In case the word carry both genders, output \"Both\". Output \
             only \"Feminine\", \"Masculine\" or \"Both\", nothing else."

    for row in word_gender_csv.iterrows():
        # row[0] is the index, row[1] is the word_gender_csv
        noun = row[1][0]
        gender = row[1][1]
        json_line = {
            "input": [
                {
                    "role": "system",
                    "content": prompt
                },
                {
                    "role": "user",
                    "content": noun
                }
            ],
            "ideal": [
                gender
            ]
        }
        # ensure_ascii=False to print hebrew.
        # source: https://stackoverflow.com/questions/18337407/saving-utf-8-texts-with-json-dumps-as-utf-8-not-as-a-u-escape-sequence
        print(json.dumps(json_line, ensure_ascii=False))


def create_random_pairs():
    numbers = list(range(100))  # Generate list of numbers from 0 to 99
    pairs = []

    while len(pairs) < 100:
        # Select two random numbers from the list
        pair = tuple(random.sample(numbers, 2))
        # Add the pair to the list of pairs
        if pair not in pairs:
            pairs.append(pair)

    return pairs


def print_words_pairs_as_samples_jsonl(word_gender_csv: pd.DataFrame):
    prompt = "You will be prompted with two Hebrew nouns. Do these nouns have the same grammatical gender? " \
             "Answer Y or N, nothing else."

    word_gender_dict = word_gender_csv.to_dict()
    words_dict = word_gender_dict["noun"]
    gender_dict = word_gender_dict["gender"]

    random_pairs_100 = create_random_pairs()

    for pair in random_pairs_100:
        words = [words_dict[pair[0]], words_dict[pair[1]]]
        genders = [gender_dict[pair[0]], gender_dict[pair[1]]]

        concat_nouns = ", ".join(words)
        Y_or_N = 'Y' if genders[0] == genders[1] else 'N'

        json_line = {
            "input": [
                {
                    "role": "system",
                    "content": prompt
                },
                {
                    "role": "user",
                    "content": concat_nouns
                }
            ],
            "ideal": [
                Y_or_N
            ]
        }

        print(json.dumps(json_line, ensure_ascii=False))


if __name__ == "__main__":
    # >>> step 1: create csv word_gender_csv of hebrew noun, and it's grammatical_gender
    # word_gender_dict = create_hebrew_gender_csv()
    # pd.DataFrame.from_dict(word_gender_dict, orient="index").to_csv("word_gender_data.csv")

    # >>> step 2: convert word_gender_csv to samples.jsonl. Make sure word_gender_data not contains UNKNOWN values
    # word_gender_csv = pd.read_csv("word_gender_data.csv")
    # print_data_as_samples_jsonl(word_gender_csv)

    # >>> step 3: convert word_gender_csv to noun pairs with labels Y and N for same/not same gender
    data = pd.read_csv("word_gender_data.csv")
    print_words_pairs_as_samples_jsonl(data)

