# coding=utf-8
# Copyright (c) 2021 VinAI Research

import os

REPLACE_PATH = "/home/nam/codeproj/rasa-my-first-model"

import sys
sys.path.append('/home/nam/codeproj/rasa-my-first-model/pipelines')
import VietnameseTextNormalizer

def replace_all(text):
    text = VietnameseTextNormalizer.Normalize(text)
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
            if file.endswith('.yml') or file.endswith('.yaml') or file.endswith('.txt'):
                file_path = os.path.join(root, file)
                process_file(file_path)


if __name__ == "__main__":
  print("Tone normalization started")
  replace_in_directory(REPLACE_PATH)