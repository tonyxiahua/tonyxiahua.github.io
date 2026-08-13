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
    r"\\(?:(?P<continuation>\r\n|[\n\r\f])|(?P<hex>[0-9a-fA-F]{1,6})[ \t\r\n\f]?|(?P<char>.))",
    re.DOTALL,
)
RESOURCE_ATTRIBUTES = {
    "base": ("href",),
    "link": ("href",),
    "script": ("src",),
    "img": ("src",),
    "iframe": ("src",),
    "audio": ("src",),
    "video": ("src", "poster"),
    "source": ("src",),
    "track": ("src",),
    "embed": ("src",),
    "object": ("data",),
    "image": ("href", "xlink:href"),
    "use": ("href", "xlink:href"),
    "feimage": ("href", "xlink:href"),
    "mpath": ("href", "xlink:href"),
}
SRCSET_ATTRIBUTES = {"img": ("srcset",), "source": ("srcset",), "link": ("imagesrcset",)}


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.resources = []
        self.srcsets = []
        self.scripts = []
        self.inline_styles = []
        self.style_blocks = []
        self.in_style_block = False
        self.text = []

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag == "a" and "href" in values:
            self.links.append(values["href"])
        if tag in RESOURCE_ATTRIBUTES:
            for attribute in RESOURCE_ATTRIBUTES[tag]:
                resource = values.get(attribute)
                if resource:
                    self.resources.append(resource)
        if tag in SRCSET_ATTRIBUTES:
            for attribute in SRCSET_ATTRIBUTES[tag]:
                srcset = values.get(attribute)
                if srcset:
                    self.srcsets.append(srcset)
        if "style" in values:
            self.inline_styles.append(values["style"])
        if tag == "script":
            self.scripts.append(values)
        if tag == "style":
            self.in_style_block = True

    def handle_endtag(self, tag):
        if tag == "style":
            self.in_style_block = False

    def handle_data(self, data):
        self.text.append(data)
        if self.in_style_block:
            self.style_blocks.append(data)


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
    for srcset in parser.srcsets:
        for candidate in srcset.split(","):
            resource = candidate.strip().split(maxsplit=1)[0]
            if resource:
                verify_local_resource(resource, "resource")
    for source in parser.inline_styles + parser.style_blocks:
        verify_stylesheet(source)


