from typing import Dict, Text, Any, List

from rasa.engine.graph import GraphComponent, ExecutionContext
from rasa.engine.recipes.default_recipe import DefaultV1Recipe
from rasa.engine.storage.resource import Resource
from rasa.engine.storage.storage import ModelStorage
from rasa.shared.nlu.training_data.message import Message
from rasa.shared.nlu.training_data.training_data import TrainingData

import sys
sys.path.append("D://IT//PyCharm//rasa-my-first-model//pipelines")
# import VietnameseTextNormalizer

# Path to the stopword file
stopword_file = "D:/IT/PyCharm/rasa-my-first-model/pipelines/vietnamese-stopwords.txt"

# List of symbols to remove
symbols = "!$%&'*+;<=>?@^`~"

@DefaultV1Recipe.register(
    [DefaultV1Recipe.ComponentType.MESSAGE_FEATURIZER], is_trainable=False
)

class Preprocesser(GraphComponent):
    @classmethod
    def create(
        cls,
        config: Dict[Text, Any],
        model_storage: ModelStorage,
        resource: Resource,
        execution_context: ExecutionContext
    ) -> GraphComponent:
        
        print('initialising Preprocesser')
        # with open(stopword_file, "r") as f:
        #     cls.stopwords = set(word.strip() for word in f)

        return super().create(config, model_storage, resource, execution_context)
    
    def process_training_data(self, training_data: TrainingData) -> TrainingData:
        # for message in training_data.training_examples:
        #     text_preprocess(message)
        return training_data

  
    def process(self, messages: List[Message]) -> List[Message]:

        # Preprocess user input
        # for message in messages:
        #     text_preprocess(message)

        return messages

def text_preprocess(message: Message) -> None:
    sentence : str = message.get("text")
    # Tone Normalize
    sentence = VietnameseTextNormalizer.Normalize(sentence)
    print(f"###### Normalize: {sentence}")

    # Remove stop words & symbols
    sentence = remove_symbols_stop_words(sentence)
    print(f"###### Remove symbols & Stop words: {sentence}")
    
    message.set("text", sentence)
    return
    
def remove_symbols_stop_words(text: str) -> str:
    text = text.lower()
    for i in Preprocesser.stopwords:
        text = text.replace(' ' + i + ' '," ")
        if text.startswith(i):
            text = text.replace(i + ' ',"")
        if text.endswith(' ' + i):
            text = text.replace(' ' + i,"")
    
    for i in symbols:
        text = text.replace(i, " ")
    return text