# -*- coding: utf-8 -*-
"""
Created on Wed Mar  7 16:49:26 2018

@author: pisto
"""

from pyomo.opt import SolverFactory
from pyomo.environ import Objective, minimize, Constraint


def Model_Resolution(model,datapath="Example/data.dat"):   
    '''
    This function creates the model and call Pyomo to solve the instance of the proyect 
    
    :param model: Pyomo model as defined in the Model_creation library
    :param datapath: path to the input data file
    
    :return: The solution inside an object call instance.
    '''
    
    from Constraints_Thermal import  Net_Present_Cost, Solar_Energy,State_of_Charge,\
    Maximun_Charge, Minimun_Charge, Max_Power_Battery_Charge, Max_Power_Battery_Discharge, Max_Bat_in, Max_Bat_out, \
    Financial_Cost, Energy_balance, Maximun_Lost_Load, Maximun_Lost_Load_Th, Scenario_Net_Present_Cost, Scenario_Lost_Load_Cost, Scenario_Lost_Load_Cost_Th, \
    Initial_Inversion, Operation_Maintenance_Cost, Total_Finalcial_Cost, Battery_Reposition_Cost, Maximun_Diesel_Energy, Diesel_Comsuption,Diesel_Cost_Total, \
    Solar_Thermal_Energy, State_Of_Charge_Tank, Maximun_Tank_Charge, Maximum_Boiler_Energy, \
    NG_Consumption, Maximum_Resistance_Thermal_Energy, Total_Thermal_Energy_Demand, Thermal_Energy_Balance, Total_Electrical_Resistance_Demand, SC_Financial_Cost, \
    Tank_Financial_Cost, Boiler_Financial_Cost , Resistance_Financial_Cost, NG_Cost_Total , Minimun_Tank_Charge, Max_Power_Tank_Discharge, \
    Max_Tank_out
    
    
    # OBJETIVE FUNTION:
    model.ObjectiveFuntion = Objective(rule=Net_Present_Cost, sense=minimize)  
    
    # CONSTRAINTS
    #Energy constraints
    model.EnergyBalance = Constraint(model.scenario,model.periods, rule=Energy_balance)
    model.MaximunLostLoad = Constraint(model.scenario, rule=Maximun_Lost_Load) # Maximum permissible lost load
    model.MaximunLostLoadTh = Constraint(model.scenario, model.classes, rule=Maximun_Lost_Load_Th) # Maximum permissible lost load
    model.ScenarioLostLoadCost = Constraint(model.scenario, rule=Scenario_Lost_Load_Cost)
    model.ScenarioLostLoadCostTh = Constraint(model.scenario, rule=Scenario_Lost_Load_Cost_Th)
    model.TotalThermalEnergyDemand = Constraint(model.scenario, model.classes, model.periods, rule=Total_Thermal_Energy_Demand)
    model.ThermalEnergyBalance = Constraint(model.scenario, model.classes, model.periods, rule=Thermal_Energy_Balance)
    model.TotalElectricalResistanceDemand = Constraint(model.scenario, model.periods, rule=Total_Electrical_Resistance_Demand)

    # Solar Collectors Constraints    
    model.SolarThermalEnergy = Constraint(model.scenario, model.classes, model.periods, rule=Solar_Thermal_Energy)

    # PV constraints
    model.SolarEnergy = Constraint(model.scenario, model.periods, rule=Solar_Energy)  # Energy output of the solar panels
    
    # Battery constraints
    model.StateOfCharge = Constraint(model.scenario, model.periods, rule=State_of_Charge) # State of Charge of the battery
    model.MaximunCharge = Constraint(model.scenario, model.periods, rule=Maximun_Charge) # Maximun state of charge of the Battery
    model.MinimunCharge = Constraint(model.scenario, model.periods, rule=Minimun_Charge) # Minimun state of charge
    model.MaxPowerBatteryCharge = Constraint(rule=Max_Power_Battery_Charge)  # Max power battery charge constraint
    model.MaxPowerBatteryDischarge = Constraint(rule=Max_Power_Battery_Discharge)    # Max power battery discharge constraint
    model.MaxBatIn = Constraint(model.scenario, model.periods, rule=Max_Bat_in) # Minimun flow of energy for the charge fase
    model.Maxbatout = Constraint(model.scenario, model.periods, rule=Max_Bat_out) #minimun flow of energy for the discharge fase

    # Tank Constraints     
    model.StateOfChargeTank = Constraint(model.scenario, model.classes, model.periods, rule =State_Of_Charge_Tank)
    model.MaximumTankCharge = Constraint(model.scenario, model.classes, model.periods, rule =Maximun_Tank_Charge)
    model.MinimunTankCharge = Constraint(model.scenario, model.classes, model.periods, rule =Minimun_Tank_Charge)
    model.MaxPowerTankDischarge = Constraint(model.classes, rule =Max_Power_Tank_Discharge)
    model.MaxTankout = Constraint(model.scenario, model.classes, model.periods, rule =Max_Tank_out)
    
    # Boiler Constraints     
    model.MaximumBoilerEnergy = Constraint(model.scenario, model.classes, model.periods, rule =Maximum_Boiler_Energy) 
    model.NGConsumption = Constraint(model.scenario, model.classes, model.periods, rule = NG_Consumption)
    model.NGCostTotal = Constraint(model.scenario, rule = NG_Cost_Total)
    
    # Electrical Resistance Constraint     
    model.MaximumResistanceThermalEnergy = Constraint(model.scenario, model.classes, model.periods, rule = Maximum_Resistance_Thermal_Energy)
    
    # Diesel Generator constraints
    model.MaximunDieselEnergy = Constraint(model.scenario, model.periods, rule=Maximun_Diesel_Energy) # Maximun energy output of the diesel generator
    model.DieselComsuption = Constraint(model.scenario, model.periods, rule=Diesel_Comsuption)    # Diesel comsuption 
    model.DieselCostTotal = Constraint(model.scenario, rule=Diesel_Cost_Total)
    
    # Financial Constraints
    #model.MinRES = Constraint(model.scenario, model.classes, rule = Min_Renewables )
    model.SCFinancialCost = Constraint(rule = SC_Financial_Cost ) 
    model.TankFinancialCost = Constraint(rule = Tank_Financial_Cost ) 
    model.BoilerFinancialCost = Constraint(rule =Boiler_Financial_Cost )
    model.ResistanceFinancialCost = Constraint(rule = Resistance_Financial_Cost )
    model.FinancialCost = Constraint(rule=Financial_Cost) # Financial cost
    model.ScenarioNetPresentCost = Constraint(model.scenario, rule=Scenario_Net_Present_Cost)    
    model.InitialInversion = Constraint(rule=Initial_Inversion)
    model.OperationMaintenanceCost = Constraint(rule=Operation_Maintenance_Cost)
    model.TotalFinalcialCost = Constraint(rule=Total_Finalcial_Cost)
    model.BatteryRepositionCost = Constraint(rule=Battery_Reposition_Cost) 

    
    instance = model.create_instance(datapath) # load parameters       
    opt = SolverFactory('cplex') # Solver use during the optimization    
    results = opt.solve(instance, tee=True) # Solving a model instance 
    instance.solutions.load_from(results)  # Loading solution into instance
    return instance
    