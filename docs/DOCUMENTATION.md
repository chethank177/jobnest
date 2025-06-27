# JobNest - Job Application Tracking System Documentation

## Project Overview
JobNest is a modern Django web application that helps job seekers efficiently track, manage, and analyze their job applications. It features a dashboard for job tracking, categorized resource sharing, and user account management—all with a responsive, interactive UI and real-time updates.

---

## Project Structure (Directory Map)
```
jobnest/                  # Project root
├── accounts/             # User authentication and profile management
├── community/            # (Optional) Community features (e.g., forums)
├── resources/            # Resource sharing, categories, and comments
│   ├── templates/resources/   # Resource-related templates
│   ├── models.py         # Resource and Comment models
│   ├── views.py          # Resource list/detail/add/edit/delete views
│   └── ...
├── tracker/              # Job application tracking core app
│   ├── templates/tracker/     # Dashboard and job modals
│   ├── models.py         # JobApplication model and manager
│   ├── views.py          # Dashboard, stats, AJAX endpoints
│   └── ...
├── static/               # Static files (CSS, JS, images)
├── templates/            # Global templates (base.html, etc.)
├── docs/                 # Project documentation
│   └── DOCUMENTATION.md  # This documentation file
├── manage.py             # Django management script
├── requirements.txt      # Python dependencies
└── db.sqlite3            # SQLite database (dev)
```

---

## Application Modules

### 1. **tracker**
- **Purpose:** Core job application management (add, edit, delete, status, notes, stats)
- **Key Features:**
  - Dashboard with job cards and filters
  - AJAX-powered add/edit/delete (no reload)
  - Real-time statistics (total, active, offers, rejected)
  - Modals for job CRUD

### 2. **resources**
- **Purpose:** Share and browse categorized resources (Resume, Job Portal, Interview, Cover Letter, Other)
- **Key Features:**
  - Category tabs with resource cards
  - Comment system for each resource
  - Admin add/edit/delete
  - Shows "No resources available" only when truly empty

### 3. **accounts**
- **Purpose:** User authentication and profile management
- **Key Features:**
  - Registration, login, logout
  - My Account modal with live stats
  - Profile details

### 4. **community** (optional)
- **Purpose:** Community features (e.g., forums, discussions)
- **Status:** Placeholder for future expansion

---

## High-Level Features
- **Job Application Tracking:** Add, edit, delete, and filter job applications with status and notes
- **Statistics Dashboard:** Live stats for total, active, offers, and rejected applications
- **Resource Library:** Browse and manage categorized resources with comments
- **User Management:** Secure authentication, profile, and account stats
- **Responsive UI:** Bootstrap 5, modals, and AJAX for a modern experience
- **Security:** CSRF protection, secure forms, user access control

---

## How It Works (User Flow)
1. **Login/Register:** Users create an account or log in
2. **Dashboard:** Users see all their job applications, can add new ones, edit, or delete
3. **Statistics:** Stats update live as jobs are managed
4. **Resources:** Users browse resources by category, add comments, and admins can manage resources
5. **My Account:** Modal shows user info and live-updating stats

---

## Quickstart
1. Clone the repo and set up a virtual environment
2. Install dependencies: `pip install -r requirements.txt`
3. Run migrations: `python manage.py migrate`
4. Create a superuser: `python manage.py createsuperuser`
5. Start the server: `python manage.py runserver`
6. Access the site at `http://localhost:8000/`

---

## For Developers
- **tracker/models.py:** JobApplication model and manager for stats
- **resources/models.py:** Resource and Comment models
- **AJAX:** Used for job CRUD and stats updates (see dashboard.html)
- **Custom template tags:** Used for category lookups in resources
- **All category tabs work even for empty categories (shows message only if truly empty)**

---

For more details, see the rest of this DOCUMENTATION.md.

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