# register

# login
import random
import database
import getpass


def initial():
    validity = False
    print("welcome to Dansu microfinance bank")

    while validity == False:
        haveAccount = input("do you have an account with us? \n if yes, press 1 \n if no, press 2 to create an instant account: \n")
        try:
            haveAccount = int(haveAccount)
            if (haveAccount == 1):
                validity = True
                login()
            elif (haveAccount == 2):
                validity = True
                register()
            else:
                print("You have selected an invalid option, please try again")
        except:
            print("Please enter an integer only")


def register():
    print("Welcome to the registration portal,please input the right details")
    email = input("Enter your email address \n (0 to cancel): \n")
    try:
        if int(email) == 0:
            print("registration cancelled!!!")
            initial()
    except:
        if database.does_email_exist(email) is True:
            print("email already exist, please try another one")
            register()
        else:
            First_name = input("what is your first name: \n")
            last_name = input("What is your last name: \n")
            state = False
            while state == False:
                password = input("Please create password: \n")
                confirm_password = input("Please confirm your password: \n")
                if confirm_password == password:
                    acc = generateAccountNumber()
                    if database.does_acc_exist(acc) is True:
                        print("Technical error with account creation, please try again")
                        register()
                        state= True
                    else:
                        database.create(acc, [First_name, last_name, email, password, 0])
                        print("Congratulations, your account has been succesfully created, \n your account number is %s, please save this and log in to continue" % acc)
                        login()
                        state= True
                else:
                    print("Password does not match! \n try again")
def login():
    print("log in to your account")
    loginvalidity = False
    while loginvalidity == False:
        acc = input("Enter your account number: \n")
        if account_validation(acc) is True:
            if database.does_acc_exist(acc) is True:
                user_password = input("Enter your password: \n")
                if database.login_auth(acc, user_password):
                    print("login succesful")
                    loginvalidity = True
                    bankoperation(acc)
                else:
                    print("incorrect password, please try again")
                    loginvalidity = False
            else:
                print("account number not found, please try again")
                loginvalidity = False
        else:
            loginvalidity == False


def bankoperation(acc):
    details = database.read(acc)
    first_name = details.split()[0]
    first_name = first_name[2:-2]
    second_name = details.split()[1]
    second_name = second_name[1:-2]
    print("Welcome %s %s" % (first_name, second_name))
    validation = False
    while validation == False:
        activity = input("What will you like to do? : \n 1 to withdraw \n 2 to deposit \n 3 to Check your balance \n 4 to logout  \n")
        try:
            activity = int(activity)
            if activity == 1:
                withdrawaloperation(acc)
                validation = True
            elif activity == 2:
                validation = True
                depositoperation(acc)
            elif activity == 3:
                check_balance(acc)
            elif activity == 4:
                validation = True
                initial()
            else:
                print("invalid option selected")
                print("select right option")
                validation = False
        except:
            print("Enter an integer only")


def depositoperation(acc):
    verification = False
    a = database.read(acc)
    balance = a.split()[4]
    balance = int(balance[:-1])
    while verification == False:
        amount = input("Please enter amount in digit \n 0 to cancel: \n")
        try:
            amount = int(amount)
            if amount == 0:
                print("Transaction cancelled")
                verification = True
                bankoperation(acc)
            else:
                print("deposit succesful")
                updated_balance = str(balance + amount)
                database.update(acc,updated_balance)
                stat = False
                while stat == False:
                    next_op = input(
                        "Do you want to perform another operation? \n 1 yes and continue \n 2 no and logout \n")
                    try:
                        next_op = int(next_op)
                        if int(next_op) == 1:
                            stat == True
                            verification = True
                            bankoperation(acc)
                        elif int(next_op) == 2:
                            print('Thank you for choosing Dansu Bank')
                            stat == True
                            verification = True
                            initial()
                        else:
                            print("invalid input, try again")
                    except:
                        print("Enter an integer only")
        except:
            print("Enter an integer only")


def withdrawaloperation(acc):
    a = database.read(acc)
    balance = a.split()[4]
    balance = int(balance[:-1])
    verification = False
    while verification == False:
        amount = input("Please enter amount in digit \n 0 to cancel: \n")
        try:
            amount = int(amount)
            if amount == 0:
                print("Transaction cancelled")
                verification = True
                bankoperation(acc)
            elif amount > int(balance):
                print("Insufficient Funds, try again")
                verification = True
                withdrawaloperation(acc)
            else:
                print("withdrawal succesful")
                print("Please take your cash")
                updated_balance = str(int(balance) - amount)
                database.update(acc, updated_balance)
                verification == True
                stat = False
                while stat == False:
                    next_op = input(
                        "Do you want to perform another operation? \n 1 yes and continue \n 2 no and logout \n")
                    try:
                        next_op = int(next_op)
                        if next_op == 1:
                            stat == True
                            bankoperation(acc)
                        elif next_op == 2:
                            print('Thank you for choosing Dansu Bank')
                            initial()
                            stat == True
                        else:
                            print("invalid input, try again")
                    except:
                        print("Enter an integer only")
                        stat = False
        except:
            print("Enter an integer only")
        verification = False


def check_balance(acc):
    a = database.read(acc)
    balance = a.split()[4]
    balance = int(balance[:-1])
    first_name = a.split()[0]
    first_name = first_name[2:-2]
    second_name = a.split()[1]
    second_name = second_name[1:-2]
    print("Dear %s %s your account balance is %s" % (first_name, second_name, balance))
    stat = False
    while stat == False:
        next_op = input("Do you want to perform another operation? \n 1 yes and continue \n 2 no and logout \n")
        try:
            next_op = int(next_op)
            if next_op == 1:
                stat = True
                bankoperation(acc)
            elif next_op == 2:
                print('Thank you for choosing Dansu Bank')
                initial()
                stat = True
            else:
                print("invalid input, try again")
                stat = False
        except:
            print("Enter an integer only")
            stat = False


def account_validation(acc):
    # check if account is 10 digit
    # check if account is integer
    try:
        int(acc)
        if len(str(acc)) != 10:
            print("Account number must be 10 digits long")
            return False
        else:
            return True
    except:
        print("Account number must be integers only")


def generateAccountNumber():
    return random.randrange(1111111111, 9999999999)


initial()
###Banking system
