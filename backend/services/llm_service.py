from datetime import datetime 
from llm_guard.input_scanners import Code
import os

llm_guard_code_object = None
class SimpleLLMService:
    def __init__(self, log_file="llm_service.log"):
        self.summarizer = None
        self.running = False
        self.log_file_path = log_file
        self.log_file = None

    def start(self):
        if self.running:
            print("Server already running.")
            return
        print("Loading Server...")

        self.log_file = open(self.log_file_path, "a", encoding="utf-8")
        global llm_guard_code_object
        llm_guard_code_object = Code(["C", "C++", "Java", "Python", "PHP", "C#"])
        self.running = True
        print(llm_guard_code_object)
        print("Server started and ready!")

    def summarize(self, text: str):
        # Log input text with timestamp
        if self.log_file:
            timestamp = datetime.now().isoformat()
            self.log_file.write(f"[{timestamp}] Input: {text}\n")
            self.log_file.flush()

        return "Log added into file."

    def stop(self):
        if not self.running:
            print("Server is already stopped.")
            return

        print("Stopping Server...")
        self.summarizer = None  
    
        if self.log_file:
            self.log_file.close()
            self.log_file = None 
            print(f"Log file {self.log_file_path} closed.")

        self.running = False
        print("Sever stopped")
