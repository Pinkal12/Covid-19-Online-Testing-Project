from SQues import TQues

import mysql.connector
import datetime
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="mysql",
    auth_plugin='mysql_native_password',
    database="covid_db"
)

mycursor=mydb.cursor()




# mycursor.execute("DROP table covid_person_risk")

stmt = "SHOW TABLES LIKE 'covid_person_risk'"
mycursor.execute(stmt)
checkOne = mycursor.fetchone()
print(checkOne)
if checkOne:
 print()
else:
    mycursor.execute("CREATE TABLE covid_person_risk(person_id VARCHAR(100), date VARCHAR(100), risk VARCHAR(100))")
#mycursor.execute("CREATE TABLE covid_person_info(name VARCHAR(200),address VARCHAR(200),phone_no bigint(20),person_id VARCHAR(100) NOT NULL UNIQUE)")

setuQues = [
    "Are you experiencing symptoms of cough?\nPress 1 for Yes \nPress 0 for No \n\n",
    "Are you experiencing symptoms of Fever?\nPress 1 for Yes \npress 0 for No \n\n",
    "Are you experiencing difficult to breathing?\nPress 1 for Yes \nPress 0 for No \n\n",
    "Are you experiencing loss of senses of smell and test?\nPress 1 for Yes \nPress 0 for No \n\n",
    "Have you traveled anywhere Internationally in the las 28 to 45 days? Press 1 for yes \nPress 0 for No \n\n "
]

setuDiease = [
    "Press one for chronic cough\nPress two for Dry cough\nPress three for Wet cough\nPress four for none of these\n\n",
    "Press one for chronic Fever\nPress two for low Fever \nPress three for low Fever\nPress four for none of these\n\n",
    "Press one for loss of consciousness\nPress two for Asthma \npress Three for chest pain \nPress four for none of these\n\n",
    "Press one for Diabetes\nPress two for kidney\nPress Three for Lung Disease\nPress four for none of these\n\n",
    "Press one for National travel\npress two for International travel\nPress Three for both above\nPress four for none of these\n\n "
]

msg = [
    "% Risk, your infection risk is low.\nWe recommend that you stay at home to avoid\nany chance of exposure to the Novel coronavirus.\nif you show symptoms of COVID-19 then call on \nFamily Welfare's 24x7 helpline at 1075.\nThank you. ",
    "% Risk, your infection risk is average.\nWe recommend to you should contact your family Doctor.\nAnd stay home, if you show symptoms of COVID-19\nthen call on Family Welfare's 24x7 helpline at 1075.\nThank you.",
    "% Risk, your infection risk is high.\nWe recommend to you should contact your family Doctor.\nAnd stay home, if you show symptoms of COVID-19\nthen call on Family Welfare's 24x7 helpline at 1075.\nThank you. ",
    "% Risk, your infection risk is very high.\ndo not leave your home.\nAnd call on Family Welfare's 24x7 helpline at 1075.\nIndian government provide you instruction and free Medicare.\nThank you. "
   ]

quesAns = [
    TQues(setuQues[0], 1, setuDiease[0]),
    TQues(setuQues[1], 1, setuDiease[1]),
    TQues(setuQues[2], 1, setuDiease[2]),
    TQues(setuQues[3], 1, setuDiease[3]),
    TQues(setuQues[4], 1, setuDiease[4]),

]



def setuques(ques):
    sql = "SELECT * FROM covid_person_info INNER JOIN covid_person_risk ON covid_person_info.person_id = covid_person_risk.person_id"
    mycursor.execute(sql)
    fetchtb = mycursor.fetchall()
    for x in fetchtb:
        print(x)
    mydb.commit()
    data = []
    for ques in quesAns:
        quesA = ques.setuquestion
        comp_ans = int(input(quesA))
        while comp_ans > 1:
            if comp_ans> 1:
                comp_ans = int(input(quesA))
            else:
                exit()
        data.append(comp_ans)
        comp_dis = ques.setuanswer
        if comp_ans == comp_dis:
            nxtqu = int(input(ques.id))
            while nxtqu > 4 :
                if nxtqu > 4 :
                    nxtqu = int(input(ques.id))
                else:
                    exit()
            data.append(nxtqu)

        else:
            continue
    result = [0, 5, 8, 12, 0]
    def show(total):
        sumRisk = 0
        for x in data:
            var = ((result[x]))
            sumRisk += var

        if sumRisk <= 25:
            print(sumRisk,msg[0])
        elif sumRisk <= 45:
            print(sumRisk,msg[1])
        elif sumRisk <= 65:
            print(sumRisk,msg[2])
        elif sumRisk <= 85:
            print(sumRisk,msg[3])

        today_date = datetime.date.today()
        mycursor.execute("INSERT INTO covid_person_risk(person_id, date, risk) VALUES(%s,%s,%s)",(id_var, today_date, sumRisk))
        mydb.commit()
    show(data)
    mycursor.execute("SELECT * FROM covid_person_risk")
    fetchtb = mycursor.fetchall()
    for x in fetchtb:
        print(x)
    exit()

def info():
    global id_var
    mycursor.execute("SELECT * FROM covid_person_info")
    fetchtb = mycursor.fetchall()
    for x in fetchtb:
        print(x)

    name = input("Enter your Name: ")
    address = input("Enter your Address: ")
    phone_no = input("Enter your Phone Number: ")
    confom = int(input("Press one for confirmed otherwise Zero \n\n"))

    name_var = name[0:3]
    phone_var = phone_no[-3:]
    id_var = name_var + phone_var

    while confom <= 1:
        if confom == 0:
            info()

        elif confom == 1 :
            mycursor.execute("INSERT INTO covid_person_info(name,address,phone_no,person_id) VALUES(%s,%s,%s,%s)",(name,address,phone_no,id_var))
            mydb.commit()
            setuques(quesAns)

        else:
            break

info()




