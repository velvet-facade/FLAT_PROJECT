from tkinter import *
from PIL import Image
from mysql.connector import *
from string import *
mydb = connect(host='localhost', user='root',
               passwd='1234', database='flat')

cursor = mydb.cursor()
communityNameFinal = ''
monthLst = ['January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December']
yrLst = ['2021', '2022', '2023', '2024', '2025',
         '2026', '2027', '2028', '2029', '2030']
flag1_1 = 1
flag1_2 = 1
flag2 = 1
flag3 = 1
flag4 = 1
flagMainDetails = 0
flagComDetails = 0
flagExpenses = 0
flagSuggestions = 0
flag5 = 1
flatName = str()


def destroyWin1_2():
    window1.destroy()
    global flag1_2
    flag1_2 = 0


def destroyWin1_1():
    window1.destroy()
    global flag1_1
    flag1_1 = 0


def destroyWin2():
    window2.destroy()
    global flag2
    flag2 = 0


def destroyWin3():
    window3.destroy()
    global flag3
    flag3 = 0


def newAcc():
    fName = ent1.get()
    l = fName.split()
    global flatName

    for i in l:
        flatName = flatName+i
    floors = ent2.get()
    numHouse = ent3.get()
    FHouse = ent4.get()  # House per floor
    admnPW = ent5.get()

    st1 = "create table {} (Floors int(5),Houses int(5),Houses_per_floor int(5),Admin_password char(10))".format(
        flatName)
    cursor.execute(st1)
    st2 = 'insert into {} values({},{},{},"{}")'.format(
        flatName, floors, numHouse, FHouse, admnPW)
    cursor.execute(st2)

    st3 = 'create table {} (House_number varchar(5),HouseOwner_name varchar(20),Phone_number bigint)'.format(
        flatName+'owner')
    cursor.execute(st3)
    st4 = 'create table {} (House_number varchar(5), status_january_2022 varchar(10))'.format(
        flatName+'mainstatus')
    cursor.execute(st4)
    st5 = 'create table {} (Maintenance_total bigint)'.format(
        flatName+'maintenancetotal')
    cursor.execute(st5)
    cursor.execute("insert into {} values({})".format(
        flatName+'maintenancetotal', 0))
    st6 = 'create table {} (water bigint,electricity bigint,drainage bigint,watchmen bigint,other bigint,total_expenses bigint,timeline varchar(20))'.format(
        flatName+'expenses')
    cursor.execute(st6)
    st7 = 'create table {} (house_number varchar(5),house_owner varchar(20),suggestions varchar(1000))'.format(
        flatName+'suggestions')
    cursor.execute(st7)
    mydb.commit()
    destroyWin2()


def pwdVerify():

    global communityNameFinal

    def pwGet():
        pw = pwEnt.get()

        if pw != pwd:
            Label(text='Enter correct admin password!', font=(
                'arial', 15), bg='red', fg='black').place(x=340, y=500)
        if pw == pwd:
            global flag4
            window4.destroy()
            flag4 = 0

        Label(text='Enter admin password:', font=('Arial', 17),
              bg='skyblue', fg='black').place(x=180, y=330)
        pwEnt = Entry(window4,)
        pwEnt.place(x=450, y=335)
        fName = flatEnt.get()
        l = fName.split()

        for i in l:
            communityNameFinal += i

        cursor.execute('select * from {}'.format(communityNameFinal))
        data = cursor.fetchall()
        pwd = data[0][3]
        but = Button(text='Click to continue',
                     font=('arial', 13), command=pwGet)
        but.place(x=400, y=400)


def destroyWin4():
    global flag4
    global communityNameFinal
    fName = flatEnt.get()
    l = fName.split()
    for i in l:
        communityNameFinal += i
    window4.destroy()
    flag4 = 0


def comDetails():
    global flagComDetails
    global flag5
    flagComDetails = 1
    flag5 = 0

    window5.destroy()


