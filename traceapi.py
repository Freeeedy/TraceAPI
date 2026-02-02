import argparse
import httpx
import html
import re
from urllib.parse import urljoin

parser = argparse.ArgumentParser()

group = parser.add_mutually_exclusive_group(required=True) # ensure at least one in the group is True
group.add_argument("-t", help="Provide a target URL.")
group.add_argument("-tL", help="Provide target list from a file.")

parser.add_argument("-o", required=False, default="output.txt", help="Provide output file.")

args = parser.parse_args()

targets = []

if args.t:
    targets.append(args.t)

if args.tL:
    with open(args.tL, "r", encoding="utf-8") as f:
        # strip newline and whitespace from each line
        targets.extend(line.strip() for line in f if line.strip())

output_file = args.o

client = httpx.Client(follow_redirects=True) # create HTTP client

API_REGEX = re.compile(
    r'('
    r'/wp-json/[^\s"\'<>`,{}]+'
    r'|/wp-admin/admin-ajax\.php'
    r'|/xmlrpc\.php'
    r'|\?rest_route=[^\s"\'<>`,{}]+'
    r'|/api/[^\s"\'<>`,{}]+'
    r'|/rest/[^\s"\'<>`,{}]+'
    r'|/graphql[^\s"\'<>`,{}]*'
    r'|/ajax/[^\s"\'<>`,{}]+'
    r'|/auth/[^\s"\'<>`,{}]+'
    r'|/oauth[^\s"\'<>`,{}]+'
    r'|/token[^\s"\'<>`,{}]+'
    r'|/internal/[^\s"\'<>`,{}]+'
    r'|/backend/[^\s"\'<>`,{}]+'
    r')',
    re.IGNORECASE
)

def extract_apis(text): # extract API endpoints from text
    return set(API_REGEX.findall(text))

for target in targets:
    print(f"Processing: {target}")
    html_content = client.get(target).text # fetch HTML source code
    html_content = html.unescape(html_content) # decode HTML into text

    found_apis = extract_apis(html_content) # extract from HTML source code

    js_links = re.findall(r'src=["\']([^"\']+\.js)["\']', html_content) # find JS file links in HTML source code

    for link in js_links: # fetch and analyze each JS file
        js_url = urljoin(target, link) # construct full URL
        js_content = client.get(js_url).text # fetch JS file content
        found_apis.update(extract_apis(js_content)) # extract APIs from JS content

    with open(output_file, "a", encoding="utf-8") as f: # append found apis into a txt file
        f.write(f"Target URL: {target}\nFound APIs:\n")
        for api in found_apis:
            f.write(f" - {api}\n")
        f.write("\n")

    print(f"Found {len(found_apis)} APIs for {target}\n")