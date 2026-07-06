import string
import random
from pathlib import Path
import json # loads for reading data in json file and dumps for writing the data in json file.

class Bank:

    database = 'accountdata.json'
    dummy_data = []

    try: # To tackle any unknown error
        if Path(database).exists():

            with open(database, "r+") as f:
                content = f.read()
                dummy_data = json.loads(content)

        else:
            print("No such file exist")

    except Exception as error:
        print(f"An error occured as {error}.")

    @staticmethod
    def update():
        with open(Bank.database, "w") as f:
            f.write(json.dumps(Bank.dummy_data))

    @classmethod
    def __accountgenerator(cls):
        digits = random.choices(string.digits, k = 4)
        letters = random.choices(string.ascii_letters, k = 3)
        special_char = random.choices("!@#&*", k = 1)
        # To shuffle the order, we use:
        account_no = digits + letters + special_char
        random.shuffle(account_no) # it returns a list
        return "".join(account_no)
        
    def Create_Account(self):
        user_data = {
            "name": input("Enter your name :- "),
            "age": int(input("ENter your age :- ")),
            "email": input("Enter your email :- "),
            "pin": int(input("Enter your 4-digit pin :- ")),
            "Account_number": Bank.__accountgenerator(),
            "Account_balance": 0
        }
        if user_data['age'] < 18 or len(str(user_data['pin'])) != 4:
            print("Sorry! You can't create an Account.")

        if len(Bank.dummy_data) != 0:
                pin_list = [account['pin'] for account in Bank.dummy_data]
                if user_data['pin'] in pin_list:
                    print(f"Sorry! This pin already exists. Enter any other 4-digit pin")
                    Bank.Create_Account(self)
                
                else:
                    print("Your account has been created successfully!")
                    print("Your account details are:\n")
                    for i in user_data:
                        print(f"{i} : {user_data[i]}")
                    print("Kindly note down your PIN for future purposes.")

                    Bank.dummy_data.append(user_data)
                    Bank.update()

        else:
            print("Your account has been created successfully!")
            print("Your account details are:\n")
            for i in user_data:
                print(f"{i} : {user_data[i]}")
            print("Kindly note down your Account Number for future purposes.")

            Bank.dummy_data.append(user_data)

            Bank.update()
        
    def __wrong_pin(self):
        print("There's no such account exists.")
        confirm = input("Do you want to create your account or not? (Y/n) :- ")
        if confirm.lower() == 'y':
            Bank.Create_Account(self)
        else:
            print("Enter your pin again")
        
    def Deposit_Money(self):
        pin_check = int(input("Enter your 4-digit pin :- "))
        account = [account for account in Bank.dummy_data if pin_check == account['pin']]
        if len(account) == False:
            print("No such account exists.")
            Bank.__wrong_pin(self)
            Bank.Deposit_Money(self)
        else:
            if account[0]['pin'] == pin_check:
                print(f"Your current Account Balance is :- {account[0]['Account_balance']}")
                money_add = int(input("How much money do you want to add? :- "))
                pin_confirm = int(input("Enter you 4-digit pin to confirm :- "))
                if pin_confirm == pin_check:
                    account[0]['Account_balance'] += money_add
                    print("Money added to account successfully!")
                    Bank.update()

                else:
                    print('Wrong pin entered!')
                    Bank.Deposit_Money(self)
            
            else:
                Bank.__wrong_pin(self)
                Bank.Deposit_Money(self)

    def Withdraw_Money(self):
        pin_check = int(input("Enter you 4-digit pin :- "))
        account = [account for account in Bank.dummy_data if pin_check == account['pin']]
        if len(account) == False:
            print("No such account exists.")
            Bank.__wrong_pin(self)
            Bank.Withdraw_Money(self)
        else:
            if account[0]['pin'] == pin_check:
                print(f"Your current Account Balance is :- {account[0]['Account_balance']}")
                money_withdraw = int(input("How much money do you want to withdraw? :- "))
                if money_withdraw <=  account[0]['Account_balance'] and money_withdraw > 0:
                    pin_confirm = int(input("Enter you 4-digit pin to confirm :- "))
                    if pin_confirm == pin_check:
                        account[0]['Account_balance'] -= money_withdraw
                        print("Money withdrawn successfully!")

                        Bank.update()

                    else:
                        print("Wrong pin entered")
                        Bank.Withdraw_Money(self)

                else:
                    print("You don't have that much balance in your account.\nEnter the amount again.")
                    Bank.Withdraw_Money(self)

            else:
                Bank.__wrong_pin(self)
                Bank.Withdraw_Money(self)
            
    def Account_Details(self):
        pin_check = int(input("Enter your 4-digit pin :- "))
        account = [account for account in Bank.dummy_data if pin_check == account['pin']]
        if len(account) == False:
            print("No such account exists.")
            Bank.__wrong_pin(self)
            Bank.Account_Details(self)
        else:
            if account[0]['pin'] == pin_check:
                print("\nYour account details are:")
                for i in account[0]:
                    print(f"{i} : {account[0][i]}")
                
            else:
                Bank.__wrong_pin(self)
                Bank.Account_Details(self)

    def Update_Details(self):
        pin_check = int(input("Enter your 4-digit pin :- "))
        account = [account for account in Bank.dummy_data if pin_check == account['pin']]
        if len(account) == False:
            print("No such account exists.")
            Bank.__wrong_pin(self)
            Bank.Update_Details(self)
        else:
            if account[0]['pin'] == pin_check:
                print("\nYour account details are:")
                for i in account[0]:
                    print(f"{i} : {account[0][i]}")

                print("\nNOTE :- You cannot change your AGE and your ACCOUNT NUMBER\n")
                update_choice = input("Which detail you want to update? (name / email / pin):- ")
                try:
                    if update_choice.lower() == 'name':
                        updated_name = input("Enter your new name :- ")
                        account[0]['name'] = updated_name
                        print("Name updated successfully!")

                    if update_choice.lower() == 'email':
                        updated_email = input("Enter your new email :- ")
                        account[0]['email'] = updated_email
                        print("Email updated successfully!")

                    if update_choice.lower() == 'pin':
                        updated_pin = int(input("Enter your new pin :- "))
                        account[0]['pin'] = updated_pin
                        print("Pin updated successfully!")

                    Bank.update()
                        
                except:
                    print("Sorry! An error occured as you can only update your (name / email / pin).")
                    Bank.Update_Details(self)
                
            else:
                Bank.__wrong_pin(self)
                Bank.Account_Details(self)

    def Delete_Account(self):
        pin_check = int(input("Enter your 4-digit pin :- "))
        account = [account for account in Bank.dummy_data if pin_check == account['pin']]
        if len(account) == False:
            print("No such account exists.")
            Bank.__wrong_pin(self)
            Bank.Delete_Account(self)
        else:
            if account[0]['pin'] == pin_check:
                print("\nYour account details are:")
                for detail in account[0]:
                    print(f"{detail} : {account[0][detail]}")
                print("\nNOTE :- Do you want to delete your account") 
                confirm = input("Please confirm (y/n) :- ")
                if confirm.lower() == 'y' or confirm.lower() == 'yes':
                    Bank.dummy_data.remove(account[0])
                    print("Account Deleted!")

                    Bank.update()
                    
                else:
                    print("No changes have been made to your account!")

            else:            
                Bank.Delete_Account(self)

print("\n-------------------- WELCOME TO THE BANK OPERATING SYSTEM --------------------\n")

while True:
    user = Bank()
    print("\nWhat task do you want to perform?\n1. Create an Account\n2. Money Deposit into the Account." \
    "\n3. Withdrawing the money\n4. Bank Acccount Details\n5. Update the details\n6. Delete your account")

    try: 
        check = int(input("Enter your response: "))

        if check == 1:
            user.Create_Account()

        elif check == 2:
            user.Deposit_Money()

        elif check == 3:
            user.Withdraw_Money()

        elif check == 4:
            user.Account_Details()

        elif check == 5:
            user.Update_Details()

        elif check == 6:
            user.Delete_Account()

        more_task = input("Do you want to LOG OUT? (y/n) :- ")
        if more_task.lower() in ['y', 'yes']:
            print("\nThankyou. Hope you liked it!\n")
            break

    except Exception as error:

        print(f"Sorry! An error occured as {error}")
        break