def mainDetails():
    global flagMainDetails
    global flag5
    flagMainDetails = 1
    flag5 = 0
    window5.destroy()


def suggestions():
    global flagSuggestions
    global flag5
    flagSuggestions = 1
    flag5 = 0
    window5.destroy()


def expensesDetails():
    monthExp = str(clickExp1.get())
    yearExp = str(clickExp2.get())
    timeLine = monthExp+yearExp
    waterExp = int(waterBill.get())
    electricityExp = int(electricityBill.get())
    drainageExp = int(drainageBill.get())
    watchmenExp = int(watchmenBill.get())
    otherExp = int(otherBill.get())
    totalExp = waterExp+electricityExp+drainageExp+watchmenExp+otherExp
    totalBill.delete(0.0, END)
    totalBill.insert(END, totalExp)

    cursor.execute(
        'select * from {}'.format(communityNameFinal+'maintenancetotal'))
    mainTotTup = cursor.fetchall()
    mainTot = mainTotTup[0][0]
    alertMsg = Text(windowExpenses, width=30, height=1)
    alertMsg.place(x=750, y=400)
    if (mainTot-totalExp) > 0:
        cmd = "insert into {} values({},{},{},{},{},{},'{}')".format(
            communityNameFinal+'expenses', waterExp, electricityExp, drainageExp, watchmenExp, otherExp, totalExp, timeLine)
        cursor.execute(cmd)
        mydb.commit()
        cmd2 = 'update {} set maintenance_total= {}-{}'.format(
            communityNameFinal+'maintenancetotal', mainTot, totalExp)
        cursor.execute(cmd2)
        cursor.execute(
            'select * from {}'.format(communityNameFinal+'maintenancetotal'))
        mainTotTup2 = cursor.fetchall()
        mainTot2 = mainTotTup2[0][0]

        totalText.delete(0.0, END)
        totalText.insert(END, mainTot2)
        alertMsg.delete(0.0, END)
        alertMsg.insert(END, 'Data saved')

    if (mainTot-totalExp) < 0:
        alertMsg.delete(0.0, END)
        alertMsg.insert(END, 'Alert! Insufficient amount')


def hOwnName():

    fl = clicked1.get()
    houseNo = clicked2.get()
    houseOwnName = hOwnNameEnt.get()
    phNo = phNoEnt.get()

    cursor.execute("insert into {} values('{}','{}',{})".format(
        flatName+str('owner'), houseNo, houseOwnName, phNo))
    cursor.execute("insert into {} values('{}','{}')".format(
        flatName+str('mainstatus'), houseNo, 'Due'))

    mydb.commit()


def mainView():
    month = click1.get()
    year = click2.get()
    yAxis = 115
    cursor.execute("select house_number from {}".format(
        communityNameFinal+'owner'))
    people = cursor.fetchall()
    totalPeople = len(people)

    try:
        yAxis = 115

        cursor.execute("select status_{}_{} from {}".format(
            month, year, communityNameFinal+str('mainstatus')))
        statusData = cursor.fetchall()

        for i in statusData:

            maintenanceText = Text(
                windowMainDetails, width=20, height=1, wrap=WORD, background='white')

            maintenanceText.place(x=xAxis, y=yAxis)
            maintenanceText.insert(END, i)
            yAxis += 40

    except:
        for i in range(totalPeople):

            maintenanceText = Text(
                windowMainDetails, width=20, height=1, wrap=WORD, background='white')
            maintenanceText.place(x=520, y=yAxis)
            maintenanceText.insert(END, 'Due')
            yAxis += 40

    cursor.execute(
        'select * from {}'.format(communityNameFinal+'maintenancetotal'))
    maintenanceTotalTup = cursor.fetchone()
    Label(windowMainDetails, text='Total amount:', bg='skyblue',
          fg='black', font='arial',).place(x=650, y=500)
    totalText = Text(windowMainDetails, width=20, height=1,
                     wrap=WORD, background='white')
    totalText.place(x=800, y=500)
    maintenanceTotal = maintenanceTotalTup[0]
    totalText.insert(END, maintenanceTotal)


