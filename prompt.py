import Best_Fit as BF
import File_Loader
import sys
import ast

class prompt:

    def __init__(self):
        self.best_fit = BF.Best_Fit

    def show_menu(self):
        '''
        Menu for the user.
        '''
        print("--------Main Menu--------")
        print("Press 1 to exit\n")

    def show_reg_type(self):
        '''
        Possible types of Regression Models.
        '''
        print("\n1. lin")
        print("2. las")
        print("3. rid\n")

    def load_pr(self):
        '''
        Prompt the user to enter path for data file.
        Loading the file with the File_Loader class.
        '''
        while True:
            self.show_menu()
            inp = input("Please enter path to CSV File:\n")

            match inp:
                case '1':
                    sys.exit()
                case _:
                    fl = File_Loader.File_Loader(inp)
                    self.load = fl.loadFile()
                    self.best_fit = BF.Best_Fit(self.load)
                    break

    def regression_pr(self):
        '''
        Function that prompts the user to select a regression model,
        test_size, additional parameters and the x-range of the resulting plot.
        '''
        while True:
            inp_x = input("\nPlease enter name of x column:\n")
            inp_y = input("Please enter name of output column:\n")

            if inp_y in self.best_fit.data.columns \
                and inp_x in self.best_fit.data.columns:
                self.best_fit.classify(inp_x, inp_y)
                break
            else:
                print("The column is not present! Try again!\n")

        while True:
            print("\n")
            print("Type of Regression Model")
            self.show_reg_type()
            regression_type_in = input("Please enter the type of regression model:\n")
            type_no = int()
            match regression_type_in:
                case 'lin':
                    type = 'lin'
                    type_no = 0
                    break
                case 'rid':
                    type = 'rid'
                    type_no = 1
                    break
                case 'las':
                    type = 'las'
                    type_no = 2
                    break
                case _:
                    print('not valid!')
                    
        while True:
            test_size_input = input("Please enter the test size (ex. .333):\n")
            try:
                test_size = float(test_size_input)
            except ValueError:
                print("You need to type in a floating point" 
                " n like .2 without additional space\n")
            if test_size < 1 and test_size > 0:
                break
            else:
                print("Test Size can only be between 0 and 1.")
            
        while True:
            print("\noptional arguments example {'fit_intercept': False}\n")
            regression_optional = input("Please enter optional arguments "
            "for the regression as a dictionary string:\n")
            if len(regression_optional) == 0:
                print(self.best_fit.operate(type, test_size))
                break
            else:
                try:
                    dic = ast.literal_eval(regression_optional)
                    if type_no == 0:
                        self.best_fit.operate(type, test_size, LR=dic)
                        break
                    elif type_no == 1:
                        self.best_fit.operate(type, test_size, RR=dic)
                        break
                    elif type_no == 2:
                        self.best_fit.operate(type, test_size, Las=dic)
                        break

                except ValueError:
                    print("You need to type in a dictionary"
                    " like {'fit_intercept': False}")

        while True:
            print("--------Plot--------")
            print("\noptional arguments example {'color': 'green'}\n")
            regression_plot_optional = input("Please enter optional arguments"
            " for the regression plot as a dictionary string:\n")
            if len(regression_plot_optional) == 0:
                dic_linear_plot = {}
                break
            else:
                try:
                    dic_linear_plot = ast.literal_eval(regression_plot_optional)
                    break
                except ValueError:
                    print("You need to type in a dictionary"
                    " like {'c': 'green'}")
        while True:
            print("--------Plot--------")
            print("\noptional arguments example {'c': 'orange'}\n")
            scatter_plot_optional = input("Please enter optional arguments"
            " for the scatter data plot as a dictionary string:\n")
            if len(scatter_plot_optional) == 0:
                dic_scatter_plot = {}
                break
            else:
                try:
                    dic_scatter_plot = ast.literal_eval(scatter_plot_optional)
                    break
                except ValueError:
                    print("You need to type in a dictionary"
                    " like {'color': 'green'}")
        
        while True:
            try:
                start = float(input("\nPlease enter start of range:"))
                end = float(input("Please enter end of range: "))
                self.best_fit.plot_xy(inp_x, inp_y, start, end, plot_args=dic_linear_plot, scat_args=dic_scatter_plot)
                break
            except ValueError:
                print("You need to enter a number for the range which can be converted to float.")
                            
def main():
    pr = prompt()
    pr.load_pr()
    pr.regression_pr()

if __name__=='__main__':
    main()

