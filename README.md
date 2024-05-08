# Code Smell Detector and Refactoring Tool

## Overview
This individual project for CPSC 5910 Software Refactoring is focused on creating a program that detects and refactors code smells. The program includes a graphical user interface (GUI) to facilitate user interaction.

## Features

### Code Smell Detection
The program is designed to detect the following code smells:
- **Long Method/Function**: Defined as a method/function exceeding 15 lines of code (excluding blank lines).
- **Long Parameter List**: Defined as a method/function with four or more parameters.
- **Duplicated Code**: Detection is based on Jaccard Similarity, with a threshold set at 0.75.

### Refactoring
If duplicated code is detected, the tool prompts the user to refactor this code. The program then generates a file containing the refactored code.

### Graphical User Interface
The GUI allows users to:
1. Upload a single code file.
2. Analyze the code for smells and prompt for detected issues.
3. Optionally refactor duplicated code.
4. Exit the program.

