
import os


stopwords = []
symbols = "!$%&'*+;<=>?@^`~"

BASE_PATH = "D://IT//PyCharm//rasa-my-first-model"
INPUT_PATH = os.path.join(BASE_PATH, 'data')
OUTPUT_PATH = os.path.join(BASE_PATH, 'data_preprocessed')

def replace_stop_word(text: str) -> str:
  text = text.lower()
  for i in stopwords:
    text = text.replace(' ' + i + ' '," ")
    text = text.replace(' ' + i + '\n',"\n")
  
  for i in symbols:
    text = text.replace(i, " ")
  return text

def process_file(file_path) -> str:
  print(f"Processing file: {file_path}")
  with open(file_path, 'r', encoding='utf-8') as file:
    data = file.read()
    data = replace_stop_word(data)
    return data

def process_directory(directory):
  for root, _, files in os.walk(directory):
    for file in files:
      if file.endswith(".yml") or file.endswith(".yaml"):
        data = process_file(os.path.join(root, file))
        with open(os.path.join(OUTPUT_PATH, file), 'w', encoding='utf-8') as file:
          file.write(data)

if __name__ == "__main__":
  if not os.path.exists(OUTPUT_PATH):
    os.makedirs(OUTPUT_PATH)
  
  with open(os.path.join(BASE_PATH, 'pipelines/vietnamese-stopwords.txt'), 'r', encoding='utf-8') as f:
    stopwords = f.read().splitlines()

  process_directory(INPUT_PATH)
