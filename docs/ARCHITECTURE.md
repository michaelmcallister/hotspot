# Architecture

## System Overview

This is a simple architecture running a Docker container on an AWS t3.micro instance that contains the entire application stack. It's primary guiding principle is simplicity, and ease of development, there is a section that acknowledges the shortcomings and tradeoffs made to meet this objective. 

## Architecture Diagram

```mermaid
flowchart TB
  %% Users
  Users[Users
  Web Browser
  Mobile]

  %% AWS Infrastructure
  subgraph AWS["AWS Cloud"]
    subgraph EC2["EC2 Instance (t3.micro)"]
      subgraph Docker["Docker Container"]
        Frontend[Frontend
        Static HTML/CSS/JS
        Vue App]
        Backend[Python Backend
        FastAPI
        Business Logic]
        DB[(SQLite Database
        Application Data
        User Information)]

        Frontend <--> Backend
        Backend <--> DB
      end
    end
  end

  Users -->|HTTPS:443| EC2

  %% Styling
  classDef user fill:#e1f5fe,stroke:#01579b,stroke-width:2px
  classDef container fill:#fff3e0,stroke:#e65100,stroke-width:2px
  classDef app fill:#e8f5e9,stroke:#1b5e20,stroke-width:2px
  classDef data fill:#fce4ec,stroke:#880e4f,stroke-width:2px

  class Users user
  class Docker,EC2 container
  class Frontend,Backend app
  class DB data
```
```
```

## Component Details

### EC2 Instance
- **Type**: t3.micro (1 vCPU, 1 GB RAM)
- **OS**: Amazon Linux 2
- **Network**: Public IP with security group allowing HTTPS (443)

### Docker Container
Single container running the entire application stack:

- **Frontend**: Served as static files (HTML, CSS, JavaScript)
- **Backend**: Python web framework handling API requests
- **Database**: SQLite file stored in a Docker volume for persistence

## Data Flow

1. User sends HTTPS request to EC2 public IP
2. Docker container receives request on port 443
3. Frontend serves static files for web interface
4. API calls route to Python backend
5. Backend reads/writes to SQLite database
6. Response sent back to user

## Limitations

- **Single point of failure**: No redundancy
- **Limited scalability**: Bound by t3.micro resources
- **SQLite constraints**: Not suitable for high concurrency
- **No load balancing**: Single instance only
- **Manual backups**: Need to implement backup strategy
