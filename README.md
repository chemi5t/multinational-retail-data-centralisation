# Multinational Retail Data Centralisation

# Table of Contents

# A description of the project
The Multinational Retail Data Centralisation Project aims to address the challenge of their sales data being spread across many different data sources. This hinders accessibility and analysis of the data. The project's primary objective is to establish a centralised database system that consolidates all sales data into a single location. This centralised repository will serve as the primary source of truth for sales data, enabling easy access and analysis for team members. The project will involve storing existing sales data in the database and developing querying mechanisms to generate up-to-date metrics for business analysis and decision-making.

# Project Milestones 1 to 4

Refer to the appendix for a step by step guide of how the project was conducted. Here you will find answers to several business questions that required querying the sales_data database using SQLTools/pgAdmin 4.

## Milestone summary

**Outcomes from Milestone 1 (Setting up the environment):** Prerequisites and setup of laptop and GitHub were successful. The project can now be saved and tracked for changes via Git and GitHub. Visual Studio Code was used for writing the code.


**Outcomes from Milestone 2 (Extracting and cleaning the data from the data sources):** Milestone 2 continues from Milestone 1. The company's current up-to-date data is stored in a database locally titled 'sales_data' in 'pgAdmin 4' so that it is accessed from one centralised location and acts as a single point of reference for sales data. Data has been extracted from various sources in JSON, CSV, and PDF formats hosted on different platforms. Data was cleaned using pandas and stored in a local PostgreSQL database, pgAdmin 4, using SQLAlchemy. Progress was updated to the repository on GitHub, and code reviewed for better maintainability and efficiency.

A db_cred.yaml file was created containing the credentials and subsequently all other future sensitive information. This file was added to .gitignore as to not upload any sensitive information to the public GitHub for security purposes.

Three classes were created in separate Python files:

- DataExtractor class in data_extraction.py for extracting data from different sources.
- DataCleaning class in data_cleaning.py for cleaning data extracted from different sources.
- DatabaseConnector class in database_utils.py for connecting to and uploading data to the database.

These classes were all called within a main.py file where the ETL (Extract, Transform, Load) operations would occur. All the extracted tables were cleaned correctly by checking for NULL values, errors with dates, incorrectly typed values, unnecessary columns, and erroneous values. For the products_details table, the weights were converted to a common unit (kg) and cleaned. A summary of the desired table extracted, from what source, connection method required, and the name given to the table once uploaded to the database is given below:

            | Table Name       | Source              | Connection Method | Uploaded Table Name |
            |------------------|---------------------|-------------------|---------------------|
            | legacy_users     | AWS RDS database    | SQLAlchemy        | dim_users           |
            | card_details     | AWS S3 bucket (PDF) | tabula-py         | dim_card_details    |
            | store_details    | API                 | API requests      | dim_store_details   |
            | products_details | AWS S3 bucket (CSV) | boto3             | dim_products        |
            | orders_table     | AWS RDS database    | SQLAlchemy        | orders_table        |
            | date_details     | AWS S3 bucket (JSON)| boto3             | dim_date_times      |


**Outcomes from Milestone 3 (Creating the database schema):** Milestone 3 continues from Milestone 2. Columns in the following tables were all cast to the correct data types using SQL, ensuring consistency and accuracy: orders_table, dim_users, dim_store_details, dim_products, dim_date_times and dim_card_details. 

It was found the dim_store_details table did not require merging the 'latitude' columns as the data in the 'lat' column has all been isloated and found to not be of use and the column dropped. 

Changes were made to the dim_products table via SQL; removal of '£' from the values of the 'product_price_(gbp)' column and adding a new 'weight_class' column. Also, a column name was altered from 'removed' to 'still available'. Upon changing this column data type to BOOL it was found the values needed to be updated to reflect 'True' and 'False'. This is where an error was missed from the initial clean due to the values in thie column containing 'Removed' and the incorrectly spelt 'Still_avaliable'. The error shown via SQL during the updating of this table had drawn attention to the error that was then addressed. 

Primary keys were added to dimension (dim) tables, establishing the foundation for the star-based schema. Foreign keys were created in the orders_table to reference primary keys in other dimension tables, completing the star-based schema. Latest code changes, including schema modifications, were pushed to the GitHub repository, and the README file was updated to reflect the project's progress and structure.

**Entity-Relationship Diagram (ERD) for the 'sales_data' database in 'pgAdmin 4'.**
![ERD for database](_07_images\ERD.png)


**Outcomes from Milestone 4 (Querying the data):** Milestone 4 continues from Milestone 3. Now the schema for the database and all the sales_data is in one location. Queries were be run against this for data-driven decisions and to get a better understanding of its sales. Below is an example of a question together with its answer. For all the questions tackled, refer to the appendix 'Milestone 4'.

- Task 1: How man stores does the business have and in which countries?
The Operations team would like to know which countries we currently operate in and which country now has the most stores. Perform a query on the database to get the information, it should return the following information:

            | country | total_no_stores |       
            |---------|-----------------|
            | GB      | 265             |
            | DE      | 141             |
            | US      | 34              |

            Note: DE is short for Deutschland (Germany)

 Below was the searched query showing a match with the table above showing the total number of stores in each country where the business operates. This provided insight into the geographical distribution of the stores.

