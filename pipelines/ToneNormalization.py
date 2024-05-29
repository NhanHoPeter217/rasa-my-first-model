from typing import Dict, Text, Any, List

from rasa.engine.graph import GraphComponent, ExecutionContext
from rasa.engine.recipes.default_recipe import DefaultV1Recipe
from rasa.engine.storage.resource import Resource
from rasa.engine.storage.storage import ModelStorage
from rasa.shared.nlu.training_data.message import Message

@DefaultV1Recipe.register(
    [DefaultV1Recipe.ComponentType.INTENT_CLASSIFIER], is_trainable=False
)

class ToneNormalization(GraphComponent):
    @classmethod
    def create(
        cls,
        config: Dict[Text, Any],
        model_storage: ModelStorage,
        resource: Resource,
        execution_context: ExecutionContext
    ) -> GraphComponent:
        
        print('initialised Tone Normalization')
        
        return super().create(config, model_storage, resource, execution_context)

    def process(self, messages: List[Message]) -> List[Message]:
        print('processing Tone Normalizing...')
        # Normalize user input
        for message in messages:
            message.set("text", message.get("text"))
        
        return messages

def replace_all(text: str) -> str:
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