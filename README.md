# Authentication Service

## Overview

The Authentication Service is a FastAPI-based microservice designed to manage authentication functionalities for your application. This service includes three primary modules:

- **Authentication Module:** Handles user login and authentication.
- **Token Module:** Manages the issuance, validation, and revocation of tokens.
- **Session Module:** Handles session management, including token storage and invalidation.

## Features

- **Authentication Module:**

  - User login and authentication
  - Integration with OAuth 2.0 / OpenID Connect for Single Sign-On (SSO)

- **Token Module:**

  - Issuance of JWT tokens upon successful authentication
  - Token validation for incoming requests
  - Token revocation and blacklisting

- **Session Module:**
  - Management of active sessions
  - Session expiration and invalidation
  - Integration with Redis for session storage

## Getting Started

### Prerequisites

- **Python 3.8+**
- **Docker** (for containerization, optional)
- **Redis** (for session management)

### Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/your-username/authentication-service.git
   cd authentication-service
   ```

2. **Install Dependencies:**

   Create a virtual environment (optional but recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

   Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

### Configuration

1. **Environment Variables:**

   Create a `.env` file in the root directory and add the following configuration:

   ```env
   SECRET_KEY=your_secret_key
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   REDIS_URL=redis://localhost:6379/0
   ```

   Adjust the values as necessary for your environment.

2. **Database Configuration:**

   Ensure that Redis is running and accessible at the specified `REDIS_URL`. You can start Redis using Docker if needed:

   ```bash
   docker run -d -p 6379:6379 --name redis redis
   ```

### Running the Service

1. **Start the FastAPI Application:**

   ```bash
   uvicorn app.main:app --reload
   ```

   The application will be available at `http://127.0.0.1:8000`.

### API Endpoints

- **Authentication Module:**

  - `POST /login`: Authenticate users and issue JWT tokens.
  - `GET /oauth/callback`: Handle OAuth 2.0 / OpenID Connect callback.

- **Token Module:**

  - `POST /token/refresh`: Refresh JWT tokens.
  - `POST /token/revoke`: Revoke JWT tokens.

- **Session Module:**
  - `GET /session/status`: Check session status.
  - `POST /session/invalidate`: Invalidate sessions.

### Testing

Run the tests using `pytest`:

```bash
pytest
```

### Docker Setup

1. **Build the Docker Image:**

   ```bash
   docker build -t auth-service .
   ```

2. **Run the Docker Container:**

   ```bash
   docker run -d -p 8000:8000 --name auth-service auth-service
   ```

### Contributing

Contributions are welcome! Please follow the standard Git workflow and submit a pull request with your changes.

### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Feel free to adjust any sections based on the specific details of your implementation or additional requirements.
