# Habit tracker in python

The habit tracker app allows users to create habits by simply selecting “Create” and entering a name, description, and selecting a periodicity (Either “Daily” or “Weekly”)
The user is then able to “check off” these habits and also receive analytical data about their habits simply by selecting the habit’s name. This creates a system where the user only has to type when they create a habit.


## What it is?

This habit tracker is a simple yet useful program written in python that allows users to create, check-off and analyse their habits.
The user can  see historical data regarding their habits through the user of a SQLite3 database and the inbuilt python Datetime module.
This application also uses the two external libraries, questionary and pytest. These provide a sleek command line interface and a robust testing system respectively.

## Installation

The user will need to install the questionary and pytest modules as the program is dependent on them to run. The user can simply run:

```shell
pip install -r requirements.txt
```
When run successfully the questionary and pytest modules will be installed.
## Usage

To start the program the user will have to run the main module by typing:

```shell
python main.py
```

After the program starts the user will simply have to follow the instructions on screen.
They will first be asked whether they are ready or not which they can respond with either 'Y' or 'Enter' for Yes which continues program execution or 'N' for No which ends program execution.
If the user proceeds with Yes then they will then be able to select which action they want to take.
## Tests

```shell
pytest .
```