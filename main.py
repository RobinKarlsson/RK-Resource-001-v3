from os.path import isfile, join
from mecbrowser import *
from misc import *
from member import *

makefolder(["data", "config", "config/invites", "data/messages", "data/invite lists"])

def login(br, x = None):
    while x not in ["y", "n"]:
        x = raw_input("login? (y/n) ")

    if x == "y":
        username = raw_input("your username: ")
        password = raw_input("your password: ")
        meclogin(br, username, password)
        

def inviter(br, targetlist, endless = True):
    redo = True
    print targetlist

    while redo:
        if not endless:
            redo = False

        for target in targetlist:
            target = target[1]
            invgroup = target[0:-4]

            condic = loadconfig("config/invites/%s" %target)

            minrat = condic["Min online chess rating"]
            maxrat = condic["Max online chess rating"]

            joindate = condic["Member on chess.com for days"]
            if joindate:
                joindate = dateDaysAgo(joindate)

            groupID = condic["Group ID"]
            infile = condic["File containing the main invites list"]
            priofile = condic["File containing those who should receive priority invites (circumvents filter)"]
            leftfile = condic["Invites file for those who has left the group"]
            alrfile = condic["File containing those who has received an invite"]
            msglistleft = condic["File containing your invites message for members who has left your group"]
            msgliststand = condic["File containing your invites message for standard and priority invites lists"]
            notToInvite = condic["Comma seperated list of usernames that should not be invited"]
            if notToInvite:
                notToInvite = notToInvite.replace(" ", "").split(",")

            memalrinv = readMemFile(alrfile)
            usedfile = priofile
            memtinv = readMemFile(priofile)
            priolst = True
            deserterlst = False
            standardlst = False
            invfilter = False

            if len(memtinv) == 0:
                memtinv = readMemFile(leftfile)
                deserterlst = True
                priolst = False
                usedfile = leftfile

            if len(memtinv) == 0:
                memtinv = readMemFile(infile)
                usedfile = infile
                memtinv = [x for x in memtinv if x not in memalrinv]
                standardlst = True
                invfilter = True
                deserterlst = False

            if len(memtinv) == 0:
                print "\n\nWarning, empty invites list: %s" %infile
                continue

            if priolst or standardlst:
                msg = fileopen(msgliststand)
            elif deserterlst:
                msg = fileopen(msglistleft)

            invited = []
            for member in memtinv:
                if notToInvite:
                    if member in notToInvite:
                        memtinv.remove(member)
                        continue

                member = makeMember(br, member)

                if invfilter:
                    if not memberfilter(member, minonlinerat = minrat, maxonlinerat = maxrat, membersince = joindate):
                        print "%s didnt pass filter" %member.username
                        continue

                print "\nAttempting to invite '%s' to '%s'" %(member.username, invgroup)
                if not sendInvite(br, groupID, member, msg):
                    print "No invites available, continuing to next group"
                    break

                invited.append(member.username)

            updinvlist = set(memtinv).difference(set(invited))

            with open(usedfile, "wb") as tmp:
                tmp.write("\n".join(updinvlist))

            if len(invited) != 0:
                with open(alrfile, "ab") as tmp:
                    tmp.write("\n%s" %"\n".join(invited))





