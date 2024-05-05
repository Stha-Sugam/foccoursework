import read
import operations

def updateAvailability(kittanum, status): 
    landlist = read.readfile()

    for line in landlist:
        if line[0] == kittanum:
            if status == "Available":
                line[-1] = "Not Available"
                break
            if status == "Not Available":
                line[-1] = "Available"
                break

    file = open("land.txt","w")
    for line in landlist:
        file.write(",".join(line) + "\n")
    
    file.close()

def updaterentmonths(kittanum, rentmonths):
    landlist = read.readfile()

    for line in landlist:
        if int(kittanum) == int(line[0]):
            line[-2] = str(rentmonths)

    file = open("land.txt", "w")
    for line in landlist:
        file.write(",".join(line)+"\n")
    
    file.close()
    
def updatereturnmonths(kittanum):
    landlist = read.readfile()

    for line in landlist:
        if line[0] == kittanum:
            line[-2] = "0"
            
    file = open("land.txt","w")
    for line in landlist:
        file.write(",".join(line)+"\n")
    
    file.close()


def invoice(name, rentedlist):
    nameoffile = operations.uniqueId(name) + ".txt"
    invoicefile = open(nameoffile, "w")

    invoicefile.write("---------------------------------------\n                INVOICE                \n---------------------------------------")
    invoicefile.write("\n-------------------------\n     Name: " + name + "\n-------------------------")
    
    totalamount = 0

    for land in rentedlist:
        invoicefile.write("\n---------------------")
        invoicefile.write("\nKitta number:" + str(land[0]))
        invoicefile.write("\nMonths for renting:" + str(land[1]))
        invoicefile.write("\nPrice:" + str(land[2]))
        invoicefile.write("\n---------------------\nTotal Price: " + str(land[3]) + "\n---------------------")
        
        totalamount += int(land[3])

    invoicefile.write("\n---------------------\nGrand Total: " + str(totalamount) + "\n---------------------")
    invoicefile.close()

def bill(name, returnedlist, totalamount):
    nameoffile = operations.uniqueId(name)+".txt"
    billfile = open(nameoffile,"w")

    billfile.write("----------------------------------------\n                  BILL                  \n----------------------------------------")
    billfile.write("\n-------------------------\n     Name: " + name + "\n-------------------------")

    totalamount = 0

    for land in returnedlist:
        billfile.write("\n---------------------")
        billfile.write("\nKitta number: " + str(land[0]))
        billfile.write("\nMonths for renting: " + str(land[1]))
        billfile.write("\nAmount: "+str(land[2]))
        billfile.write("\nPrice: " + str(land[3]))
