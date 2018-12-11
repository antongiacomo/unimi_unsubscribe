import json
import os
from pprint import pprint
from smtplib import SMTP_SSL
from tqdm import tqdm
from time import sleep


def unsubscribe(user: str, password: str, server: str="smtp.unimi.it", sympa_mail: str="sympa@liste.unimi.it", port: int=465, timeout: int= 5):
    """Method to unsubscribe from given sympa service.
        user: str, Your user name in the server, usually follows a format such as name.surname@studenti.unimi.it
        password: str, Your account password. We use SSL.
        server: str="smtp.unimi.it", Your SSL SMTP server account
        sympa_mail: str="sympa@liste.unimi.it", The address to which to send the unsubscribe mails.
        port: int=465, The SSL server port
        timeout: int= 5, timeout to be waited beetween mails.
    """
    server_ssl = SMTP_SSL(server, port)
    server_ssl.login(user, password)
    spam_path = "{dir}/spam_list.json".format(
        dir=os.path.dirname(os.path.realpath(__file__))
    )
    with open(spam_path, "r", encoding='utf-8') as f:
        spam_lists = json.load(f)
    print("Proceeding to unsubscribe from the following lists:")
    pprint(spam_lists)
    print(
        "To avoid being flagged as spam, a timeout of {timeout} seconds will be waited beetween each mail.".format(timeout=timeout))
    print("If you'd like to customize said timeout, you can pass an optional parameter `timeout` when calling `unsubscribe`.")
    sure = input("Proceed? [y/n] ")
    if sure != "y":
        print("Entered {sure}, aborting.".format(sure=sure))
        return
    for spam_list in tqdm(spam_lists):
        server_ssl.sendmail(user, sympa_mail, "From: {you}\nTo: {spam}\nSubject: {spam_list}\n\n".format(
            you=user,
            spam=sympa_mail,
            spam_list=spam_list
        ))
        sleep(timeout)
    server_ssl.close()
    print("All done.")
