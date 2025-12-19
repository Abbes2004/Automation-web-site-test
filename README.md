# ISTQB Project – Automated Software Testing

## Project Overview
This project is part of an ISTQB-oriented software testing practice.

It focuses on the design, implementation, and execution of automated tests for a SaaS online service booking application (**Trafft**). 
The primary goal is to validate the functional behavior, robustness, and reliability of the application using automated testing techniques.

## Project Objectives
* Apply ISTQB principles in a real-world scenario.
* Design functional, negative, and boundary value test cases.
* Automate test execution using **Selenium WebDriver** and **PyTest**.
* Detect and document anomalies (bugs).
* Improve test repeatability and coverage.

## Test Scope
* Frontend (Client-side) testing.
* Booking workflow validation.
* Data input verification and error message handling.
* Multi-browser compatibility.
* Load and concurrency testing.

## Technologies and Tools Used
* **Language:** Python 3.11
* **Testing Framework:** PyTest
* **Automation Tool:** Selenium WebDriver
* **Design Pattern:** Page Object Model (POM)
* **IDE:** PyCharm / VS Code
* **Browsers:** Google Chrome, Firefox, Microsoft Edge

## Project Structure
The project is organized modularly to facilitate test automation:

* **tests/:** Automated test cases.
* **pages/:** POM classes representing each application page.
* **utils/:** Reusable helper functions and utilities.
* **screenshots/:** Screen captures of anomalies and test results.
* **reports/:** Test execution reports.
* **README.md:** Project documentation.
* **requirements.txt:** Python dependencies.
* **pytest.ini:** PyTest configuration file.

## How to Run the Tests
1. Install Python dependencies: `pip install -r requirements.txt`
2. Run tests using PyTest: `pytest`
3. Generate detailed execution reports (HTML) for each run.

## Defect Management
Detected bugs are documented with:
* Test Case ID
* Problem description
* Expected result vs. Actual result
* Screenshots

This approach ensures efficient reproduction and tracking of anomalies.

## Authors
* **Amine Abbes**
* **Med Bechir Torki**
* **Academic Year:** 2025–2026
