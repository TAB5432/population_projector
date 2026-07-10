# population_projector
A population projector which compares two census with a model I wrote and a quadratic model. Based on ModSimPy world population project.

Custom model uses the second derivative of population (the rate of change of growth) to calculate the future projected population. It also includes a decay factor which slowly reduces this projected growth over time. It also ensures the growth can never become negative. There is a maximum growth for when this is needed (around the year 2100), and this maximum should stay below 0.001 as otherwise growth becomes out of hand. The constants are arbitrary, and are easy to play around with for more interesting projections. 

Needs modsim and a html file for the wikipedia page with the data.
