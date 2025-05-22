# JobNest - Job Application Tracking System

JobNest is a comprehensive job application tracking system built with Django that helps job seekers organize and manage their job search process effectively. With a modern, user-friendly interface and powerful features, JobNest makes it easy to keep track of your job applications, important resources, and career progress.

## Quick Start

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/jobnest.git
   cd jobnest
   ```

2. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run migrations:
   ```bash
   python manage.py migrate
   ```

5. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```bash
   python manage.py runserver
   ```

7. Visit http://127.0.0.1:8000/ in your browser

## Key Features

- **Dashboard Overview**: Visual dashboard showing all your job applications
- **Application Management**: Add, edit, and delete job applications with real-time updates
- **Status Tracking**: Track application status (Applied, Interviewing, Offer, Rejected)
- **Statistics**: Monthly application statistics with dynamic updates
- **Resource Center**: Access and share helpful resources in categories
- **User Features**: Secure authentication and private dashboard

## Technology Stack

- **Backend**: Django 5.2.1
- **Frontend**: Bootstrap 5, JavaScript (AJAX)
- **Database**: SQLite (default), compatible with PostgreSQL
- **UI Components**: Bootstrap Icons

## Documentation

For detailed documentation about:
- Project structure
- Implementation details
- API documentation
- Deployment guide
- Troubleshooting
- And more...

Please see the [Documentation](docs/DOCUMENTATION.md).

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with Django and Bootstrap
- Icons from Bootstrap Icons
- Community contributions welcome

## Future Enhancements

1. User Experience
   - Email notifications for application status changes
   - Interview scheduling and reminder system
   - Mobile app version
   - Advanced filtering and sorting options

2. Data and Analytics
   - Resume parser and ATS compatibility checker
   - Salary and benefits tracking
   - Job search analytics and insights
   - Company research integration

3. Integration and Export
   - Integration with popular job boards
   - Export functionality for application data
   - Network tracking for referrals
   - Calendar synchronization 
