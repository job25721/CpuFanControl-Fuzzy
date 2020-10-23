import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

# define fuzzy variables
core_temp = ctrl.Antecedent(np.arange(0, 101, 1), 'core_temp')
clock_spd = ctrl.Antecedent(np.arange(0, 4.1, 0.1), 'clock_spd')
fan_spd = ctrl.Consequent(np.arange(0, 6001, 1), 'fan_spd')


# add fuzzy membership function
core_temp['cold'] = fuzz.trimf(core_temp.universe, [0, 0, 50])
core_temp['warm'] = fuzz.trimf(core_temp.universe, [30, 50, 70])
core_temp['hot'] = fuzz.trimf(core_temp.universe, [50, 100, 100])

clock_spd['low'] = fuzz.trimf(clock_spd.universe, [0, 0, 1.5])
clock_spd['med'] = fuzz.trimf(clock_spd.universe, [0.5, 2, 3.5])
clock_spd['high'] = fuzz.trimf(clock_spd.universe, [2.5, 4, 4])

fan_spd['slow'] = fuzz.trimf(fan_spd.universe, [0, 0, 3500])
fan_spd['fast'] = fuzz.trimf(fan_spd.universe, [2500, 6000, 6000])


def show_membership():
    core_temp.view()
    clock_spd.view()
    fan_spd.view()
    plt.show()


# fuzzy rules
rule1 = ctrl.Rule(core_temp['cold'] & clock_spd['low'], fan_spd['slow'])
rule2 = ctrl.Rule(core_temp['cold'] & clock_spd['med'], fan_spd['slow'])
rule3 = ctrl.Rule(core_temp['cold'] & clock_spd['high'], fan_spd['fast'])
rule4 = ctrl.Rule(core_temp['warm'] & clock_spd['low'], fan_spd['slow'])
rule5 = ctrl.Rule(core_temp['warm'] & clock_spd['med'], fan_spd['slow'])
rule6 = ctrl.Rule(core_temp['warm'] & clock_spd['high'], fan_spd['fast'])
rule7 = ctrl.Rule(core_temp['hot'] & clock_spd['low'], fan_spd['fast'])
rule8 = ctrl.Rule(core_temp['hot'] & clock_spd['med'], fan_spd['fast'])
rule9 = ctrl.Rule(core_temp['hot'] & clock_spd['high'], fan_spd['fast'])

# add rules to conctrol system
cpu_fan_ctrl = ctrl.ControlSystem(
    [rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9])

fan_ctrl_simulation = ctrl.ControlSystemSimulation(cpu_fan_ctrl)


def simulate(core_temp, clock_spd):
    fan_ctrl_simulation.input['core_temp'] = core_temp
    fan_ctrl_simulation.input['clock_spd'] = clock_spd
    fan_ctrl_simulation.compute()
    print(f'core temp = {core_temp} Celsius,clock speed = {clock_spd} GHz')
    print(
        f'output : cpu fan speed = {fan_ctrl_simulation.output["fan_spd"]} RPM')
    fan_spd.view(sim=fan_ctrl_simulation)
    plt.show()


# simulation
simulate(core_temp=80, clock_spd=2.7)
