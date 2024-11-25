import os
from app import create_app
from app.routes import routes

app = create_app()
app.register_blueprint(routes)

environment = os.getenv("environment")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    if environment == "dev":
        app.run(host="0.0.0.0", port=port, debug=True)
    else:
        app.run(host="0.0.0.0", port=port)
