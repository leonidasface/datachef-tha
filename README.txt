# Banner Serving Application

This application is a web-based service designed to serve banners. It uses Flask, a lightweight and popular web framework for Python. The application takes a campaign ID as input and returns a selection of banners associated with that campaign.

The main functionality is encapsulated in the selector route, which accepts a campaign ID as a parameter in the URL. It attempts to convert this ID to a float and, if successful, it calls the serve_banners function with the campaign ID and a CSV ID that is determined by the current minute. The serve_banners function presumably returns a selection of banners, which are then passed to a template for rendering.

## Installation

- Create a virtual environment
- pip install -r requirements.txt
- Create static folder and unzip images.zip and csv.zip into it
- Set PYTHONPATH as the root directory of the project
- Set BASE_DIR in banner_service.py to {root directory}/static
- flask run --port 8000 (--debug for debugging)