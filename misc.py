import datetime
import os

#return [int day, int month, int year]
def todaysDate():
    now = datetime.datetime.now()
    return [now.day, now.month, now.year]

def fileopen(filename):
    msg = list()
    if os.path.isfile(filename):
        if os.stat(filename).st_size > 0:
            with open(filename, "rb") as doc:
                msg = doc.read()
        else:
            sys.exit("\n\nThe file %s is empty!!!\n\n" %filename)
    else:
        open(filename, "wb").close()
        sys.exit("\n\n%s doesn't exist, it has now been created!!!\n\n" %filename)

    return msg

def enterint(text):
    while True:
        number = raw_input(text)
        if number == "":
            return number
        try:
            number = int(number)
            return number
        except ValueError:
            print "\n\nInvalid input, try again\n\n"

def makefolder(flst):
    for folder in flst:
        if not os.path.exists(folder):
            os.makedirs(folder)

def tlstcreator():
    targetlist = []
    choice1 = ""
    while choice1 not in (["n"]):
        tlst = []
        url1 = raw_input("Paste the url here: ")

        start1 = enterint("\nEnter pagenumber to start on: ")
        if not start1 == "":
            if "?page=" in url1:
                url1 = url1[0: url1.index("?page=")]
            stop1 = enterint("\nEnter pagenumber to end on: ")

            url1 = "%s?page=" %url1
            for x in range(start1, stop1 + 1):
                tlst.append(url1 + str(x))

        else:
            tlst = [url1]
        targetlist.append(tlst)

        choice1 = ""
        while choice1 not in (["y", "n"]):
            choice1 = raw_input("\nDo you wish to process any additional targets? (y/n): ")
    return targetlist
