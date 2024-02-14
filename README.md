Project Title
Table of Contents, if the README file is long
A description of the project: what it does, the aim of the project, and what you learned
Installation instructions
Usage instructions
File structure of the project
License information

Project Title
Table of Contents, if the README file is long
A description of the project: what it does, the aim of the project, and what you learned
Installation instructions
Usage instructions
File structure of the project
License information

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

# Computer Vision RPS

> Include here a brief description of the project, what technologies are used etc.
> Rock-Paper-Scissors is a game in which each player simultaneously shows one of three hand signals representing rock, paper, or scissors. Rock beats scissors. Scissors beats paper. Paper beats rock. The player who shows the first option that beats the other player's option wins. This is an implementation of an interactive Rock-Paper-Scissors game, in which the user can play with the computer using the camera. A machine learning model is used to train it to recognising the users input and Python to code the program. 

## Milestone 1: Set up the enviroment

- Prerequisites for the task:
1. Operating Systems
2. What is the command line
3. File Navigation & File Paths
4. Git and Version Control
5. Commits and Branches
6. What is Github?
7. File Manipulation
- Task 1: Set up GitHub. 

- Outcomes from Milestone 1: Prerequisites and setup of laptop and GitHub up successful. Now able to commence the project and save/track changes via Git and GitHub. VS Code to be used for writing the code.

- Answer some of these questions in the next few bullet points. What have you built? What technologies have you used? Why have you used those?

- Example: The FastAPI framework allows for fast and easy construction of APIs and is combined with pydantic, which is used to assert the data types of all incoming data to allow for easier processing later on. The server is ran locally using uvicorn, a library for ASGI server implementation.
  
```python
"""Insert your code here"""
```

> Insert an image/screenshot of what you have built so far here.

## Milestone 2: Create the computer vision system

- Task 1: Create an image project model with four different classes: Rock, Paper, Scissors, Nothing. Use 'Techable-Machine' to create model.
- Task 2: Download the model. This is done from the 'Tensorflow' tab in 'Techable-Machine'.  Keras_model.h5 and labels.txt saved. GitHub updated.
- Task 3: Begin documenting your experience. README.md file updated and GitHub updated.

- Outcomes from Milestone 2: Milestone 2 continues from Milestone 1. A computer vision system (a model) is created via 'Techable-Machine' and used to detect the user input of either Nothing, Rock, Paper or Scissors to the camera. The keras_model.h5 and labels.txt files are downloaded to the local repo. README file is updated to the GitHub repository.

- Does what you have built in this milestone connect to the previous one? If so explain how. What technologies are used? Why have you used them? Have you run any commands in the terminal? If so insert them using backticks (To get syntax highlighting for code snippets add the language after the first backticks).

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