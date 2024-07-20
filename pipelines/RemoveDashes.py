from typing import Dict, Text, Any, List

from rasa.engine.graph import GraphComponent, ExecutionContext
from rasa.engine.recipes.default_recipe import DefaultV1Recipe
from rasa.engine.storage.resource import Resource
from rasa.engine.storage.storage import ModelStorage
from rasa.shared.nlu.training_data.message import Message
from rasa.shared.nlu.training_data.message import Text

# Path to the stopword file
stopword_file = "pipelines/vietnamese-stopwords.txt"

# List of symbols to remove
symbols = "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"


@DefaultV1Recipe.register(
    [DefaultV1Recipe.ComponentType.INTENT_CLASSIFIER], is_trainable=False
)
class RemoveDashes(GraphComponent):
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
        with open(stopword_file, "r", encoding="utf-8") as f:
            cls.stopwords = set(word.strip() for word in f)

        return super().create(config, model_storage, resource, execution_context)

    def process(self, messages: List[Message]) -> List[Message]:
        # nlp = spacy.load("vi_core_news_lg")

        for message in messages:
            sentence = message.get("text")
            sentence = sentence.replace("_", " ")
            message.set("text", sentence)
        return messages