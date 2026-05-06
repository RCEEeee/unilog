# University Database Flask App

A Flask web application for managing university data including users, students, lecturers, courses, faculties, and departments.

## Local Development

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up MySQL database:
   - Create database: `university_db`
   - Import schema: `mysql -u root -p university_db < schema.sql`

3. Set environment variables:
   ```bash
   export DB_HOST=localhost
   export DB_USER=root
   export DB_PASSWORD=your_password
   export DB_NAME=university_db
   export SECRET_KEY=your_secret_key
   ```

4. Run the app:
   ```bash
   python app.py
   ```

## Deployment to Railway (Alternative to Heroku)

Railway is a modern cloud platform that's great for Flask apps with databases.

### Automated Deployment

1. **Run the automated script**:
   ```powershell
   .\deploy-railway.ps1
   ```

   This script will:
   - Install Railway CLI if needed
   - Login to Railway
   - Create project and MySQL database
   - Set environment variables
   - Deploy your app

### Manual Deployment Steps

1. **Install Railway CLI**:
   ```bash
   npm install -g @railway/cli
   ```

2. **Login to Railway**:
   ```bash
   railway login
   ```

3. **Create project**:
   ```bash
   railway init university-portal
   ```

4. **Add MySQL database**:
   ```bash
   railway add mysql
   ```

5. **Set environment variables**:
   ```bash
   railway variables set SECRET_KEY="your-random-secret-key"
   ```

6. **Deploy**:
   ```bash
   railway up
   ```

7. **Get your app URL**:
   ```bash
   railway domain
   ```

### Railway vs Heroku

- **Railway**: Modern, fast deployments, great developer experience
- **Heroku**: Mature, extensive add-ons, slightly more complex setup

Both work well for this Flask + MySQL app!

## Features

- User authentication
- Dashboard with statistics
- CRUD operations for all entities
- Responsive design

## Technologies

- Flask
- MySQL
- Werkzeug (for password hashing)
- HTML/CSS/JavaScript