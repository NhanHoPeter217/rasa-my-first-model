import py_vncorenlp
from typing import Any, Text, Dict, List
import os
import yaml
import pandas as pd

basePath = "/home/nam/codeproj/rasa-my-first-model/"

class VnCoreNLPTokenizer(object):
    name = "vncorenlp_tokenizer"

    def __init__(self) -> None:
        super().__init__()

        if os.path.exists(os.path.join(basePath,'pipelines/VnCoreNLP')) == False:
            py_vncorenlp.download_model(save_dir=os.path.join(basePath, 'pipelines/VnCoreNLP'))

        # Load VnCoreNLP segmenter (adjust model path if needed)
        self.model = py_vncorenlp.VnCoreNLP(save_dir=os.path.join(basePath, 'pipelines/VnCoreNLP'))

        self.outputTempFile = open(os.path.join(basePath,"output.txt"), "a")
    
    def __del__(self):
        self.outputTempFile.close()

    def process(self, message : str, **kwargs):
        try:
            # Apply word segmentation
            sentences = self.model.annotate_text(message)
            print(message)
            print(pd.DataFrame(sentences[0]), '-------\n\n')

            self.outputTempFile.write(message + "\n" + pd.DataFrame(sentences[0]).to_string() + "\n\n\n")
            # Extract tokens as a list
            # tokenized_text = [token for sentence in sentences for token in sentence]
            # Add tokens back to the message
            # message.set("tokens", tokenized_text)
        except Exception as e:
            print(f"An exception occurred in the VnCoreNLP Component: {e}")



def process_yaml_files(directory : str, output : str):

    vncoreObj = VnCoreNLPTokenizer()

    skip_files = ["basic", "syn", "rule"]

    """Recursively finds YAML files, processes 'examples' values."""
    for root, _, files in os.walk(directory):
        for file in files:
            print("File:", file)

            if any(skip in file for skip in skip_files):
                continue

            if file.endswith(".yaml") or file.endswith(".yml"):
                filepath = os.path.join(root, file)
                with open(filepath, "r") as f:
                    try:
                        data = yaml.safe_load(f)
                        if isinstance(data, dict):  # Check if it's a list of dicts
                            for item in data["nlu"]:
                                if "intent" in item and "examples" in item:
                                    examples = item["examples"].strip().split("\n")
                                    for example in examples:
                                        example = vncoreObj.process(example.lstrip("- ")) 
                                    item["examples"] = "\n".join(f"- {ex}" for ex in examples)

                        # Write back the processed data to the file (optional)
                        # with open(os.path.join(output, file), "w", encoding='utf-8') as f:
                        #     yaml.dump(data, f, default_flow_style=False)

                    except yaml.YAMLError as e:
                        print(f"Error parsing YAML file {filepath}: {e}")

if __name__ == "__main__":
    directory_to_search = os.path.join(basePath, "data_no_entity")
    output = os.path.join(basePath, "data_copy_nlu_core")
    process_yaml_files(directory_to_search, output)