```python
-- Task 1. How many stores does the business have and in which countries?
SELECT 
	country_code as country, 
	COUNT(country_code) as total_no_stores
FROM 
	dim_store_details
WHERE store_type != 'Web Portal'
GROUP BY 
	country_code
ORDER BY 
	total_no_stores DESC;
```

 ![M4T1](_07_images\M4T1.png)  

Overall this section focused on developing your skill over the understanding of SELECT, JOIN, GROUP BY, and aggregate functions. The ability to break down complex queries using subqueries and CTEs. Being able to aggregating data for insight. It developed competence in being able to manipulating data for meaningful insights. It allowed the ability to analyse trends and present findings visually. Familiarity was gained of the database schema structure which made for more efficient querying. It helped with problem solving skills in the capacity to interpret business needs and translate them into effective SQL queries. Overall these skills empower efficient querying and help to facilitating informed decision-making.

# File structure of the project

There are seven folders and the root folder: 

- /_01_raw_tables_csv 
    - card_details.csv
    - date_details.csv
    - legacy_users.csv
    - orders_tabl.csv
    - products_details.csv
    - store_details.csv

- /_02_manipulate_raw_tables_ipynb 
    - card_details.ipynb
    - date_details.ipynb
    - legacy_users.ipynb
    - orders_tabl.ipynb
    - products_details.ipynb
    - store_details.ipynb

- /_03_cleaned_tables_csv 
    - card_details_data_cleaned.csv
    - date_details_data_cleaned.csv
    - legacy_users_data_cleaned.csv
    - orders_tabl_data_cleaned.csv
    - products_details_data_cleaned.csv
    - store_details_data_cleaned.csv

- /_04_cleaned_tables_ipynb 
    - card_details_data_cleaned.ipynb
    - date_details_data_cleaned.ipynb
    - legacy_users_data_cleaned.ipynb
    - orders_tabl_data_cleaned.ipynb
    - products_details_data_cleaned.ipynb
    - store_details_data_cleaned.ipynb

- /_05_SQL
    - _01_star_schema_sales_data.sql
    - _02_queries.sql
    - _03_drop_table_query.sql

- /_06_multinational_retail_data_centralisation
    - data_cleaning.py
    - data_extraction.py
    - database_utils.py

- /_07_images 
    - Contains image files

- /root
    - .env
    - .gitignore
    - conda_requirements.txt
    - db_creds.yaml
    - main.py
    - pip_requirements.txt
    - README.md
    - requirements.txt


    

data_cleaning.py
data_extraction.py
database_utils.py
/notebooks contains the work for Milestone 3 and Mileston 4

milestone3.ipynb
milestone4.ipynb
/info contains .yaml credentials files. Make sure you rename the files with _DUMMY at the end with the correct details.

api_key.json
postgresdb_creds.yaml
db_creds.yaml
/temp contains any temporary files that are downloaded during the course of the project

/images contains images of results from the database for Milestone 4. These are used in this README.md file

/ the root folder contains this README.md file, a main.py file and the star_schema.sql file for Milestone 3.

Installation instructions
You need to have sqlalchemy, pyyaml, pandas, boto3 installed. Use pip install if you don't have these.

You need to have a postgresql database set up, called "sales_data". The details for this should be in the postgresdb_cred.yaml file.

db_creds.yaml:
    RDS_HOST: data-handling-project-readonly.cq2e8zno855e.eu-west-1.rds.amazonaws.com
    RDS_PASSWORD: \***\*\*\*\*\*\*\***
    RDS_USER: **\*\***\*\***\*\***
    RDS_DATABASE: postgres
    RDS_PORT: 5432

postgres_db_creds.yaml:
    HOST: "127.0.0.1"
    USER: "postgres"
    PASSWORD: \***\*\*\*\*\***
    DATABASE: "sales_data"
    PORT: 
    
# Usage instructions
From the main downloaded directory:

python main.py
Will run the data extraction, data cleaning and database creation.

Then you can execute the star_schema.sql in pgadmin or vscode or whatever way you prefer to communicate with the postgres database. For more details on what is going on in this process, this can be found in the milestone3.ipynb file.

For the SQL queries for the business case, this can be found in the milestone4.ipynb. The answers are also in the section above for Milestone 4.









Installation instructions
Usage instructions
File structure of the project
License information












    A description of the project: what it does, the aim of the project, and what you learned
    Include here a brief description of the project, what technologies are used etc.


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


- Answer some of these questions in the next few bullet points. What have you built? What technologies have you used? Why have you used those?
- Example: The FastAPI framework allows for fast and easy construction of APIs and is combined with pydantic, which is used to assert the data types of all incoming data to allow for easier processing later on. The server is ran locally using uvicorn, a library for ASGI server implementation.
```python
"""Insert your code here"""
```
> Insert an image/screenshot of what you have built so far here.



# Appendix

## Milestone 1: Enviroment set up

