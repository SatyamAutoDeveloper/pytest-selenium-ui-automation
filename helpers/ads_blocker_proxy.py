from mitmproxy import http

# Common keywords found in URLs of dynamic ad providers
AD_BLOCK_KEYWORDS = [
    "adservice", 
    "doubleclick", 
    "googletagmanager",
    "ads.", 
    "pubads",
    "adzerk",
    "analytics",
    "utm_campaign",
    "utm_source",
    "adclick",
    "adtrack",
    "adserver",
    "adbanner",
    "adnetwork",
    "ad_impression",
    "ad_pixel",
    "ad_request",
    "ad_display",
    "ad_view",
    "ad_interstitial",
    "ad_overlay",
    "ad_injection",
    "ad_script",
    "ad_tag",
    "ad_content",
    "ad_slot",
    "ad_unit",
    "ad_zone",
    "ad_targeting",
    "ad_performance",
    "ad_revenue",
    "ad_conversion",
    "ad_click",
    "ad_impressions"
    "Offer",
    "Promo",
    "Banner",
    "Affiliate",
    "Sponsorship",
    "Marketing",
    "Advertisement",
    "Monetization",
    "Tracking",
    "Retargeting",
    "Behavioral",
    "Contextual",
    "NativeAd",
    "VideoAd",
    "InterstitialAd",
    "Popunder",
    "Skyscraper",
    "Leaderboard",
    "FooterAd",
    "HeaderAd",
    "SponsoredContent",
    "BrandedContent",
    "ContentRecommendation",
    "AdExchange",
    "RealTimeBidding",
    "Programmatic",
    "AdNetwork",
    "AdTech",
    "DSP",
    "SSP",
    "RTB",
    "offer/details",
    "promo/click",
    "banner/view",
    "affiliate/track",
    "sponsorship/load",
    "marketing/pixel",
    "advertisement/fetch",
    "monetization/script",
    "tracking/collect",
    "retargeting/show",
    "behavioral/ad",
    "contextual/ad",
    "nativead/render",
    "videoad/play",
    "interstitialad/display",
    "popunder/open",
    "skyscraper/load",
    "leaderboard/fetch",
    "footerad/show",
    "headerad/render",
    "sponsoredcontent/load",
    "brandedcontent/fetch",
    "contentrecommendation/display",
    "adexchange/request",
    "realtimebidding/bid",
    "programmatic/ad",
    "adnetwork/fetch",
    "adtech/serve",
    "dsp/bid",
    "ssp/offer",
    "rtb/request"

]

class AdBlocker:
    def request(self, flow: http.HTTPFlow) -> None:
        url = flow.request.pretty_url
        # Check if the URL contains any of the blocking keywords
        if any(keyword in url for keyword in AD_BLOCK_KEYWORDS):
            # Block the request by responding with a 404 Not Found
            flow.response = http.Response.make(
                404, 
                b"Ad Request Blocked by Proxy", 
                {"Content-Type": "text/plain"}
            )
            print(f"🛑 Blocked Ad Request: {url}")

addons = [
    AdBlocker()
]