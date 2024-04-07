# from typing import cast
# from enma import Enma, DefaultAvailableSources, CloudFlareConfig, NHentai, Sort
# from enma import logger, LogMode

# logger.mode = LogMode.DEBUG
# enma = Enma()

# config = CloudFlareConfig(
#     user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
#     cf_clearance='HSdaGr08Z2g5ILyh8xPaw1GioBCqCs19YG3ZsBeCZ_w-1712184770-1.0.1.1-ziXIDXefJdD2iIY48ts4RHUZF6rqbyZ84d29SAphTnSzZDSzzqr_1nxy3cc37pzXhr3HRtgqiCqoQ1ueU4QHgQ'
# )


# config = CloudFlareConfig(
#     user_agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
#     cf_clearance='HSdaGr08Z2g5ILyh8xPaw1GioBCqCs19YG3ZsBeCZ_w-1712184770-1.0.1.1-ziXIDXefJdD2iIY48ts4RHUZF6rqbyZ84d29SAphTnSzZDSzzqr_1nxy3cc37pzXhr3HRtgqiCqoQ1ueU4QHgQ'
# )

# enma.source_manager.set_source(source_name='nhentai')
# enma.source_manager.source.set_config(config=config)

# doujin = enma.search(query="Metamorph")
# print(doujin.results)


# config = CloudFlareConfig(
#     user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
#     cf_clearance='HSdaGr08Z2g5ILyh8xPaw1GioBCqCs19YG3ZsBeCZ_w-1712184770-1.0.1.1-ziXIDXefJdD2iIY48ts4RHUZF6rqbyZ84d29SAphTnSzZDSzzqr_1nxy3cc37pzXhr3HRtgqiCqoQ1ueU4QHgQ'
# )

# enma = Enma[DefaultAvailableSources]()
# enma.source_manager.set_source('nhentai')
# nh_source = cast(NHentai, enma.source_manager.source)
# nh_source.set_config(config=config)


# doujin = enma.random()
# print(doujin)

# enma = Enma[DefaultAvailableSources]()

# config = CloudFlareConfig(
#     user_agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
#     cf_clearance='x.84U2PUo3oGm3QhGQ31vGlcFIVVtnfhzLMdH._xw_w-1712249634-1.0.1.1-Fcigkouucww.XNLNhXPv9caX118t4C530qutQ3Dtm_sU7nppXgTPkAvRTWsYxCWnpk5BNUbTf8ouOv3czJ01cA'
# )

# enma.source_manager.set_source(source_name='nhentai')
# nh_source = cast(NHentai, enma.source_manager.source)
# nh_source.set_config(config=config)

# doujin = enma.search(query="Metamorph")
# doujin = enma.get(identifier="455417")
# print(doujin)





from hentai import Hentai

a = Hentai.exists(177013)

print(a)