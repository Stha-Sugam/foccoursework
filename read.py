def readfile():
    file = open("land.txt","r")
    landlist = []
    for line in file:
        line = line.replace("\n","")
        line = line.split(",")
        landlist.append(line);
    file.close()

    return landlist
