# Web Modular Platform for Business

A modular web platform for developing customizable business websites, currently in the early stages of development.

## Overview

The project is being designed as a reusable foundation for business websites, with a modular architecture that separates the main platform from the applications built from its website models.

The goal is to provide a structured base that can be adapted to different types of businesses while keeping the backend, frontend and deployment configuration organized and reusable.

## Technologies

### Backend

- Python
- FastAPI
- SQLModel
- PostgreSQL
- Alembic

### Frontend

- React
- Vite

### Development & Infrastructure

- Docker
- Linux
- Git
- uv
- Environment variables

## Current Architecture

The project is being structured around separate components for the platform and the customizable business websites.

```text
Web Modular Platform
│
├── Main Platform
│   └── API
│
└── Business Website Model
    ├── API
    └── Customizable Frontend
