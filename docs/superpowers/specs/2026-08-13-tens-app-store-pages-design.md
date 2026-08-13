# TENS App Store Pages Design

Date: August 13, 2026

## Goal

Publish two durable, English-language GitHub Pages URLs that satisfy the App Store requirements for a privacy policy and a support page for **TENS: Tennis Tracker**.

The pages will live in the existing `tonyxiahua.github.io` repository and will not change the existing blog or its generated assets.

## Public URLs

- Privacy policy: `https://tonyxiahua.github.io/tens/privacy/`
- Support: `https://tonyxiahua.github.io/tens/support/`

## File Structure

```text
tens/
├── assets/
│   └── styles.css
├── privacy/
│   └── index.html
└── support/
    └── index.html
```

Each page is a standalone semantic HTML document. Both pages share one local stylesheet and require no build step.

## Visual Design

The pages use a restrained tennis-inspired palette: deep court green for branding, a warm off-white background, white content surfaces, and high-contrast dark text. Typography uses the operating system font stack, so no external font request is required.

The layout consists of a compact TENS header, a readable single-column article, cross-links between Privacy and Support, and a footer. It adapts to narrow phone screens without horizontal scrolling. Motion is unnecessary.

Footer text: `© 2026 Xia Hua. All rights reserved.`

## Privacy Policy Content

The privacy page will state that TENS and Xia Hua do not collect, transmit, sell, or share personal data. It will accurately distinguish local device processing from data collection.

The policy will explain:

- Camera access is used to detect the tennis court, players, strokes, and the ball.
- Microphone access is used when recording match audio and detecting ball-strike sounds.
- Photo Library access is used only when the user chooses to save or import a video.
- HealthKit and Apple Watch data are used to support tennis workouts and display fitness information. TENS does not use HealthKit data for advertising or sell it to third parties.
- Match videos, tracking samples, session analytics, and preferences remain on the user's devices unless the user deliberately exports or shares them using Apple-provided controls.
- The app has no account system, advertising SDK, third-party analytics SDK, or developer-operated server.
- Users can remove locally stored data by deleting sessions or the app, subject to data retained by Apple services such as Photos or Health when the user has saved data there.
- The app is not directed to children under 13 and does not knowingly collect children's personal information.
- Material policy changes will be reflected on the page with an updated effective date.
- Privacy questions can be sent to `xhua006@gmail.com`.

Effective date: `August 13, 2026`.

## Support Page Content

The support page will help a user complete the core product workflow:

1. Position the iPhone so the full tennis court is visible.
2. Grant camera and microphone access when prompted.
3. Wait for court and player detection before starting a session.
4. Start and stop tracking from the iPhone, with optional Apple Watch workout support.
5. Review session totals, movement, speed, shot counts, heatmaps, and saved match video where available.

Troubleshooting will cover:

- Court detection problems caused by framing, lighting, obstructions, or incomplete court visibility.
- Missing camera, microphone, Photos, notifications, or Health permissions.
- Apple Watch pairing and reachability.
- Importing or saving video.
- Where local session data is stored and how to remove it.

The page will link to the privacy policy and offer a `mailto:xhua006@gmail.com` contact link. It will ask users to include their device model, iOS/watchOS version, and a concise description of the problem, but not sensitive health data or private recordings.

## Privacy and Security Constraints

- No cookies, analytics, trackers, third-party scripts, embedded forms, or remote fonts.
- No sensitive information in URL parameters.
- No promise that exceeds the behavior verified in the TENS source code.
- The public support email is `xhua006@gmail.com`, approved by the user.
- The public developer attribution is `Xia Hua`, approved by the user.

## Accessibility

- Use semantic landmarks, ordered heading levels, descriptive links, and a visible keyboard focus state.
- Maintain WCAG AA text contrast.
- Set a comfortable reading width and minimum touch-target size.
- Respect the user's color scheme where practical without changing meaning.

## Failure Handling

Because the site is static, runtime failure modes are limited. Pages must remain useful if CSS fails to load, and email links must display the address as readable text. All links use stable absolute-root paths within the GitHub Pages site.

If deployment fails, no App Store URL will be entered until both public pages return successful HTTP responses and display the expected content.

## Verification

Before deployment:

- Validate that both HTML files parse successfully.
- Check internal links and the email link.
- Serve the repository locally and inspect both desktop and narrow mobile layouts.
- Confirm that no external network resources are referenced.
- Confirm that existing repository files and unrelated untracked files are unchanged.

After deployment:

- Verify both HTTPS URLs load publicly.
- Verify the published pages show the approved developer name, support email, effective date, and privacy statements.
- Enter the privacy URL and support URL into App Store Connect only after public verification.

## Acceptance Criteria

- Both required URLs are public over HTTPS and work without authentication.
- The privacy page matches the App Store `Data Not Collected` declaration and the audited app behavior.
- The support page provides actionable setup and troubleshooting guidance.
- Both pages are usable on current desktop and mobile browsers.
- Existing blog content and unrelated working-tree changes remain untouched.