- Prerequisites prior to task:
    1. Operating Systems
    2. What is the command line
    3. File Navigation & File Paths
    4. Git and Version Control
    5. Commits and Branches
    6. What is Github?

- Task 1: Set up GitHub. 

**Outcomes from Milestone 1:** Prerequisites and setup of laptop and GitHub up successful. Now able to commence the project and save/track changes via Git and GitHub. Visual Studio Code to be used for writing the code.

## Milestone 2: Extract and clean the data from the data sources

- Prerequisites prior to task:
1. What is SQL?
2. SQL Setup
3. SQL Tools Setup

- Task 1: Set up a new database to store the data. Initialise a new database locally to store the extracted data. Set up a new database within pgadmin4 and name it sales_data. This database will store all the company information once you extract it for the various data sources.

- Prerequisites prior to task:
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

- Task 2: Initialise the three project Classes. Definine the scripts and Classes you will use to extract and clean the data from multiple data sources.
The Class methods won't be defined in this step yet. They will be defined when required in the subsequent tasks.

        Step 1:
        Create a new Python script named data_extraction.py and within it, create a class named DataExtractor.
        This class will work as a utility class, in it you will be creating methods that help extract data from different data sources.
        The methods contained will be fit to extract data from a particular data source, these sources will include CSV files, an API and an S3 bucket.

        Step 2:
        Create another script named database_utils.py and within it, create a class DatabaseConnector which you will use to connect with and upload data to the database.

        Step 3:
        Finally, create a script named data_cleaning.py this script will contain a class DataCleaning with methods to clean data from each of the data sources.

- Prerequisites prior to task:
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

        RDS_HOST: *private*.*private*.eu-west-1.rds.amazonaws.com
        RDS_PASSWORD: *private*   
        RDS_USER: *private*
        RDS_DATABASE: postgres
        RDS_PORT: 5432

        You should add your db_creds.yaml file to the .gitignore file in your repository, so that the database credentials are not uploaded to your public GitHub repository.
        If you don't currently have a .gitignore file, you can create one by typing touch .gitignore in the terminal. 
        Then just add the names of any files you don't want git to track.

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

- Prerequisites prior to task:
    1. Basics of APIs and Communication Protocols
    2. Working with API Requests

- Task 5: Extract and clean the details of each store. The store data can be retrieved through the use of an API. The API has two GET methods. One will return the number of stores in the business and the other to retrieve a store given a store number. To connect to the API you will need to include the API key to connect to the API in the method header. Create a dictionary to store the header details it will have a key x-api-key with the value *private* (can not be shared here for security). The two endpoints for the API are as follows:

Examples:
Retrieve a store: https://*private*.execute-api.eu-west-1.amazonaws.com/prod/store_details/{store_number}
Return the number of stores: https://*private*.execute-api.eu-west-1.amazonaws.com/prod/
*Exact links can not be shared here for security.*

        Step 1:
        Create a method in your DataExtractor class called list_number_of_stores which returns the number of stores to extract. 
        It should take in the number of stores endpoint and header dictionary as an argument.

        Step 2:
        Now that you know how many stores need to be extracted from the API.

        Step 3:
        Create another method retrieve_stores_data which will take the retrieve a store endpoint as an argument and extracts all the 
        stores from the API saving them in a pandas DataFrame.

        Step 4:
        Create a method in the DataCleaning class called_clean_store_data which cleans the data retrieve from the API and returns a pandas DataFrame.

        Step 5:
        Upload your DataFrame to the database using the upload_to_db method storing it in the table dim_store_details.

- Prerequisites prior to task:
    1. Introduction to Amazon S3
    2. AWS CLI
    3. S3 Objects and boto3

- Task 6: Extract and clean the product details. The information for each product the company currently sells is stored in CSV format in an S3 bucket on AWS.

        Step 1:
        Create a method in DataExtractor called extract_from_s3 which uses the boto3 package to download and extract the information returning a pandas DataFrame.

        The S3 address for the products data is the following s3://*private*/products.csv (exact links can not be shared for security). 
        The method will take this address in as an argument and return the pandas DataFrame.

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
        Using the database table listing methods you created earlier list_db_tables, list all the tables in the database to get the name of the table containing all information about 
        the product orders.

        Step 2:
        Extract the orders data using the read_rds_table method you create earlier returning a pandas DataFrame.

        Step 3:
        Create a method in DataCleaning called clean_orders_data which will clean the orders table data.
        You should remove the columns, first_name, last_name and 1 to have the table in the correct form before uploading to the database.
        You will see that the orders data contains column headers which are the same in other tables.
        This table will act as the source of truth for your sales data and will be at the center of your star based database schema.

        Step 4:
        Once cleaned upload using the upload_to_db method and store in a table called orders_table.

- Task 8: Retrieve and clean the date events data. The final source of data is a JSON file containing the details of when each sale happened, as well as related attributes. The file is currently stored on S3 and can be found at the following link https://*private*.s3.eu-west-1.amazonaws.com/date_details.json (exact links can not be shared for security). Extract the file and perform any necessary cleaning, then upload the data to the database naming the table dim_date_times.

- Prerequisites prior to task:
    1. Github README 

