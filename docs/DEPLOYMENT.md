# Deployment Guide

This project is deployed automatically to **AWS App Runner** whenever changes are pushed to the `main` branch.

---

## How It Works

1. **GitHub Actions Workflow**
   - Every push to `main` triggers the CI/CD workflow (`.github/workflows/deploy.yml`).
   - The workflow:
     1. Checks out the repo
     2. Builds a Docker image
     3. Tags the image with:
        - The commit SHA (`<sha>`)
        - `latest`
     4. Pushes both tags to **Amazon ECR** (`ap-southeast-2` / `hotspot`).

2. **Amazon ECR**
   - Stores the Docker images for this project.
   - The `latest` tag is always the most recent successful build from `main`.

3. **AWS App Runner**
   - Configured to deploy automatically from the ECR image `latest`.
   - As soon as a new `latest` image is pushed, App Runner rolls out a new deployment.

---

## Developer Workflow

- Push code to `main` (or merge a PR into `main`).
- Wait for GitHub Actions to finish (build + push to ECR).
- App Runner will automatically detect the new image and redeploy the service.

That’s it—no manual steps needed once your code hits `main`.


---

## Accessing AWS

- Navigate to https://023231074070.signin.aws.amazon.com/console
- username: team
- password: already provided (reach out to Michael if unsure)

Navigate to https://ap-southeast-2.console.aws.amazon.com/apprunner/home?region=ap-southeast-2 for AppRunner (where our code is hosted)
---

## Useful Notes

- **Failed build?** If the GitHub Actions job fails, no new image is pushed and nothing deploys.
- **Rollback:** To roll back, re-tag and push a known good image to `latest` in ECR.
- **Manual trigger:** You can still start a deployment manually in App Runner if needed, but it’s not required.

