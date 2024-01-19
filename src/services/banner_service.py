from functools import lru_cache
import random
import sys

from flask import url_for

from src.models.models import BannerData
sys.path.insert(0, '/Users/ibrahimnasser/Documents/Personal/datachef-tha/')

from pandas import DataFrame
from src.utils import csv_utils

# Store the last csvId used
last_csvId = None

BASE_PATH = '/Users/ibrahimnasser/Documents/Personal/datachef-tha/static'
BASE_PATH_CSV = f'{BASE_PATH}/csv/'
BASE_PATH_IMAGES = f'{BASE_PATH}/images/'

def serve_banners(campaignId, csvId):
    # Gets impressions, clicks, conversions
    impressions: DataFrame = get_impressions(campaignId, csvId)
    campaign_banners = impressions['banner_id'].reset_index(drop=True).drop_duplicates()

    banner_data = build_banner_data(campaign_banners, campaignId, csvId)
    
    banners = select_banners(banner_data)

    banner_images = [url_for('static', filename=f'images/image_{int(banner)}.png') for banner in banners]

    random.shuffle(banner_images)

    return {'ids': banners, 'images': banner_images}

    # Return banner IDs by criteria
def get_banner_ids(banners, count):
    return [banner.bannerId for banner in banners[:count]]

def fill_with_random_banners(banners, count, random_banners):
    while len(banners) < count:
        banners.append(random.choice(random_banners))
    return banners

# Select banenrs to be sorted
def select_banners(banner_data):
    sorted_bd_with_conversions, sorted_bd_clicks_no_conversions, bd_no_clicks = prepare_sorted_banner_data(banner_data)

    count = len(sorted_bd_with_conversions)
    if count >= 10:
        return get_banner_ids(sorted_bd_with_conversions, 10)
    elif count >= 5:
        return get_banner_ids(sorted_bd_with_conversions, 5)
    else:
        final_banner_list = sorted_bd_with_conversions
        banners_with_top_clicks_count = 5 - len(final_banner_list)
        final_banner_list.extend(get_banner_ids(sorted_bd_clicks_no_conversions, banners_with_top_clicks_count))
        if len(final_banner_list) < 5:
            final_banner_list = fill_with_random_banners(final_banner_list, 5, bd_no_clicks)
        return get_banner_ids(final_banner_list, 5)

# Sort banner data by relevant criteria
def prepare_sorted_banner_data(banner_data):
    bd_with_conversions = [banner for banner in banner_data if (len(banner.conversions) > 0 and banner.total_revenue > 0)]

    sorted_bd_with_conversions = sorted(bd_with_conversions, 
                                            key=lambda banner: banner.total_revenue, 
                                            reverse=True)
        
    bd_clicks_no_conversions = [banner for banner in banner_data if (len(banner.clicks) > 0 and len(banner.conversions) == 0)]

    sorted_bd_clicks_no_conversions = sorted(bd_clicks_no_conversions, 
                                            key=lambda banner: len(banner.clicks), 
                                            reverse=True)
        
    bd_no_clicks = [banner for banner in banner_data if (len(banner.clicks) == 0)]
    return sorted_bd_with_conversions,sorted_bd_clicks_no_conversions,bd_no_clicks

def build_banner_data(campaign_banners, campaignId, csvId):
    banner_data = []

    clicks = get_clicks(campaignId, csvId)
    conversions = get_conversions(csvId)

    for bannerId in campaign_banners:
        bannerData: BannerData = BannerData(bannerId, [], [], 0)
        
        # Filter the clicks data for the current bannerId
        banner_clicks = clicks[clicks['banner_id'] == bannerId]['click_id'].drop_duplicates().reset_index(drop=True)
        bannerData.clicks.extend([click for click in banner_clicks]) 

        for clickId in bannerData.clicks:
            # Filter the conversions data for the current clickId
            click_conversions = conversions[conversions['click_id'] == clickId].drop_duplicates()
            conversionIds = conversions['conversion_id'].reset_index(drop=True)
            bannerData.conversions.extend([conversion for conversion in conversionIds])
            bannerData.total_revenue += click_conversions['revenue'].sum()

        banner_data.append(bannerData)
    
    return banner_data

@lru_cache(maxsize=None)
def get_impressions(campaignId, csvId):
    csvId_cache_clear(csvId)
    impressions_file = f'{BASE_PATH_CSV}/{csvId}/impressions_{csvId}.csv'
    impressions = csv_utils.read_csv(impressions_file)
    
    return impressions.where(impressions.campaign_id == campaignId).dropna()

@lru_cache(maxsize=None)
def get_clicks(campaignId, 
               csvId):
    csvId_cache_clear(csvId)
    clicks_file = f'{BASE_PATH_CSV}/{csvId}/clicks_{csvId}.csv'
    clicks = csv_utils.read_csv(clicks_file)
    
    return clicks.where((clicks.campaign_id == campaignId)).dropna()

@lru_cache(maxsize=None)
def get_conversions(csvId):
    csvId_cache_clear(csvId)
    conversions_file = f'{BASE_PATH_CSV}/{csvId}/conversions_{csvId}.csv'
    conversions = csv_utils.read_csv(conversions_file)
    
    return conversions.dropna()

def clear_cache():
    get_impressions.cache_clear()
    get_clicks.cache_clear()
    get_conversions.cache_clear()

def csvId_cache_clear(csvId):
    global last_csvId
    if csvId != last_csvId:
        clear_cache()
        last_csvId = csvId