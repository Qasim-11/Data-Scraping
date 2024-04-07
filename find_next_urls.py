import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def find_direct_child_paths(base_url):
    """
    Finds direct child paths of the given URL.
    
    Parameters:
    - base_url (str): The base URL.
    
    Returns:
    - List[str]: A list of URLs that are direct child paths of the base URL.
    """
    try:
        # Make sure the base_url ends with a slash
        if not base_url.endswith('/'):
            base_url += '/'
        
        # Fetch the webpage
        response = requests.get(base_url)
        response.raise_for_status()  # Raises an error for bad responses
        
        # Parse the HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Initialize an empty list to store the direct child paths
        child_paths = []
        
        # Go through all links found on the page
        for link in soup.find_all('a', href=True):
            href = link['href']
            
            # Resolve relative URLs to absolute URLs
            full_url = urljoin(base_url, href)
            
            # Parse the URL to components
            parsed_url = urlparse(full_url)
            
            # Check if the link is a direct child of the base URL
            if parsed_url.netloc == urlparse(base_url).netloc and parsed_url.path.startswith(urlparse(base_url).path):
                path_segments = parsed_url.path.strip('/').split('/')
                base_path_segments = urlparse(base_url).path.strip('/').split('/')
                if len(path_segments) == len(base_path_segments) + 1:  # Direct child paths only
                    # Reconstruct the direct child path URL and add to the list
                    direct_child_url = urljoin(base_url, path_segments[-1] + '/')
                    if direct_child_url not in child_paths:  # Avoid duplicates
                        child_paths.append(str(direct_child_url))
        
        return child_paths
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return []