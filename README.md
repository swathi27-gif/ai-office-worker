
# AI Office Worker

An autonomous AI agent prototype for invoice processing, data extraction, validation, and database storage.

## Overview

AI Office Worker processes invoice PDF files, extracts relevant information, validates required fields, and saves valid invoice records to a database. It also identifies incomplete invoices and reports errors for review.

## Features

- PDF invoice discovery and processing
- Invoice data extraction
- Required-field validation
- Latest invoice selection
- SQLite database storage
- Duplicate-record handling
- Tool-based agent execution
- Task understanding and planning
- Error handling and retry logic
- Automated tests

## Project Structure

```text
ai-office-worker/
├── invoices/
├── app.py
├── agent.py
├── planner.py
├── tool_registry.py
├── tools.py
├── database.py
├── test_agent.py
├── test_database.py
├── test_planner.py
├── test_reliability.py
├── test_tool_registry.py
├── test_tools.py
└── .gitignore
```

## Technology Stack

- Python
- Streamlit
- SQLite
- PyMuPDF
- Pytest

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/swathi27-gif/ai-office-worker.git
cd ai-office-worker
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

Install the required packages after creating a `requirements.txt` file:

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
streamlit run app.py
```

### 5. Run the tests

```bash
python -m pytest -v
```

## Reliability

The project includes tests for invoice extraction, database operations, task planning, tool execution, and error handling.

Run the full test suite before using the application.

## Future Improvements

- Support additional invoice formats
- Improve extraction accuracy for varied layouts
- Add more invoice validation rules
- Integrate an LLM for more flexible task understanding
- Add authentication and deployment support

## Author

Swathi Nethavath

## License

This project is currently a prototype. A license can be added when the distribution terms are decided.

