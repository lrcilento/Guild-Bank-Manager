import tkinter.messagebox
import mysql.connector
import datetime

db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "passwd",
    database = "Dagon"
)

def getMonths():
    months = []
    try:
        sql = "SELECT ID, NAME FROM Earnings"
        cursor = db.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        for row in result:
            months.append(row)
    except mysql.connector.Error as err:
        tkinter.messagebox.showerror("Erro!", err)
    return months

def getCouncil():
    council = []
    try:
        sql = "SELECT Council.RANK_NAME, Council.COUNSELOR, Ranks.PAYMENT FROM Council INNER JOIN Ranks ON Council.RANK_NAME=Ranks.NAME"
        cursor = db.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        for row in result:
            council.append(row)
    except mysql.connector.Error as err:
        tkinter.messagebox.showerror("Erro!", err)
    return council

def getRanks():
    ranks = []
    try:
        sql = "SELECT NAME, PAYMENT FROM Ranks"
        cursor = db.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        for row in result:
            ranks.append(row)
    except mysql.connector.Error as err:
        tkinter.messagebox.showerror("Erro!", err)
    return ranks

def getItens():
    itens = []
    try:
        sql = "SELECT NAME FROM Itens WHERE TYPE = 'Comsumível'"
        cursor = db.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        for row in result:
            itens.append(row)
    except mysql.connector.Error as err:
        tkinter.messagebox.showerror("Erro!", err)
    return itens

def getBoEs():
    boes = []
    try:
        sql = "SELECT NAME FROM Itens WHERE TYPE = 'BoE'"
        cursor = db.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        for row in result:
            boes.append(row)
    except mysql.connector.Error as err:
        tkinter.messagebox.showerror("Erro!", err)
    return boes

def newMonth():
    monthName = datetime.date.today().strftime("%B")
    month = datetime.date.today().month
    year = datetime.date.today().year
    rowID = int(str(month) + str(year))
    rowName = str(monthName) + " " + str(year)
    sql = "INSERT INTO Earnings (ID, NAME, MONTH, YEAR, BOE_EARNINGS, TOTAL_PURCHASES, TOTAL_SALARIES, RESULT) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    values = (rowID, rowName, month, year, 0, 0, 0, 0)
    try:
        cursor = db.cursor()
        cursor.execute(sql, values)
        db.commit()
        cursor.close()
        tkinter.messagebox.showinfo("Sucesso!", "Mês inicializado com sucesso!")
    except mysql.connector.Error as err:
        tkinter.messagebox.showerror("Erro!", err)

def newItem(itemName, itemType):
    if len(itemName) > 0 and len(itemType) > 0:
        sql = "INSERT INTO Itens (NAME, TYPE) VALUES (%s, %s)"
        values = (itemName, itemType)
        try:
            cursor = db.cursor()
            cursor.execute(sql, values)
            db.commit()
            cursor.close()
            tkinter.messagebox.showinfo("Sucesso!", "Item criado com sucesso!")
        except mysql.connector.Error as err:
            tkinter.messagebox.showerror("Erro!", err)

def newRank(rankName, rankSalary):
    if len(rankName) > 0 and rankSalary > 0:
        sql = "INSERT INTO Ranks (NAME, PAYMENT) VALUES (%s, %s)"
        values = (rankName, rankSalary)
        try:
            cursor = db.cursor()
            cursor.execute(sql, values)
            db.commit()
            cursor.close()
            tkinter.messagebox.showinfo("Sucesso!", "Cargo criado com sucesso!")
        except mysql.connector.Error as err:
            tkinter.messagebox.showerror("Erro!", err)

