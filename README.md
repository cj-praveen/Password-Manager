# Password Manager

This is a simple password manager backend built using Python. It encrypts passwords using the cryptography library and stores them in an SQLite database. The manager can be integrated with any frontend technology that communicates with this backend via suitable API calls.

## Requirements

- Python 3.x
- cryptography library

## Installation

1. Clone the repository:
```bash
git clone https://github.com/cj-praveen/Password-Manager.git
cd password-manager
```
   
2. Install the required libraries:
```bash
pip install cryptography
```

## Usage

1. Generating a Key

To generate a new encryption key:

```py
from password_manager import generate_key

key = generate_key()
print(key)
```

2. Initializing the Password Manager

To initialize the password manager with a generated key:

```python
from password_manager import PasswordManager

key = b'your-generated-key'
manager = PasswordManager(key)
```

3. Creating a New Record

To create a new record:

```python
response = manager.new_record("user@example.com", "password123", "example.com")
print(response)
```

4. Fetching a Record

To fetch a specific record:

```python
response = manager.fetch_record("user@example.com", "example.com")
print(response)
```

5. Fetching All Records

To fetch all records:

```python
response = manager.fetch_records()
print(response)
```

6. Deleting a Record

To delete a record:

```python
response = manager.delete_record("user@example.com", b'encrypted-token', "example.com")
print(response)
```
