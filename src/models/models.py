class Click:
    def __init__(self, clickId, bannerId, campaignId):
        self.clickId = clickId
        self.bannerId = bannerId
        self.campaignId = campaignId

class Conversion:
    def __init__(self, conversionId: str, click: Click, revenue: float):
        self.conversionId = conversionId
        self.click = click
        self.revenue = revenue

class BannerData:
    def __init__(self, bannerId: str, clicks: list(Click), conversions: list(Conversion), total_revenue: float):
        self.bannerId = bannerId
        self.clicks = clicks
        self.conversions = conversions
        self.total_revenue = total_revenue

class CampaignData:
    def __init__(self, campaignId, bannerData: BannerData):
        self.campaignId = campaignId
        self.bannerData = bannerData



