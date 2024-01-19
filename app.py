import os
from flask import Flask, render_template
from src.services.banner_service import serve_banners
from src.utils import csv_utils

csvId = csv_utils.csv_by_minute()

# Get the path of the directory where this script is located
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__, template_folder=os.path.join(basedir, 'src/templates'))

@app.route('/<campaign_Id>', methods=['GET', 'POST'])
def selector(campaign_Id):
    try:
        selection = float(campaign_Id)
    except ValueError:
        return "Invalid campaign ID", 400
    banners = serve_banners(selection, csvId)
    return render_template('selector.html', campaign_id = campaign_Id, image_files=banners["images"])