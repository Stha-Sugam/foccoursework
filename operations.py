import datetime

import read
import write
import messages

def listoflands():
    list = read.readfile()
    return list

def displayLands():
    print("\n--------------------------------------------------------------------\nKitta\tLocation\tSide\tanna\tprice\tmonth\tavailability status\n---------------------------------------------------------------------\n");
    landlist = read.readfile()
    for i in range(len(landlist)):
        for j in range(len(landlist[i])):
            print(landlist[i][j], end="\t")
        print("\n")
    print("---------------------------------------------------------------------")

def availabilityStatus(kittanumber):
    landlist = listoflands()
    for line in landlist:
        if kittanumber == line[0]:
            status = line[-1]
            break
        else:
            status = "Invalid"
    return status

def landPrice(kittanumber):
    landlist = listoflands()
    for line in landlist:
        if kittanumber == line[0]:
            price = line[4]
            break
        else:
            price = "0"
    return price

def uniqueId(name):
    minute = str(datetime.datetime.now().minute)
    second = str(datetime.datetime.now().second)
    microsecond = str(datetime.datetime.now().microsecond)

    random = minute + second + microsecond
    filename = name+str(random)
    
    return filename

def printstatement(kittanum,month,totalamount,grandtotal):
    landlist = listoflands()

    for line in landlist:
        if int(kittanum) == int(line[0]):
            print("\n-------------------------\nKitta num:", line[0])
            print("Location:", line[1])
            print("Side faced:", line[2])
            print("Anna:", line[3])
            print("Price:", line[4])
            print("Months for land rented:", str(month) + "\n")
            print("Total amount:", str(totalamount) + "\n-------------------------") 
            print("\n--------------------\nGrand Total:", str(grandtotal),"\n--------------------")

def rentLand():
    landlist = listoflands()
    rentmore = True
    name = input("Enter your full name: ")
    uniqueId(name)
    rentedlist = []
    grandTotal = 0

    while rentmore == True:
        print("\n------------------------------\nYou are now renting lands\n------------------------------")
        displayLands()
        rentkitta = input("Enter the kitta number of the land you want to rent: ")
        rentstatus = availabilityStatus(rentkitta)
        price = landPrice(rentkitta)
        if rentstatus == "Available":
            rentmonths = int(input("Enter the number of months for renting this land: "))
            totalamount = rentmonths * int(price)
            landlist = listoflands() 
            for line in landlist:
                if int(rentkitta) == int(line[0]):
                    rentedlist.append([rentkitta, rentmonths, price, totalamount])
                    grandTotal += totalamount
                    printstatement(rentkitta, rentmonths, totalamount, grandTotal)
                    
            write.updaterentmonths(rentkitta, rentmonths)
            write.updateAvailability(rentkitta, rentstatus)
            
        elif rentstatus == "Not Available":
            print("Sorry, the land you are looking for is not available.")
        elif rentstatus == "Invalid":
            print("Invalid Kitta number")
        
        rentValid = False
        rentAnother = input("Enter 'y' to rent more land or 'n' to stop renting: ").lower()
        while rentValid == False:
            if rentAnother == "n":
                rentmore = False
                rentValid = True
            elif rentAnother == "y":
                rentmore = True
                rentValid = True
            else:
                print("Please provide valid input")
                rentValid = False
                rentAnother = input("Enter 'y' to rent more land or 'n' to stop renting: ").lower()
    write.invoice(name, rentedlist)
    

def returnLand():
    returnlandlist = listoflands()
    returnmore = True
    name = input("Enter your full name: ")
    uniqueId(name)
    returnedlist = []
    
    while returnmore == True:
        print("\n------------------------------\nYou are now returning lands\n------------------------------")
        displayLands()
        returnkitta = input("Enter the kitta number of the land you want to return: ")
        returnstatus = availabilityStatus(returnkitta)
        price = landPrice(returnkitta)
        totalamount = 0
        if returnstatus == "Not Available":
            returnmonth = input("Enter the number of months you have rented this land: ")
            for line in returnlandlist:
                rentmonth = line[-2]
                if returnkitta == line[0]:
                    if int(returnmonth) == int(rentmonth):
                        print("Kitta number: "+ str(line[0]))
                        print("Location:", line[1])

                        print("Anna:", line[3])
                        print("Price: "+ str(line[4]))
                        print("Months for rented: "+str(line[5]))
                        tamount = int(rentmonth) * int(price)
                        print("Total amount: "+str(tamount))
                        amount = int(price) * int(returnmonth)
                        print("\n------------------------------\nYou have to pay: Rs." + str(amount)+"\n------------------------------\n")
                    elif int(returnmonth) > int(rentmonth):
                        amount = int(price) * int(returnmonth)
                        print("You have to pay " + str(amount))
                    elif int(returnmonth) < int(rentmonth):
                        amount = int(price) * int(returnmonth)
                        print("You have to pay " + str(amount))
                    totalamount += amount
                    print("\n----------------------------------------\nYour total amount to be paid is: "+totalamount+"----------------------------------------\n")
                    returnedlist.append([returnkitta, returnmonth, amount, price])
            write.updatereturnmonths(returnkitta)
            write.updateAvailability(returnkitta, returnstatus)
        elif returnstatus == "Available":
            print("The land cannot be returned as not rented")
        elif returnstatus == "Invalid":
            print("Invalid Kitta Number !!")

        returnvalid = False
        returnAnother = input("Enter 'y' to return more lands or 'n' to stop returning: ").lower()
        while returnvalid == False:
            if returnAnother == "n":
                returnmore = False
                returnvalid = True
            elif returnAnother == "y":
                returnmore = True
                returnvalid = True
            else:
                print("Please provide valid input")
                returnvalid = False
                returnAnother = input("Enter 'y' to return more lands or 'n' to stop returning: ").lower()
    write.bill(name, returnedlist, totalamount)

def mainLoop():
    exitSystem = False
    while exitSystem == False:
        print("\nEnter 'rent' to rent the land,\nEnter 'return' to return the land,\nEnter 'exit' to exit the system")
        inputval = input("Enter the value: ").lower()
        if inputval == "rent":
            rentLand()
        elif inputval == "return":
            returnLand()
        elif inputval == "exit":
            messages.thankmsg()
            exitSystem= True
        else:
            print("Wrong Input, enter the value again.")