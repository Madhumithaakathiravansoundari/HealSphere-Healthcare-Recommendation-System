# HealSphere

HealSphere is a Flask-based health guidance web application that helps users explore diseases, body systems, treatments, nutrition, exercise, and wellness information. It also includes an AI assistant powered by Google Gemini and a few health calculators.

## Features

- Interactive dashboard and health-related landing pages
- Disease and symptom-based recommendations
- Information for:
  - symptoms
  - diagnosis
  - medicines
  - primary treatment
  - diet and hydration
  - exercise and yoga
  - prevention and emergency guidance
- AI assistant for health-related queries
- BMI calculator
- Water intake calculator
- Calorie calculator
- Subscription form for contact collection

## Project Structure

- app.py - Main Flask application
- datasets/ - CSV datasets used for disease and treatment information
- templates/ - HTML templates for the web pages
- static/ - Static assets such as CSS, JavaScript, and images
- report.pdf - Sample report file

## Requirements

Make sure you have Python installed.

Install the required Python packages:

```bash
pip install flask pandas google-genai pdfkit playwright
```

You will also need wkhtmltopdf installed on your system for PDF generation.

### Windows

Download and install wkhtmltopdf from:
https://wkhtmltopdf.org/downloads.html

Then make sure the executable is available in your system PATH or update the path inside app.py if needed.

## Run the Application

From the project folder, run:

```bash
python app.py
```

Then open your browser and go to:

```text
http://127.0.0.1:5000/
```

## Environment and Security Notes

The current application contains hard-coded credentials and API keys in app.py. For a production-ready version, move these values to environment variables and keep them out of source code.

## Notes

- The app reads disease-related data from CSV files in the datasets folder.
- The AI assistant uses Google Gemini and requires a valid API key.
- Some pages and features may require additional setup depending on your environment.

## License

This project is intended for educational and demonstration purposes.
