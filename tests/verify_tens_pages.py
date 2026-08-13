from html.parser import HTMLParser
from pathlib import Path
import re
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
PRIVACY = ROOT / "tens/privacy/index.html"
SUPPORT = ROOT / "tens/support/index.html"
STYLES = ROOT / "tens/assets/styles.css"
CSS_URL = re.compile(
    r'''url\(\s*(?:["'](?P<quoted>.*?)["']|(?P<bare>[^)\s]+))\s*\)''', re.IGNORECASE
)
CSS_IMPORT = re.compile(
    r'''@import\s+(?:url\(\s*)?["'](?P<url>.*?)["']''', re.IGNORECASE
)
CSS_ESCAPE = re.compile(
    r"\\(?:(?P<hex>[0-9a-fA-F]{1,6})[ \t\r\n\f]?|(?P<char>.))", re.DOTALL
)
RESOURCE_ATTRIBUTES = {
    "link": "href",
    "script": "src",
    "img": "src",
    "iframe": "src",
    "audio": "src",
    "video": "src",
    "source": "src",
    "track": "src",
    "embed": "src",
    "object": "data",
}


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.resources = []
        self.scripts = []
        self.text = []

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag == "a" and "href" in values:
            self.links.append(values["href"])
        if tag in RESOURCE_ATTRIBUTES:
            resource = values.get(RESOURCE_ATTRIBUTES[tag])
            if resource:
                self.resources.append(resource)
        if tag == "script":
            self.scripts.append(values)

    def handle_data(self, data):
        self.text.append(data)


def parse(path):
    parser = PageParser()
    parser.feed(path.read_text(encoding="utf-8"))
    return parser, " ".join(parser.text)


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def verify_local_resource(resource, context):
    parsed = urlparse(resource.strip())
    require(
        not parsed.scheme and not parsed.netloc,
        f"External {context}: {resource}",
    )


def verify_html_resources(parser):
    require(not parser.scripts, "Script tags are not allowed")
    for resource in parser.resources:
        verify_local_resource(resource, "resource")


def decode_css_escapes(value):
    def replace(match):
        if match.group("hex"):
            return chr(int(match.group("hex"), 16))
        return match.group("char")

    return CSS_ESCAPE.sub(replace, value)


def verify_stylesheet(source):
    source = decode_css_escapes(source)
    references = [match.group("url") for match in CSS_IMPORT.finditer(source)]
    references.extend(
        match.group("quoted") or match.group("bare") for match in CSS_URL.finditer(source)
    )
    for reference in references:
        verify_local_resource(reference, "stylesheet resource")


def require_rejected(action, expected_message):
    try:
        action()
    except AssertionError as error:
        require(expected_message in str(error), f"Unexpected failure: {error}")
    else:
        raise AssertionError(f"Expected rejection: {expected_message}")


def verify_negative_regressions():
    remote_stylesheet = '@import url("https://example.com/font.css");'
    remote_background = '.court { background-image: url(//example.com/court.png); }'
    escaped_background = r'.court { background-image: url(https\3a//example.com/court.png); }'
    escaped_import = r'@\69mport "https://example.com/font.css";'
    script_page = '<!doctype html><script>window.track = true;</script>'
    video_page = '<!doctype html><video src="https://example.com/match.mp4"></video>'

    require_rejected(
        lambda: verify_stylesheet(remote_stylesheet),
        "External stylesheet resource: https://example.com/font.css",
    )
    require_rejected(
        lambda: verify_stylesheet(remote_background),
        "External stylesheet resource: //example.com/court.png",
    )
    require_rejected(
        lambda: verify_stylesheet(escaped_background),
        "External stylesheet resource: https://example.com/court.png",
    )
    require_rejected(
        lambda: verify_stylesheet(escaped_import),
        "External stylesheet resource: https://example.com/font.css",
    )
    parser = PageParser()
    parser.feed(script_page)
    require_rejected(lambda: verify_html_resources(parser), "Script tags are not allowed")
    parser = PageParser()
    parser.feed(video_page)
    require_rejected(
        lambda: verify_html_resources(parser),
        "External resource: https://example.com/match.mp4",
    )


def verify_page(path, required_text):
    require(path.is_file(), f"Missing page: {path.relative_to(ROOT)}")
    parser, text = parse(path)
    for phrase in required_text:
        require(phrase in text, f"{path.name}: missing {phrase!r}")
    verify_html_resources(parser)
    source = path.read_text(encoding="utf-8").lower()
    for forbidden in ("google-analytics", "googletagmanager", "facebook.net", "<iframe", "<form"):
        require(forbidden not in source, f"Forbidden integration: {forbidden}")
    return parser


verify_negative_regressions()


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
        "Information We Do Not Collect",
        "has no account system, advertising SDK, third-party analytics SDK, or developer-operated server",
        "On-Device Data",
        "stored locally on your devices",
        "deleting a session or removing the app",
        "Videos you save to Photos and health information you save through HealthKit may remain in Apple services",
        "Health Data",
        "does not use HealthKit data for advertising or sell it to third parties",
        "Children's Privacy",
        "not directed to children under 13 and does not knowingly collect children's personal information",
        "Changes to This Policy",
        "this page will be updated and its effective date will be revised",
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
        "Court detection",
        "Make sure the full court is in frame",
        "Improve lighting where possible, clear obstructions",
        "Permissions",
        "camera, microphone, Photos, notifications, or Health permissions",
        "Apple Watch",
        "Apple Watch is paired with the iPhone, unlocked, and reachable",
        "Video import or save",
        "When importing or saving video, allow Photos access when prompted",
        "Local data removal",
        "Delete a session to remove its locally stored session data, or remove the app to remove its local data",
        "Please do not send sensitive health data or private recordings",
        "xhua006@gmail.com",
        "© 2026 Xia Hua. All rights reserved.",
    ],
)

require(STYLES.is_file(), "Missing tens/assets/styles.css")
verify_stylesheet(STYLES.read_text(encoding="utf-8"))
require("/tens/assets/styles.css" in privacy_parser.resources, "Privacy CSS link is incorrect")
require("/tens/assets/styles.css" in support_parser.resources, "Support CSS link is incorrect")
require("/tens/support/" in privacy_parser.links, "Privacy page must link to Support")
require("/tens/privacy/" in support_parser.links, "Support page must link to Privacy")
require("mailto:xhua006@gmail.com" in privacy_parser.links, "Privacy email link is incorrect")
require("mailto:xhua006@gmail.com" in support_parser.links, "Support email link is incorrect")

print("TENS privacy and support pages passed verification.")
