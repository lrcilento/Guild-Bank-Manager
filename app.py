import tkinter as tk
from manager import *

root = tk.Tk()

root.title("Guild Bank Manager v0.1")
root.geometry("1200x680")
root.resizable(False, False)
selectedMonth = tk.StringVar()

def render():
    monthFrame = tk.LabelFrame(root, text = "Selecione um mês:")
    monthFrame.grid(row = 0, column = 0, padx = 15, pady = 10)
    monthListBox = tk.Listbox(monthFrame, selectmode=tk.SINGLE, width = 28)
    months = getMonths()
    for month in months:
        monthListBox.insert(month[0], month[1])
    monthListBox.grid(row = 0, column = 0, columnspan = 2, padx = 35, pady = 5)
    newMonthButton = tk.Button(monthFrame, text = "Iniciar um novo mês", command=newMonth)
    newMonthButton.grid(row = 1, column = 0, padx = 5, pady = 5)
    def selectMonth():
        selectedMonth.set(monthListBox.get(monthListBox.curselection()))
        render()
    selectMonthButton = tk.Button(monthFrame, text = "Selecionar", command=selectMonth)
    selectMonthButton.grid(row = 1, column = 1, padx = 5, pady = 5)

    itemMenuFrame = tk.LabelFrame(root, text = "Gerenciar itens:")
    itemMenuFrame.grid(row = 1, column = 0)
    itemNameLabel = tk.Label(itemMenuFrame, text = "Nome:")
    itemNameLabel.grid(row = 0, column = 0, padx = 10, pady = 5)
    itemName = tk.StringVar()
    itemNameEntry = tk.Entry(itemMenuFrame, textvariable = itemName)
    itemNameEntry.grid(row = 0, column = 1, columnspan = 2)
    itemTypeLabel = tk.Label(itemMenuFrame, text = "Tipo:")
    itemTypeLabel.grid(row = 1, column = 0, padx = 10, pady = 5)
    itemType = tk.StringVar()
    itemTypeRadioComsumable = tk.Radiobutton(itemMenuFrame, text="Comsumível", variable = itemType, value = "Comsumível")
    itemTypeRadioComsumable.grid(row = 1, column = 1, padx = 10)
    itemTypeRadioBoE = tk.Radiobutton(itemMenuFrame, text="BoE", variable = itemType, value = "BoE")
    itemTypeRadioBoE.grid(row = 1, column = 2, padx = 10)
    def createItem(itemName, itemType):
        newItem(itemName, itemType)
        render()
    def removeItem(itemName):
        deleteItem(itemName)
        render()
    deleteItemButton = tk.Button(itemMenuFrame, text = "Remover", command=lambda: removeItem(itemName.get()))
    deleteItemButton.grid(row = 2, column = 1, padx = 5, pady = 5)
    newItemButton = tk.Button(itemMenuFrame, text = "Adicionar", command=lambda: createItem(itemName.get(), itemType.get()))
    newItemButton.grid(row = 2, column = 2, padx = 5, pady = 5)

    ranksFrame = tk.LabelFrame(root, text = "Gerenciar cargos:")
    ranksFrame.grid(row = 2, column = 0, pady = 10)
    rankNameLabel = tk.Label(ranksFrame, text = "Nome:")
    rankNameLabel.grid(row = 0, column = 0, padx = 15, pady = 5)
    rankName = tk.StringVar()
    rankNameEntry = tk.Entry(ranksFrame, textvariable = rankName)
    rankNameEntry.grid(row = 0, column = 1, columnspan = 3, padx = 18)
    rankSalaryLabel = tk.Label(ranksFrame, text = "Salário:")
    rankSalaryLabel.grid(row = 1, column = 0, padx = 15, pady = 5)
    rankSalary = tk.DoubleVar()
    rankSalaryEntry = tk.Entry(ranksFrame, textvariable = rankSalary)
    rankSalaryEntry.grid(row = 1, column = 1, columnspan = 3)
    def removeRank(rankName):
        deleteRank(rankName)
        render()
    deleteRankButton = tk.Button(ranksFrame, text = "Remover", command=lambda: removeRank(rankName.get()))
    deleteRankButton.grid(row = 2, column = 0, padx = 5, pady = 5)
    def callUpdateRank(rankName, rankSalary):
        updateRank(rankName, rankSalary)
        render()
    updateRankButton = tk.Button(ranksFrame, text = "Atualizar", command=lambda: callUpdateRank(rankName.get(), rankSalary.get()))
    updateRankButton.grid(row = 2, column = 1, padx = 5, pady = 5)
    def createRank(rankName, rankSalary):
        newRank(rankName, rankSalary)
        render()
    newRankButton = tk.Button(ranksFrame, text = "Adicionar", command=lambda: createRank(rankName.get(), rankSalary.get()))
    newRankButton.grid(row = 2, column = 2, padx = 5, pady = 5)

    councilFrame = tk.LabelFrame(root, text = "Gerenciar conselho:")
    councilFrame.grid(row = 3, column = 0)
    councilNameLabel = tk.Label(councilFrame, text = "Nome:")
    councilNameLabel.grid(row = 0, column = 0, columnspan = 2)
    councilName = tk.StringVar()
    councilNameEntry = tk.Entry(councilFrame, textvariable = councilName)
    councilNameEntry.grid(row = 1, column = 0, columnspan = 2)
    councilRanksListBox = tk.Listbox(councilFrame, selectmode=tk.SINGLE, height = 3, width = 11)
    ranks = getRanks()
    indexaux = 0
    for rank in ranks:
        councilRanksListBox.insert(indexaux, rank[0])
        indexaux += 1
    councilRanksListBox.grid(row = 0, column = 2, rowspan = 2, padx = 7)
    def removeCouncil(councilName):
        deleteCouncil(councilName)
        render()
    deleteCouncilButton = tk.Button(councilFrame, text = "Remover", command=lambda: removeCouncil(councilName.get()))
    deleteCouncilButton.grid(row = 2, column = 0, padx = 5, pady = 5)
    def changeCouncil(councilName, councilRank):
        updateCouncil(councilName, councilRank)
        render()
    updateCouncilButton = tk.Button(councilFrame, text = "Atualizar", command=lambda: changeCouncil(councilName.get(), councilRanksListBox.get(councilRanksListBox.curselection())))
    updateCouncilButton.grid(row = 2, column = 1, padx = 5, pady = 5)
    def createCouncil(councilName, councilRank):
        newCouncil(councilName, councilRank)
        render()
    newCouncilButton = tk.Button(councilFrame, text = "Adicionar", command=lambda: createCouncil(councilName.get(), councilRanksListBox.get(councilRanksListBox.curselection())))
    newCouncilButton.grid(row = 2, column = 2, padx = 5, pady = 5)

    purchasesFrame = tk.LabelFrame(root, text = "Compras:")
    purchasesFrame.grid(row = 0, column = 1, pady = 10, sticky = tk.N)
    itensListBox = tk.Listbox(purchasesFrame, selectmode=tk.SINGLE, height = 12, width = 25)
    itens = getItens()
    indexaux = 0
    for item in itens:
        itensListBox.insert(indexaux, item[0])
        indexaux += 1
    itensListBox.grid(row = 0, column = 0, rowspan = 5, padx = 15, pady = 7)
    itemQntLabel = tk.Label(purchasesFrame, text = "Quantidade:")
    itemQntLabel.grid(row = 0, column = 1, pady = 10)
    itemQnt = tk.IntVar()
    itemQntEntry = tk.Entry(purchasesFrame, textvariable = itemQnt)
    itemQntEntry.grid(row = 1, column = 1, padx = 15, pady = 10)
    itemTotalLabel = tk.Label(purchasesFrame, text = "Valor total:")
    itemTotalLabel.grid(row = 2, column = 1, pady = 10)
    itemTotal = tk.IntVar()
    itemTotalEntry = tk.Entry(purchasesFrame, textvariable = itemTotal)
    itemTotalEntry.grid(row = 3, column = 1, padx = 15, pady = 10)
    def createPurchase(itemName, itemQnt, itemTotal):
        purchase(itemName, itemQnt, itemTotal)
        render()
    buyButton = tk.Button(purchasesFrame, text = "Salvar compra", command=lambda: createPurchase(itensListBox.get(itensListBox.curselection()), itemQnt.get(), itemTotal.get()))
    buyButton.grid(row = 4, column = 1, padx = 5, pady = 15)

    boeFrame = tk.LabelFrame(root, text = "Vendas:")
    boeFrame.grid(row = 1, column = 1, rowspan = 2, sticky = tk.N)
    boeListBox = tk.Listbox(boeFrame, selectmode=tk.SINGLE, height = 12, width = 25)
    boes = getBoEs()
    indexaux = 0
    for boe in boes:
        boeListBox.insert(indexaux, boe[0])
        indexaux += 1
    boeListBox.grid(row = 0, column = 0, rowspan = 6, padx = 15, pady = 7)
    boeItemLevelLabel = tk.Label(boeFrame, text = "Item level:")
    boeItemLevelLabel.grid(row = 0, column = 1, pady = 8)
    boeItemLevel = tk.IntVar()
    boeItemLevelEntry = tk.Entry(boeFrame, textvariable = boeItemLevel)
    boeItemLevelEntry.grid(row = 1, column = 1, padx = 15)
    boeSocket = tk.StringVar()
    boeSocketCheckBox = tk.Checkbutton(boeFrame, text = "Socket?", variable = boeSocket, onvalue = "Yes", offvalue = "No")
    boeSocketCheckBox.grid(row = 2, column = 1, pady = 15)
    boePriceLabel = tk.Label(boeFrame, text = "Valor de venda:")
    boePriceLabel.grid(row = 3, column = 1)
    boePrice = tk.IntVar()
    boePriceEntry = tk.Entry(boeFrame, textvariable = boePrice)
    boePriceEntry.grid(row = 4, column = 1, padx = 15, pady = 9)
    def createSell(boeName, boeItemLevel, boeSocket, boePrice):
        sell(boeName, boeItemLevel, boeSocket, boePrice)
        render()
    sellButton = tk.Button(boeFrame, text = "Salvar venda", command=lambda: createSell(boeListBox.get(boeListBox.curselection()), boeItemLevel.get(), boeSocket.get(), boePrice.get()))
    sellButton.grid(row = 5, column = 1, padx = 5, pady = 15)

    if len(selectedMonth.get()) < 1:
        try:
            months = getMonths()
            selectedMonth.set(months[len(months)-1][1])
        except:
            newMonth()
            months = getMonths()
            selectedMonth.set(months[len(months)-1][1])
            render()
    resumeFrame = tk.LabelFrame(root, text = "Resumo ("+selectedMonth.get()+"):")
    resumeFrame.grid(row = 0, column = 2, padx = 15, pady = 10)
    resume = getResume(selectedMonth.get())
    resultLabel = tk.Label(resumeFrame, text = "Saldo atual:")
    resultLabel.grid(row = 0, column = 0, padx = 65, pady = 10)
    if resume[2] > 0:
        resultNumber = tk.Label(resumeFrame, text = str(resume[3])+"g", fg='green')
    else:
        resultNumber = tk.Label(resumeFrame, text = "-"+str(resume[3])+"g", fg='red')
    resultNumber.grid(row = 0, column = 1, padx = 65, pady = 10)
    earningsFrame = tk.LabelFrame(resumeFrame, text = "Ganhos:")
    earningsFrame.grid(row = 1, column = 0, columnspan = 2, pady = 5, padx = 5)
    tk.Label(earningsFrame, text = "Vendas:").grid(row = 0, column = 0, padx = 82)
    tk.Label(earningsFrame, text = str(resume[0])+"g", fg='green').grid(row = 0, column = 1, padx = 49)
    expenduresFrame = tk.LabelFrame(resumeFrame, text = "Gastos:")
    expenduresFrame.grid(row = 2, column = 0, columnspan = 2)
    tk.Label(expenduresFrame, text = "Comsumíveis:").grid(row = 0, column = 0, padx = 49)
    tk.Label(expenduresFrame, text = "-"+str(resume[1])+"g", fg='red').grid(row = 0, column = 1, padx = 44)
    tk.Label(expenduresFrame, text = "Pagamentos:").grid(row = 1, column = 0, padx = 60)
    tk.Label(expenduresFrame, text = "-"+str(resume[2])+"g", fg='red').grid(row = 1, column = 1, padx = 55)
    salaryFrame = tk.LabelFrame(resumeFrame, text = "Pagamentos:")
    salaryFrame.grid(row = 3, column = 0, columnspan = 2, pady = 7, padx = 5)
    indexaux = 0
    for rank in ranks:
        tk.Label(salaryFrame, text = rank[0]+":").grid(row = indexaux, column = 0, padx = 58)
        tk.Label(salaryFrame, text = str(int(resume[0]*rank[1]))+"g").grid(row = indexaux, column = 1, padx = 58)
        indexaux += 1
    transactionsFrame = tk.LabelFrame(root, text = "Transações:")
    transactionsFrame.grid(row = 1, column = 2, rowspan = 2, padx = 15, sticky = tk.N)
    transactionsListBox = tk.Listbox(transactionsFrame, selectmode=tk.SINGLE, width = 45, height = 9)
    transactions = getTransactions(selectedMonth.get())
    indexaux = 0
    for transaction in transactions:
        transactionsListBox.insert(transaction[0], transaction[2])
        indexaux =+ 1
    transactionsListBox.grid(row = 0, column = 0, padx = 18, pady = 9)
    #TODO: Criar o botão de "verificar transação"
    def removeTransaction(transactionString):
        trimString(transactionString, selectedMonth.get())
        render()
    removeTransactionButton = tk.Button(transactionsFrame, text = "Reverter", command = lambda: removeTransaction(transactionsListBox.get(transactionsListBox.curselection())))
    removeTransactionButton.grid(row = 1, pady = 10)

render()
root.mainloop()