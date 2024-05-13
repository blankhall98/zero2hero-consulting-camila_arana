import numpy as np
import matplotlib.pyplot as plt

##########
### Variables
# inversion segura
investment_rate = 11/12
# inversion de riesgo
risk_mean = 1
risk_std = 2
# inflacion
inflation = 6/12
# ingreso mensual
influx = 5000
# tiempo de simulacion
time = 12*10
##########

def calculate_investment(investment_rate, risk_mean, risk_std, inflation, influx, time):
    no_investment = []
    investment = []
    risk = [np.random.normal(risk_mean, risk_std) for _ in range(time)]
    risk_investment = []
    for t in range(time):
        no_investment.append(no_investment[-1] * (1 - inflation/100) + influx if t > 0 else influx)
        investment.append(investment[-1] * (1 + (investment_rate-inflation)/100) + influx if t > 0 else influx)
        risk_investment.append(risk_investment[-1] * (1 + risk[t]/100) + influx if t > 0 else influx)

    plt.figure(figsize=(10,5))
    plt.plot(no_investment, label='No Investment')
    plt.plot(investment, label='Investment')
    plt.plot(risk_investment, label='Risk Investment')
    plt.legend()
    plt.xlabel('Months')
    plt.ylabel('Money')
    plt.title('Investment vs No Investment')
    plt.show()

calculate_investment(investment_rate, risk_mean, risk_std, inflation, influx, time)