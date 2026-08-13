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
