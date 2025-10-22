# OlympiadHub

**OlympiadHub** is a comprehensive platform designed to help students prepare for academic olympiads and university admissions. The system consists of three main components working together to provide olympiad information, notifications, and user management.

## 🏆 Features

- **Web Application**: Django-based platform for browsing olympiad information
- **Telegram Bot**: Real-time notifications and interaction via Telegram
- **User Management**: Registration, authentication, and profile management
- **Notification System**: Email and Telegram notifications for olympiad deadlines
- **Subject Filtering**: Browse olympiads by academic subjects
- **Admin Panel**: Comprehensive administration interface

## 🏗️ Architecture

The project follows a microservices architecture with the following components:

1. **Django Web Application** - Main web interface
2. **Telegram Bot** - Notification and interaction service
3. **PostgreSQL** - Primary database
4. **Redis** - Caching and message broker
5. **Celery** - Asynchronous task processing
6. **Nginx** - Reverse proxy and static file serving
7. **Flower** - Celery monitoring interface

## 📂 Project Structure

```
OlympiadHub/
├── Site/                    # Django web application
│   ├── manage.py
│   ├── Site/               # Django project settings
│   ├── olympic/            # Main Django app
│   │   ├── models.py       # Database models
│   │   ├── views.py        # View functions
│   │   ├── urls.py         # URL routing
│   │   ├── forms.py        # Django forms
│   │   ├── templates/      # HTML templates
│   │   └── static/         # Static files (CSS, JS, images)
│   └── requirements.txt
├── TelegramBot/            # Telegram bot application
│   ├── main_olympiads.py   # Bot entry point
│   ├── handlers/           # Message handlers
│   ├── keyboards/          # Bot keyboards
│   ├── utils/              # Utility functions
│   └── requirements.txt
├── nginx/                  # Nginx configuration
│   ├── Dockerfile
│   └── nginx.conf
├── docker-compose.yml      # Docker services orchestration
└── README.md
```

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/OlympiadHub.git
   cd OlympiadHub
   ```

2. **Create environment files**
   
   Create `.env.db` in the root directory:
   ```env
   SQL_ENGINE=django.db.backends.postgresql
   POSTGRES_USER=olympiad_user
   POSTGRES_PASSWORD=your_secure_password
   POSTGRES_HOST=postgres
   POSTGRES_DB=olympiadhub
   POSTGRES_PORT=5432
   ```

   Create `Site/.env.site`:
   ```env
   SECRET_KEY=your_django_secret_key_here
   DEBUG=False
   ALLOWED_HOSTS=localhost,your-domain.com
   DATABASE_URL=postgres://olympiad_user:your_secure_password@postgres:5432/olympiadhub
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   EMAIL_HOST_USER=your_email@gmail.com
   EMAIL_HOST_PASSWORD=your_app_password
   ```

   Create `TelegramBot/.env.tg`:
   ```env
   TELEGRAM_TOKEN=your_telegram_bot_token
   ADMINS=123456789,987654321
   ```

3. **Start the application**
   ```bash
   docker-compose up --build -d
   ```

4. **Run database migrations**
   ```bash
   docker-compose exec django python manage.py migrate
   ```

5. **Create a superuser**
   ```bash
   docker-compose exec django python manage.py createsuperuser
   ```

6. **Collect static files**
   ```bash
   docker-compose exec django python manage.py collectstatic --noinput
   ```

## 🌐 Access Points

- **Web Application**: http://localhost
- **Admin Panel**: http://localhost/admin/
- **Flower (Celery Monitor)**: http://localhost:5555

## 🔧 Configuration

### Database Models

The application includes the following main models:

- **Olympiad**: Stores olympiad information (title, dates, subjects, etc.)
- **Subject**: Academic subjects for olympiad categorization
- **SiteRegistration**: User registrations from the web platform
- **TelegramRegistration**: User registrations from the Telegram bot
- **NotificationSubscription**: User notification preferences
- **UserTelegramConnection**: Links web users with Telegram accounts
- **SecretToken**: Tokens for connecting web and Telegram accounts

### Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `POSTGRES_USER` | PostgreSQL username | `olympiad_user` |
| `POSTGRES_PASSWORD` | PostgreSQL password | `secure_password123` |
| `POSTGRES_DB` | Database name | `olympiadhub` |
| `SECRET_KEY` | Django secret key | `django-insecure-...` |
| `TELEGRAM_TOKEN` | Telegram bot token | `123456789:ABC...` |
| `EMAIL_HOST_USER` | SMTP email address | `your_email@gmail.com` |

## 📱 Telegram Bot Commands

- `/start` - Initialize the bot and show main menu
- Main menu options:
  - Get Secret Token for synchronization
  - Get olympiad information
  - View connected notifications
  - Connect/Remove notifications
  - Leave feedback
  - Contact technical support

## 🛠️ Development

### Running in Development Mode

1. **Install Python dependencies**
   ```bash
   cd Site
   pip install -r requirements.txt
   
   cd ../TelegramBot
   pip install -r requirements.txt
   ```

2. **Set up PostgreSQL database**
   ```bash
   # Install PostgreSQL and create database
   createdb olympiadhub
   ```

3. **Run Django development server**
   ```bash
   cd Site
   python manage.py runserver
   ```

4. **Run Telegram bot**
   ```bash
   cd TelegramBot
   python main_olympiads.py
   ```

### Database Migrations

```bash
# Create new migration
python manage.py makemigrations

# Apply migrations
python manage.py migrate
```

### Static Files

```bash
# Collect static files
python manage.py collectstatic
```

## 🧪 Testing

```bash
# Run Django tests
python manage.py test

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

## 📊 Monitoring

- **Flower**: Monitor Celery tasks at http://localhost:5555
- **Django Admin**: Manage data at http://localhost/admin/
- **Logs**: View container logs with `docker-compose logs -f [service_name]`

## 🔒 Security

- Environment variables for sensitive data
- CSRF protection enabled
- Secure password hashing
- SQL injection protection via Django ORM
- XSS protection in templates

## 🚀 Deployment

### Production Deployment

1. **Update environment variables for production**
2. **Set up SSL certificates**
3. **Configure domain names**
4. **Set up monitoring and logging**
5. **Configure backup strategies**

### Docker Production Build

```bash
docker-compose -f docker-compose.prod.yml up --build -d
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **Your Name** - *Initial work* - [YourGitHub](https://github.com/yourusername)

## 🙏 Acknowledgments

- Django community for the excellent web framework
- aiogram library for Telegram bot development
- All contributors and users who provided feedback

## 📞 Support

For support and questions:
- Create an issue in the GitHub repository
- Contact via email: your.email@example.com
- Join our community discussions

---

**Made with ❤️ for students pursuing academic excellence through olympiads**