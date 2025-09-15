# Testing Guide

This project uses Playwright for end-to-end (E2E) testing. Tests are written to align directly with our user journeys and acceptance criteria, and they automatically generate artefacts (screenshots + videos) for review.

---

## How It Works

1. **Playwright Test Runner**
   - Located in the `/e2e` directory
   - Runs headless Chromium by default
   - Each test corresponds to a defined user journey or acceptance criterion (based on our Trello board)

2. **Artefact Capture**
   - Every test automatically saves:
     - **Screenshots** (`.png`)
     - **Videos** (`.webm`)
   - All artefacts are written to `/e2e/artefacts`
   - We then can manually add them to our shared Google Drive

3. **Configuration**
   - Defined in `playwright.config.ts`:
     - `outputDir: artefacts`
     - `screenshot: on`
     - `video: on`
   - Web server started with `make dev` before tests run.

---

## Developer Workflow

- Install dependencies:
  ```bash
  cd e2e
  npm install