def newCouncil(councilName, councilRank):
    if len(councilName) > 0 and len(councilRank) > 0:
        month = datetime.date.today().month
        year = datetime.date.today().year
        date = int(str(month) + str(year))
        sql = "SELECT TOTAL_SALARIES, RESULT, BOE_EARNINGS, SERVICE_EARNINGS FROM Earnings WHERE ID = {0}".format(date)
        try:
            cursor = db.cursor()
            cursor.execute(sql)
            earningsData = cursor.fetchone()
            sql = "SELECT PAYMENT FROM Ranks WHERE NAME = '{0}'".format(councilRank)
            try:
                cursor.execute(sql)
                ranksData = cursor.fetchone()
                sql = "UPDATE Earnings SET TOTAL_SALARIES = {0}, RESULT = {1} WHERE ID = {2}".format(earningsData[0]+(earningsData[2]*ranksData[0])+(earningsData[3]*ranksData[0]), earningsData[1]-(earningsData[2]*ranksData[0])-(earningsData[3]*ranksData[0]), date)
                try:
                    cursor.execute(sql)
                    db.commit()
                    sql = "INSERT INTO Council (COUNSELOR, RANK_NAME) VALUES (%s, %s)"
                    values = (councilName, councilRank)
                    try:           
                        cursor.execute(sql, values)
                        db.commit()
                        cursor.close()
                        tkinter.messagebox.showinfo("Sucesso!", "Conselheiro adicionado com sucesso!")
                    except mysql.connector.Error as err:
                        tkinter.messagebox.showerror("Erro!", err)
                except mysql.connector.Error as err:
                    tkinter.messagebox.showerror("Erro!", err)
            except mysql.connector.Error as err:
                tkinter.messagebox.showerror("Erro!", err)
        except mysql.connector.Error as err:
            tkinter.messagebox.showerror("Erro!", err)

def deleteItem(itemName):
    if len(itemName) > 0:
        sql = "DELETE FROM Itens WHERE NAME = '{0}'".format(itemName)
        try:
            cursor = db.cursor()
            cursor.execute(sql)
            db.commit()
            cursor.close()
            tkinter.messagebox.showinfo("Sucesso!", "Item deletado com sucesso!")
        except mysql.connector.Error as err:
            tkinter.messagebox.showerror("Erro!", err)

def deleteRank(rankName):
    if len(rankName) > 0:
        sql = "DELETE FROM Ranks WHERE NAME = '{0}'".format(rankName)
        try:
            cursor = db.cursor()
            cursor.execute(sql)
            db.commit()
            cursor.close()
            tkinter.messagebox.showinfo("Sucesso!", "Cargo deletado com sucesso!")
        except mysql.connector.Error as err:
            tkinter.messagebox.showerror("Erro!", err)

def deleteCouncil(councilName):
    if len(councilName) > 0:
        month = datetime.date.today().month
        year = datetime.date.today().year
        date = int(str(month) + str(year))
        sql = "SELECT TOTAL_SALARIES, RESULT, BOE_EARNINGS, SERVICE_EARNINGS FROM Earnings WHERE ID = {0}".format(date)
        try:
            cursor = db.cursor()
            cursor.execute(sql)
            earningsData = cursor.fetchone()
            sql = "SELECT RANK_NAME FROM Council WHERE COUNSELOR = '{0}'".format(councilName)
            try:
                cursor.execute(sql)
                councilData = cursor.fetchone()
                sql = "SELECT PAYMENT FROM Ranks WHERE NAME = '{0}'".format(councilData[0])
                try:
                    cursor.execute(sql)
                    ranksData = cursor.fetchone()
                    sql = "UPDATE Earnings SET TOTAL_SALARIES = {0}, RESULT = {1} WHERE ID = {2}".format(earningsData[0]-(earningsData[2]*ranksData[0])-(earningsData[3]*ranksData[0]), earningsData[1]+(earningsData[2]*ranksData[0])+(earningsData[3]*ranksData[0]), date)
                    try:
                        cursor.execute(sql)
                        db.commit()
                        sql = "DELETE FROM Council WHERE COUNSELOR = '{0}'".format(councilName)
                        try:
                            cursor = db.cursor()
                            cursor.execute(sql)
                            db.commit()
                            cursor.close()
                            tkinter.messagebox.showinfo("Sucesso!", "Conselheiro removido com sucesso!")
                        except mysql.connector.Error as err:
                            tkinter.messagebox.showerror("Erro!", err)
                    except mysql.connector.Error as err:
                        tkinter.messagebox.showerror("Erro!", err)
                except mysql.connector.Error as err:
                    tkinter.messagebox.showerror("Erro!", err)
            except mysql.connector.Error as err:
                tkinter.messagebox.showerror("Erro!", err)
        except mysql.connector.Error as err:
            tkinter.messagebox.showerror("Erro!", err)

