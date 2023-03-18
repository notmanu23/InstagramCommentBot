import time
import names
import random
from instagrapi import Client
from instagrapi.exceptions import LoginRequired
import sys
import requests
import os


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
        random.shuffle(lst)
        return lst


def changeAcc(client, account):
    try:
        print(f"Setting Profile Picture for {ig_username}...")
        timer(random.randint(10, 20))
        client.account_change_picture("image_name.jpg")

        print("Profile Picture Set.")

        images = os.listdir("images")
        random.shuffle(images)

        for image in images:
            print(f"Uploading {image}")
            timer(random.randint(10, 20))
            try:
                media = client.photo_upload(
                    f"images/{image}",
                    "Caption"
                )
                print(media)
            except Exception as e:
                print("Login Required")
                client = Client()
                client.login(account[0], account[1])
                print("Logged in")
            timer(random.randint(10, 20))

        print("Uploading Media Done...")
    except Exception as e:
        print(e)


def follow(client, user_account):
    print("Following Accounts")
    accounts = read_users("accounts.txt")
    for account in accounts[:random.randint(10, len(accounts))]:
        try:
            timer(random.randint(10, 20))
            try:
                print("Requesting User ID for the Account")
                id = client.user_id_from_username(account[0])
                print(f"Following {account[0]}")
                timer(random.randint(10, 20))
            except:
                continue
            client.user_follow(id)
            print(f"Followed {account[0]}")
        except Exception as e:
            client = Client()
            print("Login Required")
            client.login(user_account[0], user_account[1])
            print("Logged in")



def timer(count):
    for remaining in range(count, 0, -1):
        sys.stdout.write("\r")
        sys.stdout.write("{:2d} seconds remaining.".format(remaining))
        sys.stdout.flush()
        time.sleep(1)

    sys.stdout.write("\rComplete!            \n")
    print("")


for account in read_users("accounts.txt"):
    print(account[0])
    ig_username = account[0]
    ig_password = account[1]

    timer(random.randint(10,20))
# Initialize the instagrapi client
    client = Client()

    # Login to your Instagram account
    try:
        client.login(ig_username, ig_password)
    except LoginRequired as e:
        print("Could not login. Check your username and password.")
        exit()
    while True:
        # Search for a random Instagram account
        query = names.get_first_name()
        results = client.search_users(query) # Search for users with the query

        # Get a random username from the search results
        if len(results) > 0:
            username = random.choice(results).username
            print(f"Random Instagram account username: {username}")
            break
        else:
            print("No results found. Trying again")
    timer(random.randint(10,20))
    reference_id = client.user_id_from_username(username)
    reference_info = client.user_info(reference_id)
    print(reference_info)
    timer(random.randint(10,20))

    img_data = requests.get(reference_info.profile_pic_url_hd).content
    with open('image_name.jpg', 'wb') as handler:
        handler.write(img_data)

    client.account_set_private()
    timer(random.randint(10,30))
    client.logout()
    timer(random.randint(10,30))

    client = Client()
    timer(random.randint(10,30))

    client.login(ig_username, ig_password)
    timer(random.randint(10,30))

    follow(client, account)
    timer(random.randint(10,30))

    changeAcc(client, account)
    print("Setting Account Private...")
    timer(random.randint(10,20))
    print("Account Private.")
    timer(10)
    client.logout()

print("Done.")

