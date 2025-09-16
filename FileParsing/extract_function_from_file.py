import os
import csv
import pandas as pd
from tree_sitter_language_pack import get_parser

class FunctionExtractor:
    FUNC_NODES = {
        "c": {"function_definition"},
        "cpp": {"function_definition"},
        "java": {"method_declaration", "constructor_declaration"},
        "python": {"function_definition"},
        "php": {"function_definition", "method_declaration"},
    }

    LANG_MAP = {
        ".c": "c",
        ".cpp": "cpp",
        ".cc": "cpp",
        ".h": "cpp",
        ".java": "java",
        ".py": "python",
        ".php": "php",
    }

    def __init__(self, csv_dir):
        self.csv_dir = csv_dir
        os.makedirs(self.csv_dir, exist_ok=True)

    def extract_functions_from_code(self, code_bytes, lang_name):
        """Extract functions from code using Tree-sitter"""
        parser = get_parser(lang_name)
        tree = parser.parse(code_bytes)
        root = tree.root_node
        functions = []

        def traverse(node):
            if node.type in self.FUNC_NODES.get(lang_name, {}):
                try:
                    func_code = code_bytes[node.start_byte:node.end_byte].decode(errors="ignore")
                    functions.append(func_code)
                except Exception as e:
                    print(f"Error decoding function: {e}")
            for child in node.children:
                traverse(child)

        traverse(root)
        return functions

    def process_file(self, file_path):
        """Process a single file and return functions as a dict"""
        ext = os.path.splitext(file_path)[1].lower()
        if ext not in self.LANG_MAP:
            print(f"Skipping unsupported file: {file_path}")
            return None

        lang = self.LANG_MAP[ext]
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                code_bytes = f.read().encode()
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return None
        funcs = self.extract_functions_from_code(code_bytes, lang)
        if not funcs:
            return None

        # Prepare a dictionary for pandas DataFrame
        data = {"file_path": file_path}
        for i, func in enumerate(funcs, start=1):
            data[f"func{i}"] = func
        
        return lang, data

    def save_to_csv(self, lang, data):
        """Save extracted functions to a CSV using pandas""" 
        try:
            csv_path = os.path.join(self.csv_dir, f"{lang}_functions.csv")
            df_new = pd.DataFrame([data])
            if os.path.exists(csv_path):
                df_existing = pd.read_csv(csv_path)
                df_combined = pd.concat([df_existing, df_new], ignore_index=True)
            else:
                df_combined = df_new

            df_combined.to_csv(csv_path, index=False, quoting=csv.QUOTE_ALL)
            print(f"CSV written/updated: {csv_path}")
        except Exception as exception:
            print("Error to save csv ", exception)
            return None

    def process_folder(self, folder_path):
        """Process all files in a folder"""
        try:
            total_files = 0
            for root, _, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    print(f"Processing file: {file_path}")
                    result = self.process_file(file_path)
                    if result:
                        lang, data = result
                        self.save_to_csv(lang, data)
                        total_files += 1
                        print(f"Processed {total_files} files so far")
                    print("-" * 50)
        except Exception as exception:
            print(f"Error Processing Folder {folder_path}: {exception}")
            return None


if __name__ == "__main__":
    folder_path = input("Enter folder path: ")
    csv_dir = input("Enter CSV output folder path: ")
    extractor = FunctionExtractor(csv_dir)
    extractor.process_folder(folder_path)