def updateRank(rankName, rankSalary):
    if len(rankName) > 0 and rankSalary > 0:
        everythingOK = True
        month = datetime.date.today().month
        year = datetime.date.today().year
        date = int(str(month) + str(year))
        sql = "SELECT TOTAL_SALARIES, RESULT, BOE_EARNINGS, SERVICE_EARNINGS FROM Earnings WHERE ID = {0}".format(date)
        try:
            cursor = db.cursor()
            cursor.execute(sql)
            earningsData = cursor.fetchone()
            sql = "SELECT PAYMENT FROM Ranks WHERE NAME = '{0}'".format(rankName)
            try:
                cursor.execute(sql)
                oldSalaryData = cursor.fetchone()
                if rankSalary > oldSalaryData[0]:
                    salaryDiff = rankSalary - oldSalaryData[0]
                    finalSQL = "UPDATE Earnings SET TOTAL_SALARIES = {0}, RESULT = {1} WHERE ID = {2}".format(earningsData[0]+(earningsData[2]*salaryDiff)+(earningsData[3]*salaryDiff), earningsData[1]-(earningsData[2]*salaryDiff)-(earningsData[3]*salaryDiff), date)
                else:
                    salaryDiff = oldSalaryData[0] - rankSalary
                    finalSQL = "UPDATE Earnings SET TOTAL_SALARIES = {0}, RESULT = {1} WHERE ID = {2}".format(earningsData[0]-(earningsData[2]*salaryDiff)-(earningsData[3]*salaryDiff), earningsData[1]+(earningsData[2]*salaryDiff)+(earningsData[3]*salaryDiff), date)
                sql = "SELECT COUNSELOR FROM Council WHERE RANK_NAME = '{0}'".format(rankName)
                try:
                    cursor.execute(sql)
                    councilData = cursor.fetchall()
                    if len(councilData) > 0:
                        for counselor in councilData:
                            everythingOK = False
                            try:
                                cursor.execute(finalSQL)
                                db.commit()
                                everythingOK = True
                            except mysql.connector.Error as err:
                                tkinter.messagebox.showerror("Erro!", err)
                    if everythingOK:
                        sql = "UPDATE Ranks SET PAYMENT = {0} WHERE NAME = '{1}'".format(rankSalary, rankName)
                        try:
                            cursor = db.cursor()
                            cursor.execute(sql)
                            db.commit()
                            cursor.close()
                            tkinter.messagebox.showinfo("Sucesso!", "Cargo atualizado com sucesso!")
                        except mysql.connector.Error as err:
                            tkinter.messagebox.showerror("Erro!", err)
                except mysql.connector.Error as err:
                    tkinter.messagebox.showerror("Erro!", err)
            except mysql.connector.Error as err:
                tkinter.messagebox.showerror("Erro!", err)
        except mysql.connector.Error as err:
            tkinter.messagebox.showerror("Erro!", err)

