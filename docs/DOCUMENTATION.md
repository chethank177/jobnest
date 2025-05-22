# JobNest - Job Application Tracking System Documentation

## Project Overview
JobNest is a Django-based web application designed to help job seekers track and manage their job applications efficiently. The application provides a modern, user-friendly interface with real-time updates and comprehensive statistics.

## Project Structure
```
jobnest_site/              # Project root directory
├── docs/                  # Documentation folder (you are here)
│   └── README.md         # This documentation file
├── jobnest/              # Main Django project directory
│   ├── accounts/         # User authentication app
│   ├── resources/        # Resource sharing app
│   ├── tracker/          # Main job tracking app
│   ├── static/           # Static files
│   ├── templates/        # Global templates
│   └── manage.py         # Django management script
├── .venv/                # Virtual environment
└── requirements.txt      # Project dependencies
```

## Technology Stack

### Backend Framework
- Django (Python web framework)
  - Used for its robust ORM, built-in authentication, and rapid development capabilities
  - Handles database operations, user authentication, and server-side logic

### Frontend Technologies
- HTML5/CSS3
- Bootstrap 5
  - Provides responsive design and modern UI components
  - Used for modals, cards, and grid system
- JavaScript (Vanilla)
  - Handles AJAX requests for real-time updates
  - Manages dynamic UI updates without page reloads

### Database
- SQLite (Development)
  - Can be easily migrated to PostgreSQL for production

### Key Libraries and Dependencies
1. python-dateutil
   - Purpose: Advanced date handling and manipulation
   - Used in: Monthly statistics and date formatting

2. Bootstrap Icons
   - Purpose: Modern icon set for UI elements
   - Used in: Navigation, buttons, and status indicators

## Core Applications

### 1. tracker (Main Application)
Location: `jobnest/tracker/`
- **models.py**
  - JobApplication model with fields:
    - role (CharField)
    - company (CharField)
    - date_applied (DateField)
    - status (CharField with choices)
    - job_url (URLField, optional)
    - notes (TextField, optional)
  - Custom JobApplicationManager for statistics

- **views.py**
  - dashboard: Main view for job applications
  - get_stats: AJAX endpoint for real-time statistics
  - get_month_stats: Monthly application statistics

- **urls.py**
  - URL patterns for all tracker functionality
  - AJAX endpoint routes

- **templates/tracker/**
  - dashboard.html: Main interface
  - Includes modals for add/edit/delete

### 2. resources (Resource Sharing)
Location: `jobnest/resources/`
- Resource sharing and management
- Comment system
- Category-based organization

### 3. accounts (User Management)
Location: `jobnest/accounts/`
- User authentication
- Profile management
- User-specific settings

## Key Features

### 1. Job Application Management
- Add/Edit/Delete applications
- Status tracking:
  - Applied
  - Interviewing
  - Offer
  - Rejected
- Notes and URL storage
- Real-time updates

### 2. Statistics Dashboard
- Total applications count
- Monthly application breakdown
- Active applications tracking
- Offer statistics

### 3. Resource Sharing
- Categorized resources
- User comments
- Admin management

### 4. User Experience
- Real-time updates without page reload
- Responsive design
- Interactive modals
- Toast notifications

## Implementation Details

### Real-time Updates
```javascript
// Global function to update statistics
function updateAllStats() {
  fetch('{% url "tracker:get_stats" %}')
    .then(response => response.json())
    .then(data => {
      document.getElementById('total-applications').textContent = data.total;
      document.getElementById('active-applications').textContent = data.active;
      document.getElementById('total-offers').textContent = data.offers;
    });
}

// Custom event for job updates
document.addEventListener('jobApplicationUpdated', updateAllStats);
```

### Custom Model Manager
```python
class JobApplicationManager(models.Manager):
    def get_month_stats(self, year=None, month=None):
        if year is None or month is None:
            today = timezone.now()
            year = today.year
            month = today.month
        return self.filter(
            date_applied__year=year,
            date_applied__month=month
        ).count()

    def get_total_active(self):
        return self.filter(status__in=['applied', 'interviewing']).count()
```

## Getting Started

1. Clone the repository
2. Create virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   source .venv/bin/activate  # Linux/Mac
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run migrations:
   ```bash
   cd jobnest
   python manage.py migrate
   ```

5. Create superuser:
   ```bash
   python manage.py createsuperuser
   ```

6. Run development server:
   ```bash
   python manage.py runserver
   ```

## Development Workflow

### Database Migrations
When modifying models:
```bash
python manage.py makemigrations
python manage.py migrate
```

### Static Files
During development:
```bash
python manage.py collectstatic
```

## Security Features
- CSRF protection enabled
- User authentication required
- Secure form handling
- XSS prevention
- SQL injection protection

## Troubleshooting

### Common Issues

1. Database migrations
   - Check migration history: `python manage.py showmigrations`
   - Reset migrations if needed: `python manage.py migrate app_name zero`

2. Static files not loading
   - Check STATIC_ROOT in settings.py
   - Run collectstatic
   - Verify static files directory structure

3. AJAX updates not working
   - Check browser console for errors
   - Verify CSRF token is being sent
   - Check URL patterns in urls.py

### Solutions

1. Clear browser cache
2. Check server logs
3. Verify JavaScript console
4. Review Django debug page

## Future Enhancements

1. Email Notifications
   - Application status changes
   - Interview reminders
   - Weekly statistics

2. Data Analytics
   - Application success rates
   - Interview conversion metrics
   - Industry-specific insights

3. API Integration
   - Job board integration
   - Calendar synchronization
   - Email parsing for automatic entry 