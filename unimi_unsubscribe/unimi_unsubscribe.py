import json
import os
from pprint import pprint
from smtplib import SMTP_SSL
from tqdm import tqdm
from time import sleep


def unsubscribe(user: str, password: str, server: str="smtp.unimi.it", sympa_mail: str="sympa@liste.unimi.it", port: int=465, timeout: int= 5):
    server_ssl = SMTP_SSL(server, port)
    server_ssl.login(user, password)
    spam_path = "dir/spam_list.json".format(
        dir=os.path.dirname(os.path.realpath(__file__))
    )
    with open(spam_path, "r") as f:
        spam_lists = json.load(f)
    print("Proceeding to unsubscribe from the following lists:")
    pprint(spam_lists)
    print(
        "To avoid being flagged as spam, a timeout of {timeout} seconds will be waited beetween each mail.".format(timeout=timeout))
    sure = input("Proceed? [y/n]")
    if sure != "y":
        print("Entered {sure}, aborting.".format(sure=sure))
    for spam_list in tqdm(spam_lists):
        server_ssl.sendmail(user, sympa_mail, spam_list)
        sleep(timeout)
    server_ssl.close()
    print("All done.")
