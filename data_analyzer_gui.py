'''
    The data_analyzer is an application which allows to make
    simple analyses of data saved as .csv file.

    It is based on the following sections:
    1) See your data details.
    2) Data preparation.
    3) Make visualisations.
    4) Load new data.
    5) Save your data
    6) Close the program.
'''

import tkinter as tk
from tkinter import filedialog, simpledialog, ttk, messagebox, scrolledtext
import logging
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler

sns.set_style('white')

class Analyze():
    '''
    This class allows to:
    - Create dummy variables.
    - Perform scaling.
    - Manage outliers.
    '''
    def __init__(self, datafr=None):

        self.datafr = datafr

    def dummies(self, listdum=None):
        '''
        Creating  dummy variable for indicated variables.
        Arguments:
        listdum: list of variables which will be transformed into dummy variables.
        '''

        self.datafr = pd.get_dummies(self.datafr,
                                     columns=listdum,
                                     drop_first=True)

    def standscal(self,
                  scaler=None,
                  scfeat=None,
                  listsc=None,
                  scfeatdf=None):
        '''
        Allowing to perform standard scaling for indicated variables.
        For more details see "StandardScaler()".
        '''

        scaler = StandardScaler()
        scaler.fit(self.datafr[listsc])
        scfeat = scaler.transform(self.datafr[listsc])
        scfeatdf = pd.DataFrame(scfeat, columns=listsc)
        self.datafr[listsc] = scfeatdf[listsc]

    def outliers(self,
                 listout=None,
                 varout=None,
                 lowqua=None,
                 upqua=None):
        '''
        Managing outliers. It allows to see outliers for indicated
        variables and decide whether user want to delete them or not.
        Arguments:
        listout: list of variables which will be checked for outliers.
        varout, lowqua, upqua: arguments used for outliers detecting.
        '''

        for outvar in listout:
            varout = self.datafr[outvar]
            lowqua = varout.quantile(.25) - (varout.quantile(.75) -
                                             varout.quantile(.25))*1.5
            upqua = varout.quantile(.75) + (varout.quantile(.75) -
                                            varout.quantile(.25))*1.5

            varoutx = self.datafr[(varout < lowqua) | (varout > upqua)]

            msgbox = tk.messagebox.askyesno(title='Deleting outliers',
                                            message='''Variable "{}" has the following outliers:
                                            {}
                                            Do you want to delete them?'''.format(outvar, varoutx))

            if msgbox is True:
                self.datafr[outvar] = varout[varout.between(lowqua, upqua)]
                tk.messagebox.showinfo('Deleting outliers', 'Outliers has been removed')

            else:
                pass

class Visual():
    '''
    Making following visualisations for loaded dataset.
    Can be performed the following visualisations:
    1) Regression
    2) Heatmap
    3) Barplot
    4) Countplot
    5) Boxplot
    6) Distribution
    7) Jointplot
    8) Pairplot
    '''
    def __init__(self, datatovis):

        self.datatovis = datatovis

    def regression(self, xdata=None, ydata=None):
        '''
        See "lmplot" for seaborn.
        '''
        xdata = simpledialog.askstring(title='Regression',
                                       prompt='Give the name of variable for X axis.')
        ydata = simpledialog.askstring(title='Regression',
                                       prompt='Give the name of variable for Y axis.')

        sns.lmplot(x=xdata, y=ydata, data=self.datatovis)
        plt.show()

    def heatmap(self):
        '''
        See "heatmap" for seaborn.
        '''
        sns.heatmap(data=self.datatovis, cmap='coolwarm')
        plt.show()

    def barplot(self, xdata=None, ydata=None):
        '''
        See "barplot" for seaborn.
        '''

        xdata = simpledialog.askstring('Barplot', 'Give the name of variable for X axis.')
        ydata = simpledialog.askstring('Barplot', 'Give the name of variable for Y axis.')

        sns.barplot(x=xdata, y=ydata, data=self.datatovis)
        plt.show()

    def countplot(self, xdata=None):
        '''
        See "countplot" for seaborn.
        '''

        xdata = simpledialog.askstring('Countplot',
                                       ('Give the name of variable '
                                        'which you want to count and plot. '))

        sns.countplot(x=xdata, data=self.datatovis)
        plt.show()

    def boxplot(self, xdata=None, ydata=None):
        '''
        See "boxplot" for seaborn.
        '''

        xdata = simpledialog.askstring('Boxplot',
                                       'Give the name of variable to categorize data.')
        ydata = simpledialog.askstring('Boxplot',
                                       'Give the name of variable for Y axis.')

        sns.boxplot(x=xdata, y=ydata, data=self.datatovis)
        plt.show()

    def distribution(self, xdata=None):
        '''
        See "distribution" for seaborn.
        '''

        xdata = simpledialog.askstring('Distribution', 'Give the name of variable to plot. ')

        sns.distplot(self.datatovis[xdata])
        plt.show()

    def jointplot(self, xdata=None, ydata=None):
        '''
        See "jointplot" for seaborn.
        '''

        xdata = simpledialog.askstring('Jointplot',
                                       'Give the name of the first variable.')
        ydata = simpledialog.askstring('Jointplot',
                                       'Give the name of the second variable.')

        sns.jointplot(x=xdata, y=ydata, data=self.datatovis)
        plt.show()

    def pairplot(self):
        '''
        See "pairplot" for seaborn.
        '''
        sns.pairplot(data=self.datatovis)
        plt.show()

