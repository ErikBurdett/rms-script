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
    "901businessmail.com",
    "allenstristate.com",
    "allstatestruck.com",
    "amarillocustomhomes.com",
    "amarillodogboarding.com",
    "amarilloea.com",
    "amarillofp.com",
    "amarillopanhellenic.org",
    "amarillorealtors.org",
    "amarilloseniorcitizens.com",
    "amarillosparkviewrealty.com",
    "amarillothunder.com",
    "andrewsama.com",
    "apsama.com",
    "austinbikefarm.com",
    "badgerofwesttexas.com",
    "barfieldlawfirm.net",
    "bf-law.com",
    "bivinsfoundation.org",
    "bluemondayrealestate.com",
    "brownconsultingengineers.com",
    "budgriffin.com",
    "canyonrimconsulting.com",
    "cctxp.org",
    "charleysautos.com",
    "childrenslc.org",
    "christianchurchofgod.org",
    "cib-inc.com",
    "circlelirrigationtx.com",
    "collingsworthcountymuseum.org",
    "connerindustriestx.com",
    "crossroadscountrychurch.org",
    "deafsmithcountymuseum.org",
    "diamondwcorrals.com",
    "djamarillo.com",
    "dlockeinc.net",
    "dougricketts.com",
    "dovecreekequinerescue.org",
    "dukeelec.com",
    "dyersbbq.com",
    "ericspellmann.com",
    "evensontrucking.com",
    "familyphotoamarillo.com",
    "fimcrealty.com",
    "gatewaysupplytx.com",
    "golfdynamics.com",
    "graysonsbdc.org",
    "gurssconstruction.com",
    "heartofthedesert.com",
    "highlandparkvillageamarillo.com",
    "hogbait.com",
    "hpa4u.com",
    "hubcityav.com",
    "iaedonline.com",
    "insurancestoptexas.com",
    "integrityoverheaddoor.com",
    "jaredblankenship.com",
    "kalscoops.com",
    "kimrad.com",
    "kmocfm.com",
    "kyliehinermemorialplayground.com",
    "ladybuginc.net",
    "lawfirmrlt.com",
    "lonestarconstruction.com",
    "lonestarcreativeproductions.com",
    "lonestarrunnersclub.net",
    "lovell-law.net",
    "mandrliquoronline.com",
    "mathistrans.com",
    "midriverscc.org",
    "midwestmachinellc.com",
    "mollydavismarketing.com",
    "navarrocollegesbdc.org",
    "ncsbdc.org",
    "neatcoaching.com",
    "officecenterinc.com",
    "onechairatatime.org",
    "opportunityplan.com",
    "originalfactoryscent.com",
    "pancakestation.com",
    "panhandleherald.com",
    "panhandleoilmens.org",
    "parissbdc.com",
    "parissbdc.org",
    "patdavisproperties.com",
    "pattersonlawgroup.com",
    "peeplescleaning.com",
    "pizzaplanet.com",
    "plainstransportation.com",
    "premier-alarm.com",
    "randrscales.com",
    "rdad-inc.com",
    "scarabmfg.com",
    "scrappc.com",
    "sgmtexaslaw.com",
    "sister-bear.com",
    "southwestambucs.org",
    "speedsilks.com",
    "srlawtx.com",
    "starlightcanyon.com",
    "susanbarros.com",
    "terrywestercounseling.com",
    "texasbpwfoundation.org",
    "texaspanhandlecenters.org",
    "texaspanhandlecharities.org",
    "themarkandrewsagency.com",
    "theplazarestaurant.com",
    "thesolawfirm.com",
    "todaysmemoriesamarillo.com",
    "traleecrisiscenter.org",
    "tuckerhvac.com",
    "twentyfive20.com",
    "ucidev.com",
    "ucidigital.com",
    "ucidocuments.com",
    "ucishredding.com",
    "ucisupport.com",
    "uciwebware.com",
    "watleyseed.com",
    "wellingtonritztheatre.com",
    "westtexasfresh.com",
    "westtexasrx.com",
    "whaonline.net",
    "williamsboyce.com"
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
