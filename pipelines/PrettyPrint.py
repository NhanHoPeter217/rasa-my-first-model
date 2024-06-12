from typing import Dict, Text, Any, List

from rasa.engine.graph import GraphComponent, ExecutionContext
from rasa.engine.recipes.default_recipe import DefaultV1Recipe
from rasa.engine.storage.resource import Resource
from rasa.engine.storage.storage import ModelStorage
from rasa.shared.nlu.training_data.message import Message
from rasa.shared.nlu.training_data.training_data import TrainingData

from pprint import pprint


@DefaultV1Recipe.register(
    [DefaultV1Recipe.ComponentType.MESSAGE_FEATURIZER], is_trainable=False
)

class PrettyPrint(GraphComponent):
    @classmethod
    def create(
        cls,
        config: Dict[Text, Any],
        model_storage: ModelStorage,
        resource: Resource,
        execution_context: ExecutionContext
    ) -> GraphComponent:

        return cls(config, model_storage, resource, execution_context)
    
    @staticmethod
    def get_default_config() -> Dict[Text, Any]:
        return {
            "title": "PrettyPrint",
            "out_file": False 
        }
    
    def __init__(self, config: Dict[Text, Any], model_storage: ModelStorage, resource: Resource, execution_context: ExecutionContext) -> None:
        self.config = config
        super().__init__()

  
    def process(self, messages: List[Message]) -> List[Message]:
        print("[LOG] " + self.config.get("title"))
        
        for message in messages:
            pprint(vars(message))

        return messages
    
    def process_training_data(self, training_data: TrainingData) -> TrainingData:
        print("[LOG] " + self.config.get("title"))

        outFile = self.config.get("out_file")
        title = self.config.get("title")

        if outFile:
            with open('log_' + title+ '.txt' , "wt") as f:
                for example in training_data.training_examples:
                    pprint(vars(example), stream=f)
        else:
            for example in training_data.training_examples:
                pprint(vars(example))
        
        return training_data