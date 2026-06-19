from flask import Flask, render_template, request
import joblib
import pandas as pd

from feature_extractor import extract_features


app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 1 * 1024 * 1024

model = joblib.load("trained_model.pkl")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["GET", "POST"])
def predict():

    if request.method == "GET":
        return render_template("index.html")

    uploaded_file = request.files.get("file")
    pasted_code = request.form.get("code_input", "").strip()

    file_provided = uploaded_file and uploaded_file.filename != ""
    paste_provided = pasted_code != ""

    if file_provided and paste_provided:
        return render_template(
            "index.html",
            error="Please use only one input method: either upload a file OR paste code, not both."
        )

    if file_provided:

        if not uploaded_file.filename.lower().endswith(".py"):
            return render_template(
                "index.html",
                error="Please upload a Python (.py) file."
            )

        filename = uploaded_file.filename
        code = uploaded_file.read().decode(
            "utf-8",
            errors="replace"
        )

    elif paste_provided:
        filename = "Pasted Python Code"
        code = pasted_code

    else:
        return render_template(
            "index.html",
            error="Please upload a file or paste some Python code."
        )

    if code.strip() == "":
        return render_template(
            "index.html",
            error="The submitted code is empty. Please provide Python code to analyse."
        )

    features = extract_features(code)

    input_features = pd.DataFrame([features])

    prediction = model.predict(input_features)[0]
    probability = model.predict_proba(input_features)[0]
    confidence = round(max(probability) * 100, 2)

    rule_based_bug = False

    bug_reason = "No major issue detected."
    bug_impact = (
        "The code does not show an obvious beginner-level bug pattern."
    )
    bug_fix = "No specific fix is required."
    corrected_code = ""

    bug_checks = {
        "/ 0": {
            "reason": "Possible division by zero detected.",
            "impact": (
                "Dividing by zero causes the program to stop with a "
                "ZeroDivisionError at runtime."
            ),
            "fix": (
                "Check that the denominator is not zero before performing "
                "division."
            ),
            "corrected_code": (
                "denominator = 2\n"
                "\n"
                "if denominator != 0:\n"
                "    result = 10 / denominator\n"
                "    print(result)\n"
                "else:\n"
                "    print('Cannot divide by zero')"
            )
        },

        "while True": {
            "reason": "Possible infinite loop detected.",
            "impact": (
                "An infinite loop may cause the program to run forever "
                "and become unresponsive."
            ),
            "fix": (
                "Add a stopping condition or break statement to prevent "
                "the loop from running forever."
            ),
            "corrected_code": (
                "count = 0\n"
                "\n"
                "while count < 5:\n"
                "    print(count)\n"
                "    count += 1"
            )
        },

        "open(\"missing.txt\"": {
            "reason": "Possible missing file error detected.",
            "impact": (
                "Trying to open a file that does not exist can stop the "
                "program with a FileNotFoundError."
            ),
            "fix": (
                "Check that the file exists before opening it or use "
                "try/except for file handling."
            ),
            "corrected_code": (
                "try:\n"
                "    with open('sample.txt', 'r') as file:\n"
                "        content = file.read()\n"
                "        print(content)\n"
                "except FileNotFoundError:\n"
                "    print('File not found')"
            )
        },

        "open('missing.txt'": {
            "reason": "Possible missing file error detected.",
            "impact": (
                "Trying to open a file that does not exist can stop the "
                "program with a FileNotFoundError."
            ),
            "fix": (
                "Check that the file exists before opening it or use "
                "try/except for file handling."
            ),
            "corrected_code": (
                "try:\n"
                "    with open('sample.txt', 'r') as file:\n"
                "        content = file.read()\n"
                "        print(content)\n"
                "except FileNotFoundError:\n"
                "    print('File not found')"
            )
        },

        "print(totl)": {
            "reason": "Possible wrong variable name detected.",
            "impact": (
                "Using a misspelled variable name can cause a NameError "
                "because the variable was never defined."
            ),
            "fix": (
                "Check the spelling of variable names. You may have meant "
                "'total' instead of 'totl'."
            ),
            "corrected_code": (
                "total = 0\n"
                "\n"
                "for number in range(1, 6):\n"
                "    total += number\n"
                "\n"
                "print(total)"
            )
        },

        "nam)": {
            "reason": "Possible undefined variable detected.",
            "impact": (
                "Using an undefined variable prevents the program from "
                "running correctly."
            ),
            "fix": (
                "Use the correct variable name. You may have meant "
                "'name' instead of 'nam'."
            ),
            "corrected_code": (
                "def greet(name):\n"
                "    print('Hello ' + name)\n"
                "\n"
                "greet('Emad')"
            )
        },

        "radius = \"five\"": {
            "reason": "Possible wrong data type detected.",
            "impact": (
                "Mathematical operations require numeric values. Using "
                "text can cause a TypeError."
            ),
            "fix": (
                "Use a numeric value such as radius = 5 instead of a "
                "text value."
            ),
            "corrected_code": (
                "import math\n"
                "\n"
                "radius = 5\n"
                "area = math.pi * radius ** 2\n"
                "\n"
                "print(area)"
            )
        },

        "radius = 'five'": {
            "reason": "Possible wrong data type detected.",
            "impact": (
                "Mathematical operations require numeric values. Using "
                "text can cause a TypeError."
            ),
            "fix": (
                "Use a numeric value such as radius = 5 instead of a "
                "text value."
            ),
            "corrected_code": (
                "import math\n"
                "\n"
                "radius = 5\n"
                "area = math.pi * radius ** 2\n"
                "\n"
                "print(area)"
            )
        },

        "print(numbers[i])": {
            "reason": "Possible list index out of range detected.",
            "impact": (
                "The loop may use an index that is larger than the number "
                "of items in the list, causing an IndexError."
            ),
            "fix": (
                "Use range(len(numbers)) or iterate directly over the "
                "list items."
            ),
            "corrected_code": (
                "numbers = [1, 2, 3]\n"
                "\n"
                "for number in numbers:\n"
                "    print(number)"
            )
        },

        "int(input(": {
            "reason": "Possible unsafe input conversion detected.",
            "impact": (
                "Converting user input directly with int() will crash "
                "with a ValueError if the user enters non-numeric text."
            ),
            "fix": (
                "Wrap the conversion in a try/except block to handle "
                "invalid input safely."
            ),
            "corrected_code": (
                "try:\n"
                "    number = int(input('Enter a number: '))\n"
                "    print(number)\n"
                "except ValueError:\n"
                "    print('Please enter a valid number')"
            )
        }
    }

    for pattern, details in bug_checks.items():
        if pattern in code:
            rule_based_bug = True
            bug_reason = details["reason"]
            bug_impact = details["impact"]
            bug_fix = details["fix"]
            corrected_code = details.get(
                "corrected_code",
                ""
            )
            break

    if features["syntax_error"] == 1:
        rule_based_bug = True

        bug_reason = "Syntax error detected in the Python code."

        bug_impact = (
            "Syntax errors prevent Python from understanding and running "
            "the program."
        )

        bug_fix = (
            "Check for missing colons, brackets, indentation problems, "
            "or other incorrect Python syntax."
        )

        corrected_code = (
            "# Example of valid Python syntax:\n"
            "condition = True\n"
            "\n"
            "if condition:\n"
            "    print('Correct indentation and syntax')"
        )

    ml_result = "Buggy" if prediction == 1 else "Not Buggy"

    if rule_based_bug:
        result = "Buggy"
        confidence = max(confidence, 85)

    else:
        result = ml_result

        if result == "Not Buggy":
            bug_reason = (
                "No obvious syntax or rule-based bug was detected."
            )

            bug_impact = (
                "The code appears structurally valid, but logical "
                "correctness should still be confirmed using test cases."
            )

            bug_fix = (
                "Test the program with normal, boundary, and invalid "
                "inputs."
            )

            corrected_code = ""

        else:
            bug_reason = (
                "The machine-learning model identified structural "
                "patterns associated with buggy or low-quality code."
            )

            bug_impact = (
                "The code may contain a logical or structural issue that "
                "is not covered by the current rule-based checks."
            )

            bug_fix = (
                "Review the program logic, variable use, conditions, "
                "loops, and expected outputs."
            )

            corrected_code = ""

    quality_score = 100

    quality_score -= features["syntax_error"] * 40
    quality_score -= features["loops"] * 5
    quality_score -= features["ifs"] * 3
    quality_score -= features["functions"] * 2
    quality_score -= features["try_blocks"] * 1

    if rule_based_bug:
        quality_score -= 35

    quality_score = max(
        0,
        min(100, quality_score)
    )

    if quality_score >= 80:
        severity = "Low"

    elif quality_score >= 50:
        severity = "Medium"

    else:
        severity = "High"

    if quality_score >= 85:
        health_status = "Excellent"

    elif quality_score >= 65:
        health_status = "Moderate Risk"

    else:
        health_status = "Critical Risk"

    complexity_score = (
        features["loops"]
        + features["ifs"]
        + features["functions"]
    )

    if complexity_score <= 2:
        complexity_level = "Low"

    elif complexity_score <= 5:
        complexity_level = "Medium"

    else:
        complexity_level = "High"

    suggestions = []

    if features["syntax_error"] == 1:
        suggestions.append(
            "Fix syntax errors before running the code."
        )

    if "division by zero" in bug_reason.lower():
        suggestions.append(
            "Add a condition to check that the denominator is not zero."
        )

    if "infinite loop" in bug_reason.lower():
        suggestions.append(
            "Add a stopping condition to avoid an infinite loop."
        )

    if "undefined variable" in bug_reason.lower():
        suggestions.append(
            "Check variable names and make sure all variables are "
            "defined before use."
        )

    if "wrong variable name" in bug_reason.lower():
        suggestions.append(
            "Check the spelling of variable names and replace the "
            "incorrect name with the intended variable."
        )

    if (
        "type error" in bug_reason.lower()
        or "wrong data type" in bug_reason.lower()
    ):
        suggestions.append(
            "Check data types before performing operations."
        )

    if "missing file" in bug_reason.lower():
        suggestions.append(
            "Check that the file exists before opening it."
        )

    if "index out of range" in bug_reason.lower():
        suggestions.append(
            "Use range(len(numbers)) or iterate directly over the "
            "list items."
        )

    if "unsafe input conversion" in bug_reason.lower():
        suggestions.append(
            "Use a try/except block when converting user input with "
            "int() or float()."
        )

    if len(suggestions) == 0:

        if result == "Not Buggy":
            suggestions.append(
                "The code appears structurally safe based on the current "
                "analysis."
            )

        else:
            suggestions.append(
                "Review the program logic and test with different inputs."
            )

    return render_template(
        "result.html",
        result=result,
        confidence=confidence,
        quality_score=quality_score,
        severity=severity,
        health_status=health_status,
        complexity_level=complexity_level,
        bug_reason=bug_reason,
        bug_impact=bug_impact,
        bug_fix=bug_fix,
        corrected_code=corrected_code,
        suggestions=suggestions,
        code=code,
        filename=filename,
        features=features
    )


if __name__ == "__main__":
    app.run(debug=True)