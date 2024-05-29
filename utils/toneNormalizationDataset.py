# coding=utf-8
# Copyright (c) 2021 VinAI Research

import os


dict_map = {
  "òa": "oà",
  "Òa": "Oà",
  "ÒA": "OÀ",
  "óa": "oá",
  "Óa": "Oá",
  "ÓA": "OÁ",
  "ỏa": "oả",
  "Ỏa": "Oả",
  "ỎA": "OẢ",
  "õa": "oã",
  "Õa": "Oã",
  "ÕA": "OÃ",
  "ọa": "oạ",
  "Ọa": "Oạ",
  "ỌA": "OẠ",
  "òe": "oè",
  "Òe": "Oè",
  "ÒE": "OÈ",
  "óe": "oé",
  "Óe": "Oé",
  "ÓE": "OÉ",
  "ỏe": "oẻ",
  "Ỏe": "Oẻ",
  "ỎE": "OẺ",
  "õe": "oẽ",
  "Õe": "Oẽ",
  "ÕE": "OẼ",
  "ọe": "oẹ",
  "Ọe": "Oẹ",
  "ỌE": "OẸ",
  "ùy": "uỳ",
  "Ùy": "Uỳ",
  "ÙY": "UỲ",
  "úy": "uý",
  "Úy": "Uý",
  "ÚY": "UÝ",
  "ủy": "uỷ",
  "Ủy": "Uỷ",
  "ỦY": "UỶ",
  "ũy": "uỹ",
  "Ũy": "Uỹ",
  "ŨY": "UỸ",
  "ụy": "uỵ",
  "Ụy": "Uỵ",
  "ỤY": "UỴ"
}

def replace_all(text):
    for i, j in dict_map.items():
        text = text.replace(i, j)
    return text

def process_file(file_path):

    print(f"Processing file: {file_path}")

    with open(file_path, 'r', encoding='utf-8') as file:
        data = file.read()

    new_data = replace_all(data)

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(new_data)

def replace_in_directory(directory_path):
    """Recursively processes text files within a directory.

    Args:
        directory_path: The path to the directory.
        dict_map: The dictionary of text replacements.
    """

    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.yml') or file.endswith('.yaml'):  # Process only yml files
                file_path = os.path.join(root, file)
                process_file(file_path)


if __name__ == "__main__":
  print("Tone normalization started")
  directory_path = "/home/nam/codeproj/rasa-my-first-model"
  replace_in_directory(directory_path)