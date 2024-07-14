from typing import Dict, Text, Any, List, Optional, Tuple

from rasa.engine.graph import GraphComponent, ExecutionContext
from rasa.engine.recipes.default_recipe import DefaultV1Recipe
from rasa.engine.storage.resource import Resource
from rasa.engine.storage.storage import ModelStorage
from rasa.shared.nlu.training_data.message import Message
from rasa.shared.nlu.training_data.training_data import TrainingData
from rasa.shared.nlu.constants import TEXT

import os
import sys
from pprint import pprint
import yaml
import re

# coding=utf-8
# Copyright (c) 2021 VinAI Research

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
    "ỤY": "UỴ",
    }

def replace_all(text, dict_map):
    for i, j in dict_map.items():
        text = text.replace(i, j)
    return text



BASE_PATH = os.getcwd()

sys.path.append(os.path.join(BASE_PATH, 'pipelines/'))
import VietnameseTextNormalizer

abbreviations_file = os.path.join(BASE_PATH, "pipelines/vietnamese-abbreviations.yml") # Abbreviations file
stopword_file = os.path.join(BASE_PATH, "pipelines/vietnamese-stopwords.txt") # Stop words file
symbols = "!$%&'*+;<=>?@^`~" # Symbols to remove

class Abbreviation:
    def __init__(self, value: str, shorthands: str):
        self.value = value
        self.shorthands = shorthands.split('\n')
        if self.shorthands[-1] == '':
            self.shorthands.pop()

@DefaultV1Recipe.register(
    [DefaultV1Recipe.ComponentType.MESSAGE_FEATURIZER], is_trainable=False
)

class Preprocesser(GraphComponent):
    @staticmethod
    def supported_languages() -> Optional[List[Text]]:
        supported_languages = ["vi"]
        return supported_languages

    @staticmethod
    def get_default_config() -> Dict[Text, Any]:
        return {
            "remove_stopwords": False,
        }

    def __init__(
        self,
        config: Dict[Text, Any],
        model_storage: ModelStorage,
        resource: Resource,
        execution_context: ExecutionContext
    ) -> None:
        self.config = config
        super().__init__()

    @classmethod
    def create(
        cls,
        config: Dict[Text, Any],
        model_storage: ModelStorage,
        resource: Resource,
        execution_context: ExecutionContext
    ) -> GraphComponent:
        print('[Preprocesser] - Init Preprocesser')

        with open(abbreviations_file, "r") as f:
            arrs = yaml.safe_load(f)
            cls.abbreviations = [Abbreviation(item['value'], item['shorthands']) for item in arrs]

        with open(stopword_file, "r") as f:
            cls.stopwords = [word.strip() for word in f]

        print("[Preprocesser] - Remove stopwords turned " + ("on" if config.get("remove_stopwords") else "off"))

        return cls(config, model_storage, resource, execution_context)
    

    def process_training_data(self, training_data: TrainingData) -> TrainingData:
        for example in training_data.training_examples:
            if (
                example.get(TEXT) is not None
                and not example.get(TEXT) == ""
            ):
                print(f"\nPREPROCESS: {TEXT} | {example.get(TEXT)}")
                
                self.normalize(example, TEXT)
                
                print(f"OUTPUT: {TEXT} | {example.get(TEXT)}")
        
        return training_data

  
    def process(self, messages: List[Message]) -> List[Message]:
        # Preprocess user input
        for message in messages:
            self.normalize(message, TEXT)

        return messages

    @classmethod
    def normalize(cls, message: Message, attribute: Text) -> None:
        sentence : str = message.get(attribute)
        
        # remove redundant spaces
        sentence = re.sub(' +', ' ', sentence)
        
        # lowercase
        sentence = sentence.lower()

        # Replace short hand
        sentence = cls.replace_abbreviations(sentence)

        # Tone Normalize
        sentence = VietnameseTextNormalizer.Normalize(sentence)
        
        sentence = replace_all(sentence, dict_map)

        # Remove stop words
        if cls.config.get("remove_stopwords"):
            sentence = cls.remove_words(sentence, cls.stopwords)

        sentence = sentence.strip()
        
        message.set(attribute, sentence)
        return
    
    @classmethod
    def replace_abbreviations(cls, text: str) -> str:
        for item in cls.abbreviations:
            for i in item.shorthands:
                text = text.replace(' ' + i + ' ', ' ' + item.value + ' ')
                if text.startswith(i + ' '):
                    text = text.replace(i + ' ', item.value + ' ', 1)
                if text.endswith(' ' + i):
                    text = text.replace(' ' + i, ' ' + item.value, 1)
        return text


    @staticmethod
    def remove_words(text: str, words: List[str]) -> str:
        for i in words:
            text = text.replace(' ' + i + ' '," ")
            if text.startswith(i):
                text = text.replace(i + ' ',"")
            if text.endswith(' ' + i):
                text = text.replace(' ' + i,"")
        return text
    
    @staticmethod
    def remove_symbols(text: str) -> str:
        for i in symbols:
            text = text.replace(i, " ")
        return text