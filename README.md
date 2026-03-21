# security-first
![DCDD7FA1-F0DB-4BC4-AC77-964D8014B095_1_201_a](https://github.com/user-attachments/assets/f44619e9-2529-4d54-8446-dba4130920c3)

A lightweight tool for evaluating the security posture of websites by inspecting HTTP response headers.

## Project Structure

- `security1st/` - Core package
  - `scanner/` - Security check modules
  - `report/` - Report generation
  - `utils/` - Shared utilities (scoring, assessment)
- `run.py` - Entry point (CLI and Web UI)

## Usage

```bash
# CLI mode
python run.py

# Web UI mode (Flask, port 5001)
python run.py --web
```

## Headers Checked

Checks 8 security headers across three categories:

**Critical:** Strict-Transport-Security, Content-Security-Policy, X-Frame-Options

**Recommended:** X-Content-Type-Options, Referrer-Policy

**Modern:** Permissions-Policy, Cross-Origin-Opener-Policy

**Legacy:** X-XSS-Protection

Results are scored with weighted assessment and ranked S through D.

## Output

- Terminal display with score summary and prioritized recommendations
- JSON report (`security_report.json`)

## Tech Stack

- Python 3.x
- `requests` for HTTP inspection
- Flask for Web UI

## Development

- Follow the Research, Strategy, Execution cycle.
- Add tests when introducing new scanner modules.
- Verify changes locally before deploying.
- Use this tool only against authorized targets.

## Future Improvements

- Local file scanning
- More advanced assessment methods
- Diagnostics beyond HTTP headers
