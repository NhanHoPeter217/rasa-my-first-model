from typing import Dict, Text, Any, List

from rasa.engine.graph import GraphComponent, ExecutionContext
from rasa.engine.recipes.default_recipe import DefaultV1Recipe
from rasa.engine.storage.resource import Resource
from rasa.engine.storage.storage import ModelStorage
from rasa.shared.nlu.training_data.message import Message

# Path to the stopword file
stopword_file = "pipelines/vietnamese-stopwords.txt"

# List of symbols to remove
symbols = "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"

@DefaultV1Recipe.register(
    [DefaultV1Recipe.ComponentType.INTENT_CLASSIFIER], is_trainable=False
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

        print('initialising Stop Words Removal')
        with open(stopword_file, "r") as f:
            cls.stopwords = set(word.strip() for word in f)

        return super().create(config, model_storage, resource, execution_context)

  
    def process(self, messages: List[Message]) -> List[Message]:

        # Preprocess user input
        for message in messages:
            text_preprocess(message)

        return messages

def text_preprocess(message: Message) -> None:
    sentence : str = message.get("text")
    
    # Remove symbols
    for i in symbols:
        sentence = sentence.replace(i, "")

    # Remove stop words
    sentence = replace_stop_word(sentence)
    
    # Tone Normalize
    sentence = replace_tone(sentence)

    message.set("text", sentence)
    return
    
def replace_stop_word(text: str) -> str:
    for i in Preprocesser.stopwords:
        text.replace(i,"")
    return text


def replace_tone(text: str) -> str:
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
    for i, j in dict_map.items():
        text = str(text.replace(i, j))
    return text