- Task 9: Update the latest changes to GitHub. Update your GitHub repository with the latest code changes from your local project. Start by staging your modifications and creating a commit. Then, push the changes to your GitHub repository.
Additionally, document your progress by adding to your GitHub README file. You can refer to the relevant lesson in the prerequisites for this task for more information.
At minimum, your README file should contain the following information:

        Project Title
        Table of Contents, if the README file is long
        A description of the project: what it does, the aim of the project, and what you learned
        Installation instructions
        Usage instructions
        File structure of the project
        License information

You don't have to write all of this at once, but make sure to update your README file as you go along, so that you don't forget to add anything.

- Task 10: Refactor and optimise current code. Refactoring will be a continuous and constant process, but this is the time to really scrutinise your code. You can use the following list to make improvements:
    - Meaningful Naming: Use descriptive names for methods and variables to enhance code readability. For example, create_list_of_website_links() over links() and use for element in web_element_list instead of for i in list.
    - Eliminate Code Duplication: Identify repeated code blocks and refactor them into separate methods or functions. This promotes code reusability and reduces the likelihood of bugs.
    - Single Responsibility Principle (SRP): Ensure that each method has a single responsibility, focusing on a specific task. If a method handles multiple concerns, split it into smaller, focused methods.
    - Access Modifiers: Make methods private or protected if they are intended for internal use within the class and not externally accessible
    - Main Script Execution: Use the if __name__ == "__main__": statement to include code blocks that should only run when the script is executed directly, not when imported as a module
    - Consistent Import Order: Organize import statements in a consistent manner, such as alphabetically, and place from statements before import statements to maintain readability
    - Avoid Nested Loops: Minimize nested loops whenever possible to improve code efficiency and reduce complexity
    - Minimal Use of self: When writing methods in a class, only use self for variables that store information unique to each object created from the class. This helps keep the code organized and ensures that each object keeps its own special data separate from others.
    - Avoid import *: Import only the specific methods or classes needed from a module to enhance code clarity and prevent naming conflicts
    - Consistent Docstrings: Provide clear and consistent docstrings for all methods, explaining their purpose, parameters, and return values. This aids code understanding for other developers.
    - Type Annotations: Consider adding type annotations to method signatures, variables, and return values to improve code maintainability and catch type-related errors during development

**Outcomes from Milestone 2 (Extracting and cleaning the data from the data sources):** Milestone 2 continues from Milestone 1. The company's current up-to-date data is stored in a database locally titled 'sales_data' in 'pgAdmin 4' so that it is accessed from one centralised location and acts as a single point of reference for sales data. Data has been extracted from various sources in JSON, CSV, and PDF formats hosted on different platforms. Data was cleaned using pandas and stored in a local PostgreSQL database, pgAdmin 4, using SQLAlchemy. Progress was updated to the repository on GitHub, and code reviewed for better maintainability and efficiency.

A db_cred.yaml file was created containing the credentials and subsequently all other future sensitive information. This file was added to .gitignore as to not upload any sensitive information to the public GitHub for security purposes.

Three classes were created in separate Python files:

- DataExtractor class in data_extraction.py for extracting data from different sources.
- DataCleaning class in data_cleaning.py for cleaning data extracted from different sources.
- DatabaseConnector class in database_utils.py for connecting to and uploading data to the database.

These classes were all called within a main.py file where the ETL (Extract, Transform, Load) operations would occur. All the extracted tables were cleaned correctly by checking for NULL values, errors with dates, incorrectly typed values, unnecessary columns, and erroneous values. For the products_details table, the weights were converted to a common unit (kg) and cleaned. A summary of the desired table extracted, from what source, connection method required, and the name given to the table once uploaded to the database is given below:

            | Table Name       | Source              | Connection Method | Uploaded Table Name |
            |------------------|---------------------|-------------------|---------------------|
            | legacy_users     | AWS RDS database    | SQLAlchemy        | dim_users           |
            | card_details     | AWS S3 bucket (PDF) | tabula-py         | dim_card_details    |
            | store_details    | API                 | API requests      | dim_store_details   |
            | products_details | AWS S3 bucket (CSV) | boto3             | dim_products        |
            | orders_table     | AWS RDS database    | SQLAlchemy        | orders_table        |
            | date_details     | AWS S3 bucket (JSON)| boto3             | dim_date_times      |

## Milestone 3: Create the database scheme

- Prerequisites prior to task:
    1. SQL Best Practices
    2. SELECT and Sorting
    3. The WHERE Clause
    4. CRUD Creating Tables
    5. CRUD Altering Tables
    6. SQL JOINs
    7. SQL JOIN Types
    8. SQL Common Aggregations

- Task 1: Cast the columns of the orders_table to the correct data types. Change the data types to correspond to those seen in the table below.

            |   orders_table   | current data type  | required data type |
            |------------------|--------------------|--------------------|
            | date_uuid        | TEXT               | UUID               |
            | user_uuid        | TEXT               | UUID               |
            | card_number      | TEXT               | VARCHAR(?)         |
            | store_code       | TEXT               | VARCHAR(?)         |
            | product_code     | TEXT               | VARCHAR(?)         |
            | product_quantity | BIGINT             | SMALLINT           |

