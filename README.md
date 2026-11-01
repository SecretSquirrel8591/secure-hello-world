# Secure Hello World — GitHub Actions CI/CD Discussion Assignment

This repository contains a simple **build → test → deploy** pipeline with **two or more steps per stage** and basic security checks. The site is deployed to **GitHub Pages** on pushes to `main` (or manual runs). Only Python 3 and GitHub Actions are needed.

## Setup and run

1. Create a **public** GitHub repository named `secure-hello-world`. Use `main` as its default branch. GitHub Pages is available for public repositories on GitHub Free. Don't commit credentials or sensitive information.
2. Upload the **contents** of this folder (including the hidden `.github` directory) to the repository root, either by Git or by using GitHub's **Add file → Upload files**. If using the browser, GitHub may hide dot folders in some upload dialogs; ensure `.github/workflows/ci-cd.yml` is present in the repository afterward. Git commands are below.
3. In the repository, go to **Settings → Pages → Build and deployment → Source** and select **GitHub Actions**.
4. Go to **Actions → Secure Hello World CI/CD** and inspect the automatically triggered run. If none ran, select **Run workflow**. GitHub Pages deployment will produce a live site URL when successful.
5. Confirm all three stages show success: **Build**, **Test + Security Checks**, and **Deploy**. Open the live site and verify the Hello, World! message.

### Git commands (optional)

```bash
git init
git branch -M main
git add .
git commit -m "Add secure Hello World CI/CD demo"
git remote add origin https://github.com/YOUR_USERNAME/secure-hello-world.git
git push -u origin main
```

Make sure you created the empty repository first and replace `YOUR_USERNAME`.

## Local verification (does not substitute for GitHub Actions screenshots)

```bash
python3 scripts/build.py
python3 -m unittest discover -s tests -v
python3 scripts/security_scan.py
```

## Stage-by-stage explanation

| Stage | Step 1 | Step 2 | Additional step |
|---|---|---|---|
| Build | Checkout source | Generate `dist/` output | Verify build and upload Pages artifact |
| Test | Checkout source | Run unit/security checks | Run basic secret-pattern scan |
| Deploy | Configure Pages | Deploy Pages artifact | Deployment depends on both previous jobs passing |

## Security integrations

- Unit tests validate page content and basic HTML security posture; a CSP meta tag restricts loaded resources.
- A simple Python scanner looks for certain accidentally committed secret formats in site content and workflow configuration.
- Workflow defaults to `contents: read`; only the deploy job receives `pages: write` and `id-token: write`.
- Deploy waits for a passing build and test; publishing is limited to the `main` branch.

**Limitations:** The lightweight secret-pattern check is a classroom demonstration, not a full-featured SAST or secret scanner. CSP meta tags cannot enforce all directives (such as `frame-ancestors`); a production site should use appropriate HTTP response headers as well. External GitHub Actions are versioned by major tag for ease of demonstration; production workflows should consider pinning actions to immutable commit hashes and adding a dependency/vulnerability scanner.

## Screenshots to capture from YOUR actual run

1. Open `.github/workflows/ci-cd.yml` in GitHub and screenshot the visible `build`, `test`, and `deploy` jobs. If they don't fit, take two screenshots.
2. Open **Actions → your completed workflow** and screenshot all three green job boxes.
3. Expand the **Test + Security Checks** job and screenshot `Run unit and security configuration tests` and `Scan source for accidentally committed secrets` with their successful log output.
4. Open **Deploy** and screenshot the published GitHub Pages URL (or the resulting live Hello, World! site).

**Do not fabricate execution screenshots.** A screenshot of local tests alone does not demonstrate the cloud deployment stage.

## Common issues

- **Workflow absent from Actions:** ensure `.github/workflows/ci-cd.yml` is uploaded, not merely the `site` folder.
- **Deploy fails with Pages not enabled:** Set **Settings → Pages → Source → GitHub Actions** then rerun.
- **No ability to edit Pages settings:** repository owner/admin access may be required.
- **Deployment protection error:** check environment restrictions under **Settings → Environments → github-pages**.