def updateCouncil(councilName, councilRank):
    if len(councilName) > 0 and len(councilRank) > 0:
        everythingOK = True
        month = datetime.date.today().month
        year = datetime.date.today().year
        date = int(str(month) + str(year))
        sql = "SELECT TOTAL_SALARIES, RESULT, BOE_EARNINGS, SERVICE_EARNINGS FROM Earnings WHERE ID = {0}".format(date)
        try:
            cursor = db.cursor()
            cursor.execute(sql)
            earningsData = cursor.fetchone()
            sql = "SELECT PAYMENT FROM Ranks WHERE NAME = '{0}'".format(councilRank)
            try:
                cursor.execute(sql)
                newPaymentData = cursor.fetchone()
                sql = "SELECT RANK_NAME FROM Council WHERE COUNSELOR = '{0}'".format(councilName)
                try:
                    cursor.execute(sql)
                    councilData = cursor.fetchone()
                    sql = "SELECT PAYMENT FROM Ranks WHERE NAME = '{0}'".format(councilData[0])
                    try:
                        cursor.execute(sql)
                        oldPaymentData = cursor.fetchone()
                        if oldPaymentData[0] > newPaymentData[0]:
                            everythingOK = False
                            paymentDiff = oldPaymentData[0] - newPaymentData[0]
                            sql = "UPDATE Earnings SET TOTAL_SALARIES = {0}, RESULT = {1} WHERE ID = {2}".format(earningsData[0]-(earningsData[2]*paymentDiff)-(earningsData[3]*paymentDiff), earningsData[1]+(earningsData[2]*paymentDiff)+(earningsData[3]*paymentDiff), date)
                            try:
                                cursor.execute(sql)
                                db.commit()
                                everythingOK = True
                            except mysql.connector.Error as err:
                                tkinter.messagebox.showerror("Erro!", err)
                        elif oldPaymentData[0] < newPaymentData[0]:
                            everythingOK = False
                            paymentDiff = newPaymentData[0] - oldPaymentData[0]
                            sql = "UPDATE Earnings SET TOTAL_SALARIES = {0}, RESULT = {1} WHERE ID = {2}".format(earningsData[0]+(earningsData[2]*paymentDiff)+(earningsData[3]*paymentDiff), earningsData[1]-(earningsData[2]*paymentDiff)-(earningsData[3]*paymentDiff), date)
                            try:
                                cursor.execute(sql)
                                db.commit()
                                everythingOK = True
                            except mysql.connector.Error as err:
                                tkinter.messagebox.showerror("Erro!", err)
                        if everythingOK:
                            sql = "UPDATE Council SET RANK_NAME = '{0}' WHERE COUNSELOR = '{1}'".format(councilRank, councilName)
                            try:           
                                cursor.execute(sql)
                                db.commit()
                                cursor.close()
                                tkinter.messagebox.showinfo("Sucesso!", "Conselheiro atualizado com sucesso!")
                            except mysql.connector.Error as err:
                                tkinter.messagebox.showerror("Erro!", err)
                    except mysql.connector.Error as err:
                        tkinter.messagebox.showerror("Erro!", err)
                except mysql.connector.Error as err:
                    tkinter.messagebox.showerror("Erro!", err)
            except mysql.connector.Error as err:
                tkinter.messagebox.showerror("Erro!", err)
        except mysql.connector.Error as err:
            tkinter.messagebox.showerror("Erro!", err)

def purchase(itemName, itemQnt, itemTotal):
    if itemQnt > 0 and itemTotal > 0:
        month = datetime.date.today().month
        year = datetime.date.today().year
        date = int(str(month) + str(year))
        day = datetime.date.today().day
        sql = "INSERT INTO Purchases (ITEM, QNT, TOTAL, TRANSACTION_DATE, TRANSACTION_DAY) VALUES (%s, %s, %s, %s, %s)"
        values = (itemName, itemQnt, itemTotal, date, day)
        try:
            cursor = db.cursor()
            cursor.execute(sql, values)
            db.commit()
            try:
                sql = "SELECT TOTAL_PURCHASES, RESULT FROM Earnings WHERE ID = {0}".format(date)
                cursor.execute(sql)
                result = cursor.fetchone()
                try:
                    sql = "UPDATE Earnings SET TOTAL_PURCHASES={0}, RESULT={1} WHERE ID = {2}".format(result[0]+itemTotal, result[1]-itemTotal, date)
                    cursor.execute(sql)
                    db.commit()
                    cursor.close()
                    tkinter.messagebox.showinfo("Sucesso!", "Compra salva com sucesso!")
                except mysql.connector.Error as err:
                    tkinter.messagebox.showerror("Erro!", err)
            except mysql.connector.Error as err:
                tkinter.messagebox.showerror("Erro!", err)
        except mysql.connector.Error as err:
            tkinter.messagebox.showerror("Erro!", err)
    
