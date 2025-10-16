# Voice Bot Service

A conversational AI bot for lead management that processes natural language transcripts and integrates with CRM APIs.

## Features

- **Intent Classification**: Supports LEAD_CREATE, VISIT_SCHEDULE, LEAD_UPDATE, and UNKNOWN intents
- **Entity Extraction**: Extracts names, phone numbers, cities, lead IDs, visit times, and status updates
- **CRM Integration**: Real HTTP calls to CRM endpoints with proper error handling
- **Comprehensive Testing**: 13+ unit tests covering happy paths and edge cases
- **Logging**: Structured logging for debugging and monitoring
- **Input Validation**: Rate limiting and input size validation

## Quick Start

### 1. Setup Environment

```bash
# Clone repository
git clone <your-repo-url>
cd Capserv

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt
```

### 2. Start Mock CRM Service

```bash
# Terminal 1: Start Mock CRM
uvicorn mock_crm:app --host 0.0.0.0 --port 8001 --reload
```

### 3. Start Bot Service

```bash
# Terminal 2: Start Bot Service
uvicorn bot.app:app --host 0.0.0.0 --port 8000 --reload
```

### 4. Run Tests

```bash
python -m pytest -q
```

## API Usage

### Create Lead
```bash
curl -X POST http://localhost:8000/bot/handle \
  -H "Content-Type: application/json" \
  -d '{"transcript": "Add a new lead: Rohan Sharma from Gurgaon, phone 9876543210, source Instagram"}'
```

### Schedule Visit
```bash
curl -X POST http://localhost:8000/bot/handle \
  -H "Content-Type: application/json" \
  -d '{"transcript": "Schedule a visit for lead 7b1b8f54-aaaa-bbbb-cccc-1234567890ab at 2025-10-02T17:00:00+05:30"}'
```

### Update Lead Status
```bash
curl -X POST http://localhost:8000/bot/handle \
  -H "Content-Type: application/json" \
  -d '{"transcript": "Update lead 7b1b8f54-aaaa-bbbb-cccc-1234567890ab to WON notes booked unit A2"}'
```

## Configuration

Set environment variables:

```bash
export CRM_BASE_URL=http://localhost:8001
export LOG_LEVEL=INFO
export MAX_TRANSCRIPT_LENGTH=1000
```

## Response Format

### Success Response
```json
{
  "intent": "LEAD_CREATE",
  "entities": {
    "name": "Rohan Sharma",
    "phone": "9876543210",
    "city": "Gurgaon",
    "source": "Instagram"
  },
  "result": {
    "lead_id": "uuid",
    "status": "NEW"
  },
  "crm_call": {
    "endpoint": "/crm/leads",
    "method": "POST",
    "status_code": 200
  }
}
```

### Error Response
```json
{
  "intent": "LEAD_CREATE",
  "error": {
    "type": "VALIDATION_ERROR",
    "details": "Missing required entities: phone"
  }
}
```

## Architecture

- **bot/app.py**: FastAPI application and request orchestration
- **bot/nlu.py**: Intent classification and entity extraction
- **bot/crm_client.py**: HTTP client for CRM integration
- **bot/models.py**: Pydantic request/response models
- **bot/settings.py**: Environment configuration

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=bot

# Run specific test file
pytest tests/test_lead_create.py -v
```

## What I'd Improve With More Time

1. **Advanced NLU**: Integrate OpenAI/Hugging Face for better intent classification
2. **Conversation Memory**: Support multi-turn conversations
3. **Analytics**: Add JSONL logging for analytics and monitoring
4. **Rate Limiting**: Implement Redis-based rate limiting
5. **Database**: Replace in-memory storage with PostgreSQL
6. **Authentication**: Add API key authentication

7. **Deployment**: Docker containerization and Kubernetes manifests
