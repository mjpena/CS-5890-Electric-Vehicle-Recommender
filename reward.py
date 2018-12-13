# peak schedule: https://www.rockymountainpower.net/ya/po/otou.html
# prices per kwh: https://www.rockymountainpower.net/content/dam/rocky_mountain_power/doc/About_Us/Rates_and_Regulation/Utah/Approved_Tariffs/Rate_Schedules/Residential_Service_Optional_Time_of_Day_Rider_Experimental.pdf
# ontario data: https://www.powerstream.ca/customers/rates-support-programs/time-of-use-pricing.html
# charging data: https://pushevs.com/2018/05/21/fast-charging-curves/

import math
import data1
import matplotlib.pyplot as plt
# battery capacity in percentages
EBATT_CAPACITY = 25
# how much to multiply 24 hours by to get number of sections a day is split up into
TIME_FACTOR = 3
# number of sections a day is split up into
#TIME_SECTIONS = TIME_FACTOR * 24
dayCh=data1.storecharge()   
NIGHT_TIME_SECTIONS=(72-data1.findPrevTime(data1.storePrevCharge()))
TIME_SECTIONS =data1.findTime(data1.storecharge())+NIGHT_TIME_SECTIONS
level1=4
level2=22
start_time = 1


# returns 
def max_delta_e(fullnes):
       if(((fullnes*1.0))/(EBATT_CAPACITY*1.0) < .60):
               return math.floor((level1*2)/TIME_FACTOR)
       return math.floor((level1*1.0)/TIME_FACTOR)


# dictionary holding all possible states
V = [0]*EBATT_CAPACITY
for i in range(0, EBATT_CAPACITY):
        V[i]=[0]*TIME_SECTIONS


# takes in current state and change in eBatt; gives you next state
def action(eBatt, time, delta_e):
        new_ebatt = eBatt + delta_e
        time = time + 1
        s_prime = (new_ebatt, time)
        return s_prime

# 

        #print(V)


# returns cost of energy at given time of day
tod_price = [0]*72
for i in range(0, len(tod_price)):
        if(i >= 13 * TIME_FACTOR and i<=20*TIME_FACTOR): #20 * TIME_FACTOR):
                tod_price[i] = 0.043560
        else:
                tod_price[i] = 0.016334



# returns reward at given state and action 
def reward(state, action):
        
        eBatt, time = state
        delta_e = action
        if (time<=NIGHT_TIME_SECTIONS):
                time=time+(72-NIGHT_TIME_SECTIONS)
                #print("n")
        else:
                #print("d")
                time = time-NIGHT_TIME_SECTIONS
        hour = int(start_time + (time/3))
        price = tod_price[hour % 24] * delta_e
        price-=.001
        return price

         

# fills state array with associated reward 
def value_function():
        max_error = 2
        while(max_error):
                max_error = 0
                #terminal
                
                for time in range(0, TIME_SECTIONS - 1):
                        for eBatt in range(0, EBATT_CAPACITY-1):
                                value = V[eBatt][time]
                                #print (value)
                                best = 100
                                
                                for delta_e in range(0, max_delta_e(eBatt) + 1):
                                        v_eBatt, v_time = action(eBatt, time, delta_e)
                                        #if(v_eBatt > EBATT_CAPACITY - 1):
                                         #       break
                                        #if(v_time > TIME_SECTIONS - 1):
                                         #       break
                                        
                                        best = min(best, reward((eBatt, time), delta_e)+V[v_eBatt][v_time])
                                        
                                       # eBatt=v_eBatt 
                               # print (best)
                                V[eBatt][time]=best              
                                max_error =  max(max_error, abs(value-best))
                               # print (max_error)
                                
                
def calc(eBatt) :
        x=0
        if(eBatt-trip[0]<=15):
                x = .25
        return x

# 
def termReward(goTime,hTime):
        for eBatt in range(0,EBATT_CAPACITY):
                        x=calc(eBatt)
                        V[eBatt][TIME_SECTIONS-1]=x
       # print (V)
#home =data1.storecharge()
#print(home)
trip=data1.storeUse()
home = 18


termReward(18,18*3) 
value_function() 

print(V[10])

plt.imshow(V, interpolation="nearest",origin='lower')

plt.colorbar()
plt.ylabel('battery charged')
plt.xlabel('Time in twenty minute intervals'+str(NIGHT_TIME_SECTIONS)+' is midnight')
plt.show()
'''
plt.bar(V,V[], align='center')
plt.show

    #plt.xticks(y_pos, objects)
plt.title('Estimated possible charging time per day')

plt.show()
'''
