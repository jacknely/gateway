"""Collection of views used by the service."""
from .health import bp as health_bp

# Build a list of Blueprint objects to be registered when the flask app
# is loaded.
VIEW_BLUEPRINTS = [
    health_bp
]
