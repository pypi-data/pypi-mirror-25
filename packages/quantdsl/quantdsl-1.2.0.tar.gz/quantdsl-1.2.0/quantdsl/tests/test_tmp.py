# from __future__ import division
#
# import math
#
# import numpy
# from scipy.stats import norm
#
# from quantdsl.interfaces.calcandplot import calc
#
# # def Option(date, strike, underlying, alternative):
# #     Wait(date, Choice(underlying - strike, alternative))
# #
# # def European(date, strike, underlying):
# #     Option(date, strike, underlying, 0)
# #
# # def EuropeanStockOption(start, end, strike, underlying):
# #     European(
# #         start,
# #         strike,
# #         Fixing(end, Settlement(start, Fixing(start, underlying)))
# #     )
# #
# # EuropeanStockOption(Date('2011-1-1'), Date('2012-1-1'), {strike}, Market('GAS'))
#
#
# def calc_european(spot, strike, sigma, rate=0.0):
#     source_code = """
# def Option(date, strike, underlying, alternative):
#     Wait(date, Choice(underlying - strike, alternative))
#
# def EuropeanOption(date, strike, underlying):
#     Option(date, strike, underlying, 0)
#
# def EuropeanStockOption(start, end, strike, underlying):
#     EuropeanOption(end, strike, ForwardMarket(start, underlying))
#
#
# def Option(date, strike, underlying, alternative):
#     Wait(date, Choice(underlying - strike, alternative))
#
# def EuropeanOption(date, strike, underlying):
#     Option(date, strike, underlying, 0)
#
# def EuropeanStockOption(start, end, strike, stock):
#     Option(end, strike, StockMarket(start, end, stock), 0)
#
# # @inline
# def StockMarket(start, end, stock):
#     # This doesn't get the right present time from the Wait unless inlined. Why?
#     # Fixing(end, Settlement(start, 1) * ForwardMarket(start, stock))
#     Settlement(start, 1) * ForwardMarket(start, stock)
#
# def Discount(start):
#     Settlement(start, 1)
#
#
# EuropeanStockOption(Date('2011-1-1'), Date('2012-1-1'), {strike}, 'GAS')
#     """.format(strike=strike)
#
#     results = calc(
#         source_code=source_code,
#         observation_date='2011-1-1',
#         price_process={
#             'name': 'quantdsl.priceprocess.blackscholes.BlackScholesPriceProcess',
#             # 'name': 'nfactormarkovian.NFactorMarkovian',
#             'market': ['GAS'],
#             'sigma': [sigma],
#             'alpha': [0],
#             'rho': [[1]],
#             'curve': {
#                 'GAS': [
#                     ('2011-1-1', spot),
#                     ('2012-1-1', 100 * spot),
#                 ]
#             },
#         },
#         interest_rate=rate,
#         path_count=PATHS
#     )
#     return results.fair_value.mean()
#
#
# def black_scholes_merton(spot, strike, sigma, rate):
#     S0 = spot
#     K = strike
#     I = PATHS
#     z = numpy.random.standard_normal(I)
#     T = 1
#     r = rate / 100
#     inflation = numpy.exp((r - 0.5 * sigma ** 2) * T + sigma * math.sqrt(T) * z)
#     ST = S0 * inflation
#     hT = numpy.maximum(ST - K, 0)
#     C0 = numpy.exp(-r * T) * numpy.sum(hT) / I
#     return C0
#
#
# def european_blackscholes(spot, strike, sigma, rate):
#     S = float(spot)  # spot price
#     K = float(strike)  # strike price
#     r = rate / 100  # annual risk free rate / 100
#     t = 1.0  # duration (years)
#     sigma = max(0.00000001, sigma)  # annual historical volatility / 100
#
#     sigma_squared_t = sigma ** 2.0 * t
#     sigma_root_t = sigma * math.sqrt(t)
#     try:
#         math.log(S / K)
#     except:
#         raise Exception((S, K))
#     d1 = (math.log(S / K) + t * r + 0.5 * sigma_squared_t) / sigma_root_t
#     d2 = d1 - sigma_root_t
#     Nd1 = norm(0, 1).cdf(d1)
#     Nd2 = norm(0, 1).cdf(d2)
#     e_to_minus_rt = math.exp(-1.0 * r * t)
#     # Put option.
#     # optionValue = (1-Nd2)*K*e_to_minus_rt - (1-Nd1)*S
#     # Call option.
#     return Nd1 * S - Nd2 * K * e_to_minus_rt
#
#
# SPOT = 12
# STRIKE = 10
# RATE = 15
# SIGMA = 0.2
# PATHS = 20000
#
# r1 = calc_european(SPOT, STRIKE, SIGMA, RATE)
#
# r2 = european_blackscholes(SPOT, STRIKE, SIGMA, RATE)
#
# r3 = black_scholes_merton(SPOT, STRIKE, SIGMA, RATE)
#
# a = r1
# b = r3
# print('me', round(a, 4), round(b, 4), round(100 * (a - b) / r1, 2))
