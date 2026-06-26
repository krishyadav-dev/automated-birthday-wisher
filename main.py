##################### Extra Hard Starting Project ######################
import os
from random import choice
import smtplib
import datetime as dt
import pandas
PLACEHOLDER = "[NAME]"

##################### CREDENTIALS #####################################
MY_EMAIL = os.environ.get("MY_EMAIL")
MY_PASSWORD = os.environ.get("MY_PASSWORD")

# 1. Update the birthdays.csv
with open("letter_templates/letter_1.txt", mode="r") as letter:
    letter1 = letter.read()
with open("letter_templates/letter_2.txt", mode="r") as letter:
    letter2 = letter.read()
with open("letter_templates/letter_3.txt", mode="r") as letter:
    letter3 = letter.read()
letters = [letter1, letter2, letter3]
birthday_frame = pandas.read_csv("birthdays.csv")

# 2. Check if today matches a birthday in the birthdays.csv
today = dt.datetime.now()
day = today.day
month = today.month
matching_rows = birthday_frame[(birthday_frame.day == day) & (birthday_frame.month == month)]

if not matching_rows.empty:
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=MY_PASSWORD)
        print("Connected")
        # 3. If step 2 is true, pick a random letter from letter templates and replace the [NAME] with the person's actual name from birthdays.csv
        for index, row in matching_rows.iterrows():
            letter = choice(letters)
            person_name = row["name"]
            person_email = row["email"]
            letter = letter.replace(PLACEHOLDER, person_name)

            # 4. Send the letter generated in step 3 to that person's email address.
            connection.sendmail(MY_EMAIL, person_email,
                                f"Subject:Happy Birthday!"
                                f"\n\n{letter}")
            print(f"Sent to {person_name}")

print("Done")

