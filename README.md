# SRE Demo Web Application

This is a simple Flask-based web application designed for SRE (Site Reliability Engineering) monitoring demos. The application simulates a service that can degrade, experience errors, and track various metrics. It includes endpoints for health checks, metrics collection, and the ability to simulate crashes.

The app also includes a dashboard built with HTML, CSS, and JavaScript for visualizing the health status and metrics of the web application.

## Features
- **Health Check**: Monitors the health of the application and simulates degradation with a 5% chance of failure.
- **Metrics**: Collects metrics such as the total number of requests, errors, and uptime.
- **Crash Simulation**: Simulates an application crash to demonstrate failure scenarios.
- **Frontend Dashboard**: A simple web-based dashboard that displays health status, metrics, and a button to simulate a crash.

## Directory Structure
```

sre-demo/
├── README.md                # Project overview and instructions
├── docker-compose.yml       # Docker compose file for multi-container setup
├── Dockerfile.monitor       # Dockerfile for monitoring services
├── Dockerfile.webapp        # Dockerfile for the webapp service
├── requirements.txt         # Python dependencies
├── config/                  # Configuration files for monitoring and alerts
│   ├── monitor\_config.yml
│   └── alerts.yml
├── src/                     # Source code
│   ├── **init**.py
│   ├── monitor/             # Monitoring scripts
│   │   ├── **init**.py
│   │   ├── health\_checker.py
│   │   ├── metrics\_collector.py
│   │   └── alerting.py
│   ├── webapp/              # Web application code
│   │   ├── **init**.py
│   │   ├── app.py           # Flask application entry point
│   │   ├── templates/       # HTML files
│   │   │   └── index.html   # Dashboard HTML file
│   │   └── static/          # Static files (CSS, JS)
│   │       ├── css/
│   │       │   └── style.css
│   │       └── js/
│   │           └── script.js
│   └── automation/          # Automation scripts for deployment and remediation
│       ├── **init**.py
│       ├── remediation.py
│       └── deployment.py
├── scripts/                 # Shell scripts for setup and deployment
│   ├── deploy.sh
│   ├── setup.sh
│   └── cleanup.sh
├── tests/                   # Unit tests for the application
│   ├── **init**.py
│   ├── test\_monitor.py
│   └── test\_webapp.py
├── dashboards/              # Grafana dashboards
│   └── grafana-dashboard.json
└── logs/                    # Logs directory (keep it empty for git)
└── .gitkeep

````

## Setup and Installation

### 1. Prerequisites
- **Python 3.9+**
- **Docker** (for containerized setup)
- **Docker Compose** (optional, for multi-container setup)

### 2. Install Dependencies

To run the application locally, you need to install the necessary Python dependencies:

```bash
# Install the dependencies
pip install -r requirements.txt
````

### 3. Running the Application

#### Option 1: Run with Flask (Development Mode)

If you want to run the application locally in development mode:

```bash
# Run the Flask web application
python src/webapp/app.py
```

This will start the Flask application on `http://localhost:5000`. You can access the health dashboard at this URL.

#### Option 2: Run with Docker (Production Mode)

To run the application with Docker, use the `docker-compose.yml` file. It includes both the web app and monitoring services.

```bash
# Build and start the services with Docker Compose
docker-compose up --build
```

This will start the application and the monitoring services, with the web app accessible at `http://localhost:5000`.

### 4. Endpoints

* **GET `/`**: Home page with a simple dashboard displaying application status and uptime.
* **GET `/health`**: Health check endpoint, which returns the current health status of the application (either "healthy" or "unhealthy").
* **GET `/metrics`**: Metrics endpoint, which returns application metrics in JSON format (requests, errors, and uptime).
* **GET `/crash`**: Simulates an application crash (this is for testing failure scenarios).

### 5. Dashboard

The frontend dashboard is available at the root URL (`/`). It displays the following:

* **Health Status**: A visual representation of whether the application is "healthy" or "unhealthy".
* **Metrics**: Displays metrics like the number of requests, errors, and the application's uptime.
* **Crash Simulation**: A button to simulate a crash of the application.

The frontend uses AJAX calls to update the health status and metrics dynamically without needing to reload the page.

## Monitoring and Alerts

The `monitor` directory includes scripts for checking the health of the application, collecting metrics, and sending alerts. Alerts are defined in the `config/alerts.yml` file and can be configured to notify stakeholders about application issues.

### Example Alert Configuration (`alerts.yml`)

```yaml
alerts:
  - name: "High Error Rate"
    condition: "error_count > 50"
    action: "email"
    recipient: "admin@example.com"
  - name: "Health Degraded"
    condition: "status == 'unhealthy'"
    action: "slack"
    webhook_url: "https://slack.com/api/webhook"
```

## Tests

Unit tests are located in the `tests` directory. You can run the tests using:

```bash
# Run the tests
pytest
```

This will execute all the tests and give you feedback on whether the application is functioning as expected.

## Docker Compose Setup

If you want to run the application using Docker Compose, the `docker-compose.yml` file is already configured to handle multi-container setups, such as one for the web application and one for monitoring.

To start the services with Docker Compose:

```bash
docker-compose up --build
```

This will build the images and start both the web application and monitoring services.

### Example `docker-compose.yml`

```yaml
version: '3'
services:
  webapp:
    build:
      context: .
      dockerfile: Dockerfile.webapp
    ports:
      - "5000:5000"
    depends_on:
      - monitor
  monitor:
    build:
      context: .
      dockerfile: Dockerfile.monitor
    volumes:
      - ./config:/config
    environment:
      - MONITOR_CONFIG=/config/monitor_config.yml
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

If you would like to contribute to this project, feel free to fork the repository, make changes, and submit a pull request. Contributions are always welcome!

---

Thank you for using the SRE Demo Web Application! 🎉

```
