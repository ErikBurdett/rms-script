# Domain Monitor

## Overview

Domain Monitor is a simple Python script designed to check the availability of multiple websites/domains. By periodically sending HTTP requests to each domain, the script determines whether the site is up and running, logging the results for review. This tool is ideal for administrators, developers, or anyone interested in monitoring the uptime of various websites.

## Features

- **Bulk Domain Monitoring:** Check the status of multiple domains in a single run.
- **HTTP and HTTPS Support:** Attempts to connect using both `https://` and `http://` schemes.
- **Detailed Logging:** Logs the status, response time, and HTTP status codes of each domain.
- **Error Handling:** Differentiates between various types of connection issues (e.g., timeouts, connection errors).
- **Scheduled Checks:** Automatically performs monitoring cycles at regular intervals (every 5 minutes by default).

## Prerequisites

Before setting up the Domain Monitor, ensure you have the following:

- **Python 3.6 or higher** installed on your system. You can download it from the [official website](https://www.python.org/downloads/).
- **pip** (Python package installer) is available. It typically comes bundled with Python installations.
- **Internet Connection:** To allow the script to send HTTP requests to the target domains.

## Installation

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/yourusername/domain-monitor.git
    cd domain-monitor
    ```

2. **(Optional) Create a Virtual Environment:**

    It's good practice to use a virtual environment to manage project dependencies.

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install Required Libraries:**

    The script relies on the `requests` and `schedule` libraries. Install them using `pip`:

    ```bash
    pip install -r requirements.txt
    ```

    *If a `requirements.txt` file isn't present, install the libraries manually:*

    ```bash
    pip install requests schedule
    ```

## Configuration

1. **Define Domains to Monitor:**

    Open the script (`monitor_domains.py`) in your preferred text editor and locate the `domains` list. Add or remove domain names as needed.

    ```python
    domains = [
        "example.com",
        "anotherdomain.com",
        # Add more domains here
    ]
    ```

2. **Adjust Timeout Settings (Optional):**

    The `timeout` parameter in the `check_domain` function determines how long the script waits for a response before marking a domain as "Down." You can modify it based on your network conditions.

    ```python
    def check_domain(domain, timeout=10):
        # ...
    ```

## Usage

1. **Run the Script:**

    Ensure you're in the project directory and your virtual environment is activated (if using one). Execute the script using Python:

    ```bash
    python monitor_domains.py
    ```

2. **Script Behavior:**

    - **Initial Run:** The script performs an immediate check of all listed domains.
    - **Scheduled Checks:** Every 5 minutes, the script automatically rechecks the status of all domains.
    - **Logging:** Results are appended to `domain_monitor.log` with timestamps.

3. **Stopping the Script:**

    To terminate the monitoring process, press `Ctrl+C` in the terminal where the script is running.

    ```plaintext
    ^C
    Domain monitoring stopped.
    ```

## Logging

- **Log File:** All monitoring results are logged to `domain_monitor.log` in the project directory.
- **Log Entries Include:**
  - **Timestamp:** When the check was performed.
  - **Log Level:** INFO for "Up" statuses, WARNING for "Down" statuses, and ERROR for exceptions.
  - **Message:** Details about the domain status, response time, and HTTP status codes.

### Sample Log Entries

```plaintext
2024-04-01 17:05:00,123 - INFO - Starting domain monitoring cycle.
2024-04-01 17:05:02,456 - INFO - example.com is UP. Response Time: 0.25s, Status Code: 200
2024-04-01 17:05:03,789 - WARNING - anotherdomain.com is DOWN. Reason: Connection error when accessing https://anotherdomain.com
2024-04-01 17:05:04,012 - INFO - Domain monitoring cycle completed.
```
## Troubleshooting

If the script reports all domains as "Down" despite knowing they are up, consider the following steps:

### Check URL Schemes:

- Ensure that the script correctly appends `https://` and/or `http://` to each domain.
- Domains without the proper scheme can lead to failed requests.

### Verify Internet Connection:

- Confirm that your system has an active internet connection.

### Firewall and Network Settings:

- Ensure that your firewall or network settings aren't blocking outbound HTTP/HTTPS requests.

### Inspect Log File:

- Review `domain_monitor.log` for detailed error messages that can help identify the issue.

### User-Agent Header:

- Some servers block requests with missing or default User-Agent headers. The script includes a User-Agent header to mimic a browser request.

### SSL Certificate Issues:

- If a domain has SSL certificate problems, the HTTPS request might fail. Consider allowing the script to fallback to HTTP if HTTPS fails.

### Adjust Timeout:

- Increase the timeout value if network latency is causing premature timeouts.

### Run Manual Checks:

- Test individual domains manually using a browser or tools like `curl` to ensure they are reachable.

## Contributing

Contributions are welcome! If you'd like to enhance the Domain Monitor script, follow these steps:

### Fork the Repository:

- Click the "Fork" button at the top-right corner of the repository page.

### Create a Feature Branch:

```bash
git checkout -b feature/YourFeatureName
```

### Commit Your Changes: 

```bash 
git commit -m "Add your commit message here" 
```

### Push to the Branch: 

```bash
git push origin feature/YourFeatureName
```
### Open a Pull Request and Contact Erik 

- Navigate to the repository on GitHub and click "Compare & pull request" to submit your changes.

### Author: 

Erik Burdett 
Email: erikaburdet@gmail.com / erik.burdett@andrewsama.com