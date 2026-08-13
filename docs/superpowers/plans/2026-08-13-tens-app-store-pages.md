# TENS App Store Pages Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish verified privacy-policy and support pages for TENS at stable GitHub Pages URLs, then enter those URLs in App Store Connect.

**Architecture:** Add two standalone semantic HTML documents under `/tens/` and one shared local stylesheet. A dependency-free Python verifier enforces required copy, local-only resources, valid internal links, and the absence of tracking code before deployment.

**Tech Stack:** HTML5, CSS, Python 3 standard library, GitHub Pages, Git, App Store Connect

## Global Constraints

- Public privacy URL: `https://tonyxiahua.github.io/tens/privacy/`.
- Public support URL: `https://tonyxiahua.github.io/tens/support/`.
- Public developer name: `Xia Hua`.
- Public support email: `xhua006@gmail.com`.
- Effective date: `August 13, 2026`.
- Footer: `© 2026 Xia Hua. All rights reserved.`
- Do not use cookies, analytics, trackers, third-party scripts, embedded forms, or remote fonts.
- Do not modify the existing blog or the pre-existing untracked files `.nojekyll 2`, `about/index 2.html`, `index 2.html`, and `search 2.xml`.
- Enter URLs in App Store Connect only after both public HTTPS URLs pass verification.

## File Structure

- Create `tens/assets/styles.css`: shared responsive presentation and accessibility states.
- Create `tens/privacy/index.html`: public English privacy policy.
- Create `tens/support/index.html`: public English setup, troubleshooting, and contact page.
- Create `tests/verify_tens_pages.py`: dependency-free structural, content, and link verification.

---

### Task 1: Add Automated Contract Tests for the Public Pages

**Files:**
- Create: `tests/verify_tens_pages.py`
- Test: `tests/verify_tens_pages.py`

**Interfaces:**
- Consumes: repository root and the fixed paths `tens/privacy/index.html`, `tens/support/index.html`, and `tens/assets/styles.css`.
- Produces: a command-line verifier that exits `0` only when both pages satisfy the approved public-content contract.

- [ ] **Step 1: Write the failing verifier**

Create `tests/verify_tens_pages.py` with this implementation:

```python
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
PRIVACY = ROOT / "tens/privacy/index.html"
SUPPORT = ROOT / "tens/support/index.html"
STYLES = ROOT / "tens/assets/styles.css"


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.resources = []
        self.text = []

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag == "a" and "href" in values:
            self.links.append(values["href"])
        if tag in {"link", "script", "img", "iframe"}:
            resource = values.get("href") or values.get("src")
            if resource:
                self.resources.append(resource)

    def handle_data(self, data):
        self.text.append(data)


def parse(path):
    parser = PageParser()
    parser.feed(path.read_text(encoding="utf-8"))
    return parser, " ".join(parser.text)


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def verify_page(path, required_text):
    require(path.is_file(), f"Missing page: {path.relative_to(ROOT)}")
    parser, text = parse(path)
    for phrase in required_text:
        require(phrase in text, f"{path.name}: missing {phrase!r}")
    for resource in parser.resources:
        parsed = urlparse(resource)
        require(not parsed.scheme and not parsed.netloc, f"External resource: {resource}")
    source = path.read_text(encoding="utf-8").lower()
    for forbidden in ("google-analytics", "googletagmanager", "facebook.net", "<iframe", "<form"):
        require(forbidden not in source, f"Forbidden integration: {forbidden}")
    return parser


privacy_parser = verify_page(
    PRIVACY,
    [
        "Privacy Policy",
        "August 13, 2026",
        "do not collect, transmit, sell, or share your personal data",
        "Camera",
        "Microphone",
        "Photos",
        "HealthKit",
        "Apple Watch",
        "xhua006@gmail.com",
        "© 2026 Xia Hua. All rights reserved.",
    ],
)
support_parser = verify_page(
    SUPPORT,
    [
        "TENS Support",
        "Position your iPhone",
        "full tennis court",
        "Apple Watch",
        "Troubleshooting",
        "xhua006@gmail.com",
        "© 2026 Xia Hua. All rights reserved.",
    ],
)

require(STYLES.is_file(), "Missing tens/assets/styles.css")
require("/tens/assets/styles.css" in privacy_parser.resources, "Privacy CSS link is incorrect")
require("/tens/assets/styles.css" in support_parser.resources, "Support CSS link is incorrect")
require("/tens/support/" in privacy_parser.links, "Privacy page must link to Support")
require("/tens/privacy/" in support_parser.links, "Support page must link to Privacy")
require("mailto:xhua006@gmail.com" in privacy_parser.links, "Privacy email link is incorrect")
require("mailto:xhua006@gmail.com" in support_parser.links, "Support email link is incorrect")

print("TENS privacy and support pages passed verification.")
```

- [ ] **Step 2: Run the verifier and confirm the expected failure**

Run:

