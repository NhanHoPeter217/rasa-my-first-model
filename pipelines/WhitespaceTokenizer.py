from typing import Dict, Text, Any, List

from rasa.engine.graph import GraphComponent, ExecutionContext
from rasa.engine.recipes.default_recipe import DefaultV1Recipe
from rasa.engine.storage.resource import Resource
from rasa.engine.storage.storage import ModelStorage
from rasa.shared.nlu.training_data.message import Message
from rasa.nlu.tokenizers.whitespace_tokenizer import WhitespaceTokenizer


@DefaultV1Recipe.register(
    [DefaultV1Recipe.ComponentType.INTENT_CLASSIFIER], is_trainable=False
)
class _WhitespaceTokenizer(GraphComponent):
    @classmethod
    def create(
            cls,
            config: Dict[Text, Any],
            model_storage: ModelStorage,
            resource: Resource,
            execution_context: ExecutionContext
    ) -> GraphComponent:
        return super().create(config, model_storage, resource, execution_context)

    def process(self, messages: List[Message]) -> List[Message]:
        print('After WhitespaceTokenizer:')
        tokenizer = WhitespaceTokenizer()

        tokens = tokenizer.tokenize(messages)

        # Print the tokens
        for token in tokens:
            print(token)

        return messages