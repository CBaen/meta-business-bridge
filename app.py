from http.server import BaseHTTPRequestHandler, HTTPServer
import json, os, time

VERIFY_TOKEN = os.getenv("META_VERIFY_TOKEN", "change-me")
OUTBOX = "events.jsonl"

class Handler(BaseHTTPRequestHandler):
    def send(self, code, body):
        self.send_response(code)
        self.end_headers()
        self.wfile.write(body.encode())

    def do_GET(self):
        q = self.path
        if q.startswith("/health"):
            self.send(200, "ok")
            return
        if q.startswith("/webhook") and "hub.challenge=" in q:
            parts = dict(x.split("=", 1) for x in q.split("?", 1)[1].split("&"))
            if parts.get("hub.verify_token") == VERIFY_TOKEN:
                self.send(200, parts.get("hub.challenge", ""))
                return
        self.send(403, "forbidden")

    def do_POST(self):
        if self.path != "/webhook":
            self.send(404, "not found")
            return
        length = int(self.headers.get("content-length", 0))
        raw = self.rfile.read(length).decode()
        event = {"received_at": time.time(), "raw": json.loads(raw)}
        with open(OUTBOX, "a", encoding="utf-8") as f:
            f.write(json.dumps(event) + "\n")
        self.send(200, "received")

if __name__ == "__main__":
    HTTPServer(("0.0.0.0", 8000), Handler).serve_forever()
