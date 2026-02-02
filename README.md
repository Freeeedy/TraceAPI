# TraceAPI

TraceAPI is a lightweight Python tool designed to **discover exposed API endpoints** by scanning website HTML and linked JavaScript files.  
It’s useful for **API reconnaissance**, **security research**, and **pentesting** workflows.

This is **v1** of the project — the foundation is intentionally simple, and the tool is planned to grow significantly over time.

---

##  Features

- Scan **a single target URL** or **multiple targets from a file**
- Extract API endpoints from:
  - HTML source code
  - JavaScript files referenced by the page
- Detects common API patterns such as:
  - `/api/`
  - `/rest/`
  - `/wp-json/`
  - `/graphql`
  - `/auth/`
  - `/oauth`
  - `/token`
  - `/ajax`
- Automatically follows redirects
- Appends results to an output file (default: `output.txt`)

---

##  Installation

Clone the repository and run the install script:

```bash
git clone https://github.com/yourusername/TraceAPI.git
cd TraceAPI
chmod +x install.sh
./install.sh
```

Scan a single URL
```
python traceapi.py -t https://example.com
```

Scan multiple targets from a file
```
python traceapi.py -tL targets.txt
```

Specify a custom output file
```
python traceapi.py -t https://example.com -o results.txt
```

Example Output
```
Processing: https://example.com
Found 4 APIs for https://example.com

Target URL: https://example.com
Found APIs:
 - /api/v1/users
 - /graphql
 - /auth/login
 - /wp-json/wp/v2/posts
 ```

## How It Works

1) Fetches the HTML source of the target page
2) Extracts API-like paths using regex
3) Finds all linked .js files
4) Downloads and scans each JavaScript file
5) Deduplicates and saves all discovered endpoints