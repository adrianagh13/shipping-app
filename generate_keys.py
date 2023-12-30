import pickle
from pathlib import Path

import streamlit_authenticator as stauth

names = ["Adriana Gómez", "Jose Luis Rios"]
usernames = ["agomez13", "joseluishdez01"]
passwords = ["abc123", "password"]

hashed_passwords = stauth.Hasher(passwords).generate()

file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("wb") as file:
    pickle.dump(hashed_passwords, file)