#!/usr/bin/env python
# coding: utf-8

# In[94]:


import numpy as np
import pandas as pd
from pypower.api import case9,case30pwl,case6ww,case39,case9Q,case300,case4gs,case24_ieee_rts,ppoption, runpf, printpf, makeYbus, makeB
from pypower.ppoption import ppoption


# In[95]:


data = {}

def mcarlo(a,b):
    
    for i in range(a,b):
        
        #load test case
        ppc = case9()
        gen = pd.DataFrame(ppc['gen'])
        bus = pd.DataFrame(ppc['bus'])
        print('original bus active power injection data:')
        print(bus[2])
        print('original bus reactive power injection data:')
        print(bus[3])
        
        #randomly choosing a generator

        row = np.random.randint(0,gen.index[-1]+1)
        print("generator df row:",row)

        #calculating connected bus number
        bus_no = gen.loc[row,0]
        print("connected bus:",bus_no)

        #calculating generator capacity
        gen_cap = gen.loc[row,8]
        print("generator capacity:",gen_cap)

        #calculating wind forecast
        fcst = gen_cap*0.1
        print("forecast:",fcst)

        #calculating forecasting error from a normal distribution with 0 mean and 0.05 sdv

        fcst_error = np.random.normal(loc=0, scale=0.05, size=1)[0]
        print("forecast error:",fcst_error)

        #final forecast

        final_fcst = fcst + fcst_error
        print("final forecast:",final_fcst)


        #getting dataframe row value for bus connected to selected generator

        bus_dfrow = bus[bus[0]==bus_no].index[0]
        print('bus df row:',bus_dfrow)

        
        #calculating factors from two given distributions

        factor_1 = np.random.uniform(0.8,1.2) 
        print('factor 1:',factor_1)
        factor_2 = np.random.uniform(0.15,0.25)
        print('factor 2:',factor_2)
        
        #addressing bus load fluctuations

        bus[2] = bus[2]*factor_1
        bus[3] = bus[3]*factor_1*factor_2

        #adjusting bus value for wind generation

        bus.loc[bus_dfrow,2] = bus.loc[bus_dfrow,2] - final_fcst
        

        #addressing N-1 contingency
        print("branch shape, x:", ppc['branch'].shape[0])
        brnch_row = np.random.randint(0,ppc['branch'].shape[0])
        print("branch row to be deleted:", brnch_row)
        ppc['branch'] = np.delete(ppc['branch'],brnch_row,0)
        
        #solve ACPF model (Newton's method)
        ppopt = ppoption(PF_ALG=1)
        
        #store data if model converges. Ignore if it doesn't
        try:
            r = runpf(ppc, ppopt)
            data[f'sim{i}'] = r
        except:
            continue
        
        solved = pd.DataFrame(data[f'sim{i}'][0]['bus'])
        
        print('solved:')
        print(solved)


# # Line flow 
# 
# => Col 5 gives line flow cap
# 
# => Col 13 gives line flow values
# 
# => sep g for each line

