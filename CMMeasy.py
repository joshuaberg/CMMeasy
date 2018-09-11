#!/usr/bin/env python3
from tkinter import *
from tkinter import filedialog
import csv
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import os

root = Tk()

def getFileName():
    file = filedialog.askopenfilename(title = "Select file",filetypes = (("csv files","*.csv"),("all files","*.*")))
    fileName.configure(text=file)
    return(fileName)

def returnStats():
    filename = filedialog.askopenfilename(title = "Make or Select Text File",filetypes = (("txt files","*.txt"),("all files","*.*")))
    #Overwrite the file and delete all previous content
    file = open(filename,'w')
    file.close()

    cavities = getCavities();
    dataSet = createDataSet(cavities);
    statResults(dataSet,cavities,filename)

def returnHistograms():
    foldername = filedialog.askdirectory(title = "Where do you want to save the histograms?")
    cavities = getCavities();
    dataSet = createDataSet(cavities);
    plotHistograms(dataSet,cavities,foldername)

def returnDatabyDate():
    foldername = filedalog.askdirectory(title = "Where do you want to save the scatter plots?")
    cavities = getCavities();
    dataSet = createDataSet(cavities);
    plotbyDate(dataSet,cavities,foldername)

#Get and clean up cavity names for the data analysis
def getCavities():
    data = fileName.cget("text")

    with open(data) as f:
        data = csv.reader(f)
        for row in data:
            currentCav = row[int(cavity_col.get())]
            if currentCav in cavities:
                pass
            else:
                cavities.append(currentCav)

    print('Raw Cavity Names')
    print(cavities , '\n')
    # Clean up Cavity Names
    # Remove all cavity names that aren't 2 or 3 letters
    for item in sorted(cavities):
        if len(item) > 3:
            cavities.remove(item)
        elif len(item) < 2:
            cavities.remove(item)
    # Get rid of Lower Case Letters (can edit to fix instead of remove)
    for item in sorted(cavities):
          if item[-1] != 'A' and item[-1] != 'B':
              cavities.remove(item)
    print('Cleaned Cavity Names')
    print(cavities)
    return(cavities)


def createDataSet(cavities):
    dataSet = {}
    for item in cavities:
        #dataSets[item] = "cavity_{}".format(item)
        dataSet[item] = createMatrix(item)
    return(dataSet)

#Creates Matrix of all the data in the CSV file for one CavityName
def createMatrix(cavityName):
    data = fileName.cget("text")
    matrix = []
    date = []
    A = []
    B = []
    C = []
    D = []
    E = []
    F = []

    with open(data) as f:
        file = csv.reader(f)
        for row in file:
            currentCav = row[int(cavity_col.get())]
            if currentCav == cavityName:
                date.append(row[int(date_col.get())])
                A.append(float(row[int(param_A_col.get())]))
                B.append(float(row[int(param_B_col.get())]))
                C.append(float(row[int(param_C_col.get())]))
                D.append(float(row[int(param_D_col.get())]))
                E.append(float(row[int(param_E_col.get())]))
                F.append(float(row[int(param_F_col.get())]))

    matrix = [date,A,B,C,D,E,F]
    return(matrix)

def cp(data,lsl,usl):
    arr = np.array(data).astype(np.float)
    arr = arr.ravel()
    sigma = np.std(arr)
    cp = float(usl - lsl) / (6*sigma)
    cp = round(cp,3)
    return(cp)

def cpk(data,lsl,usl):
    arr = np.array(data).astype(np.float)
    sigma = np.std(arr)
    m = np.mean(arr)

    cpu = float(usl - m) / (3*sigma)
    cpl = float(m - lsl) / (3*sigma)
    cpk = np.min([cpu , cpl])
    cpk = round(cpk,3)
    return(cpk)

