# Connectly API
## Overview

Connectly is a social media platform designed to allow users to connect, share content, and interact. This repository contains the backend API for the Connectly application, built using Python, Django, and the Django REST Framework (DRF). The API provides endpoints for user management, post creation and management, comment functionality, and more.

This README provides information on setting up the project, running the API, testing, and contributing.

## Features

*   **User Management:**
    *   User registration (with unique username and email validation).
    *   User login/logout (using JWT authentication).
    *   User profile retrieval (limited to admins for now).
    *   User update (limited to admins for now).
    *   User deletion (limited to admins for now).
    *   Secure password hashing (using Argon2).
*   **Post Management:**
    *   Create posts (text-based, with potential for future expansion to other types).
    *   Retrieve posts.
    *   Update posts (restricted to the post author).
    *   Delete posts (restricted to the post author).
*   **Comment Management:**
    *   Create comments on posts.
    *   Retrieve comments.
    *   Update comments (restricted to the comment author).
    *   Delete comments (restricted to the comment author).
*   **Security:**
    *   HTTPS for secure communication (using self-signed certificates in development).
    *   JWT (JSON Web Token) authentication for API access.
    *   Role-Based Access Control (RBAC) using Django's built-in groups and custom permissions.
    *   Protection against common web vulnerabilities (CSRF, etc.).
    *   HSTS enabled.
*   **Design Patterns:**
    *   Singleton pattern for configuration management (`ConfigManager`).
    *   Singleton pattern for logging (`LoggerSingleton`).
    *   Factory pattern for post creation (`PostFactory`).

## Technologies Used

*   Python 3.13 (adjust to your specific Python version)
*   Django 5.1.6 (adjust to your specific version)
*   Django REST Framework (DRF) 3.15.1
*   djangorestframework-simplejwt 5.3.1
*   django-extensions 3.2.3
*   argon2-cffi 23.1.0
*   SQLite (for development; easily switched to PostgreSQL, MySQL, etc.)
*   Postman (for API testing)
*   Git/GitHub (for version control)
*   OpenSSL (for generating self-signed certificates - development only)
*   Pipenv (or virtualenv) for managing dependencies.