def decode_css_escapes(value):
    def replace(match):
        if match.group("continuation"):
            return ""
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
    continued_background = ".court { background-image: url(https\\\n://example.com/court.png); }"
    continued_import = '@\\\nimport "https://example.com/font.css";'
    script_page = '<!doctype html><script>window.track = true;</script>'
    video_page = '<!doctype html><video src="https://example.com/match.mp4"></video>'
    inline_style_page = '<!doctype html><p style="background: url(https://example.com/court.png)">TENS</p>'
    style_page = '<!doctype html><style>@import "https://example.com/font.css";</style>'
    srcset_page = '<!doctype html><img srcset="https://example.com/court.png 1x">'
    poster_page = '<!doctype html><video poster="https://example.com/cover.png"></video>'
    base_page = '<!doctype html><base href="https://example.com/"><img src="court.png">'
    svg_image_page = '<!doctype html><svg><image href="https://example.com/court.png"></image></svg>'
    svg_use_page = '<!doctype html><svg><use href="https://example.com/icons.svg#icon"></use></svg>'
    svg_filter_page = '<!doctype html><svg><feImage href="https://example.com/filter.png"></feImage></svg>'

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
    require_rejected(
        lambda: verify_stylesheet(continued_background),
        "External stylesheet resource: https://example.com/court.png",
    )
    require_rejected(
        lambda: verify_stylesheet(continued_import),
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
    parser = PageParser()
    parser.feed(inline_style_page)
    require_rejected(
        lambda: verify_html_resources(parser),
        "External stylesheet resource: https://example.com/court.png",
    )
    parser = PageParser()
    parser.feed(style_page)
    require_rejected(
        lambda: verify_html_resources(parser),
        "External stylesheet resource: https://example.com/font.css",
    )
    parser = PageParser()
    parser.feed(srcset_page)
    require_rejected(
        lambda: verify_html_resources(parser),
        "External resource: https://example.com/court.png",
    )
    parser = PageParser()
    parser.feed(poster_page)
    require_rejected(
        lambda: verify_html_resources(parser),
        "External resource: https://example.com/cover.png",
    )
    parser = PageParser()
    parser.feed(base_page)
    require_rejected(
        lambda: verify_html_resources(parser),
        "External resource: https://example.com/",
    )
    parser = PageParser()
    parser.feed(svg_image_page)
    require_rejected(
        lambda: verify_html_resources(parser),
        "External resource: https://example.com/court.png",
    )
    parser = PageParser()
    parser.feed(svg_use_page)
    require_rejected(
        lambda: verify_html_resources(parser),
        "External resource: https://example.com/icons.svg#icon",
    )
    parser = PageParser()
    parser.feed(svg_filter_page)
    require_rejected(
        lambda: verify_html_resources(parser),
        "External resource: https://example.com/filter.png",
    )


def verify_required_text(text, page_name, required_text):
    for phrase in required_text:
        require(phrase in text, f"{page_name}: missing {phrase!r}")


def verify_page(path, required_text):
    require(path.is_file(), f"Missing page: {path.relative_to(ROOT)}")
    parser, text = parse(path)
    verify_required_text(text, path.name, required_text)
    verify_html_resources(parser)
    source = path.read_text(encoding="utf-8").lower()
    for forbidden in ("google-analytics", "googletagmanager", "facebook.net", "<iframe", "<form"):
        require(forbidden not in source, f"Forbidden integration: {forbidden}")
    return parser


PRIVACY_REQUIRED = [
        "Privacy Policy",
        "August 13, 2026",
        "do not collect, transmit, sell, or share your personal data",
        "Camera",
        "Used to detect the tennis court, players, strokes, and ball during a session.",
        "Microphone",
        "Used when you choose to record match audio and to detect ball-strike cues.",
        "Photos",
        "Used only when you request that TENS import a video or save a video to your photo library.",
        "HealthKit",
        "Apple Watch",
        "Used to support tennis workouts and display fitness information when you choose to connect them.",
        "Information We Do Not Collect",
        "has no account system, advertising SDK, third-party analytics SDK, or developer-operated server",
        "On-Device Data",
        "Match videos",
        "tracking samples",
        "session analytics",
        "preferences",
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
]
SUPPORT_REQUIRED = [
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
]


def verify_content_regressions():
    source = PRIVACY.read_text(encoding="utf-8")
    required_phrases = [
        "Used to detect the tennis court, players, strokes, and ball during a session.",
        "Used when you choose to record match audio and to detect ball-strike cues.",
        "Used only when you request that TENS import a video or save a video to your photo library.",
        "Used to support tennis workouts and display fitness information when you choose to connect them.",
        "Match videos",
        "tracking samples",
        "session analytics",
        "preferences",
    ]
    for phrase in required_phrases:
        mutated = source.replace(phrase, "", 1)
        parser = PageParser()
        parser.feed(mutated)
        require_rejected(
            lambda: verify_required_text(" ".join(parser.text), PRIVACY.name, PRIVACY_REQUIRED),
            f"{PRIVACY.name}: missing {phrase!r}",
        )


verify_negative_regressions()
verify_content_regressions()

privacy_parser = verify_page(PRIVACY, PRIVACY_REQUIRED)
support_parser = verify_page(SUPPORT, SUPPORT_REQUIRED)

require(STYLES.is_file(), "Missing tens/assets/styles.css")
verify_stylesheet(STYLES.read_text(encoding="utf-8"))
require("/tens/assets/styles.css" in privacy_parser.resources, "Privacy CSS link is incorrect")
require("/tens/assets/styles.css" in support_parser.resources, "Support CSS link is incorrect")
require("/tens/support/" in privacy_parser.links, "Privacy page must link to Support")
require("/tens/privacy/" in support_parser.links, "Support page must link to Privacy")
require("mailto:xhua006@gmail.com" in privacy_parser.links, "Privacy email link is incorrect")
require("mailto:xhua006@gmail.com" in support_parser.links, "Support email link is incorrect")

print("TENS privacy and support pages passed verification.")
