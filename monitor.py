import requests
from requests.exceptions import RequestException, HTTPError, Timeout, ConnectionError
import time
import logging
import schedule

# Configure logging
logging.basicConfig(
    filename='domain_monitor.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

domains = [
    "domainsgohere.com",
    "domainsgohere.com",
]

def check_domain(domain, timeout=10):
    """
    Checks if a domain is up by attempting HTTPS first, then HTTP if HTTPS fails.

    Args:
        domain (str): The domain to check.
        timeout (int): The maximum time to wait for a response, in seconds.

    Returns:
        tuple: (is_up (bool), response_time (float or None), status_code (int or None))
    """
    # List of URL schemes to try
    url_schemes = ["https://", "http://"]
    
    for scheme in url_schemes:
        url = f"{scheme}{domain}"
        try:
            start_time = time.time()
            response = requests.get(url, timeout=timeout, headers={'User-Agent': 'Mozilla/5.0'})
            response_time = time.time() - start_time
            if response.status_code == 200:
                return True, response_time, response.status_code
            else:
                # Consider other 2xx status codes as "Up"
                if 200 <= response.status_code < 300:
                    return True, response_time, response.status_code
                else:
                    return False, response_time, response.status_code
        except Timeout:
            logging.error(f"{domain} is DOWN. Reason: Timeout after {timeout} seconds when accessing {url}")
            return False, None, None
        except ConnectionError:
            logging.warning(f"{domain} is DOWN. Reason: Connection error when accessing {url}")
            continue  # Try the next scheme (e.g., HTTP if HTTPS failed)
        except HTTPError as http_err:
            logging.error(f"{domain} HTTP error occurred: {http_err}")
            return False, None, None
        except RequestException as err:
            logging.error(f"{domain} Request exception occurred: {err}")
            return False, None, None
    
    # If all schemes fail
    logging.error(f"{domain} is DOWN. Reason: All connection attempts failed.")
    return False, None, None

def monitor_domains(domain_list):
    """
    Monitors a list of domains and logs their status.

    Args:
        domain_list (list): A list of domain names to monitor.
    """
    logging.info("Starting domain monitoring cycle.")
    for domain in domain_list:
        is_up, response_time, status_code = check_domain(domain)
        if is_up:
            logging.info(f"{domain} is UP. Response Time: {response_time:.2f}s, Status Code: {status_code}")
        else:
            logging.warning(f"{domain} is DOWN. Response Time: N/A, Status Code: N/A")
    logging.info("Domain monitoring cycle completed.\n")

if __name__ == "__main__":
    # Initial run
    monitor_domains(domains)
    
    # Schedule to run every 5 minutes
    schedule.every(5).minutes.do(monitor_domains, domain_list=domains)
    
    print("Domain monitoring started. Logs are being written to 'domain_monitor.log'. Press Ctrl+C to exit.")
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nDomain monitoring stopped.")
