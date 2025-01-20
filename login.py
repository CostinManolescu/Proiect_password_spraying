import requests

url = "http://127.0.0.1:5000/login"

usernames = []
passwords = []

n = int(input("Number of passwords: "))
for i in range(n):
    password = input("Passwords: ")
    passwords.append(password)

n = int(input("Number of users: "))
for i in range(n):
    username = input("Username: ")
    usernames.append(username)

for password in passwords:
    for username in usernames:
        response = requests.post(url, data={"username": username, "password":password},)

        if response.status_code == 200:
            print(f"[SUCCESS] Username: {username} | Password: {password}")
        else:
            print(f"[FAILED] Username: {username} | Password: {password}")

