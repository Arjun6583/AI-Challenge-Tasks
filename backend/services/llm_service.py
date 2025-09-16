from datetime import datetime
import os

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

        self.running = True
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
