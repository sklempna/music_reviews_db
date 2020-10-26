import os
from datetime import datetime


class Logger():
    """
    Implements basic logging functionality for the Metalde parser.
    """
    def __init__(self, logfile='logfile.txt', rev_pointer='rev_pointer.txt'):
        self.logfile = logfile
        self.rev_pointer = rev_pointer
        
    def set_last_review(self, page):
        """
        Overwrites a logfile with the last review that was 
        written into the metalde SQL database.

        Parameters:
        page - the link to the last review that was parsed
        """
        f = open(os.getcwd()+'/'+self.rev_pointer, 'w')
        f.write(page)
        f.close()

    def get_last_review(self):
        """
        Retrieves the last review that was written into the 
        metalde SQL database.

        Returns - the link to the last review
        """
        try:
            f = open(os.getcwd()+'/'+self.rev_pointer, 'r')
            last_review = f.read()
        except:
            last_review = ''    
        return last_review

    def log(self, logstring):
        """
        Writes a logstring formatted with date, time and a 
        closing newline character to a logfile.

        Parameters:
        logstring: a string to be logged
                Parameters:
                        logstring: a string to be logged
        """
        f = open(os.getcwd()+'/'+self.logfile,'a')
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(time+' '+logstring+'\n')
        f.close()

