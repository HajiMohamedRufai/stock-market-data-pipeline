# stock_api:
# url
"""
https://query1.finance.yahoo.com/
https://query1.finance.yahoo.com/v8/finance/chart/
https://query1.finance.yahoo.com/v8/finance/chart/aapl?metrics=high?&interval=1d&range=1y

"""

# extras
{
    "endpoint": "v8/finance/chart/",
    "headers": {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0"
    }
}

# minio
{
    "endpoint_url": "http://host.docker.internal:9000"
}
