# Student Python Bug Detector

A Flask web application that analyses beginner Python code and predicts whether it is likely to be buggy, using a hybrid of machine learning and rule-based detection. It is designed as an educational tool for students learning Python.

## Overview

A user uploads a `.py` file or pastes Python code. The system extracts structural features, runs them through a Random Forest model, applies rule-based and AST-based checks for common errors, and returns a clear verdict with explanations, suggested fixes, and a quality assessment.

## Features

- Upload a `.py` file or paste code directly
- Hybrid detection: rule-based checks + machine learning model
- AST-based undefined-variable (NameError) detection
- Detection of common beginner mistakes: division by zero, infinite loops, type errors, index errors, unsafe input conversion, and more
- Clear verdict: Buggy / Not Buggy with a confidence score
- Code quality score, severity level, and complexity level
- Plain-language explanation: the issue, why it matters, and a suggested fix
- "Detected By" label showing whether the rule-based or ML method made the decision
- Side-by-side learning example (buggy vs corrected) where available
- Downloadable analysis report (TXT and JSON)
- Comparison page: this system vs general AI tools like ChatGPT
- Input validation for safe, reliable use

## Technology Stack

- Python 3.12
- Flask (web framework)
- scikit-learn (Random Forest model)
- pandas (data handling)
- Python AST module (structural analysis)
- HTML / CSS (interface)

## How It Works

The analysis follows this pipeline:

1. Python code is provided by upload or paste
2. Structural features are extracted using the AST
3. The Random Forest model and the rule-based / AST checks run
4. A hybrid decision combines both methods
5. The result is shown on the dashboard

## Project Structure

- `app.py` - main Flask application
- `feature_extractor.py` - AST feature extraction and undefined-variable detection
- `train_model.py` - trains the Random Forest model
- `create_dataset.py` - builds the dataset from sample files
- `evaluate_model.py` - evaluates model accuracy
- `pylint_baseline.py` - Pylint comparison script
- `dataset/samples/` - labelled good and buggy Python samples
- `templates/` - HTML pages
- `static/` - CSS

## Setup and Running

1. Create and activate a virtual environment:
   python -m venv venv
   .\venv\Scripts\Activate.ps1
2. Install dependencies:
   pip install -r requirements.txt
3. Run the application:
   python app.py
4. Open http://127.0.0.1:5000 in a browser.

## Evaluation

The model was evaluated on a labelled dataset of beginner Python programs. Accuracy is around 65%, with stronger performance on buggy detection than on correctly identifying all good code. Analysis of feature importance showed the model relies heavily on structural measures such as line count, which means it tends to associate complexity with bugs.

## Limitations

- Features measure structural complexity rather than actual program defects, so the model can over-flag complex but correct code.
- Rule-based checks use pattern matching and cover common beginner mistakes, not all possible bugs.
- Undefined-variable detection identifies names that are never defined; it does not track order of use within a scope.
- The system does not execute code, so it cannot detect every runtime error.

## Future Work

- Richer features that capture program behaviour, not just structure
- A larger and more diverse dataset
- Integration with large language models for deeper, natural-language code analysis
- More advanced AST-based detection of logical errors

## Author

Final Year Project - Student Python Bug Detector
Md Emad Alom - B00965974
