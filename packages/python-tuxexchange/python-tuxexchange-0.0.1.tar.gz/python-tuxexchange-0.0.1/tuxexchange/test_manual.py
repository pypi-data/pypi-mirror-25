from tuxexchange import Tuxexchange

tuxexchange = Tuxexchange()

print tuxexchange.api_query('getcoins')
print tuxexchange.api_query('getticker')
