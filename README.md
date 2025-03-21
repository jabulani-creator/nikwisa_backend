# Nikwisa Backend

## Overview

Nikwisa is a local search and business directory platform connecting users with event planning service providers (e.g., wedding planners, DJs) in Zambia. This repository contains the Django backend, handling user authentication, business listings, and API endpoints for the Next.js frontend.

- **Stack:** Django (Python), SQLite (development DB)
- **Purpose:** Provides REST API endpoints for user management, business profiles, and reviews.
- **Frontend Repo:** `https://github.com/jabulani-creator/nikwisa-frontend`
- **Current State:** Partially built—signup/login works (no OTP), business profiles save data, but features like OTP auth and search are pending.

## Problem Statement

Nikwisa solves the challenge of finding reliable service providers in a fragmented market. For event planning, users rely on word-of-mouth or scattered listings. Nikwisa centralizes search, comparison, and contact, offers verified listings for trust, streamlines communication, and boosts business visibility.

## Prerequisites

- Python 3.8+
- pip (Python package manager)
- Virtualenv (recommended for isolated environments)

## Setup Instructions

1. **Clone the Repository**

   ```bash
   git clone https://github.com/jabulani-creator/nikwisa_backend.git
   cd nikwisa_backend

   ```

2. **Set Up a Virtual Environment**  
   python -m venv env
   source env/bin/activate # On Windows: env\Scripts\activate
   cd nikwisa

3. **Install Dependencies**
   pip install -r requirements.txt

4. **Run Migrations**
   python manage.py makemigrations
   python manage.py migrate

## Running the Backend

1. **Start the Development Server**
   python manage.py runserver

The API will be available at http://localhost:8000/api/v1/test/.

2. **Test Endpoints**
   Example: GET /api/v1/test/users (list users—adjust based on your actual endpoints).
   Use tools like Postman or curl to test.
