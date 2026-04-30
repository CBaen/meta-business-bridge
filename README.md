# Meta Business Bridge

Purpose: receive Meta Business webhook events for Facebook/Instagram activity and turn them into a clean alert feed for summaries.

This repo is intentionally separate from Calming Engine.

## Handles
- Facebook page messages
- Instagram business messages
- comments
- mentions where Meta exposes them
- review/sales/escalation tagging

## Local test
Run:

```bash
python app.py
```

Then open:

```text
http://localhost:8000/health
```

Expected response:

```text
ok
```
