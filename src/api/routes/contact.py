import os
import time
import logging
import requests
from typing import Optional
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, EmailStr
from github import Github, GithubException, GithubIntegration


router = APIRouter()
logger = logging.getLogger(__name__)


#TODO: Validat the categories from the front-end? 
class ContactForm(BaseModel):
    email: EmailStr
    category: str
    subject: str
    postcode: Optional[str] = None
    details: str
    recaptchaToken: str


def verify_recaptcha(token: str) -> bool:
    recaptcha_secret = os.environ.get('RECAPTCHA_SECRET_KEY')
    if not recaptcha_secret:
        raise HTTPException(status_code=500, detail="reCAPTCHA configuration missing")

    try:
        response = requests.post(
            'https://www.google.com/recaptcha/api/siteverify',
            data={
                'secret': recaptcha_secret,
                'response': token
            },
            timeout=10
        )
        response.raise_for_status()
        result = response.json()
        return result.get('success', False)
    except requests.RequestException as e:
        logger.error(f"reCAPTCHA verification failed: {e}")
        return False


# GitHub App configuration, this is all public
APP_ID = 2009244
INSTALLATION_ID = 87350444
GITHUB_REPO = "michaelmcallister/hotspot"

# Simple in-process token cache to avoid requesting new tokens every call
_cached_token = {"token": None, "expires_at": 0}


def _get_installation_token(private_key_pem: str) -> str:
    """Get GitHub App installation token with caching"""
    global _cached_token
    now = time.time()

    # Reuse token if it has >60s remaining
    if _cached_token["token"] and _cached_token["expires_at"] - now > 60:
        return _cached_token["token"]

    # Handle escaped newlines in PEM string
    if "\\n" in private_key_pem and "-----BEGIN" in private_key_pem:
        private_key_pem = private_key_pem.replace("\\n", "\n")

    try:
        gi = GithubIntegration(APP_ID, private_key_pem)
        access = gi.get_access_token(INSTALLATION_ID)

        _cached_token["token"] = access.token
        # Add safety margin to prevent expiration during use
        _cached_token["expires_at"] = access.expires_at.timestamp() - 15
        return access.token
    except Exception as e:
        logger.error(f"Failed to get GitHub App token: {e}")
        raise HTTPException(status_code=500, detail="Contact form unavailable")

def create_github_issue(form_data: ContactForm) -> str:
    private_key_pem = os.environ.get("GITHUB_APP_PEM")
    if not private_key_pem:
        raise HTTPException(status_code=500, detail="Contact form unavailable")

    try:
        token = _get_installation_token(private_key_pem)
        gh = Github(token)
        repo = gh.get_repo(GITHUB_REPO)

        body = f"""**Contact Form Submission**

**Email:** {form_data.email}
**Category:** {form_data.category}
**Postcode:** {form_data.postcode if form_data.postcode else 'Not provided'}

**Details:**
{form_data.details}

---
*This issue was automatically created from the hotspot contact form*
"""

        category_label = form_data.category.lower().strip().replace(" ", "-")

        issue = repo.create_issue(
            title=f"[Contact] {form_data.subject}",
            body=body,
            labels=["contact-form", category_label]
        )

        logger.info(f"Created GitHub issue #{issue.number}: {issue.html_url}")
        return issue.html_url

    except GithubException as e:
        logger.error(f"GitHub API error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to capture submission")
    except Exception as e:
        logger.error(f"Unexpected error creating GitHub issue: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to capture submission")


@router.post("/v1/contact")
async def submit_contact_form(form_data: ContactForm, request: Request):
    try:
        if not verify_recaptcha(form_data.recaptchaToken):
            raise HTTPException(status_code=400, detail="reCAPTCHA verification failed")

        create_github_issue(form_data)

        logger.info(f"Contact form submitted successfully from {form_data.email}")

        return {
            "success": True
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in contact form submission: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while processing your request")