The ? in VARCHAR should be replaced with an integer representing the maximum length of the values in that column.

- Task 2: Cast the solumns of the dim_users to the correct data types. The column required to be changed in the users table are as follows:

            | dim_users      | current data type  | required data type |
            |----------------|--------------------|--------------------|
            | first_name     | TEXT               | VARCHAR(255)       |
            | last_name      | TEXT               | VARCHAR(255)       |
            | date_of_birth  | TEXT               | DATE               |
            | country_code   | TEXT               | VARCHAR(?)         |
            | user_uuid      | TEXT               | UUID               |
            | join_date      | TEXT               | DATE               |

- Task 3: Update the dim_store_details table. There are two latitude columns in the store details table. Using SQL, merge one of the columns into the other so you have one latitude column.

Then set the data types for each column as shown below:

            | store_details_table | current data type | required data type     |
            |---------------------|-------------------|------------------------|
            | longitude           | TEXT              | FLOAT                  |
            | locality            | TEXT              | VARCHAR(255)           |
            | store_code          | TEXT              | VARCHAR(?)             |
            | staff_numbers       | TEXT              | SMALLINT               |
            | opening_date        | TEXT              | DATE                   |
            | store_type          | TEXT              | VARCHAR(255) NULLABLE  |
            | latitude            | TEXT              | FLOAT                  |
            | country_code        | TEXT              | VARCHAR(?)             |
            | continent           | TEXT              | VARCHAR(255)           |


There is a row that represents the business's website change the location column values from N/A to NULL.

- Task 4: Make change to the dim_products table for the delivery team. You will need to do some work on the products table before casting the data types correctly.
The product_price column has a £ character which you need to remove using SQL.
The team that handles the deliveries would like a new human-readable column added for the weight so they can quickly make decisions on delivery weights.
Add a new column weight_class which will contain human-readable values based on the weight range of the product.

            | weight_class    | weight range(kg)  |
            |-----------------|-------------------|
            | Light           | < 2               |
            | Mid_Sized       | >= 2 - < 40       |
            | Heavy           | >= 40 - < 140     |
            | Truck_Required  | >= 140            |

- Task 5: Update the dim_products table with the required data types. After all the columns are created and cleaned, change the data types of the products table.
You will want to rename the removed column to still_available before changing its data type.
Make the changes to the columns to cast them to the following data types:

            | dim_products       | current data type  | required data type |
            |--------------------|--------------------|--------------------|
            | product_price_(gbp)| TEXT               | FLOAT              |
            | weight_(kg)        | TEXT               | FLOAT              |
            | EAN                | TEXT               | VARCHAR(?)         |
            | product_code       | TEXT               | VARCHAR(?)         |
            | date_added         | TEXT               | DATE               |
            | uuid               | TEXT               | UUID               |
            | still_available    | TEXT               | BOOL               |
            | weight_class       | TEXT               | VARCHAR(?)         |

- Task 6: Update the dim_date_times table. Now update the date table with the correct types:

            | dim_date_times | current data type | required data type |
            |----------------|-------------------|--------------------|
            | month          | TEXT              | VARCHAR(?)         |
            | year           | TEXT              | VARCHAR(?)         |
            | day            | TEXT              | VARCHAR(?)         |
            | time_period    | TEXT              | VARCHAR(?)         |
            | date_uuid      | TEXT              | UUID               |

- Task 7: Updating the dim_card_details table.
Now we need to update the last table for the card details.

Make the associated changes after finding out what the lengths of each variable should be:

            | dim_card_details       | current data type | required data type |
            |------------------------|-------------------|--------------------|
            | card_number            | TEXT              | VARCHAR(?)         |
            | expiry_date            | TEXT              | VARCHAR(?)         |
            | date_payment_confirmed | TEXT              | DATE               |


- Task 8: Create the primary keys in the dimention tables. Now that the tables have the appropriate data types we can begin adding the primary keys to each of the tables prefixed with dim. Each table will serve the orders_table which will be the single source of truth for our orders. 
Check the column header of the orders_table you will see all but one of the columns exist in one of our tables prefixed with dim. We need to update the columns in the dim tables with a primary key that matches the same column in the orders_table. 
Using SQL, update the respective columns as primary key columns.

- Task 9: Finalising the star-based schema and adding the foreign keys to the orders table. With the primary keys created in the tables prefixed with dim we can now create the foreign keys in the orders_table to reference the primary keys in the other tables.
Use SQL to create those foreign key constraints that reference the primary keys of the other table.
This makes the star-based database schema complete.

- Task 10: Update the latest code changes to your GitHub repository with the latest code changes from your local project. Start by staging your modifications and creating a commit. Then, push the changes to your GitHub repository.
Additionally, document your progress by adding to your GitHub README file. You can refer to the relevant lesson in the prerequisites for this task for more information.
At minimum, your README file should contain the following information:

        Project Title
        Table of Contents, if the README file is long
        A description of the project: what it does, the aim of the project, and what you learned
        Installation instructions
        Usage instructions
        File structure of the project
        License information

