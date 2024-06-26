from cryptography.fernet import Fernet
from cryptography.exceptions import CryptographyError
import sqlite3

def generate_key() -> bytes:
    return Fernet.generate_key()

class PasswordManager:
    def __init__(self, key: bytes) -> None:
        self.fernet = Fernet(key)
        self.db = sqlite3.connect("passwords.db")
        self.db.execute("CREATE TABLE IF NOT EXISTS store(email VARCHAR(256),site VARCHAR(512),token TEXT)")
        self.db.commit()

    def __del__(self) -> None:
        self.db.close()

    def encrypt_pwd(self, passwd: str) -> dict:
        try:
            return dict(token=self.fernet.encrypt(passwd.encode()), code=0)
        except CryptographyError:
            return dict(error="Error occured while encrypting password", code=1)

    def decrypt_pwd(self, token: bytes) -> dict:
        try:
            return dict(passwd=self.fernet.decrypt(token).decode(), code=0)
        except CryptographyError:
            return dict(error="Error occured while decrypting password", code=1)

    def new_record(self, email: str, password: str, site: str) -> dict:
        try:
            token = self.encrypt_pwd(password).decode()
            self.db.execute("INSERT INTO store VALUES(?,?,?)", (email, site, token))
            self.db.commit()
            return dict(message="Successfully created new record!", code=0)
        except sqlite3.Error:
            self.db.rollback()
            return dict(error="Error occured while creating a new record", code=1)

    
    def delete_record(self, email: str, token: bytes, site: str) -> dict:
        try:
            self.db.execute("DELETE FROM store WHERE email=? and site=? and token=?", (email, site, token))
            self.db.commit()
            return dict(message="Successfully deleted a record!", code=0)
        except sqlite3.Error:
            self.db.rollback()
            return dict(error="Error occured while deleting a record", code=1)


    def fetch_record(self, email: str, site: str) -> dict:
        try:
            record = self.db.execute("SELECT * FROM store WHERE email=? and site=?", (email, site)).fetchone()
            return dict(email=record[0],site=record[1],token=record[2], code=0) if record else {}
        except sqlite3.Error:
            return dict(error="Error occured while fetching a record", code=1)

    def fetch_records(self) -> dict:
        try:
            return dict(records=[dict(email=record[0],site=record[1],token=record[2]) for record in self.db.execute("SELECT * FROM store").fetchall()], code=0)
        except sqlite3.Error:
            return dict(error="Error occured while fetching all records", code=1)
