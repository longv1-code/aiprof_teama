import json
from dotenv import load_dotenv
import os

# Json read utility.
def read_json_file(file_path):
  """Reads a JSON file and returns its contents as a Python object.

  Args:
    file_path: The path to the JSON file.

  Returns:
    The contents of the JSON file as a Python object (typically a dictionary or list).
  """

  with open(file_path, 'r') as f:
    data = json.load(f)
  return data

# Environment variable load utility.
def load_env(name: str):
  """function to load environment variable."""
  # Specify the path to your .env file
  env_path = '../.env' # ../.env

  # Load the .env file
  try:
    load_dotenv(dotenv_path=env_path)
    print("env file loaded successfully.")
  except Exception as e:
    print(f"An error occurred while loading .env file: {e}")

  # Now you can access the environment variables
  return os.getenv(name)
