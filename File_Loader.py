import pandas as pd
import sys

class File_Loader:

    def __init__(self, name):
        self.name = name

    def loadFile(self):
        try:
            df = pd.read_csv(self.name, delimiter=',')
            return df
        except FileNotFoundError as f:
            print(f'The following file was not found: {f.filename}. Please try a valid path/file.')
            sys.exit()
        except IsADirectoryError as de:
            print(f'Please provide file instead of directory.')
            sys.exit()
