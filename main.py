from mecbrowser import *
from misc import *

makefolder(["data", "data/message"])

def login(br, x = None):
    while x not in ["y", "n"]:
        x = raw_input("login? (y/n) ")

    if x == "y":
        username = raw_input("username: ")
        password = raw_input("password: ")
        meclogin(br, username, password)

def main():
    choice = enterint("What would you like to do?\n 1. Extract member lists\n 2. send invites (under construction)\n 3. Send pm (under construction)\n 4. Send note (under construction)\nYour choice, monkeyboy: ")
    br = mecbrowser()
    print "\n"

    if choice == 1: #extract member names
        targetlst = tlstcreator()
        memlist = extractMemberList(br, targetlst)

        print "\n%i members found:" %len(memlist)
        print " ".join(memlist)

    elif choice == 2: #inviter
        login(br, "y")
        groupID = raw_input("Enter group id: ")
        invitee = raw_input("Enter member to invite: ")
        msgpath = raw_input("path to invites msg: ")
        sendInvite(br, groupID, invitee, fileopen(msgpath))

    elif choice == 3: #pm sender
        login(br, "y")
        member = raw_input("Enter member to pm: ")
        msg = raw_input("enter message: ")
        sendPM(br, member, msg)

    elif choice == 4: #note sender
        login(br, "y")
        member = raw_input("Enter member to post note to: ")
        msg = raw_input("enter message: ")
        sendNote(br, member, msg)

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
