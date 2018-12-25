import quandl


qunadl_api_key = 'CbFioSS1kKs31Uvfyctb'
data = quandl.get("WIKI/KO", start_date="2016-01-01", end_date="2018-01-01", api_key=qunadl_api_key)