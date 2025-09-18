# Architecture

## System Overview

This is a simple architecture running a Docker container on AWS AppRunner that contains the application stack with DynamoDB for data persistence (when running in production mode). It's primary guiding principle is simplicity, and ease of development, there is a section that acknowledges the shortcomings and tradeoffs made to meet this objective 

## Architecture Diagram

```mermaid
flowchart TB
  %% Users
  Users[Users
  Web Browser
  Mobile]

  %% AWS Infrastructure
  subgraph AWS["AWS Cloud"]
    subgraph AppRunner["AWS AppRunner"]
      subgraph Docker["Docker Container"]
        Frontend[Frontend
        Static HTML/CSS/JS
        Vue App]
        Backend[Python Backend
        FastAPI
        Business Logic]

        Frontend <--> Backend
      end
    end

    DynamoDB[(DynamoDB
    user_submissions)]
  end

  Users -->|HTTPS:443| AppRunner
  Backend <-->|AWS SDK| DynamoDB

  %% Styling
  classDef user fill:#e1f5fe,stroke:#01579b,stroke-width:2px
  classDef container fill:#fff3e0,stroke:#e65100,stroke-width:2px
  classDef app fill:#e8f5e9,stroke:#1b5e20,stroke-width:2px
  classDef data fill:#fce4ec,stroke:#880e4f,stroke-width:2px

  class Users user
  class Docker,AppRunner container
  class Frontend,Backend app
  class DynamoDB data
```
```
```

## Component Details

### AWS AppRunner Service
- **Platform**: Fully managed container service
- **Auto-scaling**: Automatic scaling based on traffic
- **Network**: HTTPS endpoint with custom domain support

### Docker Container
Single container running the application stack:

- **Frontend**: Served as static files (HTML, CSS, JavaScript)
- **Backend**: Python web framework handling API requests

### Database Layer
- **DynamoDB**: NoSQL database service for production data persistence
  - **Tables**: user_submissions (see entity relationship diagram)
  - **Features**: Auto-scaling, point-in-time recovery
- **SQLite**: Available inside Docker container for all other data
  - **Location**: `/app/data/hotspot.db`
  - **Usage**: Risk scores and suburbs

## Data Flow

1. User sends HTTPS request to AppRunner service endpoint
2. AppRunner routes request to Docker container
3. Frontend serves static files for web interface
4. API calls route to Python backend
5. Backend reads/writes to DynamoDB using AWS SDK (some paths may still use SQLite)
6. Response sent back to user

## Limitations

- **Single region deployment**: No multi-region redundancy
- **Container limitations**: Single container instance (though AppRunner handles scaling)
- **DynamoDB costs**: Pay-per-request pricing model
- **Limited local development**: Uses SQLite for local development which is not persistent