def sell(boeName, boeItemLevel, boeSocket, boePrice):
    if boeItemLevel > 0 and boePrice > 0:
        if len(boeSocket) == 0:
            boeSocket = "No"
        month = datetime.date.today().month
        year = datetime.date.today().year
        date = int(str(month) + str(year))
        day = datetime.date.today().day
        sql = "INSERT INTO BoEs (ITEM, ILVL, SOCKET, PRICE, TRANSACTION_DATE, TRANSACTION_DAY) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (boeName, boeItemLevel, boeSocket, boePrice, date, day)
        try:
            cursor = db.cursor()
            cursor.execute(sql, values)
            db.commit()
            try:
                sql = "SELECT BOE_EARNINGS, TOTAL_SALARIES, RESULT FROM Earnings WHERE ID = {0}".format(date)
                cursor.execute(sql)
                result = cursor.fetchone()
                calculatedTax = calculateTax(boePrice)
                try:
                    sql = "UPDATE Earnings SET BOE_EARNINGS={0}, TOTAL_SALARIES={1}, RESULT={2} WHERE ID={3}".format(result[0]+boePrice, result[1]+calculatedTax[1], result[2]+calculatedTax[0], date)
                    cursor.execute(sql)
                    db.commit()
                    cursor.close()
                    tkinter.messagebox.showinfo("Sucesso!", "Venda salva com sucesso!")
                except mysql.connector.Error as err:
                    tkinter.messagebox.showerror("Erro ao atualizar!", err)
            except mysql.connector.Error as err:
                tkinter.messagebox.showerror("Erro ao selecionar!", err)
        except mysql.connector.Error as err:
            tkinter.messagebox.showerror("Erro ao inserir!", err)

def order(serviceName, serviceBuyerName, serviceSellerName, servicePrice):
    if servicePrice > 0 and len(serviceBuyerName) > 0 and len(serviceSellerName) > 0:
        month = datetime.date.today().month
        year = datetime.date.today().year
        date = int(str(month) + str(year))
        day = datetime.date.today().day
        sql = "SELECT GUILD_SHARE FROM Packages WHERE NAME='{0}'".format(serviceName)
        try:
            cursor = db.cursor()
            cursor.execute(sql)
            serviceGuildShare = cursor.fetchone()
            print(serviceGuildShare[0])
        except mysql.connector.Error as err:
            tkinter.messagebox.showerror("Erro ao selecionar guild_share!", err)

        sql = "INSERT INTO Services (PACKAGE, BUYER, SELLER, PRICE, TRANSACTION_DATE, TRANSACTION_DAY) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (serviceName, serviceBuyerName, serviceSellerName, servicePrice*serviceGuildShare[0], date, day)
        try:
            cursor = db.cursor()
            cursor.execute(sql, values)
            db.commit()
            try:
                sql = "SELECT SERVICE_EARNINGS, TOTAL_SALARIES, RESULT FROM Earnings WHERE ID = {0}".format(date)
                cursor.execute(sql)
                result = cursor.fetchone()
                calculatedTax = calculateTax(servicePrice)
                try:
                    sql = "UPDATE Earnings SET SERVICE_EARNINGS={0}, TOTAL_SALARIES={1}, RESULT={2} WHERE ID={3}".format(result[0]+servicePrice, result[1]+calculatedTax[1], result[2]+calculatedTax[0], date)
                    cursor.execute(sql)
                    db.commit()
                    cursor.close()
                    tkinter.messagebox.showinfo("Sucesso!", "Ordem salva com sucesso!")
                except mysql.connector.Error as err:
                    tkinter.messagebox.showerror("Erro ao atualizar!", err)
            except mysql.connector.Error as err:
                tkinter.messagebox.showerror("Erro ao selecionar!", err)
        except mysql.connector.Error as err:
            tkinter.messagebox.showerror("Erro ao inserir!", err)

