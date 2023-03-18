import email
import imaplib
import re
import random
from instagrapi import Client
from instagrapi.mixins.challenge import ChallengeChoice
from os import system, name
import time
import random
import sys
from random import shuffle

def get_code_from_email(username):
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(CHALLENGE_EMAIL, CHALLENGE_PASSWORD)
    mail.select("inbox")
    result, data = mail.search(None, "(UNSEEN)")
    assert result == "OK", "Error1 during get_code_from_email: %s" % result
    ids = data.pop().split()
    for num in reversed(ids):
        mail.store(num, "+FLAGS", "\\Seen")  # mark as read
        result, data = mail.fetch(num, "(RFC822)")
        assert result == "OK", "Error2 during get_code_from_email: %s" % result
        msg = email.message_from_string(data[0][1].decode())
        payloads = msg.get_payload()
        if not isinstance(payloads, list):
            payloads = [msg]
        code = None
        for payload in payloads:
            body = payload.get_payload(decode=True).decode()
            if "<div" not in body:
                continue
            match = re.search(">([^>]*?({u})[^<]*?)<".format(u=username), body)
            if not match:
                continue
            print("Match from email:", match.group(1))
            match = re.search(r">(\d{6})<", body)
            if not match:
                print('Skip this email, "code" not found')
                continue
            code = match.group(1)
            if code:
                return code
    return False


def get_code_from_sms(username):
    while True:
        code = input(f"Enter code (6 digits) for {username}: ").strip()
        if code and code.isdigit():
            return code
    return None


def challenge_code_handler(username, choice):
    if choice == ChallengeChoice.SMS:
        return get_code_from_sms(username)
    elif choice == ChallengeChoice.EMAIL:
        return get_code_from_email(username)
    return False


def change_password_handler(username):
    # Simple way to generate a random string
    chars = list("abcdefghijklmnopqrstuvwxyz1234567890!&£@#")
    password = "".join(random.sample(chars, 10))
    return password

def timer(count):
    print("")
    for remaining in range(count, 0, -1):
        sys.stdout.write("\r")
        sys.stdout.write("{:2d} seconds remaining.".format(remaining))
        sys.stdout.flush()
        time.sleep(1)

    sys.stdout.write("\rComplete!            \n")
    print("")




if name == 'nt':
    _ = system('cls')

    # for mac and linux(here, os.name is 'posix')
else:
    _ = system('clear')



def read_users(file):
    with open(file, "r") as f:
        lines = f.read().splitlines()
        lst = []
        for line in lines:
            username = line.split(":")[0]
            password = line.split(":")[1]
            email = line.split(":")[2]
            emailPassword = line.split(":")[3]
            lst.append([username, password, email, emailPassword])
            shuffle(lst)
    return lst


accounts = read_users("accounts.txt")


question1 = """
Instagram Automator 


1. Follow an Account.
2. Comment on an Account (Random Posts).
3. Comment on a Specific Post.

Please Select : 1, 2, 3... : """

answer1 = input(question1).strip()

if answer1 == "1":
    answer2 = input("Please Enter the username to follow : ")
    answer3 = int(input(f"How many Followers do you need? (Available - {len(accounts)}): ").strip())

    print("Script Starting... ")


    for account in accounts[0:answer3]:
        try:
            username = account[0]
            password = account[1]
            CHALLENGE_EMAIL = account[2]
            CHALLENGE_PASSWORD = account[3]
            cl = Client()
            userId = cl.user_id_from_username(answer2)
            cl.challenge_code_handler = challenge_code_handler
            cl.change_password_handler = change_password_handler
            print(f"Logging into - {username}")
            cl.login(username, password)
            timer(random.randint(20, 30))
            cl.user_follow(userId)
            print(f"{username} Followed {answer2}")
            timer(random.randint(25, 35))
            print(f"Logging out from - {username}")
            cl.logout()
            timer(random.randint(10, 30))

        except Exception as e:

            print(e)
            print(username + " - Invalid Account")



elif answer1 == "2":
    answer5 = input("Please Enter the account to comment on : ")
    answer6 = input("Please Enter the account to mention the users from : ")
    answer7 = input("Please Enter a custom message if you have one. Otherwise press enter : ")
    answer9 = int(input("Please Enter how many posts you want to comment on : "))

    cl = Client()

    account = random.choice(accounts)
    username = account[0]
    password = account[1]
    print("Logging in...")
    cl.login(username, password)
    print("Logged in")
    timer(random.randint(10, 20))
    print("Requesting User Media...")
    userId = cl.user_id_from_username(answer5)
    posts = cl.user_medias(userId, answer9)
    print("Received User Media")
    timer(random.randint(10, 20))
    print("Request User Followers...")
    userId = cl.user_id_from_username(answer6)
    mentions = cl.user_followers_v1(userId, 50)
    print("Received User Followers")
    timer(random.randint(10, 20))
    cl.logout()
    timer(random.randint(10, 20))

    for post in posts:
        account = random.choice(accounts)
        accounts.remove(account)
        username = account[0]
        password = account[1]
        CHALLENGE_EMAIL = account[2]
        CHALLENGE_PASSWORD = account[3]
        cl = Client()
        print("Logging in...")
        timer(random.randint(10, 25))
        cl.login(username, password)
        print("Logged in")
        timer(random.randint(10, 25))
        for mention in mentions:
            try:
                mention = random.choice(mentions)
                mentions.remove(mention)
                print(f"Commenting...")
                cl.media_comment(post.id, f"{answer7} @{mention.username}")
                timer(random.randint(10, 25))
                print("Comment Posted")
                break
            except Exception as e:
                print(e)
                print("trying again...")
                timer(random.randint(10, 25))
        else:
            print("No Public Accounts found to mention")
            break
        cl.logout()
        timer(random.randint(10, 25))


elif answer1 == "3":
    answer8 = input("Please Enter the post URL : ")
    answer10 = int(input("How many comments do you want to post? : "))
    answer11 = input("Please Enter the account to mention the users from : ")
    answer7 = input("Please Enter a custom message if you have one. Otherwise press enter : ")

    cl = Client()
    account = random.choice(accounts)
    username = account[0]
    password = account[1]
    print("Logging in...")
    cl.login(username, password)
    print("Logged in Successfully")
    timer(random.randint(10, 20))
    print("Requesting media id...")
    pk = cl.media_pk_from_url(answer8)
    post = cl.media_id(pk)
    print("Media id received")
    timer(random.randint(10, 20))
    userId = cl.user_id_from_username(answer11)
    mentions = cl.user_followers_v1(userId, 50)
    cl.logout()
    for account in accounts[:answer10]:
        username = account[0]
        password = account[1]
        CHALLENGE_EMAIL = account[2]
        CHALLENGE_PASSWORD = account[3]
        cl = Client()
        timer(random.randint(10,25))
        print("Logging in...")
        cl.login(username, password)
        print("Logged in Successfully")
        timer(random.randint(10, 25))

        for mention in mentions:
            try:
                mention = random.choice(mentions)
                mentions.remove(mention)
                print(f"Commenting with {mention.username} mentioned...")
                cl.media_comment(post, f"{answer7} @{mention.username}")
                print("Comment Posted.")
                timer(random.randint(10, 25))
                break
            except Exception as e:
                print(e)
                print("trying again...")
                timer(random.randint(10, 25))
        else:
            print("No Public Accounts found to mention")
            break
        print("Logging Out...")
        cl.logout()
        print("Logged Out")
        timer(random.randint(10, 25))