You don't have to write all of this at once, but make sure to update your README file as you go along, so that you don't forget to add anything.

**Outcomes from Milestone 3 (Creating the database schema):** Milestone 3 continues from Milestone 2. Columns in the following tables were all cast to the correct data types using SQL, ensuring consistency and accuracy: orders_table, dim_users, dim_store_details, dim_products, dim_date_times and dim_card_details. 

It was found the dim_store_details table did not require merging the 'latitude' columns as the data in the 'lat' column has all been isloated and found to not be of use and the column dropped. 

Changes were made to the dim_products table via SQL; removal of '£' from the values of the 'product_price_(gbp)' column and adding a new 'weight_class' column. Also, a column name was altered from 'removed' to 'still available'. Upon changing this column data type to BOOL it was found the values needed to be updated to reflect 'True' and 'False'. This is where an error was missed from the initial clean due to the values in thie column containing 'Removed' and the incorrectly spelt 'Still_avaliable'. The error shown via SQL during the updating of this table had drawn attention to the error that was then addressed. 

Primary keys were added to dimension (dim) tables, establishing the foundation for the star-based schema. Foreign keys were created in the orders_table to reference primary keys in other dimension tables, completing the star-based schema. Latest code changes, including schema modifications, were pushed to the GitHub repository, and the README file was updated to reflect the project's progress and structure.

**Entity-Relationship Diagram (ERD) for the 'sales_data' database in 'pgAdmin 4'.**
![ERD for database](_07_images\ERD.png)

## Milestone 4: Querying the data

Your boss is excited that you now have the schema for the database and all the sales data is in one location. Since you've done such a great job they could like you to get some up-to-date metrics from the data. The business can then start making more data-driven decisions and get a better understanding of its sales. In this milestone, you will be tasked with answering business questions and extracting the data from the database using SQL.

- Prerequisites prior to task:
    1. SQL GROUP BY
    2. Creating Subqueries
    3. Types of Subqueries
    4. CRUD Subquery Operations
    5. Common Table Expressions (CTEs)

- **Task 1: How man stores does the business have and in which countries?**

    The Operations team would like to know which countries we currently operate in and which country now has the most stores. Perform a query on the database to get the information, it should return the following information:

            | country | total_no_stores |       
            |---------|-----------------|
            | GB      | 265             |
            | DE      | 141             |
            | US      | 34              |

            Note: DE is short for Deutschland (Germany)

    Below was the searched query showing a match with the table above showing the total number of stores in each country where the business operates. This provided insight into the geographical distribution of the stores.

    ```sql
    -- Task 1. How many stores does the business have and in which countries?
    SELECT 
        country_code as country, 
        COUNT(country_code) as total_no_stores
    FROM 
        dim_store_details
    WHERE store_type != 'Web Portal'
    GROUP BY 
        country_code
    ORDER BY 
        total_no_stores DESC;
    ```

    ![M4T1](_07_images\M4T1.png)  

- **Task 2: Which locations currently have the most stores?**

    The business stakeholders would like to know which locations currently have the most stores. They would like to close some stores before opening more in other locations. Find out which locations have the most stores currently. The query should return the following:

            | locality       | total_no_stores |
            |----------------|-----------------|
            | Chapletown     | 14              |
            | Belper         | 13              |
            | Bushley        | 12              |
            | Exeter         | 11              |
            | High Wycombe   | 10              |
            | Arbroath       | 10              |
            | Rutherglen     | 10              |

    Below was the searched query showing a match with the table above showing the highest number of stores for the various locations, assisting in strategic decision-making regarding store closures and openings.

    ```sql
    -- Task 2. Which locations currently have the most stores?
    SELECT 
        locality, 
        COUNT(locality) as total_no_stores
    FROM 
        dim_store_details
    WHERE 
        store_type != 'Web Portal'
    GROUP BY 
        locality
    ORDER BY 
        total_no_stores DESC
    LIMIT 7;
    ```

     ![M4T2](_07_images\M4T2.png)  

- **Task 3: Which months produced the largest amount of sales?**

    Query the database to find out which months have produced the most sales. The query should return the following information:

            | total_sales | month |
            |-------------|-------|
            | 673295.68   | 8     |
            | 668041.45   | 1     |
            | 657335.84   | 10    |
            | 650321.43   | 5     |
            | 645741.70   | 7     |
            | 645463.00   | 3     |

    Below was the searched query showing a match with the table above showing the months with the highest sales volume, aiding in understanding sales trends over the months in a year.

    ```sql
    -- Task 3. Which months produced the largest amount of sales
    SELECT 
        ROUND(SUM(ot.product_quantity * dp."product_price_(gbp)")::numeric, 2) AS total_sales, ddt.month
    FROM 
        dim_products AS dp
    JOIN 
        orders_table AS ot
    ON 
        dp.product_code = ot.product_code
    JOIN 
        dim_date_times AS ddt 
    ON 
        ot.date_uuid = ddt.date_uuid
    GROUP BY 
        ddt.month
    ORDER BY 
        total_sales DESC
    LIMIT 
        6;
    ```
     ![M4T3](_07_images\M4T3.png)  


