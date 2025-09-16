import subprocess
import tempfile
from pathlib import Path


class GuesslangRunner:
    def __init__(self, python_exe: str, script_path: str):
        """
        Initialize with the Python 3.8 interpreter path and the guesslang script path.
        """
        self.python_exe = python_exe
        self.script_path = script_path

    def run(self, input_data: str, input_type: str = "text") -> str | None:
        """
        Run guesslang on given input (either 'text' or 'file').

        :param input_data: Code snippet (if input_type='text') or file path (if input_type='file')
        :param input_type: 'text' or 'file'
        :return: Guesslang output string or None if failed
        """
        try:
            if input_type == "file":
                input_path = Path(input_data).resolve()
                if not input_path.exists():
                    raise FileNotFoundError(f"File not found: {input_path}")

                result = subprocess.run(
                    [self.python_exe, self.script_path, str(input_path)],
                    capture_output=True,
                    text=True
                )

            elif input_type == "text":
                with tempfile.NamedTemporaryFile("w+", delete=False, suffix=".txt") as tmp:
                    tmp.write(input_data)
                    tmp_path = tmp.name

                result = subprocess.run(
                    [self.python_exe, self.script_path, tmp_path],
                    capture_output=True,
                    text=True
                )
                Path(tmp_path).unlink(missing_ok=True)

            else:
                raise ValueError("input_type must be 'text' or 'file'")

            if result.stderr.strip():
                print(f"[Error] {result.stderr.strip()}")
                return None
            return result.stdout.strip()

        except Exception as e:
            print(f"[Exception] {e}")
            return None

    def process_folder(self, folder_path: str):
        """
        Process all files in a folder and run guesslang on them.
        """
        folder = Path(folder_path).resolve()
        if not folder.exists():
            raise FileNotFoundError(f"Folder not found: {folder}")

        fault_count, total_count = 0, 0
        
        for file_path in folder.glob("*"):
            if file_path.is_file():
                print(f"Processing file: {file_path.name}")
                try:
                    output = self.run(str(file_path), input_type="file")
                    print(f"Output: {output}")
                    total_count += 1
                    if not output:
                        fault_count += 1
                except Exception as e:
                    print(f"Error processing {file_path.name}: {e}")
                    fault_count += 1

                print(f"Faults: {fault_count} out of {total_count} files.")
                print("-" * 50)

        print(f"Final Faults: {fault_count} out of {total_count} files.")


if __name__ == "__main__":
    runner = GuesslangRunner(
        python_exe=r"D:\Language Guess\guesslang38\Scripts\python.exe",
        script_path=r"D:\TextCodeFIleUpload\FileParsing\legacy_script.py" #subprocess which run to detect a file content 
    )

    folder_path = input("Enter the Folder Path: ")
    runner.process_folder(folder_path)