def getResume(monthName):
    sql = "SELECT BOE_EARNINGS, TOTAL_PURCHASES, TOTAL_SALARIES, RESULT, SERVICE_EARNINGS FROM Earnings WHERE NAME = '{0}'".format(monthName)
    try:
        cursor = db.cursor()
        cursor.execute(sql)
        result = cursor.fetchone()
        return result
    except mysql.connector.Error as err:
        tkinter.messagebox.showerror("Erro!", err)
    
def calculateTax(amount):
    sql = "SELECT DISTINCT RANK_NAME FROM Council"
    tax = 0
    council = []
    try:
        cursor = db.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        for row in result:
            sql = "SELECT COUNT(RANK_NAME) FROM Council WHERE RANK_NAME = '{0}'".format(row[0])
            try:
                cursor.execute(sql)
                size = cursor.fetchone()
                sql = "SELECT PAYMENT FROM Ranks WHERE NAME = '{0}'".format(row[0])
                try:
                    cursor.execute(sql)
                    payment = cursor.fetchone()
                    council.append({"rank_name":row[0], "amount":size[0], "percent":payment[0]})
                except mysql.connector.Error as err:
                    tkinter.messagebox.showerror("Erro ao selecionar!", err)
            except mysql.connector.Error as err:
                tkinter.messagebox.showerror("Erro ao selecionar!", err)
        for rank in council:
            tax += amount * (rank['percent']*rank['amount'])
        amount -= tax
        return [amount, tax]
    except mysql.connector.Error as err:
        tkinter.messagebox.showerror("Erro ao selecionar!", err)

def getTransactions(date):
    def sortFunc(e):
        return e[len(e)-1]
    sql = "SELECT ID FROM Earnings WHERE NAME = '{0}'".format(date)
    transactions = []
    final = []
    try:
        cursor = db.cursor()
        cursor.execute(sql)
        date_id = cursor.fetchone()[0]
        sql = "SELECT * FROM BoEs WHERE TRANSACTION_DATE = {0}".format(date_id)
        try:
            cursor.execute(sql)
            result = cursor.fetchall()
            for row in result:
                transactions.append(row)
            sql = "SELECT * FROM Services WHERE TRANSACTION_DATE = {0}".format(date_id)
            try:
                cursor.execute(sql)
                result = cursor.fetchall()
                for row in result:
                    transactions.append(row)
                sql = "SELECT * FROM Purchases WHERE TRANSACTION_DATE = {0}".format(date_id)
                try:
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    for row in result:
                        transactions.append(row)
                    transactions.sort(key=sortFunc)
                    for transaction in transactions:
                        if len(transaction) == 7:
                            if transaction[4] == "No":
                                socketed = ""
                                final.append([transaction[0], "BoE", transaction[1]+" ("+str(transaction[3])+socketed+"): +"+str(transaction[2])+"g"])
                            elif transaction[4] == "Yes":
                                socketed = " - Socketed"
                                final.append([transaction[0], "BoE", transaction[1]+" ("+str(transaction[3])+socketed+"): +"+str(transaction[2])+"g"])
                            else:
                                final.append([transaction[0], "Serviço", transaction[1]+" ("+str(transaction[3])+" -> "+str(transaction[2])+"): +"+str(transaction[4])+"g"])
                        else:
                            final.append([transaction[0], "Consumível", str(transaction[2])+"x "+transaction[1]+": -"+str(transaction[3])+"g"])
                    return final
                except mysql.connector.Error as err:
                    tkinter.messagebox.showerror("Erro ao selecionar!", err)
            except mysql.connector.Error as err:
                tkinter.messagebox.showerror("Erro ao selecionar!", err)
        except mysql.connector.Error as err:
            tkinter.messagebox.showerror("Erro ao selecionar!", err)
    except mysql.connector.Error as err:
        tkinter.messagebox.showerror("Erro ao selecionar!", err)

