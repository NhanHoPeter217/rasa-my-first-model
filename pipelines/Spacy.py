from typing import Dict, Text, Any, List

from rasa.engine.graph import GraphComponent, ExecutionContext
from rasa.nlu.tokenizers.tokenizer import Token, Tokenizer
from rasa.engine.recipes.default_recipe import DefaultV1Recipe
from rasa.engine.storage.resource import Resource
from rasa.engine.storage.storage import ModelStorage
from rasa.shared.nlu.training_data.message import Message
import spacy

@DefaultV1Recipe.register(
    [DefaultV1Recipe.ComponentType.MESSAGE_TOKENIZER], is_trainable=False
)

class SpacyTokenizer(Tokenizer):
    @classmethod
    def create(
        cls,
        config: Dict[Text, Any],
        model_storage: ModelStorage,
        resource: Resource,
        execution_context: ExecutionContext
    ) -> Tokenizer:
        cls.nlp = spacy.load('vi_core_news_lg')
        return cls(config)
    
    @staticmethod
    def get_default_config() -> Dict[Text, Any]:
        """Returns the component's default config."""
        return {
            # Flag to check whether to split intents
            "intent_tokenization_flag": False,
            # Symbol on which intent should be split
            "intent_split_symbol": "_",
            # Regular expression to detect tokens
            "token_pattern": None,
            # Symbol on which prefix should be split
            "prefix_separator_symbol": None,
        }

    def __init__(
        self,
        config: Dict[Text, Any],
    ) -> None:
        super().__init__(config)


    def tokenize(self, message: Message, attribute: Text) -> List[Token]:
        text = message.get(attribute)

        doc = self.nlp(text)
        # for token in doc:
        #   print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
        #           token.shape_, token.is_alpha, token.is_stop)
        
        # Hiển thị thông tin về token và các token con của chúng
        for token in doc:
            print(f"Token: {token.text}, POS: {token.pos_}, Dependency: {token.dep_}")
            for child in token.children:
                print(f"  Child Token: {child.text}, Dependency: {child.dep_}")

        tokens = self._convert_words_to_tokens([token.text.replace('_',' ') for token in doc], text)
        return self._apply_token_pattern(tokens)        