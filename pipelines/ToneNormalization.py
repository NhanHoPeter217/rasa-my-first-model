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

    @classmethod
    def create(
        cls,
        config: Dict[Text, Any],
        model_storage: ModelStorage,
        resource: Resource,
        execution_context: ExecutionContext
    ) -> GraphComponent:
        
        print('initialised ToneNormalization')
        
        return super().create(config, model_storage, resource, execution_context)

    def required_packages() -> List[Text]:
        return []


    def process(self, messages: List[Message]) -> List[Message]:
        # Normalize user input
        for message in messages:
            message.data["text"] = self.normalize_tone(message.data["text"])
        
        return messages
    
    def normalize_tone(self, text: str) -> str:
        for k, v in self.dict_map.items():
            text = text.replace(k, v)
        return text