def statResults(dataSet,cavities, filename):
    for cavity in sorted(cavities):
        A = dataSet[cavity][1]
        B = dataSet[cavity][2]
        C = dataSet[cavity][3]
        D = dataSet[cavity][4]
        E = dataSet[cavity][5]
        F = dataSet[cavity][6]

        print("\n" + cavity)

        file = open(filename,'a')
        file.write(str(cavity) + '\n')
        file.close()

        statistics(param_A_name.get(), A , cavity , float(param_A_LSL.get()) , float(param_A_USL.get()) , filename, 1)
        print("\n")
        statistics(param_B_name.get(), B , cavity , float(param_B_LSL.get()) , float(param_B_USL.get()), filename, 1)
        print("\n")
        statistics(param_C_name.get(), C , cavity , float(param_C_LSL.get()) , float(param_C_USL.get()) , filename, 1)
        print("\n")
        statistics(param_D_name.get(), D , cavity , float(param_D_LSL.get()) , float(param_D_USL.get()) , filename, 1)
        print("\n")
        statistics(param_E_name.get(), E , cavity , float(param_E_LSL.get()) , float(param_E_USL.get()) , filename, 1)
        print("\n")
        statistics(param_F_name.get(), F , cavity , float(param_F_LSL.get()) , float(param_F_USL.get()) , filename, 1)
        print("\n")

def statistics(label,data,cavity,LSL,USL, filename, print_flag):
    if print_flag == 1:
       file = open(filename,'a')

    length = len(data)
    minimum = min(data)
    maximum = max(data)
    rangeData = round(np.ptp(data),3)
    mean = round(np.mean(data),3)
    median = round(np.median(data),3)
    sigma = round(np.std(data),3)
    CP = cp(data,LSL,USL)
    CPK = cpk(data,LSL,USL)
    results = [label, cavity, length, minimum, maximum, rangeData, mean, median, sigma, CP, CPK]

    if print_flag == 1:
        file.write(label + " datapoints : ".rstrip('\n'))
        file.write(str(length))
        file.write("\n")
        file.write("       min {} : ".format(label).rstrip('\n'))
        file.write(str(minimum))
        file.write("\n")
        file.write("       max {} : ".format(label).rstrip('\n'))
        file.write(str(maximum))
        file.write("\n")
        file.write("     range {} : ".format(label).rstrip('\n'))
        file.write(str(rangeData))
        file.write("\n")
        file.write("      mean {} : ".format(label).rstrip('\n'))
        file.write(str(mean))
        file.write("\n")
        file.write("    median {} : ".format(label).rstrip('\n'))
        file.write(str(median))
        file.write("\n")
        file.write("     sigma {} : ".format(label).rstrip('\n'))
        file.write(str(sigma))
        file.write("\n")
        file.write("        cp {} : ".format(label).rstrip('\n'))
        file.write(str(CP))
        file.write("\n")
        file.write("       cpk {} : ".format(label).rstrip('\n'))
        file.write(str(CPK))
        file.write("\n")
        file.write("\n")
        printStats(results)

    else:
        return(results)

def printStats(statsData):
    label = statsData[0]
    print("{} datapoints : {}".format(label,statsData[2]))
    print("       min {} : {}".format(label,statsData[3]))
    print("       max {} : {}".format(label,statsData[4]))
    print("     range {} : {}".format(label,statsData[5]))
    print("     mean {} : {}".format(label,statsData[6]))
    print("     median {} : {}".format(label,statsData[7]))
    print("     sigma {} : {}".format(label,statsData[8]))
    print("        cp {} : {}".format(label,statsData[9]))
    print("       cpk {} : {}".format(label,statsData[10]))