def trimString(transactionString, date):
    if "(" in transactionString and "->" in transactionString:
        transactionList = transactionString.split()
        transactionList[len(transactionList)-1] = transactionList[len(transactionList)-1].replace('g', '').replace('+', '')
        transactionList[len(transactionList)-2] = transactionList[len(transactionList)-2].replace('):', '')
        transactionList.pop(len(transactionList)-3)
        transactionList[len(transactionList)-3] = transactionList[len(transactionList)-3].replace('(', '')
        for word in range(1, len(transactionList)-3):
            transactionList[0] += " "+transactionList[word]
        for word in range(1, len(transactionList)-3):
            transactionList.pop(1)
        transactionList.append("Service")

    elif "(" in transactionString and "Socketed" not in transactionString:
        transactionList = transactionString.split()
        transactionList[len(transactionList)-1] = transactionList[len(transactionList)-1].replace('g', '').replace('+', '')
        transactionList[len(transactionList)-2] = transactionList[len(transactionList)-2].replace('(', '').replace('):', '')
        for word in range(1, len(transactionList)-2):
            transactionList[0] += " "+transactionList[word]
        for word in range(1, len(transactionList)-2):
            transactionList.pop(1)
        transactionList.append("Unsocketed")
        transactionList.append("BoE")

    elif "(" in transactionString and "Socketed" in transactionString:
        transactionList = transactionString.split()
        transactionList[len(transactionList)-1] = transactionList[len(transactionList)-1].replace('g', '').replace('+', '')
        transactionList.pop(len(transactionList)-2)
        transactionList.pop(len(transactionList)-2)
        transactionList[len(transactionList)-2] = transactionList[len(transactionList)-2].replace('(', '')
        for word in range(1, len(transactionList)-2):
            transactionList[0] += " "+transactionList[word]
        for word in range(1, len(transactionList)-2):
            transactionList.pop(1)
        transactionList.append("Socketed")
        transactionList.append("BoE")

    else:
        transactionList = transactionString.split()
        transactionList[len(transactionList)-1] = transactionList[len(transactionList)-1].replace('g', '').replace('-', '')
        transactionList[len(transactionList)-2] = transactionList[len(transactionList)-2].replace(':', '')
        transactionList[0] = transactionList[0].replace('x', '')
        for word in range(2, len(transactionList)-1):
            transactionList[1] += " "+transactionList[word]
        for word in range(1, len(transactionList)-2):
            transactionList.pop(2)
        transactionList.append("Consumable")
    
    print(transactionList)
    deleteTransaction(transactionList, date)

