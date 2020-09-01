# Summary

This folder contains two python files:  
  - The data_analysis.py contains a script that parses the two documents and shows the tables and results used 
in the data analysis section of the report.   
  - The test.py file parses the two documents and asks the user for a number of product he wants to be shown.
The script returns the most pertinent products.  

And a pdf file:
  - Report.pdf answers to the questions asked in the test.

# Installation
To run the scripts you need to
- Download the folder  
- Create a virtualenv in the root of the folder (these scripts run with python 3.7) 
- Activate the Virtual Environment
- Install the following python libraries: xlrd, pandas


# Commands to Run the scripts

- data_analysis.py: there is no option for this file, it is run simply by running python data_analysis.py
- test.py: the user defines the number of products he wants to be shown as an input parameter. Run python test.py nbr_to_be_shown (example: python test.py 2) 