def houseSuggBut():
    sugg = houseSuggestions.get(0.0, END)
    savedText = Text(windowSugg, width=20, height=1,
                     wrap=WORD, background='white')
    savedText.place(x=600, y=500)
    houseSuggNumber = hnoSugg.get()
    houseNameSugg = houseSuggName.get()
    savedText.delete(0.0, END)
    savedText.insert(END, 'Saved successfully!')
    insertSuggCmd = "insert into {} values ('{}','{}','{}')".format(
        communityNameFinal+'suggestions', houseSuggNumber, houseNameSugg, sugg)
    cursor.execute(insertSuggCmd)
    mydb.commit()


def expenses():
    global flagExpenses
    global flag5
    flagExpenses = 1
    flag5 = 0
    window5.destroy()


def mainModify():

    month = click1.get()
    year = click2.get()
    houseNumber = hnoClick1.get()
    status = var.get()
    if status.lower() == 'paid':
        cursor.execute(
            'select * from {}'.format(communityNameFinal+'maintenancetotal'))
        maintenanceTotalTup = cursor.fetchone()
        Label(windowMainDetails, text='Total amount:', bg='skyblue',
              fg='black', font='arial',).place(x=650, y=500)
        totalText = Text(windowMainDetails, width=20,
                         height=1, wrap=WORD, background='white')
        totalText.place(x=800, y=500)
        maintenanceTotal = maintenanceTotalTup[0]
        maintenanceTotal = maintenanceTotal+2000

        totalText.insert(END, maintenanceTotal)
        cursor.execute('update {} set maintenance_total={}'.format(
            communityNameFinal+'maintenancetotal', maintenanceTotal))
    try:
        yAxis = 115
        cursor.execute("update {} set status_{}_{} = '{}' where house_number = '{}'".format(
            communityNameFinal+str('mainstatus'), month, year, status, houseNumber))
        mydb.commit()
        cursor.execute("select status_{}_{} from {}".format(
            month, year, communityNameFinal+str('mainstatus')))
        statusData = cursor.fetchall()

        for i in statusData:
            maintenanceText = Text(
                windowMainDetails, width=20, height=1, wrap=WORD, background='white')
            maintenanceText.place(x=520, y=yAxis)
            maintenanceText.insert(END, i)
            yAxis += 40

    except:
        cursor.execute("alter table {} add (status_{}_{} varchar(10))".format(
            communityNameFinal+str('mainstatus'), month, year))
        mydb.commit()
        cursor.execute("update {} set status_{}_{} = 'due'".format(
            communityNameFinal+str('mainstatus'), month, year))
        mydb.commit()
        cursor.execute("update {} set status_{}_{} = '{}' where house_number ='{}'".format(
            communityNameFinal+str('mainstatus'), month, year, status, houseNumber))
        mydb.commit()
        cursor.execute("select status_{}_{} from {}".format(
            month, year, communityNameFinal+str('mainstatus')))
        statusData = cursor.fetchall()
        for i in statusData:

            maintenanceText = Text(
                windowMainDetails, width=20, height=1, wrap=WORD, background='white')
            maintenanceText.place(x=520, y=yAxis)
            maintenanceText.insert(END, i)
            yAxis += 40


window1 = Tk()
window1.title('WELCOME SCREEN')
window1.geometry('1000x800')
window1.configure(background='sky blue')
img = PhotoImage(file=r'assets\dubai.png')
bgImg = Label(window1, image=img, bg='skyblue')
bgImg.place(x=0, y=-70)
topic = Label(window1, text='FLAT MAINTENANCE SYSTEM',
              bg='skyblue', font=('Arial black', 20), fg='black',)
topic.place(x=280, y=20)
msg1 = Label(window1, text='Login details', font=(
    'Arial', 15), fg='black', bg='sky blue', width=12)