```bash
python3 tests/verify_tens_pages.py
```

Expected: non-zero exit with `AssertionError: Missing page: tens/privacy/index.html`.

- [ ] **Step 3: Commit the failing contract test**

```bash
git add tests/verify_tens_pages.py
git commit -m "test: define TENS public page contract"
```

---

### Task 2: Implement the Privacy and Support Pages

**Files:**
- Create: `tens/assets/styles.css`
- Create: `tens/privacy/index.html`
- Create: `tens/support/index.html`
- Test: `tests/verify_tens_pages.py`

**Interfaces:**
- Consumes: the required paths and phrases enforced by `tests/verify_tens_pages.py`.
- Produces: two static pages with stable root-relative navigation and no external runtime dependencies.

- [ ] **Step 1: Create the shared stylesheet**

Create `tens/assets/styles.css` with:

```css
:root {
  color-scheme: light dark;
  --court: #165b3a;
  --court-dark: #0d3f29;
  --accent: #d8ff52;
  --paper: #f5f3ea;
  --surface: #ffffff;
  --ink: #172019;
  --muted: #59655d;
  --line: #d8ded9;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}
* { box-sizing: border-box; }
body { margin: 0; background: var(--paper); color: var(--ink); line-height: 1.65; }
a { color: var(--court); text-underline-offset: 0.18em; }
a:focus-visible { outline: 3px solid var(--accent); outline-offset: 3px; }
.site-header { background: var(--court-dark); color: #fff; }
.header-inner, main, .footer-inner { width: min(100% - 2rem, 760px); margin-inline: auto; }
.header-inner { display: flex; align-items: center; justify-content: space-between; gap: 1rem; min-height: 72px; }
.brand { color: #fff; font-weight: 800; letter-spacing: 0.08em; text-decoration: none; }
nav { display: flex; gap: 1rem; }
nav a { color: #fff; min-height: 44px; display: inline-flex; align-items: center; }
main { padding-block: clamp(2rem, 6vw, 4.5rem); }
.eyebrow { color: var(--court); font-size: 0.82rem; font-weight: 800; letter-spacing: 0.12em; text-transform: uppercase; }
h1 { font-size: clamp(2.1rem, 8vw, 4.25rem); line-height: 1.02; letter-spacing: -0.045em; margin: 0.35rem 0 1rem; }
h2 { margin-top: 2.2rem; line-height: 1.2; }
.lede { color: var(--muted); font-size: 1.12rem; max-width: 64ch; }
.card { background: var(--surface); border: 1px solid var(--line); border-radius: 18px; padding: clamp(1.25rem, 4vw, 2rem); margin-top: 1.5rem; box-shadow: 0 12px 34px rgb(20 65 43 / 8%); }
.notice { border-left: 5px solid var(--court); }
li + li { margin-top: 0.55rem; }
.site-footer { border-top: 1px solid var(--line); }
.footer-inner { padding-block: 1.5rem 2.5rem; color: var(--muted); }
@media (max-width: 520px) {
  .header-inner { align-items: flex-start; flex-direction: column; padding-block: 1rem; }
  nav { width: 100%; }
  nav a { flex: 1; }
}
@media (prefers-color-scheme: dark) {
  :root { --paper: #0e1511; --surface: #152019; --ink: #f2f6f3; --muted: #b5c1b8; --line: #314139; --court: #82d8a9; }
  .card { box-shadow: none; }
}
```

- [ ] **Step 2: Create the privacy policy page**

Create `tens/privacy/index.html` as semantic HTML with:

- `<title>Privacy Policy — TENS: Tennis Tracker</title>`.
- A shared header with root-relative links to `/tens/privacy/` and `/tens/support/`.
- Introductory copy: `TENS and its developer, Xia Hua, do not collect, transmit, sell, or share your personal data.`
- Sections named `Information We Do Not Collect`, `Device Permissions`, `On-Device Data`, `Health Data`, `Children's Privacy`, `Changes to This Policy`, and `Contact`.
- Permission explanations matching the approved design: Camera for court/player/stroke/ball detection; Microphone for recorded match audio and ball-strike cues; Photos for user-requested import/save; notifications for session feedback; HealthKit and Apple Watch for workouts and fitness information.
- A local-storage explanation covering match videos, tracking samples, session analytics, and preferences, plus deletion through session deletion or app removal and the Photos/Health exceptions.
- A statement that the app has no account system, advertising SDK, third-party analytics SDK, or developer-operated server.
- A visible email link: `<a href="mailto:xhua006@gmail.com">xhua006@gmail.com</a>`.
- The exact effective date and footer required by Global Constraints.

- [ ] **Step 3: Create the support page**

Create `tens/support/index.html` as semantic HTML with:

