# Job Application Tracker

A command-line interface (CLI) application to help you track and manage your job applications during your job search.

## Overview

Job Application Tracker is a Python-based CLI tool that makes it easy to:
- Keep track of job applications
- Manage companies you've applied to
- Tag applications for better organization
- Monitor application statuses
- Record follow-up dates

The application implements object-oriented programming principles to provide a clean, maintainable codebase with a user-friendly interface.

## Features

- **Job Application Management**
  - Create, update, and delete job applications
  - Track application status (applied, pending, rejected, offer)
  - Record application dates and follow-up dates

- **Company Management**
  - Store company information including websites and contact details
  - Easily associate companies with job applications
  - Create companies on-the-fly during job application creation

- **Tagging System**
  - Create custom tags for job applications
  - Support for different tag types (location, length)
  - Filter job applications by tags

- **User-Friendly Interface**
  - Color-coded terminal output for better readability
  - Clear command structure
  - Helpful error messages and validation

## Installation

### Prerequisites
- Python 3.6 or higher
- pip (Python package installer)

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/job-application-tracker.git
   cd job-application-tracker
   ```

2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Initialize the database:
   ```bash
   python setup_db.py
   ```

## Usage

### Starting the Application

Run the following command in your terminal:
```bash
python main.py
```

### Available Commands

| Command | Description |
|---------|-------------|
| `help` or `?` | Show all available commands |
| `list jobs` | Show all job applications |
| `create job` | Add a new job application |
| `update job` | Update an existing job application |
| `delete job` | Remove a job application |
| `list companies` | Show all companies |
| `create company` | Add a new company |
| `update company` | Update an existing company |
| `delete company` | Remove a company |
| `list tags` | Show all available tags |
| `create tag` | Add a new tag |
| `delete tag` | Remove a tag by ID |
| `assign tag` | Assign a tag to a job application |
| `remove tag` | Remove a tag from a job application |
| `list jobs by tag` | Show jobs associated with a tag |
| `exit` or `quit` | Exit the program |

## Project Structure

```
job-application-tracker/
├── main.py              # Application entry point
├── cli.py               # CLI class implementation
├── helpers.py           # Helper functions
├── setup_db.py          # Database initialization script
├── models/              # Database models
│   ├── __init__.py
│   ├── company.py       # Company model
│   ├── job_application.py  # Job application model
│   ├── tag.py           # Tag model
│   └── job_application_tag.py  # Many-to-many relationship model
├── requirements.txt     # Package dependencies
└── README.md            # This file
```

## Database Schema

The application uses a relational database with the following structure:

- **companies**
  - id (INTEGER PRIMARY KEY)
  - name (TEXT)
  - website (TEXT)
  - contact_info (TEXT)

- **job_applications**
  - id (INTEGER PRIMARY KEY)
  - job_title (TEXT)
  - company_id (INTEGER, FOREIGN KEY)
  - description (TEXT)
  - date_applied (DATE)
  - last_follow_up (DATE)
  - status (TEXT)

- **tags**
  - id (INTEGER PRIMARY KEY)
  - name (TEXT)
  - tag_type (TEXT)

- **job_application_tags**
  - id (INTEGER PRIMARY KEY)
  - job_application_id (INTEGER, FOREIGN KEY)
  - tag_id (INTEGER, FOREIGN KEY)

## Development

### Adding New Features

To add new commands:

1. Add a new method to the `CLI` class in `cli.py`
2. Add the command to the `command_handlers` dictionary in the `__init__` method

### Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [Rich](https://github.com/Textualize/rich) library for beautiful terminal formatting
- SQLite for database functionality