- **Task 4: How many sales are coming from online?**

    The company is looking to increase its online sales. They want to know how many sales are happening online vs offline. Calculate how many products were sold and the amount of sales made for online and offline purchases. You should get the following information:

            | numbers_of_sales | product_quantity_count | location |
            |------------------|------------------------|----------|
            | 26957            | 107739                 | Web      |
            | 93166            | 374047                 | Offline  |

    Below was the searched query showing a match with the table above showing the amount of sales made online versus offline, helping assess the performance of online sales channels.

    ```sql
    -- Task 4. How many sales are coming from online? 
    SELECT
        COUNT(dsd.store_type) AS number_of_sales,
        SUM(ot.product_quantity) AS product_quantity_count,
        CASE 
            WHEN dsd.store_type = 'Web Portal' THEN 'Web' 
            ELSE 'Offline' 
        END AS location
    FROM 
        dim_store_details AS dsd
    JOIN orders_table as ot
    ON dsd.store_code = ot.store_code
    GROUP BY 
        location
    ORDER BY number_of_sales ASC;
    ```
     ![M4T4](_07_images\M4T4.png)  

- **Task 5: What eprcentage of sales come through each type of store?**

     The sales team wants to know which of the different store types are generating the most revenue so they know where to focus. Find out the total and percentage of sales coming from each of the different store types. The query should return:

            | store_type  | total_sales | percentage_total(%) |
            |-------------|-------------|---------------------|
            | Local       | 3440896.52  | 44.87               |
            | Web portal  | 1726547.05  | 22.44               |
            | Super Store | 1224293.65  | 15.63               |
            | Mall Kiosk  | 698791.61   | 8.96                |
            | Outlet      | 631804.81   | 8.10                |

    Below was the searched query showing a match with the table above showing the total sales and percentage contribution from the various store types, aiding in the focus of sales strategies.

    ```sql
    -- Task 5. What percentage of sales come through each type of store?
    WITH sum_of_sales AS (
        SELECT dsd.store_type, 
            ROUND(SUM(ot.product_quantity * dp."product_price_(gbp)")::numeric, 2) AS total_sales
        FROM dim_products AS dp
        JOIN orders_table AS ot ON dp.product_code = ot.product_code
        JOIN dim_store_details AS dsd ON ot.store_code = dsd.store_code
        GROUP BY dsd.store_type
    ),
    total_sales_all AS (
        SELECT ROUND(SUM(ot.product_quantity * dp."product_price_(gbp)")::numeric, 2) AS total_sales
        FROM dim_products AS dp
        JOIN orders_table AS ot ON dp.product_code = ot.product_code
    )
    SELECT sum_of_sales.store_type, 
        ROUND(sum_of_sales.total_sales, 2) AS average_sum_of_payments, 
        ROUND((sum_of_sales.total_sales / total_sales_all.total_sales) * 100, 2) AS "percentage_total(%)"
    FROM sum_of_sales
    CROSS JOIN total_sales_all
    ORDER BY average_sum_of_payments DESC;
    ```
     ![M4T5](images\M4T5.png)  

- **Note: The question below was asked in two different ways. For clarity I have reframed them into two parts. The difference being one looks at which month in the year whilst the other months.**
- **Task 6a: Which month in each year produced the highest cost of sales?**
- **Task 6b: Which months in each year produced the highest cost of sales?**

     The company stakeholders want assurances that the company has been doing well recently. Find which **months** in which years have had the most sales historically. The query should return the following information for **Task 6b.**, Table 6b:

            | total_sales | year | month |
            |-------------|------|-------|
            | 27936.77    | 1994 | 3     |
            | 27356.14    | 2019 | 1     |
            | 27091.67    | 2009 | 8     |
            | 26679.98    | 1997 | 11    |
            | 26310.97    | 2018 | 12    |
            | 26277.72    | 2019 | 8     |
            | 26236.67    | 2017 | 9     |
            | 25798.12    | 2010 | 5     |
            | 25648.29    | 1996 | 8     |
            | 25614.54    | 2000 | 1     |

            **Table 6b:**

    Below was the searched query showing a match with the table above showing the **months** in each year with the highest cost of sales, providing insights into sales performance.

    ```sql
    -- Task 6b. Which months in each year produced the highest cost of sales?
    SELECT
        ROUND(SUM(ot.product_quantity * dp."product_price_(gbp)")::numeric, 2) AS total_sales,
        ddt.year,
        ddt.month
    FROM dim_date_times AS ddt
    JOIN orders_table AS ot
    ON ddt.date_uuid = ot.date_uuid
    JOIN dim_products AS dp
    ON ot.product_code = dp.product_code
    GROUP BY 
        ddt.year,
        ddt.month
    ORDER BY total_sales DESC
    LIMIT 10;
    ```
     ![M4T6b](_07_images\M4T6b.png)  

     Below was the searched query showing the **month** in each year with the highest cost of sales, giving a slightly differnt look.

    ```sql
    -- Task 6a. Which month in each year produced the highest cost of sales?
    WITH monthly_sales AS (
        SELECT
            ROUND(SUM(ot.product_quantity * dp."product_price_(gbp)")::numeric, 2) AS total_sales,
            ddt.year,
            ddt.month,
            ROW_NUMBER() OVER (PARTITION BY ddt.year ORDER BY SUM(ot.product_quantity * dp."product_price_(gbp)") DESC) AS month_rank
        FROM dim_date_times AS ddt
        JOIN orders_table AS ot ON ddt.date_uuid = ot.date_uuid
        JOIN dim_products AS dp ON ot.product_code = dp.product_code
        GROUP BY 
            ddt.year,
            ddt.month
    )
    SELECT
        ms.total_sales,
        ms.year,
        ms.month
    FROM
        monthly_sales AS ms
    WHERE
        month_rank = 1
    ORDER BY
        total_sales DESC
    LIMIT 10;
    ```
     ![M4T6a](_07_images\M4T6a.png)  

