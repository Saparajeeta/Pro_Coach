import os
import pickle 
from pathlib import Path

from dotenv import load_dotenv
import streamlit_authenticator as stauth 

load_dotenv()

names =  ["Aparajeeta","Aditya"]
usernames = ['aparajeeta','aditya']
passwords = [os.getenv("APARA_PASS"), os.getenv("ADIT_PASS")]

hashed_passwords = stauth.Hasher(passwords).generate()

file_path = Path(__file__).parent / "hashed.pkl"

with open(file_path, "wb") as f:
    pickle.dump(hashed_passwords, f)