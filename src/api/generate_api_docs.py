#!/usr/bin/env python3

import json
import sys
from pathlib import Path

# Add parent directory to path to import main
sys.path.insert(0, str(Path(__file__).parent))

from main import app

openapi_spec = app.openapi()
with open("../../docs/openapi.json", "w") as f:
    json.dump(openapi_spec, f, indent=2)

from openapi_markdown.generator import to_markdown
to_markdown("../../docs/openapi.json", "../../docs/api-spec.md")
