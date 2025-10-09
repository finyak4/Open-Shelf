# Open-Shelf

Open-Shelf is a modern web-based library management system built with Django. It allows staff to manage books, authors, genres, reservations, and borrowings. The system supports user authentication and provides an intuitive interface for searching and managing library resources.

## Live Demo

Try it out at [Open-Shelf](https://open-shelf.onrender.com/)

**⚠️ Important Notes:**
- **Using Render's free tier** - the app may take **20-50 seconds** to wake up if inactive
- **Please be patient** on first load - Render spins down inactive apps to conserve resources

## 🔐 Demo Accounts

### 👤 Regular User Account
- **Email:** `user@example.com`
- **Password:** `userpass`
- **Features:** Browse books, filter, view details

### 👑 Admin Account  
- **Email:** `admin@example.com`
- **Password:** `adminpass`
- **Features:** Full admin access, add/edit books

## Features

- **User Authentication**
  - Register, login, and logout for users.
  - Secure password handling and validation.

- **Library Management**
  - Add, edit, and view books, authors, and genres.
  - Paginated listings for easy navigation.

- **Responsive UI**
  - Clean, responsive design with HTML5 and CSS Grid.
  - Interactive elements handled with modern JavaScript.

- **Admin & Staff Support**
  - Staff-only sections for management.
  - Detailed book and user information displayed.

- **Database Seeding**
  - Example data for books, authors, and genres for demo/testing.

- **Deployment Ready**
  - Dockerized for easy setup and hosting.
  - Entrypoint script handles migrations and static file collection.

## Development Stack

- **Backend:** [Django 5.2.4](https://www.djangoproject.com/)
- **Frontend:** HTML5, CSS3 (Grid, responsive), JavaScript (vanilla)
- **Database:** PostgreSQL (via Django ORM)
- **Authentication:** Django’s built-in user system (custom User model)
- **Containerization:** Docker, Docker Compose
- **Server:** Gunicorn (WSGI), Nginx
- **Other:** Python 3.11, decouple for environment variables

## Getting Started

1. **Clone the repository**
   ```bash
   git clone https://github.com/finyak4/Open-Shelf.git
   cd Open-Shelf
   ```

2. **Set up environment variables**
   - Create a `.env` file and specify:
     ```
     SECRET_KEY=your_secret_key
     DEBUG=True
     POSTGRES_DB=your_db
     POSTGRES_USER=your_user
     POSTGRES_PASSWORD=your_password
     POSTGRES_HOST=db
     POSTGRES_PORT=5432
     ALLOWED_HOSTS=localhost,127.0.0.1
     ```

3. **Build and Run with Docker**
   ```bash
   docker-compose up --build
   ```

4. **Access the app**
   - Visit [http://localhost:8000](http://localhost:8000)

## License

MIT License

## Author

Made by [finyak4](https://github.com/finyak4)