msg1.place(x=420, y=120)
but1 = Button(window1, text='Create a new account',
              font='Arial', width=20, command=destroyWin1_1)
but1.place(x=240, y=180)
but2 = Button(window1, text='Already have an account',
              font='Arial', width=20, command=destroyWin1_2)
but2.place(x=550, y=180)
window1.mainloop()
if flag1_1 == 0:
    window2 = Tk()
    window2.title('LOGIN SCREEN')
    window2.geometry('1000x550')
    window2.configure(background='sky blue')
 # img1=PhotoImage(file=r'C:\Users\Nandu\OneDrive\Desktop\sampleLogoFinal.png')
 # logoImg=Label(window2,image=img1,bg='skyblue')
 # logoImg.place(x=800,y=0)
    topic = Label(window2, text='FLAT MAINTENANCE SYSTEM',
                  bg='skyblue', font=('Arial black', 20), fg='black',)
    topic.place(x=280, y=20)
    Label(window2, text='Login details', font=('Arial ', 18),
          fg='black', bg='sky blue', width=12).place(x=420, y=110)
    txt1 = Label(window2, text='Enter your community name:',
                 font=('Arial', 15), bg='sky blue', fg='black')
    txt1.place(x=240, y=180)
    ent1 = Entry(window2,)
    ent1.place(x=560, y=187)
    fName = ent1.get()
    l = fName.split()

    txt2 = Label(window2, text='Enter number of floors in your community:', font=(
        'Arial', 15), bg='skyblue', fg='black')
    txt2.place(x=180, y=220)
    ent2 = Entry(window2,)
    ent2.place(x=560, y=227)
    txt3 = Label(window2, text='Enter total number of houses:',
                 font=('Arial', 15), bg='sky blue', fg='black')
    txt3.place(x=200, y=260)
    ent3 = Entry(window2,)
    ent3.place(x=560, y=267)
    txt4 = Label(window2, text='Enter total number of houses in each floor:', font=(
        'Arial', 15), bg='skyblue', fg='black')
    txt4.place(x=170, y=300)
    ent4 = Entry(window2,)
    ent4.place(x=560, y=307)
    txt5 = Label(window2, text='Enter admin password:',
                 font=('Arial', 15), bg='sky blue', fg='black')
    txt5.place(x=200, y=340)
    ent5 = Entry(window2,)
    ent5.place(x=560, y=347)
    but3 = Button(window2, text='Click to proceed', width=14,
                  font='Arial', bg='white', fg='black', command=newAcc)
    but3.place(x=650, y=450)
    Label(window2, text='===>', bg='skyblue', fg='black',
          font=('Arial', 15)).place(x=820, y=455)

    window2.mainloop()

if flag2 == 0:
    window3 = Tk()
    window3.title('LOGIN SCREEN')
    window3.geometry('1000x550')
    window3.configure(background='sky blue')
    # img1=PhotoImage(file=r'C:\Users\Nandu\OneDrive\Desktop\sampleLogoFinal.png')
    # logoImg=Label(window3,image=img1,bg='skyblue')
    # logoImg.place(x=800,y=0)
    Label(window3, text='LOGIN DETAILS', bg='skyblue', font=(
        'Arial black', 20), fg='black').place(x=30, y=20)

    cursor.execute('select * from {}'.format(flatName))
    data = cursor.fetchall()  # 0 - floors, 1-houses, 2- houses_per_floor, 3-admnPW
    fl = data[0][0]
    flLst = []
    for i in range(1, fl+1):
        flLst.append('Floor '+str(i))

    Label(window3, text='Floor', bg='skyblue', font=(
        'Arial black', 15), fg='black').place(x=100, y=200)
    Label(window3, text='House number', bg='skyblue', font=(
        'Arial black', 15), fg='black').place(x=250, y=200)
    Label(window3, text='House owner', bg='skyblue', font=(
        'Arial black', 15), fg='black').place(x=500, y=200)
    Label(window3, text='Phone number', bg='skyblue', font=(
        'Arial black', 15), fg='black').place(x=750, y=200)
    hno = data[0][2]
    hname = ascii_uppercase
    hlst = []
    for i in range(fl):
        for j in range(1, hno+1):
            hlst.append(hname[i]+str(j))

    hOwnNameEnt = Entry(window3,)
    hOwnNameEnt.place(x=510, y=250)
    phNoEnt = Entry(window3,)
    phNoEnt.place(x=770, y=250)

    clicked1 = StringVar()
    clicked1.set(flLst[0])
    drop1 = OptionMenu(window3, clicked1, *flLst)
    drop1.place(x=85, y=250)
    clicked2 = StringVar()
    clicked2.set(hlst[0])
    drop2 = OptionMenu(window3, clicked2, *hlst)
    drop2.place(x=295, y=250)

    Button(window3, text='Click to save', font='ComicsansMS',
           width=10, command=hOwnName).place(x=400, y=350)
    Button(window3, text='Exit', font='Arial', width=10,
           command=destroyWin3).place(x=800, y=500)
    window3.mainloop()

