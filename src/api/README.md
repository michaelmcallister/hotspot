# Hotspot API Backend

## Developer Documentation

### Install Dependencies

You'll need `uv` (see https://docs.astral.sh/uv/getting-started/installation/ for instructions)

once installed you should be able to run `uv sync` to install the dependencies 

### Running the development server

```
uv run fastapi dev main.py
```

You'll now be able to access the API health endpoint at http://127.0.0.1:8000/health which should return "ok"

### Adding new routes

Please place routes under the `routes` directory, and for the endpoint follow the format of `/api/v1/<method>` so that endpoints are version


