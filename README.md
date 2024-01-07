# IrateInBackend

## Description

ChatApp Full-Stack Role Hands-On Tasks.

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)

## Requirements

- Python 3.12.1
- Django 5.0
- pip 23.3.2

## Installation

### Clone the Repositoy

```bash
git clone https://github.com/adedamolabasit/IrateInBackend
cd IrateInBackend
```

### Create and Activate Virtual Environment

```bash
python -m venv venv
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### Install Dependencies

```bash
pip3 install -r requirements.txt
```

## Configuration

### Install Dependencies

```bash
python manage.py migrate
```

### Create a Superuser (Optional)
```bash
python manage.py createsuperuser
```

### Environment Variables
***Copy the .env.example file to .env and update the values accordingly.***
```bash
cp .env.example .env
```

## Usage
```bash
python manage.py runserver
```