def deleteTransaction(transactionList, date):
    month = datetime.date.today().month
    year = datetime.date.today().year
    date = int(str(month) + str(year))
    get_old_data = "SELECT BOE_EARNINGS, TOTAL_PURCHASES, TOTAL_SALARIES, RESULT, SERVICE_EARNINGS FROM Earnings WHERE ID = {0}".format(date)
    try:
        cursor = db.cursor()
        cursor.execute(get_old_data)
        results = cursor.fetchone()
    except mysql.connector.Error as err:
        tkinter.messagebox.showerror("Erro!", err)
    if "BoE" in transactionList:
        if "Unsocketed" in transactionList:
            socketed = "No"
        else:
            socketed = "Yes"
        sql = "DELETE FROM BoEs WHERE ITEM='{0}' AND ILVL={1} AND SOCKET='{2}' AND PRICE={3}".format(transactionList[0], transactionList[1], socketed, transactionList[2])
        calculatedTax = calculateTax(int(transactionList[2]))
        secondsql = "UPDATE Earnings SET BOE_EARNINGS={0}, TOTAL_SALARIES={1}, RESULT={2} WHERE ID={3}".format(results[0]-int(transactionList[2]), results[2]-calculatedTax[1], results[3]-calculatedTax[0], date)
    elif "Service" in transactionList:
        sql = "DELETE FROM Services WHERE PACKAGE='{0}' AND SELLER='{1}' AND BUYER='{2}' AND PRICE={3}".format(transactionList[0], transactionList[1], transactionList[2], transactionList[3])
        calculatedTax = calculateTax(int(transactionList[3]))
        secondsql = "UPDATE Earnings SET SERVICE_EARNINGS={0}, TOTAL_SALARIES={1}, RESULT={2} WHERE ID={3}".format(results[4]-int(transactionList[3]), results[2]-calculatedTax[1], results[3]-calculatedTax[0], date)
    else:
        sql = "DELETE FROM Purchases WHERE ITEM='{0}' AND QNT={1} AND TOTAL={2}".format(transactionList[1], transactionList[0], transactionList[2])
        secondsql = "UPDATE Earnings SET TOTAL_PURCHASES={0}, RESULT={1} WHERE ID={2}".format(results[1]-int(transactionList[2]), results[3]+int(transactionList[2]), date)
    try:
        cursor.execute(secondsql)
        db.commit()
        try:
            cursor.execute(sql)
            db.commit()
            cursor.close()
            tkinter.messagebox.showinfo("Sucesso!", "Transação revertida com sucesso!")
        except mysql.connector.Error as err:
            tkinter.messagebox.showerror("Erro!", err)
    except mysql.connector.Error as err:
            tkinter.messagebox.showerror("Erro!", err)

def updatePackage(packageName, packageShare):
    if len(packageName) > 0 and packageShare > 0:
        sql = "UPDATE Packages SET GUILD_SHARE = {0} WHERE NAME = '{1}'".format(packageShare, packageName)
        try:
            cursor = db.cursor()
            cursor.execute(sql)
            db.commit()
            cursor.close()
            tkinter.messagebox.showinfo("Sucesso!", "Serviço atualizado com sucesso!")
        except mysql.connector.Error as err:
            tkinter.messagebox.showerror("Erro!", err)

def newPackage(packageName, packageShare):
    if len(packageName) > 0 and packageShare > 0:
        sql = "INSERT INTO Packages (NAME, GUILD_SHARE) VALUES (%s, %s)"
        values = (packageName, packageShare)
        try:
            cursor = db.cursor()
            cursor.execute(sql, values)
            db.commit()
            cursor.close()
            tkinter.messagebox.showinfo("Sucesso!", "Serviço criado com sucesso!")
        except mysql.connector.Error as err:
            tkinter.messagebox.showerror("Erro!", err)

def deletePackage(packageName):
    if len(packageName) > 0:
        sql = "DELETE FROM Packages WHERE NAME = '{0}'".format(packageName)
        try:
            cursor = db.cursor()
            cursor.execute(sql)
            db.commit()
            cursor.close()
            tkinter.messagebox.showinfo("Sucesso!", "Serviço deletado com sucesso!")
        except mysql.connector.Error as err:
            tkinter.messagebox.showerror("Erro!", err)

def getPackages():
    packages = []
    try:
        sql = "SELECT * FROM Packages"
        cursor = db.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        for row in result:
            packages.append(row)
    except mysql.connector.Error as err:
        tkinter.messagebox.showerror("Erro!", err)
    return packages