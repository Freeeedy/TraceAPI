import argparse
import httpx
import html
import re
from urllib.parse import urljoin

parser = argparse.ArgumentParser()
parser.add_argument("-t", required=True, help="Provide a target URL.")
args = parser.parse_args()

target_url = args.t
print(f"Target URL is: {target_url}")

client = httpx.Client(follow_redirects=True) # create HTTP client

html_content = client.get(target_url).text # fetch HTML source code
html_content = html.unescape(html_content) # decode HTML into text

API_REGEX = re.compile( # pattern to match common API endpoints
        r'('
        r'/wp-json/[^\s"\'<>]+'
        r'|/wp-admin/admin-ajax\.php'
        r'|/xmlrpc\.php'
        r'|\?rest_route=[^\s"\'<>]+'
        r'|/api/[^\s"\'<>]+'
        r'|/rest/[^\s"\'<>]+'
        r'|/graphql[^\s"\'<>]*'
        r'|/ajax/[^\s"\'<>]+'
        r'|/auth/[^\s"\'<>]+'
        r'|/oauth[^\s"\'<>]+'
        r'|/token[^\s"\'<>]+'
        r'|/internal/[^\s"\'<>]+'
        r'|/backend/[^\s"\'<>]+'
        r')',
        re.IGNORECASE
)

def extract_apis(text): # extract API endpoints from text
    return set(API_REGEX.findall(text))

found_apis = extract_apis(html_content) # extract from HTML source code

js_links = re.findall(r'src=["\']([^"\']+\.js)["\']', html_content) # find JS file links in HTML source code

for link in js_links: # fetch and analyze each JS file
    js_url = urljoin(target_url, link) # construct full URL
    js_content = client.get(js_url).text # fetch JS file content
    found_apis.update(extract_apis(js_content)) # extract APIs from JS content

print(found_apis)
