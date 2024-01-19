class BannerData:
    def __init__(self, bannerId: str, clicks: list, conversions: list, total_revenue: float):
        self.bannerId = bannerId
        self.clicks = clicks
        self.conversions = conversions
        self.total_revenue = total_revenue

