# FRA Atlas - Forest Rights Act Dashboard & Decision Support System

A Django-based web application for visualizing Forest Rights Act (FRA) data across Indian states and districts with interactive dashboards and mapping capabilities.

## Features

- **Interactive Dashboard**: Charts and statistics for FRA claims data
- **GIS Mapping**: District-wise visualization with color-coded approval rates
- **Decision Support System**: AI-powered scheme recommendations
- **Multi-state Coverage**: Data for Madhya Pradesh, Chhattisgarh, Odisha, and Telangana

## Tech Stack

- **Backend**: Django 4.x, PostgreSQL
- **Frontend**: Bootstrap 5, Chart.js, Leaflet.js
- **Database**: PostgreSQL with spatial capabilities
- **Maps**: OpenStreetMap tiles

## Setup Instructions

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Configure PostgreSQL database in `settings.py`
4. Run migrations: `python manage.py migrate`
5. Load sample data: `python load_data.py`
6. Start server: `python manage.py runserver`

## Project Structure

- `main/` - Main Django app with models, views, templates
- `load_data.py` - Script to populate database with FRA statistics
- `static/` - CSS, JS, and image assets
- `templates/` - HTML templates for dashboard, map, and home pages

## Database Models

- **State**: Indian states with FRA implementation
- **District**: Districts within states
- **ClaimStatistics**: FRA claim filing and approval data
- **SchemeRecommendation**: Government scheme suggestions

## License

MIT License