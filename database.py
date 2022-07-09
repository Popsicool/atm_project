import os

user_db_path = "data/user_record/"


def create(account_number: object, user_details: object) -> object:
    state = False
    try:
        f = open(user_db_path + str(account_number) + ".txt", "a")
        f.write(str(user_details))
        state = True
    except:
        print("user already exist")
        # delete already created record
        # delete(account_number)
    finally:
        return state
        f.close()

def does_email_exist(email):
    all_users = os.listdir(user_db_path)
    for user in all_users:
        user = open(user_db_path + user, "r")
        user= user.readline()
        user= user.split(",")[2]
        user= user[2:-1]
        if user== email:
            return True
def does_acc_exist(acc):
    all_users = os.listdir(user_db_path)
    for user in all_users:
        user = user.split()[0]
        user =user[0:-4]
        if user == acc:
            return True



def read(user_account_number):
    try:
        f = open(user_db_path + str(user_account_number) + ".txt", "r")
        return f.readline()
    except:
        print("user not found")


def update(acc, updated_balance):
    a= read(acc)
    balance = a.split()[4]
    balance = balance[:-1]
    a= a.replace(balance, updated_balance)
    f = open(user_db_path + str(acc) + ".txt", "w")
    f.write(a)
    f.close()



def delete(user_account_number):
    is_delete_successful = False
    try:
        os.remove(user_db_path + str(user_account_number) + ".txt")
        is_delete_successful = True
    except:
        print("user not found")
    finally:
        return is_delete_successful
def login_auth(acc, password):
    a= read(acc)
    saved_pass = a.split()[3]
    saved_pass= saved_pass[1:-2]
    if saved_pass == password:
        return True