if flag1_2 == 0:
    window4 = Tk()
    window4.geometry('1000x550')
    window4.configure(background='skyblue')
 # img1=PhotoImage(file=r'C:\Users\Nandu\OneDrive\Desktop\sampleLogoFinal.png')
 # logoImg=Label(window4,image=img1,bg='skyblue')
 # logoImg.place(x=800,y=0)
    Label(window4, text='LOGIN DETAILS', font=('Arial black', 20),
          bg='skyblue', fg='black').place(x=350, y=10)
    Label(window4, text='Enter your community name:', font=(
        'Arial ', 17), bg='sky blue', fg='black').place(x=210, y=180)
    flatEnt = Entry(window4,)
    flatEnt.place(x=560, y=187)
    Label(window4, text='Login as:', font=('Arial', 17),
          bg='skyblue', fg='black').place(x=250, y=260)
    Button(text='Admin', font='Arial', bg='white',
           fg='black', command=pwdVerify).place(x=400, y=260)
    Button(text='Guest', font='Arial', bg='white', fg='black',
           command=destroyWin4).place(x=500, y=260)
    window4.mainloop()
if flag4 == 0:
    window5 = Tk()
    window5.geometry('1000x550')
    window5.configure(background='skyblue')
    # img1=PhotoImage(file=r'C:\Users\Nandu\OneDrive\Desktop\sampleLogoFinal.png')
    # logoImg=Label(window5,image=img1,bg='skyblue')
    # logoImg.place(x=800,y=0)
    Button(text='Community details', font='Arial', bg='white',
           fg='black', command=comDetails).place(x=150, y=150)
    Button(text='Maintenance details', font='Arial', bg='white',
           fg='black', command=mainDetails).place(x=550, y=150)
    Button(text='Expenses', font='Arial', bg='white',
           fg='black', command=expenses).place(x=165, y=250)
    Button(text='Suggestion box', font='Arial', bg='White',
           fg='Black', command=suggestions).place(x=550, y=250)
    window5.mainloop()

if flagComDetails == 1 and flag5 == 0:
    cursor.execute('select * from {}'.format(communityNameFinal+'owner'))
    data = cursor.fetchall()
    win = Tk()
    win.geometry('1000x550')
    win.configure(background='skyblue')

    xAxis = 70
    yAxis = 70
    Label(win, text='House Owner Details', font=('Arial black', 15),
          bg='skyblue', fg='black').place(x=330, y=10)
    Label(win, text='House number', font=('Arial black', 15),
          bg='sky blue', fg='black').place(x=xAxis+20, y=yAxis)
    Label(win, text='House owner', font=('Arial black', 15),
          bg='sky blue', fg='black').place(x=xAxis+220, y=yAxis)
    Label(win, text='Phone number', font=('Arial black', 15),
          bg='sky blue', fg='black').place(x=xAxis+480, y=yAxis)
    for i in data:
        yAxis += 40
        for j in i:
            Label(win, text='{}'.format(j), font='Arialblack',
                  bg='skyblue', fg='black').place(x=xAxis, y=yAxis)
            xAxis += 250
        xAxis = 70
    win.mainloop()

