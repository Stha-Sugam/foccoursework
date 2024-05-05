def openfile():
    file = open("land.txt","r")
    return file

def readfile():
    file = openfile()
    landlist = []
    for line in file:
        line = line.replace("\n","")
        line = line.split(",")
        landlist.append(line);
    file.close()

    return landlist
