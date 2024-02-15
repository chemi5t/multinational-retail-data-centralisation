Project Title
Table of Contents, if the README file is long
A description of the project: what it does, the aim of the project, and what you learned
Installation instructions
Usage instructions
File structure of the project
License information

## This is an H2 heading
[this is a hyperlink](https://www.google.com)

- This
- Is
- A
- Bulletpoint 
- List

1. This 
2. Is 
3. A
4. Numbered
5. List 

### This is an H3 Heading

This is how you add an image:
![image info](/pictures/image.png)

You can also use any HTML you want in a Markdown file:
<br>
<p align=center><img src=images/example_image.png width=900></p>
<br>

# Multinational Retail Data Centralisation

>The Multinational Retail Data Centralisation Project aims to address the challenge of their sales data being spread across many different data sources. This hinders accessibility and analysis of the data. The project's primary objective is to establish a centralised database system that consolidates all sales data into a single location. This centralised repository will serve as the primary source of truth for sales data, enabling easy access and analysis for team members. The project will involve storing existing sales data in the database and developing querying mechanisms to generate up-to-date metrics for business analysis and decision-making.


> Include here a brief description of the project, what technologies are used etc.
> Rock-Paper-Scissors is a game in which each player simultaneously shows one of three hand signals representing rock, paper, or scissors. Rock beats scissors. Scissors beats paper. Paper beats rock. The player who shows the first option that beats the other player's option wins. This is an implementation of an interactive Rock-Paper-Scissors game, in which the user can play with the computer using the camera. A machine learning model is used to train it to recognising the users input and Python to code the program.



## Milestone 1: Set up the enviroment

- Project Task Prerequisites:
1. Operating Systems
2. What is the command line
3. File Navigation & File Paths
4. Git and Version Control
5. Commits and Branches
6. What is Github?

- Task 1: Set up GitHub. 

- Outcomes from Milestone 1: Prerequisites and setup of laptop and GitHub up successful. Now able to commence the project and save/track changes via Git and GitHub. Visual Studio Code to be used for writing the code.




- Answer some of these questions in the next few bullet points. What have you built? What technologies have you used? Why have you used those?
- Example: The FastAPI framework allows for fast and easy construction of APIs and is combined with pydantic, which is used to assert the data types of all incoming data to allow for easier processing later on. The server is ran locally using uvicorn, a library for ASGI server implementation.
```python
"""Insert your code here"""
```
> Insert an image/screenshot of what you have built so far here.

## Milestone 2: Extract and clean the data from the data sources

- Project Task Prerequisites:
1. What is SQL?
2. SQL Setup
3. SQL Tools Setup

- Task 1: Set up a new database to store the data. Initialise a new database locally to store the extracted data. Set up a new database within pgadmin4 and name it sales_data. This database will store all the company information once you extract it for the various data sources.

- Project Task Prerequisites:
1. What is Python?
2. Google Colab
3. Variables
4. Comments
5. Numbers
6. Strings
7. Booleans
8. Lists
9. Dictionaries
10. Tuples
11. Sets
12. Intro to Control Flow
13. Functions
14. For Loops, Iteration and Control Flow Tricks
15. Error Handling with Control Flow
16. Context Managers
17. Comprehensions
18. Defining Functions
19. Object Oriented Programming
20. Principles of OOP Design

- Task 2: Initialise the three prject Classes. Definine the scripts and Classes you will use to extract and clean the data from multiple data sources.
The Class methods won't be defined in this step yet. They will be defined when required in the subsequent tasks.

    Step 1:
    Create a new Python script named data_extraction.py and within it, create a class named DataExtractor.
    This class will work as a utility class, in it you will be creating methods that help extract data from different data sources.
    The methods contained will be fit to extract data from a particular data source, these sources will include CSV files, an API and an S3 bucket.

    Step 2:
    Create another script named database_utils.py and within it, create a class DatabaseConnector which you will use to connect with and upload data to the database.

    Step 3:
    Finally, create a script named data_cleaning.py this script will contain a class DataCleaning with methods to clean data from each of the data sources.

- Project Task Prerequisites:
1. File Manipulation
2. File Permissions
3. Command Line Basics Recap
4. Package 
5. pip
6. conda
7. Understanding Imports in Python
8. Tabular Data
9. Pandas Basics
10. Exploring Data in Pandas
11. Pandas Data Types
12. Handling Missing Data
13. DataFrame Manipulations
14. Running terminal commands
15. Setting up
16. A tour of VSCode
17. The VSCode integrated terminal
18. Markdown
19. Python files and Python Notebooks
20. YAML
21. JSON
22. CSV Data
23. Summary of Common File Types
24. Python + CSV, JSON, YAML, Images, Audio, Video
25. SQL Commands
26. psycopg2 and SQLAlchemy
27. What is the Cloud?
28. Essential Cloud Concepts
29. What is AWS?
30. AWS Identity and Access Management (IAM)
31. Amazon EC2
32. Virtual Private Cloud (VPC)
33. Amazon RDS

- Task 3: Extract and clean the user data. The historical data of users is currently stored in an AWS database in the cloud. Now create methods in your DataExtractor and DatabaseConnector class which help extract the information from an AWS RDS database.

    Step 1:
    Create a db_creds.yaml file containing the database credentials, they are as follows:

    RDS_HOST: *private*
    RDS_PASSWORD: *private*   
    RDS_USER: *private*
    RDS_DATABASE: *private*
    RDS_PORT: *private*

    You should add your db_creds.yaml file to the .gitignore file in your repository, so that the database credentials are not uploaded to your public GitHub repository.
    If you don't currently have a .gitignore file, you can create one by typing touch .gitignore in the terminal. Then just add the names of any files you don't want git to track.

    Now you will need to develop methods in your DatabaseConnector class to extract the data from the database.

    Step 2:
    Create a method read_db_creds this will read the credentials yaml file and return a dictionary of the credentials.
    You will need to pip install PyYAML and import yaml to do this.

    Step 3:
    Now create a method init_db_engine which will read the credentials from the return of read_db_creds and initialise and return an sqlalchemy database engine.

    Step 4:
    Using the engine from init_db_engine create a method list_db_tables to list all the tables in the database so you know which tables you can extract data from.
    Develop a method inside your DataExtractor class to read the data from the RDS database.

    Step 5:
    Develop a method called read_rds_table in your DataExtractor class which will extract the database table to a pandas DataFrame.

    It will take in an instance of your DatabaseConnector class and the table name as an argument and return a pandas DataFrame.
    Use your list_db_tables method to get the name of the table containing user data.
    Use the read_rds_table method to extract the table containing user data and return a pandas DataFrame.

    Step 6:
    Create a method called clean_user_data in the DataCleaning class which will perform the cleaning of the user data.

    You will need clean the user data, look out for NULL values, errors with dates, incorrectly typed values and rows filled with the wrong information.

    Step 7:
    Now create a method in your DatabaseConnector class called upload_to_db. This method will take in a Pandas DataFrame and table name to upload to as an argument.

    Step 8:
    Once extracted and cleaned use the upload_to_db method to store the data in your sales_data database in a table named dim_users.

- Task 4: Extracting users and cleaning card details. The users card details are stored in a PDF document in an AWS S3 bucket.

    Step 1:
    Install the Python package tabula-py this will help you to extract data from a pdf document. The documentation can be found here .

    Step 2:
    Create a method in your DataExtractor class called retrieve_pdf_data, which takes in a link as an argument and returns a pandas DataFrame.
    Use the tabula-py Python package, imported with tabula to extract all pages from the pdf document at following link .
    Then return a DataFrame of the extracted data.

    Step 3:
    Create a method called clean_card_data in your DataCleaning class to clean the data to remove any erroneous values, NULL values or errors with formatting.

    Step 4:
    Once cleaned, upload the table with your upload_to_db method to the database in a table called dim_card_details.

- Project Task Prerequisites:
1. Basics of APIs and Communication Protocols
2. Working with API Requests

- Task 5: Extract and clean the details of each store. The store data can be retrieved through the use of an API. The API has two GET methods. One will return the number of stores in the business and the other to retrieve a store given a store number. To connect to the API you will need to include the API key to connect to the API in the method header. Create a dictionary to store the header details it will have a key x-api-key with the value *private* (can not be shared here for security). The two endpoints for the API are as follows:

Examples:
Retrieve a store: https://*private*.execute-api.eu-west-1.amazonaws.com/prod/store_details/{store_number}
Return the number of stores: https://*private*.execute-api.eu-west-1.amazonaws.com/prod/
*Exact links can not be shared here for security.*

    Step 1:
    Create a method in your DataExtractor class called list_number_of_stores which returns the number of stores to extract. It should take in the number of stores endpoint and header dictionary as an argument.

    Step 2:
    Now that you know how many stores need to be extracted from the API.

    Step 3:
    Create another method retrieve_stores_data which will take the retrieve a store endpoint as an argument and extracts all the stores from the API saving them in a pandas DataFrame.

    Step 4:
    Create a method in the DataCleaning class called_clean_store_data which cleans the data retrieve from the API and returns a pandas DataFrame.

    Step 5:
    Upload your DataFrame to the database using the upload_to_db method storing it in the table dim_store_details.

- Project Task Prerequisites:
1. Introduction to Amazon S3
2. AWS CLI
3. S3 Objects and boto3

- Task 6: Extract and clean the product details. The information for each product the company currently sells is stored in CSV format in an S3 bucket on AWS.

    Step 1:
    Create a method in DataExtractor called extract_from_s3 which uses the boto3 package to download and extract the information returning a pandas DataFrame.

    The S3 address for the products data is the following s3://*private*/products.csv (exact links can not be shared for security). The method will take this address in as an argument and return the pandas DataFrame.

    You will need to be logged into the AWS CLI before you retrieve the data from the bucket.

    Step 2:
    Create a method in the DataCleaning class called convert_product_weights this will take the products DataFrame as an argument and return the products DataFrame.
    If you check the weight column in the DataFrame the weights all have different units.
    Convert them all to a decimal value representing their weight in kg. Use a 1:1 ratio of ml to g as a rough estimate for the rows containing ml.
    Develop the method to clean up the weight column and remove all excess characters then represent the weights as a float.

    Step 3:
    Now create another method called clean_products_data this method will clean the DataFrame of any additional erroneous values.

    Step 4:
    Once complete insert the data into the sales_data database using your upload_to_db method storing it in a table named dim_products.

- Task 7: Retrieve and clean the orders table. This table which acts as the single source of truth for all orders the company has made in the past is stored in a database on AWS RDS.

    Step 1:
    Using the database table listing methods you created earlier list_db_tables, list all the tables in the database to get the name of the table containing all information about the product orders.

    Step 2:
    Extract the orders data using the read_rds_table method you create earlier returning a pandas DataFrame.

    Step 3:
    Create a method in DataCleaning called clean_orders_data which will clean the orders table data.
    You should remove the columns, first_name, last_name and 1 to have the table in the correct form before uploading to the database.
    You will see that the orders data contains column headers which are the same in other tables.
    This table will act as the source of truth for your sales data and will be at the center of your star based database schema.

    Step 4:
    Once cleaned upload using the upload_to_db method and store in a table called orders_table.

- Task 8: Retrieve and clean the date events data. The final source of data is a JSON file containing the details of when each sale happened, as well as related attributes. The file is currently stored on S3 and can be found at the following link https://data-handling-public.s3.eu-west-1.amazonaws.com/date_details.json. Extract the file and perform any necessary cleaning, then upload the data to the database naming the table dim_date_times.



- Example below:

```bash
/bin/kafka-topics.sh --list --zookeeper 127.0.0.1:2181
```

- The above command is used to check whether the topic has been created successfully, once confirmed the API script is edited to send data to the created kafka topic. The docker container has an attached volume which allows editing of files to persist on the container. The result of this is below:

```python
"""Insert your code here"""
```

> Insert screenshot of what you have built working.

## Milestone 3: Install the dependencies

- Prerequisites for the task:
1. File Permissions
2. Command Line Basics Recap
3. Package managers
4. What is Python?
5. pip
6. conda
7. Running terminal commands

- Task 1: Create a new virtual environment. Create a conda environment and install the following libraries: opencv-python, tensorflow, and ipykernel. 
Important: If you are on Ubuntu, the latest version of Tensorflow doens't work with the default version of Python. When creating the virtual environment, use Python 3.8 instead by running:
conda create -n my_env python=3.8

- Task 2: Create a new virtual environment - For Users who are on a Mac with an M1 Chip (support not given in this project)

- Prerequisites for the task:
1. File Permissions
2. Command Line
1. Editing Files in the Command Line
2. Terminal Customisation
3. Advanced Command Line Features

- Task 3: Combine the installation of dependencies. Install ipykernel by running the following command: pip install ipykernel. Create a requirements.txt file by running the command: pip list > requirements.txt.

- Prerequisites for the task:
1. Running Python files from the terminal
2. Setting up
3. A tour of VSCode
4. The VSCode integrated terminal
5. Markdown
6. Python files and Python Notebooks
7. How (and how not) to run Python files from VSCode
8. Exactly cloning a conda environment

- Task 4: Check the model works. Run this file (https://aicore-files.s3.amazonaws.com/Foundations/Python_Programming/RPS-Template.py) just to check the model you downloaded is working as expected.

- Prerequisites for the task:
1. Google Colab
2. Variables
3. Comments
4. Numbers
5. Strings
6. Booleans
7. Listscals
8. Dictionaries
9. Tuples
10. Sets
11. Intro to Control Flow
12. For Loops, Iteration and Control Flow Tricks
13. Assertions
14. Debugging
15. Functions
16. Error Handling with Control Flow
- Task 5: Get familiar with the code. Knowledge of Tensorflow and Keras is outside the scope of this project. Both libraries are used to build deep learning models (neural networks), and you learn more about them via the Data Science or Machine Learning Engineering specialisations at AiCore. The variable predictions contains the output of the model, and each element in the output corresponds to the probability of the input image representing a particular class. For example, if the prediction has the output: [[0.8, 0.1, 0.05, 0.05]], there is an 80% chance that the input image shows rock, a 10% chance that it shows paper, a 5% chance that it shows scissors, and a 5% chance that it shows nothing. The prediction is a numpy array with one row and four columns. So first, you need to access the first row, and then get the index of the highest value in the row.

- Outcomes from Milestone 3: Milestone 3 continues from Milestone 2. Creation of a virtual environment and installation of libraries (opencv-python, tensorflow, and ipykernel). Model is checked vs RPS-Template.py file.

Model checked using template file in RSP_env.
> [Title](RPS-Template.py)

## Milestone 4: Create a Rock-Paper-Sissors game

- Prerequisites for the task:
1. Context Managers
2. Comprehensions
3. Defining Functions
4. Imports
- Task 1: Store the user's and the computer's choices. Create a file called manual_rps.py to play the game without the camera. Two functions are created: get_computer_choice and get_user_choice. The first will randomly pick an option between "Rock", "Paper", and "Scissors" and return the choice. The second function will ask the user for an input and return it.
- Task 2: Figure out who won. The script now chooses a winner based on the classic rules of Rock-Paper-Scissors and wrap the code in a function called get_winner and return the winner. This function takes two arguments: computer_choice and user_choice. If the computer wins, the function should print "You lost", if the user wins, the function should print "You won!", and if it's a tie, the function should print "It is a tie!".
- Task 3: Create a function to simulate the game. Wrap it all in one function called 'play' which tells you who has won at the end.
- Task 4: Update your documentation. Add documentation to README file. Describe the code written in this milestone.
- Task 5: Start documenting experience. Create/update README file, discuss test environment and the code written for the game. Upload files to the repository.
- Task 6: Update the latest code changes to GitHub.

- Outcomes from Milestone 4: Milestone 4 continues from Milestone 3. Created a script that simulates a Rock-Paper-Sissors game in which the code will run the 'play' function and ask for an input from the user to then compare your input with the computer's choice to show the winner. The code can be run and tested by:

i.e. in the command line:
a. git clone https://github.com/chemi5t/computer-vision-rock-paper-scissors.git
b. cd to that directory
c. python manual_rps.py

RPS code written using VS Code and saved as manual_rps.py.
> ![Alt text](MS4_print_screen_v3.jpg)

GitHub updated.
> ![Alt text](MS4_GH_print_screen_v3.jpg)

## Milestone n

- Continue this process for every milestone, making sure to display clear understanding of each task and the concepts behind them as well as understanding of the technologies used.

- Also don't forget to include code snippets and screenshots of the system you are building, it gives proof as well as it being an easy way to evidence your experience!

## Conclusions

- Maybe write a conclusion to the project, what you understood about it and also how you would improve it or take it further.

- Read through your documentation, do you understand everything you've written? Is everything clear and cohesive?