def plotHistograms(dataSet,cavities,foldername):
    #basePath = os.path.dirname(os.path.abspath(__file__))
    for cavity in cavities:
        A = dataSet[cavity][1]
        B = dataSet[cavity][2]

        x = 0.75
        y = 0.75

        stats = statistics(param_A_name.get(), A , cavity , float(param_A_LSL.get()) , float(param_A_USL.get()) , 'none', 0)

        plt.hist(A, bins = 'auto')
        plt.title('Histogram of {} Dimensions: Cavity {}'.format(param_A_name.get(), cavity))
        plt.xlabel('Dimension, {}'.format(param_A_name.get()))
        plt.ylabel('Frequency')
        plt.axvline(x=float(param_A_LSL.get()),color = 'red')
        plt.axvline(x=float(param_A_USL.get()),color = 'red')
        plt.subplots_adjust(right=(x - 0.02))
        namedFile = os.path.join(foldername,'Hist_Seal_{}_{}.png'.format(param_A_name.get(),cavity))
        plt.annotate('length {} : {}'.format(stats[0], stats[2]),  (x,y), xycoords=('figure fraction'))
        plt.annotate('    min {} : {}'.format(stats[0], stats[3]),  (x,y-0.05), xycoords=('figure fraction'))
        plt.annotate('    max {} : {}'.format(stats[0], stats[4]),  (x,y-0.1), xycoords=('figure fraction'))
        plt.annotate(' range {} : {}'.format(stats[0], stats[5]),  (x,y-0.15), xycoords=('figure fraction'))
        plt.annotate('  mean {} : {}'.format(stats[0], stats[6]),  (x,y-0.2), xycoords=('figure fraction'))
        plt.annotate('median {} : {}'.format(stats[0], stats[7]),  (x,y-0.25), xycoords=('figure fraction'))
        plt.annotate('  sigma {} : {}'.format(stats[0], stats[8]),  (x,y-0.3), xycoords=('figure fraction'))
        plt.annotate('       cp {} : {}'.format(stats[0], stats[9]),  (x,y-0.35), xycoords=('figure fraction'))
        plt.annotate('      cpk {} : {}'.format(stats[0], stats[10]), (x,y-0.4), xycoords=('figure fraction'))
        plt.savefig(namedFile)
        plt.close()

        stats = statistics(param_B_name.get(), B , cavity , float(param_B_LSL.get()) , float(param_B_USL.get()) , 'none', 0)

        plt.hist(B, bins = 'auto')
        plt.title('Histogram of {} Dimensions: Cavity {}'.format(param_B_name.get(),cavity))
        plt.xlabel('Dimension, {}'.format(param_B_name.get()))
        plt.ylabel('Frequency')
        plt.axvline(x=float(param_B_LSL.get()),color = 'red')
        plt.axvline(x=float(param_B_USL.get()),color = 'red')
        plt.subplots_adjust(right=0.7)
        namedFile = os.path.join(foldername,'Hist_Seal_{}_{}.png'.format(param_B_name.get(), cavity))
        plt.annotate('length {} : {}'.format(stats[0], stats[2]),  (x,y), xycoords=('figure fraction'))
        plt.annotate('    min {} : {}'.format(stats[0], stats[3]),  (x,y-0.05), xycoords=('figure fraction'))
        plt.annotate('    max {} : {}'.format(stats[0], stats[4]),  (x,y-0.1), xycoords=('figure fraction'))
        plt.annotate(' range {} : {}'.format(stats[0], stats[5]),  (x,y-0.15), xycoords=('figure fraction'))
        plt.annotate('  mean {} : {}'.format(stats[0], stats[6]),  (x,y-0.2), xycoords=('figure fraction'))
        plt.annotate('median {} : {}'.format(stats[0], stats[7]),  (x,y-0.25), xycoords=('figure fraction'))
        plt.annotate('  sigma {} : {}'.format(stats[0], stats[8]),  (x,y-0.3), xycoords=('figure fraction'))
        plt.annotate('       cp {} : {}'.format(stats[0], stats[9]),  (x,y-0.35), xycoords=('figure fraction'))
        plt.annotate('      cpk {} : {}'.format(stats[0], stats[10]), (x,y-0.4), xycoords=('figure fraction'))
        plt.savefig(namedFile)
        plt.close()


def plotbyDate(dataSet,cavities,foldername):
    data = fileName.cget("text")

    for cavity in cavities:
        dateData = dataByDate(cavity,data)
        plt.plot(dateData[0],dateData[1], 'o', color='black')
        plt.title('Scatter Plot of Seal {} Data by Month: Cavity {}'.format(param_A_name.get(),cavity))
        plt.xlabel('Month')
        plt.ylabel('Dimention, Seal {}'.format(param_A_name.get()))
        plt.axhline(y=float(param_A_LSL.get()),color = 'red')
        plt.axhline(y=float(param_A_LSL.get()),color = 'red')
        namedFile = os.path.join(foldername,'ScatterDate_Seal_{}_{}.png'.format(param_A_name.get(),cavity))
        plt.savefig(namedFile)
        plt.close()

        plt.plot(dateData[0],dateData[2], 'o', color='black')
        plt.title('Scatter Plot of Seal {} Data by Month: Cavity {}'.format(param_B_name.get(),cavity))
        plt.xlabel('Month')
        plt.ylabel('Dimention, Seal {}'.format(param_B_name.get()))
        plt.axhline(y=float(param_B_LSL.get()),color = 'red')
        plt.axhline(y=float(param_B_LSL.get()),color = 'red')
        namedFile = os.path.join(foldername,'ScatterDate_Seal_{}_{}.png'.format(param_B_name.get(),cavity))
        plt.savefig(namedFile)
        plt.close()


