# Task Manager MVP

A modern full-stack task management application built with React TypeScript frontend and Node.js backend.

## Features

- 🔐 User authentication (register/login)
- ✅ Create, read, update, delete tasks
- 🎨 Modern, responsive UI with Tailwind CSS
- 🚀 RESTful API with Express.js
- 💾 SQLite database with Prisma ORM
- 🔒 JWT-based authentication
- 📱 Mobile-friendly design

## Tech Stack

### Frontend
- React 18 with TypeScript
- Vite for fast development
- Tailwind CSS for styling
- Axios for API calls
- React Router for navigation

### Backend
- Node.js with Express.js
- Prisma ORM with SQLite
- JWT for authentication
- bcrypt for password hashing
- CORS for cross-origin requests

## Quick Start

1. **Install dependencies:**
   ```bash
   npm run install:all
   ```

2. **Set up the database:**
   ```bash
   cd server
   npx prisma migrate dev
   cd ..
   ```

3. **Start the development servers:**
   ```bash
   npm run dev
   ```

4. **Open your browser:**
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:3001

## Project Structure

```
├── client/          # React TypeScript frontend
├── server/          # Node.js Express backend
├── package.json     # Root package.json with scripts
└── README.md        # This file
```

## API Endpoints

- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `GET /api/tasks` - Get user's tasks
- `POST /api/tasks` - Create new task
- `PUT /api/tasks/:id` - Update task
- `DELETE /api/tasks/:id` - Delete task

## Environment Variables

Create a `.env` file in the `server` directory:

```
DATABASE_URL="file:./dev.db"
JWT_SECRET="your-super-secret-jwt-key-here"
PORT=3001
```

## Development

- Run frontend only: `npm run client:dev`
- Run backend only: `npm run server:dev`
- Run both: `npm run dev`

## Building for Production

```bash
npm run build
npm start
```

This MVP demonstrates modern full-stack development practices and can be extended with additional features as needed.