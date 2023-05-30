# Hebrew Word Gender Data - OpenAI Evals
This repository was used to create data of hebrew noun and grammatical gender for OpenAI Evals. Pull Request here:
https://github.com/openai/evals/pull/634

The csv data is in `word_gender_data.csv`. I used selenium to scrape the data from [wiktionary in Hebrew](https://he.wiktionary.org/wiki/%D7%95%D7%99%D7%A7%D7%99%D7%9E%D7%99%D7%9C%D7%95%D7%9F:%D7%A2%D7%9E%D7%95%D7%93_%D7%A8%D7%90%D7%A9%D7%99)

## How to run
Run the file `create_hebrew_gender_data.py`. It has three steps:

```python
  # >>> step 1: create csv `word_gender_csv` of hebrew noun, and it's grammatical_gender
  word_gender_dict = create_hebrew_gender_dict()
  # save as csv with noun/gender cols
  df = pd.DataFrame.from_dict(word_gender_dict, orient="index", columns=["gender"])
  df["word"] = df.index
  df.to_csv("word_gender_data.csv", index=False)

  # Check the data manually and fix the UNKNOWN values

  # >>> step 2: convert word_gender_csv to samples.jsonl. Make sure word_gender_data not contains UNKNOWN values
  word_gender_csv = pd.read_csv("word_gender_data.csv")
  print_word_gender_as_samples_jsonl(word_gender_csv)

  # >>> step 3: convert word_gender_csv to noun pairs with labels Y and N for same/not same gender
  data = pd.read_csv("word_gender_data.csv")
  print_words_pairs_as_samples_jsonl(data)
```

