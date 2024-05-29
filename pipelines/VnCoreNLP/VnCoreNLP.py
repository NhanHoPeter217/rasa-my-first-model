import py_vncorenlp

# Automatically download VnCoreNLP components from the original repository
# and save them in some local working folder
py_vncorenlp.download_model(save_dir='/absolute/path/to/vncorenlp')

# Load VnCoreNLP from the local working folder that contains both `VnCoreNLP-1.2.jar` and `models` 
model = py_vncorenlp.VnCoreNLP(save_dir='/absolute/path/to/vncorenlp')
# Equivalent to: model = py_vncorenlp.VnCoreNLP(annotators=["wseg", "pos", "ner", "parse"], save_dir='/absolute/path/to/vncorenlp')

# Annotate a raw corpus
model.annotate_file(input_file="/absolute/path/to/input/file", output_file="/absolute/path/to/output/file")

# Annotate a raw text
model.print_out(model.annotate_text("Ông Nguyễn Khắc Chúc  đang làm việc tại Đại học Quốc gia Hà Nội. Bà Lan, vợ ông Chúc, cũng làm việc tại đây."))

from typing import Any, Text, Dict, List

class VnCoreNLPTokenizer(object):
    name = "vncorenlp_tokenizer"

    def __init__(self, component_config: Dict[Text, Any]) -> None:
        super().__init__()

        # Load VnCoreNLP segmenter (adjust model path if needed)
        self.model = py_vncorenlp.VnCoreNLP(annotate_tokens=True, 
                                             max_heap_size='-Xmx500m',
                                             annotators="wseg",
                                             save_dir='./VnCoreNLP-1.2.jar')  

    def process(self, message, **kwargs):
        try:
            # Apply word segmentation
            sentences = self.model.annotate_text(message.get('text'))

            # Extract tokens as a list
            tokenized_text = [token for sentence in sentences for token in sentence]

            # Add tokens back to the message
            message.set("tokens", tokenized_text)
        except Exception as e:
            print(f"An exception occurred in the VnCoreNLP Component: {e}") 