# # Issues
# 
# 1. Does lowering row indexes by 1 for bus data (column 0) and branch data (columns 0 and 1) affect other values (columns) within bus and branch data ? If so, what are they and how should they be adjusted?
# 
# Everything being considered for case9(). Following info MAY vary for other cases.
# 
# => For ppc['bus'] lower indexes by 1 for first column that records bus numbers
# 
# => For ppc['branch'] lower indexes by 1 for first two columns that record branch numbers
# 
# => For ppc['gen'] lower index by 1 for first column that records genarator numbers
# 
# 
# 2. Renewable generation fluctuation (part of the generators considered as wind generators) has been addressed as multiplying P column with -1. Is this correct ? As described in the paper, the wind speed forecast error is assumed to follow a normal distribution with zero mean and a standard deviation of 0.05.
# 
# Everything being considered for case9(). Following info MAY vary for other cases.
# 
# => consider column 8 of ppc['gen'] that records max capacity for each generators
# 
# => Randomly pick one generator. Figure out which bus is said generator connected to. [Look into column names/definitions for standard IEEE test cases from either MATPOWER or PYPOWER]
# 
# => Assume a forecast that 10% from said genarator's max capacity is attributed to wind power. Calculate this wind power.
# 
# => Adjust said wind power value for forecast error by randomly picking error value from distribution mentioned in the paper (mean=0,sdv=0.05) and adding it to the said wind power value. 
# 
# => Subtract this value now from the P column (column 2 in ppc['bus']) row corresponding to the bus connected to generator
# 
# => Now multiply P and Q columns with the factors mentioned in the paper. Randomly drop row from branch data to maintain N-1 contingency
# 
# => Solve ACPF model.
# 
# 
# 3. Do the ACPF calculation results make sense? Are there any outragous values ?
# 
# => They don't make sense. Q values are outragous after solving ACPF model.
# 
# 4. Do results look okay after improving on first 3 concerns?
# 
# => flip wind and load fluctuation
# 
# 5. How to set wind gen forecast for cases other than case 9 (10%)?
# 
# => Okay (you can actually choose anything between 10 to 30%). value chosen from a normal dist with mean = 25 , sdv = 5 can also work
# 
# 6. From the result bus data, does column 7 (Vm) gives ith bus voltage?
# 
# => yes
# 
# 7. Do the limits (alarm/security) and desired voltage make sense? (especially alarm and sec up)
# 
# => yes
# 
# 8. Do the formulae for g_up and g_low make sense?
# 
# => They do
# 
# 9. Do the formula for d_up and d_low make sense?
# 
# => NO. 
# 
# => Get rid of the if else statements and the 0 limits in the code. Stick to the logic presented in the paper
# 
# => Consider column 7 (Vm) for a random simulation that has been solved (ACPF). By hand, calculate SI for said Vm as per the SI formula , ignore d(p,l) and g(p,l). Should give you an idea of how the SI value shapes up (less, equal or greater than 0 or 1) in general
# 
# => Show this calculation to Dr. Bai to get his thoughts, as well as the one done by Abhijith which he shared with you on teams. 
# 
# => Check the paper that has been referenced for the SI formula to understand the formula better.
# 
# 
# 10. How to calculate d(p,l) and g(p,l)?
# 
# => not necessary

# In[283]:


#N/A


import multiprocessing

for i in [[(1,1001),(1001,2001),(2001,3001),(3001,4001),(4001,5001)]]:
    
    if __name__ == "__main__":
        
        p1 = multiprocessing.Process(target=mcarlo(i[0][0],i[0][1]))
        p2 = multiprocessing.Process(target=mcarlo(i[1][0],i[1][1]))
        p3 = multiprocessing.Process(target=mcarlo(i[2][0],i[2][1]))
        p4 = multiprocessing.Process(target=mcarlo(i[3][0],i[3][1]))
        p5 = multiprocessing.Process(target=mcarlo(i[4][0],i[3][1]))
        #p5 = multiprocessing.Process(target=mcarlo(i[4][0],i[4][1]))
        #p6 = multiprocessing.Process(target=mcarlo(i[5][0],i[5][1]))
        #p7 = multiprocessing.Process(target=mcarlo(i[6][0],i[6][1]))
        #p8 = multiprocessing.Process(target=mcarlo(i[7][0],i[7][1]))
    
 
        p1.start()
        p2.start()
        p3.start()
        p4.start()
        p5.start()
        #p5.start()
        #p6.start()
        #p7.start()
        #p8.start()
        
        p1.join()
        p2.join()
        p3.join()
        p4.join()
        p5.join()
        #p5.join()
        #p6.join()
        #p7.join()
        #p8.join()


# In[98]:


values = {}
for i in data:
    values[f"{i}"] = {'baseMVA':data[i][0]['baseMVA'],'bus_voltages':pd.DataFrame(data[i][0]['bus'])[7],'line':{'line_flow_abs':pd.DataFrame(data[i][0]['branch'])[13].abs(),'line_flow_alarm':(pd.DataFrame(data[i][0]['branch'])[5])*0.9,'line_flow_sec':pd.DataFrame(data[i][0]['branch'])[5]}}


