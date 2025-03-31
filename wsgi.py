from app import app
import os

if __name__ == "__main__":
    # Bind to 0.0.0.0 to allow external connections
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5001)))