if __name__ == "__main__":

    ALPHA = Analyze()

    def opendirectory():
        '''
        Open the file with data which you want to analyze
        '''

        filename = filedialog.askopenfilename(parent=WIN,
                                              initialdir="C:/",
                                              title="Select file",
                                              filetypes=[("csv files", "*.csv")])

        separatorl = simpledialog.askstring(title="Separator",
                                            prompt="Enter separator of your data:")

        ALPHA.datafr = pd.read_csv(filename, separatorl)

    def savefile():
        '''
        Saves your dataset with changes if the has been made.
        savename - asks you for filename for your modified dataset.
        savesep - asks you for separator for your modified dataset.
        '''
        savename = filedialog.asksaveasfilename(defaultextension=".csv",
                                                initialdir="C:/")

        savesep = simpledialog.askstring(title="Separator",
                                         prompt="Enter separator of your data:")
        ALPHA.datafr.to_csv(savename, sep=savesep)

    def newwindow1():
        '''
        Shows information about your loaded dataset:
        - Head of dataset.
        - Descriptive statistics.
        - Correlation matrix.
        '''
        datadetails = '''
        This is head of your data:

        {}
        
        Descriptive statistics:
        
        {}
        
        Correlation matrix:
        
        {}
        '''.format(ALPHA.datafr.head(),
                   ALPHA.datafr.describe(),
                   ALPHA.datafr.corr())

        window = tk.Toplevel(WIN)
        window.title("Your data details:")

        ent = tk.Text(window, height=40, width=100)
        ent = scrolledtext.ScrolledText(window, height=40, width=60)
        ent.insert(tk.INSERT, datadetails)
        ent.pack()
        window.mainloop()

    def newwindow2():
        '''
        Prepare your data for analyze.
        This function contains following inner functions:
        window2dum() -> create dummy variables.
        window2std() -> standarize your data.
        window2out() -> manage your outliers.
        window2na() -> manage your N/A values.
        '''
        window2 = tk.Toplevel(WIN)
        window2.title("Choose an action:")

        def window2dum():
            catvar = simpledialog.askinteger(title="Number",
                                             prompt=("How many categorical "
                                                     "variables your dataset has:"))
            lidum = []
            dumcounter = 0
            while catvar > dumcounter:
                try:
                    dumchecker = simpledialog.askstring(
                        title="Categorical Variable",
                        prompt="Give the name of your categorical variable:")
                    if str(dumchecker) not in ALPHA.datafr.columns:
                        raise IOError()
                except IOError:
                    tk.messagebox.showerror('Error', ('Given variable is not in dataset. '
                                                      'Enter the right variable.'))
                else:
                    lidum.append(dumchecker)
                    dumcounter += 1

            ALPHA.datafr = pd.get_dummies(ALPHA.datafr,
                                          columns=lidum,
                                          drop_first=True)

        def window2std():
            stdnum = simpledialog.askinteger(title="Number",
                                             prompt=("How many variables "
                                                     "you want to standarize?"))
            liststd = []
            stdcounter = 0

            while stdnum > stdcounter:
                try:
                    stdchecker = simpledialog.askstring(
                        title="Variable to standarize",
                        prompt="Give the name of variable which you want to standarize:")
                    if str(stdchecker) not in ALPHA.datafr.columns:
                        raise IOError()
                except IOError:
                    tk.messagebox.showerror('Error', 'Given variable is not in dataset. '
                                                     'Enter the right variable.')
                else:
                    liststd.append(stdchecker)
                    stdcounter += 1

            ALPHA.standscal(listsc=liststd)

        def window2out():
            outnum = simpledialog.askinteger(title="Number",
                                             prompt=("How many variables "
                                                     "you want to check for outliers?"))
            listoutliers = []
            outcounter = 0

            while outnum > outcounter:
                try:
                    outchecker = simpledialog.askstring(
                        title="Variable to be checked for outliers",
                        prompt="Give the name of variable which you want to check for outliers:")
                    if str(outchecker) not in ALPHA.datafr.columns:
                        raise IOError()
                except IOError:
                    tk.messagebox.showerror('Error', 'Given variable is not in dataset. '
                                                     'Enter the right variable.')
                else:
                    listoutliers.append(outchecker)
                    outcounter += 1

            ALPHA.outliers(listout=listoutliers)

        def window2na():
            def btn1yes():
                ALPHA.datafr.dropna(inplace=True)
                tk.messagebox.showinfo("NA values", "NA values has been deleted.")
                window2natop.destroy()

            sns.heatmap(ALPHA.datafr.isna(),
                        cmap='coolwarm',
                        linewidths=.2)

            window2natop = tk.Toplevel(WIN)
            window2natop.title('Do you want to delete your N/A values?')
            window2natop.geometry("350x100")

            btn1 = tk.Button(window2natop, text='Yes', command=btn1yes, width=10)
            btn1.grid(column=1, row=1, padx=160, pady=10)
            btn2 = tk.Button(window2natop, text='No', command=window2natop.destroy, width=10)
            btn2.grid(column=1, row=2, padx=160, pady=10)

            plt.show()

        paction1 = ttk.Button(window2, text="Create dummy variables", command=window2dum)
        paction1.grid(column=1, row=1, pady=10, padx=10)

        paction2 = ttk.Button(window2, text="Standarize your data", command=window2std)
        paction2.grid(column=1, row=2, pady=10, padx=10)

        paction3 = ttk.Button(window2, text="Manage outliers", command=window2out)
        paction3.grid(column=1, row=3, pady=10, padx=10)

        paction4 = ttk.Button(window2, text="Manage NA values", command=window2na)
        paction4.grid(column=1, row=4, pady=10, padx=10)

        paction5 = ttk.Button(window2, text="Exit this section", command=window2.destroy)
        paction5.grid(column=1, row=5, pady=10, padx=10)

    def newwindow3():
        '''
        This section of program allows to make visualisations:

        1) Regression
        2) Heatmap
        3) Barplot
        4) Countplot
        5) Boxplot
        6) Distribution
        7) Jointplot
        8) Pairplot
        '''
        beta = Visual(ALPHA.datafr)
        window3 = tk.Toplevel()
        window3.title('Which visualisation you want to make?')

        visbtn1 = ttk.Button(window3, text='Regression', command=beta.regression)
        visbtn1.grid(column=1, row=1, pady=10, padx=10)

        visbtn2 = ttk.Button(window3, text='Heatmap', command=beta.heatmap)
        visbtn2.grid(column=1, row=2, pady=10, padx=10)

        visbtn3 = ttk.Button(window3, text='Barplot', command=beta.barplot)
        visbtn3.grid(column=1, row=3, pady=10, padx=10)

        visbtn4 = ttk.Button(window3, text='Countplot', command=beta.countplot)
        visbtn4.grid(column=1, row=4, pady=10, padx=10)

        visbtn5 = ttk.Button(window3, text='Boxplot', command=beta.boxplot)
        visbtn5.grid(column=1, row=5, pady=10, padx=10)

        visbtn6 = ttk.Button(window3, text='Distribution', command=beta.distribution)
        visbtn6.grid(column=1, row=6, pady=10, padx=10)

        visbtn7 = ttk.Button(window3, text='Jointplot', command=beta.jointplot)
        visbtn7.grid(column=1, row=7, pady=10, padx=10)

        visbtn8 = ttk.Button(window3, text='Pairplot', command=beta.pairplot)
        visbtn8.grid(column=1, row=8, pady=10, padx=10)

        visbtn9 = ttk.Button(window3, text='Exit this section', command=window3.destroy)
        visbtn9.grid(column=1, row=9, pady=10, padx=10)

    WIN = tk.Tk()
    WIN.title("Data Analyzer")
    WIN.geometry("200x300")

    ACTION1 = ttk.Button(WIN, text="See your data details", command=newwindow1)
    ACTION1.grid(column=1, row=1, pady=10, padx=10)

    ACTION2 = ttk.Button(WIN, text="Data preparation", command=newwindow2)
    ACTION2.grid(column=1, row=2, pady=10, padx=10)

    ACTION3 = ttk.Button(WIN, text="Make visualisations", command=newwindow3)
    ACTION3.grid(column=1, row=3, pady=10, padx=10)

    ACTION4 = ttk.Button(WIN, text="Load new data", command=opendirectory)
    ACTION4.grid(column=1, row=4, pady=10, padx=10)

    ACTION5 = ttk.Button(WIN, text="Save your dataset", command=savefile)
    ACTION5.grid(column=1, row=5, pady=10, padx=10)

    ACTION6 = ttk.Button(WIN, text="Close program", command=WIN.destroy)
    ACTION6.grid(column=1, row=6, pady=10, padx=10)

    WIN.mainloop()