# In[101]:


bus_limits = {'desired_voltage':1,'alarm_low':0.93, 'alarm_up':1.07,'sec_low':0.90,'sec_up':1.10}


# In[102]:


n=1

sec_ind = {}

g_up_bus = (bus_limits['sec_up']-bus_limits['alarm_up'])/bus_limits['desired_voltage']
g_low_bus = (bus_limits['alarm_low']-bus_limits['sec_low'])/bus_limits['desired_voltage']


 
for sim in values:
    
    sum_bus = 0
    sum_branch = 0
    
    for i_vol in values[sim]['bus_voltages'] :
        
        if i_vol > bus_limits['alarm_up']:
            d_up_bus = (i_vol - bus_limits['alarm_up'])/bus_limits['desired_voltage']
        else:
            d_up_bus = 0
    
        if i_vol < bus_limits['alarm_low']:
            d_low_bus = (bus_limits['alarm_low'] - i_vol)/bus_limits['desired_voltage']
        else:
            d_low_bus = 0
        
        sum_1 = (d_up_bus/g_up_bus)**(2*n)
        sum_2 = (d_low_bus/g_low_bus)**(2*n)
    
        sum_bus += sum_1 + sum_2
    
    line = pd.DataFrame(values[sim]['line'])
    
    for i in line.index:
        
        if line.loc[i,'line_flow_abs'] > line.loc[i,'line_flow_alarm']:
            d_branch = (line.loc[i,'line_flow_abs'] - line.loc[i,'line_flow_alarm'])/values[sim]['baseMVA']
        else:
            d_branch = 0
        
        g_branch = (line.loc[i,'line_flow_sec'] - line.loc[i,'line_flow_alarm'])/values[sim]['baseMVA']
    
        sum_branch += (d_branch/g_branch)**(2*n)
    
    
    SI = (sum_bus + sum_branch)**(1/(2*n))
    
    if SI == 0:
        sec_ind[sim] = [values[sim],0]
    elif 0 < SI <= 1:
        sec_ind[sim] = [values[sim],1]
    else:
        sec_ind[sim] = [values[sim],2]


# In[103]:


sec_ind


# In[104]:


sum_0 = 0
sum_1 = 0
sum_2 = 0
for i in sec_ind:
    if sec_ind[i][1]==0:
        sum_0 += 1
    elif sec_ind[i][1] == 1:
        sum_1 += 1
    else:
        sum_2 += 1
        
total = sum_0 + sum_1 + sum_2
        
print('secure:',sum_0)
print('alarm:',sum_1)
print('insecure:',sum_2)
print('total:',total)


# In[105]:


final = {}

for i in data:
    
    baseMVA = data[i][0]['baseMVA']
    
    
    bus = np.copy(data[i][0]['bus'])
    bus = pd.DataFrame(bus)
    bus[0] = bus[0] - 1
    
    
    branch = np.copy(data[i][0]['branch'])
    branch = pd.DataFrame(branch)
    branch[0] = branch[0] - 1
    branch[1] = branch[1] - 1
    
    adm_mat,b,c = makeYbus(baseMVA,bus.to_numpy(),branch.to_numpy()) 
    
    B = np.diag(adm_mat.toarray())
    
    B_final = np.array([])
    
    for j in B:
        B_final = np.append(B_final,j.imag)
    
       
    final[i] = np.array([np.array(bus[2]),np.array(bus[3]),B_final])


# In[106]:


for i in final:
    for j in sec_ind:
        if i == j:
            final[i] = [final[i],sec_ind[j][1]]


# In[398]:


import json
class NumpyEncoder(json.JSONEncoder):
    """ Special json encoder for numpy types """
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)



with open(f'/Users/ishti/Downloads/case9[tot={total},sec={sum_0},alrm={sum_1},insec={sum_2}].txt','w') as data: 
      data.write(json.dumps(final,cls=NumpyEncoder))