if flagMainDetails == 1 and flag5 == 0:
    windowMainDetails = Tk()
    windowMainDetails.geometry('1000x550')
    windowMainDetails.configure(background='skyblue')
    cursor.execute('select house_number,houseowner_name from {}'.format(
        communityNameFinal+'owner'))
    data = cursor.fetchall()
    xAxis = 70
    yAxis = 70
    Label(windowMainDetails, text='House number', font=('Arial black', 15),
          bg='sky blue', fg='black').place(x=xAxis-20, y=yAxis)
    Label(windowMainDetails, text='House owner', font=('Arial black', 15),
          bg='sky blue', fg='black').place(x=xAxis+220, y=yAxis)
    Label(windowMainDetails, text='Status', font=('Arial black', 15),
          bg='skyblue', fg='black').place(x=xAxis+480, y=yAxis)
    for i in data:
        yAxis += 40
    for j in i:

        Label(windowMainDetails, text='{}'.format(j), font='Arialblack',
              bg='skyblue', fg='black').place(x=xAxis, y=yAxis)
        xAxis += 250
    xAxis = 70
    cursor.execute('select status_january_2022 from {} '.format(
        communityNameFinal+'mainstatus'))
    statusData = cursor.fetchall()
    xAxis = 520
    yAxis = 115
    for i in statusData:

        maintenanceText = Text(windowMainDetails, width=20,
                               height=1, wrap=WORD, background='white')
        maintenanceText.place(x=xAxis, y=yAxis)
        maintenanceText.insert(END, i)
    yAxis += 40

    var = StringVar()
    cursor.execute('select house_number from {} '.format(
        communityNameFinal+'mainstatus'))
    hnoData = cursor.fetchall()
    hnoLst = []

    for i in hnoData:
        hnoLst.append(i[0])

    Label(text='Flat maintenance charges', font=('Arial black', 15),
          bg='skyblue', fg='black').place(x=350, y=0)
    click1 = StringVar()
    click2 = StringVar()
    click1.set(monthLst[0])
    click2.set(yrLst[0])
    OptionMenu(windowMainDetails, click1, *monthLst).place(x=800, y=70)
    OptionMenu(windowMainDetails, click2, *yrLst).place(x=900, y=70)

    hnoClick1 = StringVar()
    hnoClick1.set(hnoLst[0])
    houseNo1 = OptionMenu(windowMainDetails, hnoClick1, *hnoLst)
    houseNo1.place(x=800, y=200)
    c = Checkbutton(windowMainDetails, text='Paid',
                    variable=var, onvalue='Paid', offvalue='Due')
    c.deselect()
    c.place(x=900, y=200)
    cursor.execute(
        'select * from {}'.format(communityNameFinal+'maintenancetotal'))
    maintenanceTotalTup = cursor.fetchone()
    Label(windowMainDetails, text='Total amount:', bg='skyblue',
          fg='black', font='arial',).place(x=650, y=500)
    totalText = Text(windowMainDetails, width=20, height=1,
                     wrap=WORD, background='white')
    totalText.place(x=800, y=500)
    maintenanceTotal = maintenanceTotalTup[0]

    totalText.insert(END, maintenanceTotal)
    Button(text='Modify', font='Arial', bg='white',
           fg='black', command=mainModify).place(x=800, y=300)
    Button(text='View', font='Arial', bg='white',
           fg='black', command=mainView).place(x=800, y=120)

    windowMainDetails.mainloop()