def dataByDate(cavityName, data):
    months = [1,2,3,4,5,6,7,8,9,10,11,12]
    month = []
    A = []
    B = []

    with open(data) as f:
        file = csv.reader(f)

        for row in file:
            currentCav = row[int(cavity_col.get())]
            currentMonth = row[int(date_col.get())].split("/")[0]
            for m in months:
                if currentCav == cavityName and currentMonth == str(m):
                    month.append(currentMonth)
                    A.append(float(row[int(param_A_col.get())]))
                    B.append(float(row[int(param_B_col.get())]))

    matrix = [month,A,B]
    return(matrix)




root.title("Data Analysis App")

root.geometry('1200x400')

background = 'gray15'
root.configure(bg = background)
root.grid_rowconfigure(0, minsize=20)
root.grid_rowconfigure(2, minsize=30)
root.grid_rowconfigure(5, minsize=20)
root.grid_rowconfigure(7, minsize=30)
root.grid_rowconfigure(8, minsize=30)
root.grid_rowconfigure(9, minsize=30)
root.grid_rowconfigure(10, minsize=30)
root.grid_rowconfigure(11, minsize=30)
root.grid_rowconfigure(12, minsize=30)


root.grid_columnconfigure(0,minsize =20)
root.grid_columnconfigure(1,minsize =140)
root.grid_columnconfigure(2,minsize =100)
root.grid_columnconfigure(3,minsize =100)
root.grid_columnconfigure(4,minsize = 100)
root.grid_columnconfigure(5,minsize = 10)
root.grid_columnconfigure(6,minsize = 120)
root.grid_columnconfigure(7,minsize = 10)
root.grid_columnconfigure(8,minsize = 120)
root.grid_columnconfigure(9,minsize = 10)
root.grid_columnconfigure(10,minsize = 120)



#Create Widgets
get_data_button = Button(root, text="Select Data File", bg = 'gold', command = getFileName)
fileName = Label(root, text="None", bg = background, fg = 'white')
cavity_callout = Label(root, text = 'Cavity Column')
cavity_col = Entry(root, justify = 'center')
date_callout = Label(root, text = 'Date Column')
date_col = Entry(root, justify = 'center')
cavity_col.insert(0,'2')
date_col.insert(0,'4')

param_callout = Label(root,text = 'Parameter Name')
col_callout = Label(root,text = 'Column Number')
LSL_callout = Label(root,text = 'LSL')
USL_callout = Label(root,text = 'USL')

param_A_name = Entry(root, justify = 'center')
param_A_col = Entry(root, justify = 'center')
param_A_LSL = Entry(root, justify = 'center')
param_A_USL = Entry(root, justify = 'center')

param_A_name.insert(0,'X')
param_A_col.insert(0,'6')
param_A_LSL.insert(0,156.2)
param_A_USL.insert(0,157.9)

param_B_name = Entry(root, justify = 'center')
param_B_col = Entry(root, justify = 'center')
param_B_LSL = Entry(root, justify = 'center')
param_B_USL = Entry(root, justify = 'center')

param_B_name.insert(0,'Y')
param_B_col.insert(0,'7')
param_B_LSL.insert(0,156.2)
param_B_USL.insert(0,157.9)

param_C_name = Entry(root, justify = 'center')
param_C_col = Entry(root, justify = 'center')
param_C_LSL = Entry(root, justify = 'center')
param_C_USL = Entry(root, justify = 'center')

param_C_name.insert(0,'45(a)')
param_C_col.insert(0,'8')
param_C_LSL.insert(0,176.7)
param_C_USL.insert(0,178.1)

param_D_name = Entry(root, justify = 'center')
param_D_col = Entry(root, justify = 'center')
param_D_LSL = Entry(root, justify = 'center')
param_D_USL = Entry(root, justify = 'center')

param_D_name.insert(0,'45(b)')
param_D_col.insert(0,'9')
param_D_LSL.insert(0,176.7)
param_D_USL.insert(0,178.1)

