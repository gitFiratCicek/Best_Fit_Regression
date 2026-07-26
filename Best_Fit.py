import numpy as np
import pandas as pd
import File_Loader as file
import matplotlib.pyplot as plt
import pypalettes as lett
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Ridge,LinearRegression, Lasso

class Best_Fit:
    '''
    Class for fitting a linear model and solving the
    linear least squares problem.

    Class also includes function to plot the results.
    '''

    def __init__(self, data: pd.DataFrame):
        self.data = data
        self.y_col = str()
        self.y_col_in = int()
        self.y = self.data.values[:, self.y_col_in]
        self.unique_vals = np.ndarray([])
        self.coef = np.ndarray([])
        self.incept = np.ndarray([])
        self.score = float()

    def __str__(self):
        return f'The coefs are {self.coef} and \
            the intercept is {self.incept} and \
            the score is r^2 {self.score:.3f}'

    def classify(self, y_col):
        '''
        Use this first to classify your data.
        This function will make sure that all the columns
        in your dataset will be mapped accordingly.

        y_col: name of output column
        '''
        try:
            self.y_col = y_col
            self.y_col_in = self.data.columns.get_loc(self.y_col)
            self.unique_vals = self.data[str(y_col)].unique()
        except KeyError as k:
            print(f'The following key is not correct.{k}')

    def plot_xy(self, xcol, ycol, start, end, scat_args=None, plot_args=None):
        '''
        Plot linear function with coefficient and y-intercept
        which was determined by operate() function.
        The original data will also be output as a scatter plot.

        xcol: name of x column

        ycol: name of y column

        start: start of range

        end: end of range

        scat_args: pass dict to specify optional args for the scatter plot

        plot_args: pass dict to specify optional args for the linear plot
        '''

        plot_args = plot_args or dict()
        scat_args = scat_args or dict()

        beta0 = self.incept
        beta1 = self.coef
        interval = np.linspace(start, end, end)
        plt.title(f'{self.incept=} and {self.coef=}')
        plt.xlabel(xcol)
        plt.ylabel(ycol)
        plt.scatter(self.data[xcol].to_numpy(), self.data[ycol].to_numpy(), **scat_args)
        plt.plot(interval, beta0 + interval*beta1, **plot_args)
        plt.show()

    def plot_xy_rel(self, xplt_col, yplt_col, pallete, scat_args=None):
        '''
        Plot the feature inputs as x and y scatter plot.
        And color every data point according to 
        the coressponding output color palette. 

        xplt_col: column name for x
        yplt_col: column name for y
        palette: name of palette (reference https://y-sunflower.github.io/pypalettes/)

        scat_args: pass a dict to specify optional
        args you would like to pass to plt.scatter()
        '''
        scat_args = scat_args or dict()

        try:
            category_mapping = {category: idx for idx, category in enumerate(self.unique_vals)}
            cmap = lett.load_cmap( \
                    pallete,  # Name of the palette
                    keep_first_n=len(category_mapping)-1,  # Number of colors to keep
                    )

            plt.scatter(self.data[xplt_col].to_numpy(), self.data[yplt_col].to_numpy(), c=self.data[self.y_col].to_numpy(), cmap=cmap, **scat_args)
            plt.colorbar()
            plt.xlabel(xplt_col)
            plt.ylabel(yplt_col)
            plt.show()
        except KeyError as k:
            print(f'The following name is not a real column: {k}')
        except ValueError as v:
            print(f"Y values are outside the range of the color palette. {v}")
    
    def operate(self, type, test_size, tts=None, LR=None, RR=None, Las= None):
        '''
        Before using this function it is best to use classify() first.
        Use this to perform regression (linear least squares)
        on given linear model. Use the test_size to split the data
        into training and testing data. A r^2 score will be calculated
        and a score closer to 1 is better.
               
        type: regression type
            - lin (linear regression),
            - las (lasso regression)
            - rid (ridge regression)

        test_size: size of test part 
        
        tts: pass a dictionary containing all optional
        args you would like to pass to train_test_split()

        LR: pass a dictionary containing all optional
        args you would like to pass to LinearRegression()

        RR: pass a dictionary containing all optional
        args you would like to pass to Ridge()

        Las: pass a dictionary containing all optional
        args you would like to pass to Lasso()
        '''
        tts = tts or dict()
        LR = LR or dict()
        RR = RR or dict()
        Las = Las or dict()

        X = self.data.values[:, :self.y_col_in]
        Y = self.data.values[:, self.y_col_in]

        X_Train, X_Test, Y_Train, Y_Test = train_test_split(X, Y, test_size=test_size, **tts)

        match type:
            case 'lin':
                model = LinearRegression(**LR)
                
            case 'las':
                try:
                    val = float(input('Input penalty value(λ):'))
                except ValueError:
                    print("Not a number")
                model = Lasso(alpha=val, **Las)
            case 'rid':
                try:
                    val = float(input('Input penalty value(λ):'))
                except ValueError:
                    print("Not a number")
                model = Ridge(alpha=val, **RR)           
            case _:
                print("not valid type")

        fit = model.fit(X_Train,Y_Train)

        self.score = model.score(X_Test, Y_Test)

        self.coef = fit.coef_

        self.incept = fit.intercept_

        return self.__str__()
