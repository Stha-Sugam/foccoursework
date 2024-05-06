import datetime

import read
import write
import messages

def listoflands():
    list = read.readfile()
    return list

def displayLands():
    print("\n-------------------------------------------------------------------------------\nKitta\tLocation\tSide\tanna\tprice\tmonth\tAvailability status\n-------------------------------------------------------------------------------\n");
    landlist = listoflands()
    for i in range(len(landlist)):
        for j in range(len(landlist[i])):
            print(landlist[i][j], end="\t")
        print("\n")
    print("-------------------------------------------------------------------------------")

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

def rentprintstatement(kittanum,month,totalamount,grandtotal):
    landlist = listoflands()

    for line in landlist:
        if int(kittanum) == int(line[0]):
            print("\n-----------------------------------\nKitta number :", line[0])
            print("Location:", line[1])
            print("Side faced:", line[2])
            print("Anna:", line[3])
            print("Price per Month:", line[4])
            print("Months for land rented:", str(month) + "\n")
            print("Total amount:", str(totalamount) + "\n-----------------------------------") 
            print("\n-------------------------\nGrand Total:", str(grandtotal),"\n-------------------------")

def returnprintstatement(kittanum, month, rentamount, returnmonth, totalamount, grandtotal, state):
    landlist = listoflands()

    for line in landlist:
        if int(kittanum) == int(line[0]):
            print("\n-----------------------------------\nKitta num:", line[0])
            print("Location:", line[1])
            print("Side faced:", line[2])
            print("Anna:", line[3])
            print("Price per Month:", line[4])
            print("Months(Rented):", str(month))
            print("Price for land rented: ", str(rentamount) + "\n-----------------------------------")
            print("\n-----------------------------------\nMonths(Returned):",returnmonth)
            if state == "high":
                print(str(rentamount)+" + '10%' fine") 
            print("Total amount:", str(totalamount) + "\n-----------------------------------")
            
            print("\n------------------------\nGrand Total:", str(grandtotal),"\n------------------------")
            

def rentLand():
    landlist = listoflands()
    rentmore = True
    correctname = False
    while not correctname:
        name = str(input("Enter your full name: "))
        if name == "":
            print("Don't leave this field empty")
        elif not name.replace(" ","").isalpha():
            print("Please Input your name here")
        else:
            correctname = True
    uniqueId(name)
    rentedlist = []
    grandTotal = 0

    while rentmore == True:
        print("\n------------------------------\nYou are now renting lands\n------------------------------")
        displayLands()
        rentkitta = input("Enter the kitta number of the land you want to rent: ")
        rentstatus = availabilityStatus(rentkitta)
        pricepermonth = landPrice(rentkitta)
        if rentstatus == "Available":
            rentcontd = True
            while rentcontd:
                try:
                    rentmonths = int(input("Enter the number of months for renting this land: "))
                    if rentmonths == "":
                        print("Cannot leave this field empty")
                    else:
                        totalamount = int(rentmonths) * int(pricepermonth)
                        landlist = listoflands() 
                        for line in landlist:
                            if int(rentkitta) == int(line[0]):
                                rentedlist.append([rentkitta, int(rentmonths), pricepermonth, totalamount, grandTotal])
                                grandTotal += totalamount
                                rentprintstatement(rentkitta, int(rentmonths), totalamount, grandTotal)
                        write.updaterentmonths(rentkitta, int(rentmonths))
                        write.updateAvailability(rentkitta, rentstatus)
                    rentcontd = False
                except:
                    print("Month not Valid")
                    rentcontd = True
            
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
    correctname = False
    while not correctname:
        name = str(input("Enter your full name: "))
        if name == "":
            print("Don't leave this field empty")
        elif not name.replace(" ","").isalpha():
            print("Please Input your name here")
        else:
            correctname = True
    uniqueId(name)
    returnedlist = []
    grandtotal = 0
    
    while returnmore == True:
        print("\n------------------------------\nYou are now returning lands\n------------------------------")
        displayLands()
        returnkitta = input("Enter the kitta number of the land you want to return: ")
        returnstatus = availabilityStatus(returnkitta)
        pricepermonth = landPrice(returnkitta)
        if returnstatus == "Not Available":
            
            for line in returnlandlist:
                rentmonth = line[-2]
                if returnkitta == line[0]:
                    returncontd = True
                    while returncontd:
                        try:
                            returnmonth = int(input("Enter the number of months you have rented this land: "))
                            if int(returnmonth) == int(rentmonth):
                                rentedamount = int(pricepermonth) * int(rentmonth)
                                totalamount = int(pricepermonth) * int(returnmonth)
                                grandtotal += totalamount
                                state = "equal"
                            elif int(returnmonth) > int(rentmonth):
                                rentedamount = int(pricepermonth) * int(rentmonth)
                                totalamount = rentedamount + (rentedamount * 0.1)
                                grandtotal += totalamount
                                state = "high"
                            elif int(returnmonth) < int(rentmonth):
                                rentedamount = int(pricepermonth) * int(rentmonth)
                                totalamount = int(pricepermonth) * int(returnmonth)
                                grandtotal += totalamount
                                state = "low"
                            else:
                                print("Invalid Month Input")
                            returnprintstatement(returnkitta, rentmonth, rentedamount, returnmonth, totalamount, grandtotal, state)
                            returnedlist.append([returnkitta, rentmonth, pricepermonth, rentedamount, returnmonth, totalamount, grandtotal, state])
                            write.updatereturnmonths(returnkitta)
                            write.updateAvailability(returnkitta, returnstatus)
                            returncontd = False
                        except:
                            print("Month not Valid")
                            returncontd = True
            
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
    write.bill(name, returnedlist)

def mainLoop():
    contd = True
    exitSystem = False
    while exitSystem == False:
        try:
            messages.choose()
            inputval = int(input("Enter the value: "))
            if inputval == 1:
                rentLand()
            elif inputval == 2:
                returnLand()
            elif inputval == 3:
                messages.thankmsg()
                exitSystem= True
            else:
                print("wrong inut")
            contd = False
        except:
            print("Invalid Input")
            contd = True