if flagExpenses == 1 and flag5 == 0:
    windowExpenses = Tk()
    windowExpenses.geometry('1000x550')
    windowExpenses.configure(background='sky blue')
    clickExp1 = StringVar()
    clickExp2 = StringVar()
    clickExp1.set(monthLst[0])
    clickExp2.set(yrLst[0])
    OptionMenu(windowExpenses, clickExp1, *monthLst).place(x=800, y=70)
    OptionMenu(windowExpenses, clickExp2, *yrLst).place(x=900, y=70)
    Label(windowExpenses, text='Expenses', font=('arial black', 20),
          bg='sky blue', fg='black').place(x=300, y=10)
    Label(windowExpenses, text='Water Expenses: ', font=(
        'arial black', 15), bg='sky blue', fg='black').place(x=100, y=110)
    waterBill = Entry(windowExpenses,)
    waterBill.place(x=400, y=120)
    Label(windowExpenses, text='Electricity bill: ', font=(
        'arial black', 15), bg='skyblue', fg='black').place(x=100, y=170)
    electricityBill = Entry(windowExpenses,)
    electricityBill.place(x=400, y=180)
    Label(windowExpenses, text='Drainage charges: ', font=(
        'arial black', 15), bg='skyblue', fg='black').place(x=100, y=230)
    drainageBill = Entry(windowExpenses,)
    drainageBill.place(x=400, y=240)
    Label(windowExpenses, text='Watchmen salary: ', font=(
        'arial black', 15), bg='skyblue', fg='black').place(x=100, y=290)
    watchmenBill = Entry(windowExpenses,)
    watchmenBill.place(x=400, y=300)
    Label(windowExpenses, text='Others: ', font=('arial black', 15),
          bg='skyblue', fg='black').place(x=100, y=350)
    otherBill = Entry(windowExpenses,)
    otherBill.place(x=400, y=360)
    Label(windowExpenses, text='Total expenses: ', font=(
        'arial black', 15), bg='skyblue', fg='black').place(x=100, y=450)
    totalBill = Text(windowExpenses, width=20, height=1,
                     wrap=WORD, background='white')
    totalBill.place(x=400, y=460)
    cursor.execute(
        'select * from {}'.format(communityNameFinal+'maintenancetotal'))
    maintenanceTotalTup = cursor.fetchone()
    Label(windowExpenses, text='Total amount:', bg='skyblue',
          fg='black', font='arial',).place(x=650, y=500)
    totalText = Text(windowExpenses, width=20, height=1,
                     wrap=WORD, background='white')
    totalText.place(x=800, y=500)
    maintenanceTotal = maintenanceTotalTup[0]

    totalText.insert(END, maintenanceTotal)

    Button(windowExpenses, text='Save', font='arial', bg='white',
           fg='black', command=expensesDetails).place(x=850, y=450)
    windowExpenses.mainloop()

if flagSuggestions == 1 and flag5 == 0:
    windowSugg = Tk()
    windowSugg.geometry('1000x550')
    windowSugg.configure(background='skyblue')
    Label(windowSugg, text='Suggestion box', font=('arialblack', 15),
          bg='skyblue', fg='black').place(x=350, y=10)
    cursor.execute('select house_number from {} '.format(
        communityNameFinal+'mainstatus'))
    hnoData = cursor.fetchall()

    hnoLst = []
    for i in hnoData:
        hnoLst.append(i[0])
    Label(windowSugg, text='House number', font='arial',
          bg='skyblue', fg='black',).place(x=200, y=60)
    hnoSugg = StringVar()
    hnoSugg.set(hnoLst[0])
    houseSuggNo = OptionMenu(windowSugg, hnoSugg, *hnoLst)
    houseSuggNo.place(x=225, y=100)
    Label(windowSugg, text='House owner', font='Arial',
          bg='skyblue', fg='black').place(x=350, y=60)
    houseSuggName = Entry(windowSugg,)
    houseSuggName.place(x=350, y=100)
    houseSuggestions = Text(windowSugg, width=100, height=20, wrap=WORD)
    houseSuggestions.place(x=100, y=150)
    Button(windowSugg, text='Click to save', font='Arial',
           command=houseSuggBut).place(x=800, y=500)
    windowSugg.mainloop()
