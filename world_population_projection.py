from pandas import read_html
from modsim import *
import matplotlib.pyplot as plt

DECAY_RATE = 0.99 #recommended at 0.99
MAX = 0.0001 #0.001 IS ABSOLUTE LIMIT

filename = "World_population_estimates.html"
tables = read_html(filename,
                   header=0, 
                   index_col=0,
                   decimal='M')

#world population statistics 1960-2016
table2 = tables[2]
table2.columns = ["census", "prb", "un", "maddison", "hyde", "tanton", "biraben", "mj", "thomlinson", "durand", "clark"]

census = table2.census / 1e9
un = table2.un / 1e9


#world population projections
table3 = tables[3]
table3.columns = ['census', 'prb', 'un']

def plot_projections(table):
    census_proj = table.census.dropna() / 1e9
    un_proj = table.un.dropna() / 1e9

    census_proj.plot(style =":", label = "US Census")
    un_proj.plot(style="--", label = "UN DESA")
    decorate(xlabel="Year", ylabel="World Population in Billions")

#1960-2016
t_0 = int(census.index[0])
t_end = int(census.index[-2])

total_time = t_end - t_0

p_0 = census[t_0]
p_end = census[t_end]

total_growth = p_end - p_0
annual_growth = total_growth / total_time

system = System(t_0=t_0, t_end=2500, p_0=p_0, annual_growth=annual_growth)

#for 1950
system.birth_rate = 35.35/1000
system.death_rate = 16.88/1000
system.past_alpha = system.birth_rate - system.death_rate

#for quadratic
system.curr_alpha = 25 / 1000
system.beta = -1.8/1000

#1950-2010
system.birth_rates = [35.35, 33.00, 28.19, 26.09, 21.73, 19.99]
system.death_rates = [16.88, 12.90, 10.47, 9.33, 8.65, 7.89]

#calculates changes
alphas = [
    (b-d)/1000
    for b,d in zip(system.birth_rates, system.death_rates)
]

#average delta in growth
system.avg_alpha_change = (alphas[-1] - alphas[0]) / (2020-1960)

def custom_model(t, curr_pop, system):
    decay  = DECAY_RATE ** ((t - 1960) / 10)
    curr_alpha = system.past_alpha + (t - 1960) * (system.avg_alpha_change / decay)
    curr_alpha = max(curr_alpha, MAX)
    return curr_alpha * curr_pop

def quadratic_model(t, curr_pop, system):
    return system.curr_alpha * curr_pop + system.beta * curr_pop**2

def run_model(system, model):
    results = TimeSeries()
    results[system.t_0] = system.p_0

    for t in range(system.t_0, system.t_end):
        growth = model(t, results[t], system)
        results[t+1] = results[t] + growth
    
    return results

my_results = run_model(system, custom_model)
my_results.plot(color='red', label='Custom Model')

quad_results = run_model(system, quadratic_model)
quad_results.plot(color='blue', label='Quadratic Model')
plot_projections(table3)
decorate(title = "Comparing Our Model")
plt.show()













