from typing import Dict, Text, Any, List

from rasa.engine.graph import GraphComponent, ExecutionContext
from rasa.nlu.tokenizers.tokenizer import Token, Tokenizer
from rasa.engine.recipes.default_recipe import DefaultV1Recipe
from rasa.engine.storage.resource import Resource
from rasa.engine.storage.storage import ModelStorage
from rasa.shared.nlu.training_data.message import Message

import py_vncorenlp
import os
import regex
import pprint

# Automatically download VnCoreNLP components from the original repository
# and save them in some local working folder
VNCORE_NLP = '/home/nam/codeproj/rasa-my-first-model'

@DefaultV1Recipe.register(
    [DefaultV1Recipe.ComponentType.MESSAGE_TOKENIZER], is_trainable=False
)


class VnCoreNLPTokenizer(Tokenizer):    
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
        """Returns the component's default config."""
        return {
            # Flag to check whether to split intents
            "intent_tokenization_flag": True,
            # Symbol on which intent should be split
            "intent_split_symbol": "+",
            # Regular expression to detect tokens
            "token_pattern": None,
            # Symbol on which prefix should be split
            "prefix_separator_symbol": None,
        }

    def __init__(
        self,
        config: Dict[Text, Any],
        model_storage: ModelStorage,
        resource: Resource,
        execution_context: ExecutionContext
    ) -> None:
        if not os.path.exists(VNCORE_NLP):
            py_vncorenlp.download_model(save_dir=VNCORE_NLP)
        self.rdrsegmenter = py_vncorenlp.VnCoreNLP(annotators=["wseg"], save_dir=VNCORE_NLP)
        super().__init__(config)


    def tokenize(self, message: Message, attribute: Text) -> List[Token]:
        try:
            text = message.get(attribute)
            segmented : List[str] = self.rdrsegmenter.annotate_text(text).get(0)
            words : List[str] = []
            temp = ''
            
            words = [i.get('wordForm').replace('_', ' ') for i in segmented if regex.match(r'[^._~:/?#\[\]()@!$&*+,;=-]', i.get('wordForm'))]
            
            tokens = self._convert_words_to_tokens(words, text)
    
            return self._apply_token_pattern(tokens)

        except Exception as e:
            print(f"[Err]: {e} || word: {temp} || in text: {text} || words: {words}") 
            return words
