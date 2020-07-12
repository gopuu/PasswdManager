import sqlite3
import random
import string
import datetime
conn = sqlite3.connect('PasswdMngr.db')
c = conn.cursor()

def generatePasswd():
    N = 3
    str1 = random.choices(string.ascii_uppercase, k = N) 
    str2 = random.choices(string.ascii_lowercase, k = N) 
    str3 = random.choices(string.digits, k = N)
    str4 = random.choices("@#$&*<>{}", k = 1)
    #str4 = random.choices("['@','#','$','&','*','<','>','{','}']", k = 1)

    #passwd = ''.join(random.choices(string.ascii_uppercase + string.digits + string.ascii_lowercase+'@#', k = N)) 
    passwdList = str1 + str2 + str4 + str3
    random.shuffle(passwdList)
    passwd = ""
    for ch in passwdList:
        passwd += ch
    return passwd
    
#===== METHODS ======
def insert(app_name):
    option = input(" \n 1. AutoGenerate Password \n 2. Type Your Password \n SELECT: ")
    passwd = None
    if int(option)==1:
        passwd = generatePasswd()
    elif int(option)==2:
        passwd = input("\n Enter Your Password: ")
    else:
        print(" \nERROR: Invalid Option.")
    #print("passwd: ",passwd)
    date = datetime.datetime.now()
    date = date.strftime("%d-%m-%Y %H:%M")
    qry = "INSERT INTO passwdMngr VALUES ('" + app_name + "','" + passwd + "','" + date + "','" + date + "')"
    #print("qry: ",qry)
    #print("date: ",date)
    #print("Passwd: ",passwd)
    c.execute(qry)
    print("  Password:", passwd)
    print("  Record Created Successfully.")
    conn.commit()

def isDataFound():
    c.execute("SELECT * FROM passwdMngr")
    rows = c.fetchall()
    if len(rows)==0:
        return False
    else:
        return True

def showAll():
    c.execute("SELECT * FROM passwdMngr")
    rows = c.fetchall()
    if len(rows)==0:
        print("\t\tNo Record(s) found")
    else:
        print(" No.  APP-NAME "," "*8," PASSWORD \t CREATED DATE-TIME \t LAST UPDATE\n")
        for row in rows:
            if rows.index(row)+1 < 10:
                print(" ", rows.index(row)+1, " ", row[0], " "*(17-len(row[0])), row[1], (" "*(15-len(row[1]))), row[2], "\t", row[3])
            elif rows.index(row)+1 < 100:
                print("", rows.index(row)+1, " ", row[0], " "*(17-len(row[0])), row[1], (" "*(15-len(row[1]))), row[2], "\t", row[3])
            else:
                print(rows.index(row)+1, " ", row[0], (" "*(17-len(row[0]))), row[1], (" "*(15-len(row[1]))), row[2], "\t", row[3])
            #print("   ",row[0],"\t",row[1],"\t",row[2])

def del_record(name=None):
    if isDataFound():
        if name==None:
            c.execute("DELETE FROM passwdMngr") 
            #c.execute("DROP TABLE passwdMngr")     #delete table
        else:
            c.execute("DELETE FROM passwdMngr WHERE app_name='" + name + "'")
            conn.commit()
        print("    Record Deleted Successfully.")
    else:
        print("\t\tNo Record(s) found")

def update_record(NewName,CurrentAppName):
    if isDataFound():
        date = datetime.datetime.now()
        date = date.strftime("%d-%m-%Y %H:%M")
        if NewName == None:     #--- update Password
            passwd = generatePasswd()
            qry = "UPDATE passwdMngr SET passwd='" + passwd + "', last_update_date='" + date + "'  WHERE app_name='" + CurrentAppName + "'"
            c.execute(qry)
        else:                   #--- update AppName
            qry = "UPDATE passwdMngr SET app_name='" + NewName + "', last_update_date='" + date + "' WHERE app_name='" + CurrentAppName + "'"
            c.execute(qry)
            conn.commit()
        print("    Record Updated Successfully.")
    else:
        print("\t\tNo Record(s) found")
        
while(True):
    #======= MENU ======
    bnnr = "PASSSWORD MANAGER"
    #====== BANNER =====
    def line(banner_len):
        print(" +","-"*banner_len,"+")
        
    line(len(bnnr))
    print(" |",bnnr,"|")
    line(len(bnnr))
    option = input("\n 1. Create New Record\n 2. View Records\n 3. Delete Record\n 4. Update Record\n 5. EXIT \n\n OPTION: ")
    line(len(bnnr)*3)
    print()

    #========== TABLE ===========
    try:
        c.execute('''SELECT count(name) FROM sqlite_master WHERE type='table' AND name='passwdMngr' ''')
        #if the count is 1, then table exists
        if c.fetchone()[0]!=1 : {
            c.execute('''CREATE TABLE passwdMngr(app_name, passwd text, created_date text, last_update_date text)''')
            }
    except:
        print("ERROR !!")

    #======= SWITCH CASE ========
    if int(option)==1:      #-------------- INSERT NEW DATA----------------------
        name = input("  Enter Website/App Name: ") 
        insert(name)
        
    elif int(option)==2:    #-------------- DISPLAY DATA  ----------------------    
        showAll()

    elif int(option)==3:    #-------------- DELETE DATA  ----------------------
        opt = input("    1. Delete All Records\n    2. Delete Specific Record(s) \n\n    OPTION: ")
        line(len(bnnr)*3)
        if int(opt) == 1:
            del_record()        #-------------- DELETE ALL RECORDS  ----------------------
        elif int(opt) == 2:
            name = input("    Enter Registered Website/App Name: ") 
            del_record(name)    #-------------- DELETE SPECIFIC RECORD(S)  ----------------------    
        else:
            print("Invalid Option")
    
    elif int(option)==4:    #-------------- UPDATE DATA ----------------------
        opt = input("    1. Update App/Domain Name\n    2. Update Password \n\n    OPTION: ")
        line(len(bnnr)*3)
        if int(opt) == 1:       #-------------- UPDATE NAME ----------------------
            CurrentAppName = input("    Enter Current Website/App Name: ") 
            NewName = input("    Enter New Website/App Name: ") 
            update_record(NewName,CurrentAppName)
        elif int(opt) == 2:     #-------------- UPDATE PASSWORD ----------------------
            CurrentAppName = input("    Enter Current Website/App Name: ") 
            update_record(None,CurrentAppName)
        else:
            print("Invalid Option")

    elif int(option)==5:    #-------------- EXIT APP  ----------------------
        exit()

    else:
        print("\n Invalid Option..")
#        exit()

    #c.execute('''CREATE TABLE passwordMngr(domain_app_name text, password text, date text)''')
    #conn.commit()
    print()
    line(len(bnnr)*3)
    opt = input(' do u want to continue [y/n]: ')  
    if opt.upper() != 'Y':
        conn.commit()
        conn.close()
        break
