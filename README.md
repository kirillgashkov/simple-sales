# Simple Sales

A simple application for an imaginary sales department to manage their work.

## Structure

The application is split into three parts:

- `database`: A PostgreSQL database and everything needed to run it.
- `backend`: A FastAPI application that serves the API.
- `frontend`: A Vue.js application that serves the frontend.

This project is mostly about the backend and the database, so the frontend is
a bit rough around the edges.

## Try it out

You can run the database and the backend using Docker Compose:

```sh
$ docker compose up -d
```

The frontend can be run using npm:

```sh
$ cd frontend
$ npm install
$ npm run dev
```

Go to `http://localhost:8080` to see the application. Also, feel free to
explore the API at `http://localhost:8000/docs`.