param_E_name = Entry(root, justify = 'center')
param_E_col = Entry(root, justify = 'center')
param_E_LSL = Entry(root, justify = 'center')
param_E_USL = Entry(root, justify = 'center')

param_E_name.insert(0,'UCX')
param_E_col.insert(0,'10')
param_E_LSL.insert(0,147.6)
param_E_USL.insert(0,149.1)


param_F_name = Entry(root, justify = 'center')
param_F_col = Entry(root, justify = 'center')
param_F_LSL = Entry(root, justify = 'center')
param_F_USL = Entry(root, justify = 'center')

param_F_name.insert(0,'UCY')
param_F_col.insert(0,'11')
param_F_LSL.insert(0,147.6)
param_F_USL.insert(0,149.1)

analyse_data_button = Button(root, text = 'Analyse Data', bg = 'chartreuse3', command = returnStats)
histogram_button = Button(root, text = 'Get Histograms', bg = 'chartreuse3', command = returnHistograms)
data_date_button = Button(root, text = 'Get Data by Date', bg = 'chartreuse3', command = returnDatabyDate)

# Place Widgets on Screen
get_data_button.grid(column = 1, row = 1, sticky=N+S+E+W)
fileName.grid(column = 2, row = 1, columnspan = 8, sticky = W, padx=5)

cavity_callout.grid(column = 1, row = 3, sticky=N+S+E+W)
date_callout.grid(column = 2, row = 3, sticky=N+S+E+W)
cavity_col.grid(column = 1, row = 4, sticky=N+S+E+W)
date_col.grid(column = 2, row = 4, sticky=N+S+E+W)

param_callout.grid(column = 1, row = 6, sticky=N+S+E+W)
col_callout.grid(column = 2, row = 6, sticky=N+S+E+W)
LSL_callout.grid(column = 3, row = 6, sticky=N+S+E+W)
USL_callout.grid(column = 4, row = 6, sticky=N+S+E+W)

param_A_name.grid(column = 1, row = 7, sticky=N+S+E+W)
param_A_col.grid(column = 2, row = 7, sticky=N+S+E+W)
param_A_LSL.grid(column = 3, row = 7, sticky=N+S+E+W)
param_A_USL.grid(column = 4, row = 7, sticky=N+S+E+W)

param_B_name.grid(column = 1, row = 8, sticky=N+S+E+W)
param_B_col.grid(column = 2, row = 8, sticky=N+S+E+W)
param_B_LSL.grid(column = 3, row = 8, sticky=N+S+E+W)
param_B_USL.grid(column = 4, row = 8, sticky=N+S+E+W)

param_C_name.grid(column = 1, row = 9, sticky=N+S+E+W)
param_C_col.grid(column = 2, row = 9, sticky=N+S+E+W)
param_C_LSL.grid(column = 3, row = 9, sticky=N+S+E+W)
param_C_USL.grid(column = 4, row = 9, sticky=N+S+E+W)

param_D_name.grid(column = 1, row = 10, sticky=N+S+E+W)
param_D_col.grid(column = 2, row = 10, sticky=N+S+E+W)
param_D_LSL.grid(column = 3, row = 10, sticky=N+S+E+W)
param_D_USL.grid(column = 4, row = 10, sticky=N+S+E+W)

param_E_name.grid(column = 1, row = 11, sticky=N+S+E+W)
param_E_col.grid(column = 2, row = 11, sticky=N+S+E+W)
param_E_LSL.grid(column = 3, row = 11, sticky=N+S+E+W)
param_E_USL.grid(column = 4, row = 11, sticky=N+S+E+W)

param_F_name.grid(column = 1, row = 12, sticky=N+S+E+W)
param_F_col.grid(column = 2, row = 12, sticky=N+S+E+W)
param_F_LSL.grid(column = 3, row = 12, sticky=N+S+E+W)
param_F_USL.grid(column = 4, row = 12, sticky=N+S+E+W)

analyse_data_button.grid(column = 6, row = 6, rowspan = 2, sticky=N+S+E+W)
histogram_button.grid(column = 8, row = 6, rowspan = 2, sticky=N+S+E+W)
data_date_button.grid(column = 10, row = 6, rowspan = 2, sticky=N+S+E+W)

root.mainloop()