- `<title>Support — TENS: Tennis Tracker</title>`.
- The same header and root-relative navigation.
- A five-step ordered list covering full-court positioning, permissions, court/player detection, session start/stop with optional Apple Watch, and analytics review.
- A `Troubleshooting` section with subsections for court detection, permissions, Apple Watch, video import/save, and local data removal.
- Contact guidance asking for device model, iOS/watchOS version, and a concise description, while asking users not to send sensitive health data or private recordings.
- A visible email link: `<a href="mailto:xhua006@gmail.com">xhua006@gmail.com</a>`.
- A visible link to `/tens/privacy/` and the exact footer required by Global Constraints.

- [ ] **Step 4: Run the automated verifier**

Run:

```bash
python3 tests/verify_tens_pages.py
```

Expected: `TENS privacy and support pages passed verification.`

- [ ] **Step 5: Check formatting and scope**

Run:

```bash
git diff --check
git status --short
git diff -- tens/assets/styles.css tens/privacy/index.html tens/support/index.html
```

Expected: no whitespace errors; only the three page assets are newly changed in this task; the four pre-existing untracked duplicate files remain unmodified.

- [ ] **Step 6: Commit the implementation**

```bash
git add tens/assets/styles.css tens/privacy/index.html tens/support/index.html
git commit -m "feat: add TENS privacy and support pages"
```

---

### Task 3: Render and Verify the Static Site Locally

**Files:**
- Verify: `tens/privacy/index.html`
- Verify: `tens/support/index.html`
- Verify: `tens/assets/styles.css`
- Test: `tests/verify_tens_pages.py`

**Interfaces:**
- Consumes: the static files from Task 2.
- Produces: verified desktop and mobile layouts ready for deployment.

- [ ] **Step 1: Start a local static server**

Run from the repository root:

```bash
python3 -m http.server 8765
```

Expected: the server listens on `http://127.0.0.1:8765/`.

- [ ] **Step 2: Inspect both pages at desktop width**

Open:

```text
http://127.0.0.1:8765/tens/privacy/
http://127.0.0.1:8765/tens/support/
```

Verify that headings, cards, navigation, email links, and footer are visible; no horizontal scrollbar is present; and both cross-page links work.

- [ ] **Step 3: Inspect both pages at a narrow mobile viewport**

Use a viewport of approximately `390 × 844`. Verify that header navigation wraps cleanly, body text remains readable, touch targets remain usable, and no content is clipped.

- [ ] **Step 4: Run the complete local verification**

```bash
python3 tests/verify_tens_pages.py
git diff --check HEAD~2..HEAD
git status --short
```

Expected: verifier passes; no whitespace errors; only the four known pre-existing untracked duplicate files remain.

---

### Task 4: Deploy and Verify GitHub Pages

**Files:**
- Deploy: commits on branch `master` in `tonyxiahua.github.io`
- Verify: public GitHub Pages responses

**Interfaces:**
- Consumes: reviewed commits from Tasks 1–3.
- Produces: two public HTTPS URLs suitable for App Store Connect.

- [ ] **Step 1: Reconcile with the remote branch**

```bash
git fetch origin master
git log --oneline --left-right --cherry-pick origin/master...master
```

Expected: local commits are visible on the right; no unexpected remote-only commit is ignored. If remote-only commits exist, integrate them non-destructively before continuing.

- [ ] **Step 2: Push the reviewed commits**

```bash
git push origin master
```

Expected: push succeeds without force.

- [ ] **Step 3: Verify public HTTP responses**

Run after GitHub Pages deploys:

```bash
curl -fsSL https://tonyxiahua.github.io/tens/privacy/ | grep -F "Privacy Policy"
curl -fsSL https://tonyxiahua.github.io/tens/support/ | grep -F "TENS Support"
```

Expected: both commands exit `0` and print their matching headings.

- [ ] **Step 4: Verify public content and links in a browser**

Open both HTTPS URLs and confirm the deployed pages match the locally approved desktop and mobile layouts. Confirm `mailto:xhua006@gmail.com`, Privacy, and Support links have the expected targets.

---

### Task 5: Connect the Verified URLs to App Store Connect

**Files:**
- External setting: App Store Connect → App Privacy → Privacy Policy URL
- External setting: App Store Connect → iOS App Version 1.0 → Support URL

**Interfaces:**
- Consumes: the publicly verified HTTPS URLs from Task 4.
- Produces: saved App Store metadata referencing the published pages.

- [ ] **Step 1: Set the privacy policy URL**

In App Store Connect, set the English (U.S.) Privacy Policy URL to:

```text
https://tonyxiahua.github.io/tens/privacy/
```

Save and re-read the field to verify the exact value persisted.

- [ ] **Step 2: Set the support URL**

In App Store Connect version 1.0, set Support URL to:

```text
https://tonyxiahua.github.io/tens/support/
```

Save and re-read the field to verify the exact value persisted.

- [ ] **Step 3: Record remaining submission blockers**

Inspect version 1.0 without submitting it. Report any remaining required fields, specifically screenshots, description, keywords, copyright, reviewer contact name/phone/email, and any Apple compliance prompt not yet completed.
