# -*- coding: utf-8 -*-
"""
Created on Wed Mar  7 16:35:49 2018

@author: pisto
"""

from pyomo.environ import  Param, RangeSet, NonNegativeReals, Var
from Initialize_Thermal import Initialize_years, Initialize_Demand, Initialize_PV_Energy, Initialize_SC_Energy, Initialize_Thermal_Demand # Import library with initialitation funtions for the parameters

## Thermal Model ##

def Model_Creation(model):
    
    '''
    This function creates the instance for the resolution of the optimization in Pyomo.
    
    :param model: Pyomo model as defined in the Micro-Grids library.
    
    '''
    
    # Time parameters
    model.Periods = Param(within=NonNegativeReals) # Number of periods of analysis of the energy variables
    model.Years = Param() # Number of years of the project
    model.StartDate = Param() # Start date of the analisis
    model.PlotTime = Param() # Quantity of days that are going to be plot
    model.PlotDay = Param() # Start day for the plot
    model.PlotScenario = Param()
    model.Scenarios = Param() 
    
    # Classes Parameters
    model.Classes = Param (within=NonNegativeReals) #Creation of a set from 1 to the number of classes of the thermal part
    
    #SETS
    model.periods = RangeSet(1, model.Periods) # Creation of a set from 1 to the number of periods in each year
    model.years = RangeSet(1, model.Years) # Creation of a set from 1 to the number of years of the project
    model.scenario = RangeSet(1, model.Scenarios) # Creation of a set from 1 to the numbero scenarios to analized
    model.classes = RangeSet(1, model.Classes) # Creation of a set from 1 to the number of classes of the thermal part
    
    # PARAMETERS
    
    # Parameters of the PV 
    model.PV_Nominal_Capacity = Param(within=NonNegativeReals) # Nominal capacity of the PV in W/unit
    model.Inverter_Efficiency = Param() # Efficiency of the inverter in %
    model.PV_invesment_Cost = Param(within=NonNegativeReals) # Cost of solar panel in USD/W
    model.PV_Energy_Production = Param(model.scenario, model.periods, within=NonNegativeReals, initialize=Initialize_PV_Energy) # Energy produccion of a solar panel in W    
    
    # Parameters of the SC (Solare Collectors)
    model.SC_Nominal_Capacity = Param(within=NonNegativeReals) #Nominal capacity of the Solar Collectors
    model.SC_investment_Cost = Param(within=NonNegativeReals) # Cost of SC pannel in USD/W
    model.SC_Energy_Production = Param (model.scenario, model.classes, model.periods, within=NonNegativeReals, initialize=Initialize_SC_Energy)

    
    # Parameters of the battery bank
    model.Charge_Battery_Efficiency = Param() # Efficiency of the charge of the battery in  %
    model.Discharge_Battery_Efficiency = Param() # Efficiency of the discharge of the battery in %
    model.Deep_of_Discharge = Param() # Deep of discharge of the battery (Deep_of_Discharge) in %
    model.Maximun_Battery_Charge_Time = Param(within=NonNegativeReals) # Minimun time of charge of the battery in hours
    model.Maximun_Battery_Discharge_Time = Param(within=NonNegativeReals) # Maximun time of discharge of the battery  in hours                     
    model.Battery_Reposition_Time = Param(within=NonNegativeReals) # Period of repocition of the battery in years
    model.Battery_Invesment_Cost = Param(within=NonNegativeReals) # Cost of battery 
    
    # Parameters of the TANK storage 
    model.Tank_Efficiency = Param() # Efficiency of the tank %   
    model.Tank_Invesment_Cost = Param(within=NonNegativeReals) # Cost of unit Tank USD/W
    model.Deep_of_Tank_Discharge = Param ()
    model.Maximun_Tank_Discharge_Time = Param (within=NonNegativeReals)
    # Parametes of the diesel generator
    model.Generator_Efficiency = Param() # Generator efficiency to trasform heat into electricity %
    model.Low_Heating_Value = Param() # Low heating value of the diesel in W/L
    model.Diesel_Unitary_Cost = Param(within=NonNegativeReals) # Cost of diesel in USD/L
    model.Generator_Invesment_Cost = Param(within=NonNegativeReals) # Cost of the diesel generator
    
    # Parameters of the Boiler 
    model.Boiler_Efficiency = Param() # Boiler efficiency %
    model.Low_Heating_Value_NG = Param() # Low heating value of the natural gas in W/L
    model.NG_Unitary_Cost = Param(within=NonNegativeReals) # Cost of natural gas in USD/L
    model.Boiler_Invesment_Cost = Param(within=NonNegativeReals) # Cost of the NG Boiler

    # Parameters of the Electric Resistance  
    model.Electric_Resistance_Efficiency = Param() # Electric Resistance efficiency %
    model.Resistance_Invesment_Cost = Param(within=NonNegativeReals)
    
    # Parameters of the Energy balance                  
    model.Energy_Demand = Param(model.scenario, model.periods, initialize=Initialize_Demand) # Energy Energy_Demand in W 
    model.Lost_Load_Probability = Param(within=NonNegativeReals) # Lost load probability in %
    model.Value_Of_Lost_Load = Param(within=NonNegativeReals) # Value of lost load in USD/W
    model.Thermal_Energy_Demand = Param(model.scenario, model.classes, model.periods, initialize=Initialize_Thermal_Demand) # Thermal Energy Demand in W 
    
    # Parameters of the proyect
    model.Delta_Time = Param(within=NonNegativeReals) # Time step in hours
    model.Porcentage_Funded = Param(within=NonNegativeReals) # Porcentaje of the total investment that is Porcentage_Porcentage_Funded by a bank or another entity in %
    model.Project_Years = Param(model.years, initialize= Initialize_years) # Years of the project
    model.Maintenance_Operation_Cost_PV = Param(within=NonNegativeReals) # Percentage of the total investment spend in operation and management of solar panels in each period in %                                             
    model.Maintenance_Operation_Cost_Battery = Param(within=NonNegativeReals) # Percentage of the total investment spend in operation and management of solar panels in each period in %
    model.Maintenance_Operation_Cost_Generator = Param(within=NonNegativeReals) # Percentage of the total investment spend in operation and management of solar panels in each period in %
    model.Discount_Rate = Param() # Discount rate of the project in %
    model.Interest_Rate_Loan = Param() # Interest rate of the loan in %
    model.Scenario_Weight = Param(model.scenario, within=NonNegativeReals) #########
    model.Users_Number_Class = Param(model.classes, within=NonNegativeReals) # This parameter defines the number of users for each class
    model.Maintenance_Operation_Cost_SC = Param(within=NonNegativeReals)    # Percentage of the total investment spend in operation and management of solar collectors in each period in %    
    model.Maintenance_Operation_Cost_Boiler = Param (within=NonNegativeReals) # Percentage of the total investment spend in operation and management of boiler in each period in %
    model.Maintenance_Operation_Cost_Tank = Param (within=NonNegativeReals)      # Percentage of the total investment spend in operation and management of tank in each period in %
    model.Maintenance_Operation_Cost_Resistance = Param (within=NonNegativeReals) # Percentage of the total investment spend in operation and management of resistance in each period in %
    
    # VARIABLES
    
    # Variables associated to the solar panels
    model.PV_Units = Var(within=NonNegativeReals) # Number of units of solar panels
    model.Total_Energy_PV = Var(model.scenario,model.periods, within=NonNegativeReals) # Energy generated for the Pv sistem in Wh
    model.SC_Units = Var(model.classes,within=NonNegativeReals) # Number of units of solar collector
    model.Total_Energy_SC = Var(model.scenario, model.classes, model.periods, within=NonNegativeReals) # Energy generated by solar collectors

    # Variables associated to the battery bank
    model.Battery_Nominal_Capacity = Var(within=NonNegativeReals) # Capacity of the battery bank in Wh
    model.Energy_Battery_Flow_Out = Var(model.scenario, model.periods, within=NonNegativeReals) # Battery discharge energy in wh
    model.Energy_Battery_Flow_In = Var(model.scenario, model.periods, within=NonNegativeReals) # Battery charge energy in wh
    model.State_Of_Charge_Battery = Var(model.scenario, model.periods, within=NonNegativeReals) # State of Charge of the Battery in wh
    model.Maximun_Charge_Power= Var() # Maximun charge power in w
    model.Maximun_Discharge_Power = Var() #Maximun discharge power in w
    
    # Variables associated to the storage TANK
    model.Tank_Nominal_Capacity = Var(model.classes, within=NonNegativeReals) # Capacity of the tank in Wh
    model.Energy_Tank_Flow_Out = Var(model.scenario, model.classes, model.periods, within=NonNegativeReals)# Tank unit discharge energy in Wh
    model.SOC_Tank = Var(model.scenario, model.classes, model.periods, within=NonNegativeReals) # State of Charge of the Tank in wh
    model.Maximun_Tank_Discharge_Power = Var(model.classes)
    
    # Variables associated to the diesel generator
    model.Generator_Nominal_Capacity = Var(within=NonNegativeReals) # Capacity  of the diesel generator in Wh
    model.Diesel_Consume = Var(model.scenario,model.periods, within=NonNegativeReals) # Diesel consumed to produce electric energy in L
    model.Generator_Energy = Var(model.scenario, model.periods, within=NonNegativeReals) # Energy generated for the Diesel generator
    model.Diesel_Cost_Total = Var(model.scenario, within=NonNegativeReals)
    
    ## Variables associated to the Boiler 
    model.Boiler_Nominal_Capacity = Var (model.classes, within=NonNegativeReals) # Capacity of the boiler in Wh
    model.NG_Consume = Var(model.scenario, model.classes, model.periods,within=NonNegativeReals) # Natural Gas consumed to produce thermal energy in Kg (considering Liquified Natural Gas)
    model.Boiler_Energy = Var(model.scenario, model.classes, model.periods, within=NonNegativeReals) # Energy generated by the boiler 
    model.NG_Cost_Total = Var(model.scenario, within=NonNegativeReals) 
    
    # Variables associated to the RESISTANCE
    model.Nominal_Power_Resistance = Var(model.classes, within=NonNegativeReals) # Electric Nominal power of the thermal resistance 
    model.Resistance_Thermal_Energy = Var(model.scenario, model.classes, model.periods, within=NonNegativeReals) # Total Electric power considering all the users in each class
    model.Total_Electrical_Resistance_Demand = Var(model.scenario,model.periods, within=NonNegativeReals) # Total Resistance Energy required by the electrical supply considered in the electric energy balance
    
    # Varialbles associated to the energy balance
    model.Lost_Load = Var(model.scenario, model.periods, within=NonNegativeReals) # Energy not suply by the system kWh
    model.Lost_Load_Th = Var(model.scenario, model.classes, model.periods, within=NonNegativeReals) # Energy not suply by the system kWh
    model.Energy_Curtailment = Var(model.scenario, model.periods, within=NonNegativeReals) # Curtailment of solar energy in kWh
    model.Scenario_Lost_Load_Cost = Var(model.scenario, within=NonNegativeReals) ####
    model.Scenario_Lost_Load_Cost_Th = Var(model.scenario, within=NonNegativeReals) ####
    model.Thermal_Energy_Curtailment = Var(model.scenario, model.classes, model.periods, within=NonNegativeReals)
    model.Total_Thermal_Energy_Demand = Var(model.scenario, model.classes, model.periods,  within=NonNegativeReals) # This is the thermal demand considering all the users in that class

    # Variables associated to the financial costs
    model.SC_Financial_Cost = Var(within=NonNegativeReals) # Financial cost of SC technology considering all the classes
    model.Tank_Financial_Cost = Var(within=NonNegativeReals) # Financial cost of Tank technology considering all the classes (he investment tank costs include the resistance cost)
    model.Boiler_Financial_Cost = Var(within=NonNegativeReals) # Financial cost of Boiler technology considering all the classes
    model.Resistance_Financial_Cost = Var(within=NonNegativeReals) # Financial cost of Boiler technology considering all the classes
    
    # Variables associated to the project
    model.Cost_Financial = Var(within=NonNegativeReals) # Financial cost of each period in USD
    model.Scenario_Net_Present_Cost = Var(model.scenario, within=NonNegativeReals) ####
    model.Initial_Inversion = Var(within=NonNegativeReals)
    model.Operation_Maintenance_Cost = Var(within=NonNegativeReals)
    model.Total_Finalcial_Cost = Var(within=NonNegativeReals)
    model.Battery_Reposition_Cost = Var(within=NonNegativeReals)