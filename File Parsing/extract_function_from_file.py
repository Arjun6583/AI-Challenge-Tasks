import csv
from pathlib import Path
from tree_sitter_language_pack import get_parser

# Increase CSV cell size
csv.field_size_limit(10_000_000)

# Supported function nodes per language
FUNC_NODES = {
    "c": {"function_definition"},
    "cpp": {"function_definition"},
    "java": {"method_declaration", "constructor_declaration"},
    "python": {"function_definition"},
    "php": {"function_definition", "method_declaration"},
}

# Extension → Language map
LANG_MAP = {
    ".c": "c",
    ".cpp": "cpp",
    ".cc": "cpp",
    ".h": "cpp",
    ".java": "java",
    ".py": "python",
    ".php": "php",
}

CSV_FILE_PATH = r"D:\TextCodeFIleUpload\File Parsing\csv_files"


def extract_functions_from_code(code_bytes: bytes, lang_name: str):
    """Parse code with tree-sitter and extract function definitions."""
    parser = get_parser(lang_name)
    tree = parser.parse(code_bytes)
    root = tree.root_node

    functions = []

    def traverse(node):
        if node.type in FUNC_NODES.get(lang_name, {}):
            try:
                func_code = code_bytes[node.start_byte:node.end_byte].decode(errors="ignore")
                functions.append(func_code)
            except Exception as e:
                print(f"⚠️ Error decoding function: {e}")
        for child in node.children:
            traverse(child)

    traverse(root)
    return functions


def write_functions_to_csv(file_path: str):
    """Extract functions from a file and append/update them in a CSV."""
    try:
        ext = Path(file_path).suffix.lower()
        if ext not in LANG_MAP:
            print(f"Skipping unsupported file: {file_path}\n")
            return

        lang = LANG_MAP[ext]
        try:
            code_bytes = Path(file_path).read_text(errors="ignore").encode()
        except Exception as e:
            print(f"⚠️ Error reading {file_path}: {e}")
            return

        funcs = extract_functions_from_code(code_bytes, lang)

        csv_path = Path(CSV_FILE_PATH) / f"{lang}_functions.csv"
        file_exists = csv_path.exists()

        rows = [[str(file_path)] + funcs]

        existing_rows = []
        max_cols = len(funcs)

        if file_exists:
            try:
                with open(csv_path, "r", newline="", encoding="utf-8") as f:
                    reader = csv.reader(f)
                    header = next(reader, None)
                    existing_rows = list(reader)

                current_func_cols = len(header) - 1 if header else 0
                max_cols = max(current_func_cols, len(funcs))
            except Exception as e:
                print(f"Error reading existing CSV {csv_path}: {e}")

        headers = ["file_path"] + [f"func{i+1}" for i in range(max_cols)]

        # Normalize rows length
        for i in range(len(existing_rows)):
            existing_rows[i] += [""] * (max_cols - (len(existing_rows[i]) - 1))
        for i in range(len(rows)):
            rows[i] += [""] * (max_cols - (len(rows[i]) - 1))

        try:
            with open(csv_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f, quoting=csv.QUOTE_ALL)
                writer.writerow(headers)
                for r in existing_rows:
                    writer.writerow(r)
                for r in rows:
                    writer.writerow(r)
            print(f"CSV written/updated: {csv_path}\n")
        except Exception as e:
            print(f"⚠️ Error writing to CSV {csv_path}: {e}")

    except Exception as e:
        print(f"Unexpected error in write_functions_to_csv for {file_path}: {e}")


if __name__ == "__main__":
    folder_path = Path(r"D:\Test Data\php")
    for file_path in folder_path.glob("*"):
        if file_path.is_file():
            print(f"Processing file: {file_path.name}\n")
            try:
                write_functions_to_csv(str(file_path))
                print("File functions added into CSV file\n")
            except Exception as e:
                print(f"Error processing {file_path.name}: {e}\n")
            print("-" * 50)