def main():
    choice = enterint("What would you like to do?\n 1. Extract member lists\n 2. send invites (under construction)\n 3. Send pm (under construction)\n 4. Send note (under construction)\nYour choice, monkeyboy: ")
    br = mecbrowser()
    print "\n"

    if choice == 1: #extract member names
        targetlst = tlstcreator()
        memlist = extractMemberList(br, targetlst)

        print "\n%i members found:" %len(memlist)
        print ", ".join(memlist)

    elif choice == 2: #inviter
        subchoice = None
        while subchoice not in [1,2,3,4,5]:
            subchoice = enterint("Would you like to\n 1. Send invites for existing groups\n 2. Add a new group\n 3. Inspect an invite list\n 4. Add names to a groups invite list\n 5. Modify a groups configuration file\n\nMake your choice, young padawan: ")

        if subchoice == 1: #inviter, send invites
            print "\n\nwhich group would you like to send invites for?\n 0 Infinite loop over all groups"

            inifilelist = getfilelist("config/invites", ".ini")
            for fname in inifilelist:
                print "", fname[0], fname[1].replace(".ini", "")
            invchoice = enterint("it would be recommended to enter your choice here: ")

            login(br, "y")
            if invchoice == 0:
                inviter(br, inifilelist)
            else:
                inviter(br, [inifilelist[invchoice - 1]], False)

        elif subchoice == 2: #inviter, add group
            name = raw_input("\n\nGroup name: ")
            ID = enterint("Group ID: ")
            createconfig(name, ID)

            print "\n\nThe following files has been created\n\n  - /data/messages/%s Standard Message (used to invite members from the standard and VIP invites lists)\n  - /data/messages/%s Deserters Message (Used to reinvite those who have left %s)\n  - /data/invite lists/%s (main invites list)\n  - /data/invite lists/%s priority (used for those whom you want to invite asap, circumvents any filters)\n  - /data/invite lists/%s members who has left (here you can place members who has left %s to reinvite them using the invites message from /data/messages/%s Deserters Message)\n  - (data/invite lists/%s already invited (stores the names of those who has received an invite from the script, members in this list wont receive an invite even if their names are in the standard invites list)\n\nTo use the inviter you need to first create a invites message for the script to use and put members whom you want to invite in the invites lists\nChanges to the filter used by %s can be made by modifying the file /config/invites/%s\n\n\n\n\nNames in the priority invites list will be invited before those in the list of members who has left and the standard list, without the use of any filters. Names in the invites list of members who has left will be invited before those in the standard list and with the deserters invites message\n\n" %(name, name, name, name, name, name, name, name, name, name, name)

        elif subchoice == 3: #inviter, inspect invite list
            count = 1
            flist = []
            for x in sorted([x for x in os.listdir("data/invite lists") if isfile(join("data/invite lists", x))]):
                if x[-1] == "~":
                    continue
                print " %i. %s" %(count, x)
                flist.append(x)
                count += 1

            chosenFile = flist[enterint("\nWhich file do you want to inspect: ") - 1]
            with open("data/invite lists/%s" %chosenFile, "rb") as f:
                nameList = f.read()
            print nameList.replace("\n", ", ")
            print "\n\nNumber of members in list: %i\n" %len(nameList.split("\n"))

        elif subchoice == 4: #inviter, add names to invites list
            count = 1
            flist = []
            for x in sorted([x for x in os.listdir("data/invite lists") if isfile(join("data/invite lists", x))]):
                if "~" in x or "already invited" in x or "members who has left" in x:
                    continue
                print " %i. %s" %(count, x)
                flist.append(x)
                count += 1

            groupChoice = flist[enterint("\nWhich file do you want to add names to: ") - 1]
            newMem = raw_input("\nEnter a comma seperated list of usernames to be added: ").replace(" ", "")

            with open("data/invite lists/%s" %groupChoice, "ab") as f:
                f.write("\n%s" %"\n".join(newMem.split(",")))

        elif subchoice == 5: #inviter, inspect/modify config file
            count = 1
            flist = []
            for x in sorted([x for x in os.listdir("config/invites") if isfile(join("config/invites", x))]):
                print " %i. %s" %(count, x)
                flist.append(x)
                count += 1

            groupChoice = flist[enterint("\nWhich file do you want to inspect/modify: ") - 1]

            with open("config/invites/%s" %groupChoice, "rb") as f:
                conelements = f.readlines()

            print "\n\n\nCurrent config file setup:\n\n"
            count = 1
            for x in conelements:
                print " %i. %s" %(count, x)
                count += 1

            conelement_index = enterint("\n\nWhich one do you want to change? ") - 1

            conelements[conelement_index] = "%s==%s\n" %(conelements[conelement_index].split("==")[0], raw_input("\nNew value: "))

            with open("config/invites/%s" %groupChoice, "wb") as f:
                for element in conelements:
                    f.write(element)

    elif choice == 3: #pm sender
        targets = raw_input("Enter comma seperated list of members to post note to: ").replace(" ", "").split(",")
        msg = "\n".join(buildMsgList())

        delay = enterint("\nDelay between PMs (s): ")

        login(br, "y")
        for member in targets:
            print "sending PM to %s" %member
            member = makeMember(br, member)
            sendPM(br, member, msg, delay)

    elif choice == 4: #note sender
        targets = raw_input("Enter comma seperated list of members to post note to: ").replace(" ", "").split(",")
        msg = raw_input("enter message: ")
        delay = enterint("\nDelay between notes (s): ")

        login(br, "y")
        for member in targets:
            print "sending note to %s" %member
            member = makeMember(br, member)
            msg = msg.replace("/name", member.name).replace("/username", member.username)
            sendNote(br, member, msg, delay)

    br.close()


if __name__ == '__main__':
    while True:
        main()

        choice = None
        while choice not in ["y", "n"]:
            choice = raw_input("\n\nrun again? (y/n) ")
        if choice == "n":
            break
        print "\n\n"