- **Task 7: What is our staff headcount?**

    The operations team would like to know the overall staff numbers in each location around the world. Perform a query to determine the staff numbers in each of the countries the company sells in. The query should return the values:

            | total_staff_numbers | country_code |
            |---------------------|--------------|
            | 13307               | GB           |
            | 6123                | DE           |
            | 1384                | US           |

    Below was the searched query showing a match with the table above showing the overall staff numbers in each country where the company operates, enabling workforce management.

    ```sql
    -- Task 7. What is our staff headcount?
    SELECT 
        SUM(staff_numbers) AS total_staff_numbers,
        country_code
    FROM 
        dim_store_details
    GROUP BY
        country_code
    ORDER BY 
        total_staff_numbers DESC;
    ```
     ![M4T7](_07_images\M4T7.png)  

- **Task 8: Which German store type is selling the most?**

    The sales team is looking to expand their territory in Germany. Determine which type of store is generating the most sales in Germany. The query will return:

            | total_sales | store_type  | country_code |
            |-------------|-------------|--------------|
            | 198373.57   | Outlet      | DE           |
            | 247634.20   | Mall Kiosk  | DE           |
            | 384625.03   | Super Store | DE           |
            | 1109909.59  | Local       | DE           |
        
    Below was the searched query showing a match with the table above showing the store type generating the most sales in Germany, helping with which type of store for expansion.

    ```sql
    -- Task 8. Which German store type is selling the most?
    SELECT
        ROUND(SUM(ot.product_quantity * dp."product_price_(gbp)")::numeric, 2) AS total_sales,
        dsd.store_type,
        dsd.country_code
    FROM 
        dim_store_details AS dsd
    JOIN
        orders_table AS ot
    ON
        dsd.store_code =  ot.store_code
    JOIN 
        dim_products AS dp
    ON
        ot.product_code = dp.product_code
    WHERE
        dsd.country_code = 'DE'
    GROUP BY
        dsd.store_type, dsd.country_code
    ORDER BY
        total_sales 
    LIMIT 10;
    ```
     ![M4T8](_07_images\M4T8.png)  

- **Task 9: How quickly is the company making sales?**

    Sales would like the get an accurate metric for how quickly the company is making sales. Determine the average time taken between each sale grouped by year, the query should return the following information:

            | year | actual_time_taken                                      |
            |------|--------------------------------------------------------|
            | 2013 | {"hours": 2, "minutes": 17, "seconds": 12, "millise... |
            | 1993 | {"hours": 2, "minutes": 15, "seconds": 35, "millise... |
            | 2002 | {"hours": 2, "minutes": 13, "seconds": 50, "millise... |
            | 2022 | {"hours": 2, "minutes": 13, "seconds": 6,  "millise... |
            | 2008 | {"hours": 2, "minutes": 13, "seconds": 2,  "millise... |

    Hint: You will need the SQL command LEAD.

    Below was the searched query showing a match with the table above showing average time taken between sales grouped by year, showing sales efficiency over time.

    ```sql
    -- Task 9: How quickly is the company making sales?
    -- work in progress
    SELECT ddt.year, ROUND(8760/COUNT(ddt.year)::numeric, 4) AS average_time_between_sales_in_a_year
    FROM orders_table AS ot
    JOIN dim_date_times AS ddt
    ON ot.date_uuid = ddt.date_uuid
    GROUP BY ddt.year
    ORDER BY average_time_between_sales_in_a_year DESC;
    ```
    ** ![M4T8](_07_images\M4T8.png)  **

- **Task 10: Update the latest code changes to GitHub.**

**Outcomes from Milestone 4:** Milestone 4 continues from Milestone 3. Now the schema for the database and all the sales_data is in one location. Queries were be run against this for data-driven decisions and to get a better understanding of its sales. 

Overall this section focused on developing your skill over the understanding of SELECT, JOIN, GROUP BY, and aggregate functions. The ability to break down complex queries using subqueries and CTEs. Being able to aggregating data for insight. It developed competence in being able to manipulating data for meaningful insights. It allowed the ability to analyse trends and present findings visually. Familiarity was gained of the database schema structure which made for more efficient querying. It helped with problem solving skills in the capacity to interpret business needs and translate them into effective SQL queries. Overall these skills empower efficient querying and help to facilitating informed decision-making.