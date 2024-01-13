import sys

from models.models import BannerData
sys.path.insert(0, '/Users/ibrahimnasser/Documents/Personal/datachef-tha/')

from pandas import DataFrame
from src.utils import csv_utils

def serve_banners(campaignId):
    # Checks time of day by minute and returns the right CSV ID
    csvId = csv_utils.csv_by_minute()

    banner_data: list(BannerData) = []

    # Gets impressions, clicks, conversions
    impressions: DataFrame = get_impressions(campaignId, csvId)
    campaign_banners = impressions['banner_id'].reset_index(drop=True)
    
    # for banner_id in campaign_banners:
    #     banner_data.append(BannerData(bannerId=banner_id, clicks=clicks, conversions=conversions, total_revenue=0))

    # print(campaign_banners[1])

def get_impressions(campaignId, csvId):
    impressions_file = '/Users/ibrahimnasser/Documents/Personal/datachef-tha/data-files/csv/{csvId}/impressions_{csvId}.csv'
    formatted_file = impressions_file.format(csvId=csvId)
    impressions = csv_utils.read_csv(formatted_file)
    
    return impressions.where(impressions.campaign_id == campaignId).dropna()

def get_clicks(campaignId, bannerId, csvId):
    clicks_file = '/Users/ibrahimnasser/Documents/Personal/datachef-tha/data-files/csv/{csvId}/clicks_{csvId}.csv'
    
    return csv_utils.read_csv(clicks_file.format(csvId)).where(this.campaignId and bannerId)

def get_conversions(clickId, csvId):
    conversions_file = '/Users/ibrahimnasser/Documents/Personal/datachef-tha/data-files/csv/{csvId}/conversions_{csvId}.csv'
    
    return csv_utils.read_csv(conversions_file.format(csvId)).where(clickId)

serve_banners(9)
