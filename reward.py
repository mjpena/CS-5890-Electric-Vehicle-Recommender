# peak schedule: https://www.rockymountainpower.net/ya/po/otou.html
# prices per kwh: https://www.rockymountainpower.net/content/dam/rocky_mountain_power/doc/About_Us/Rates_and_Regulation/Utah/Approved_Tariffs/Rate_Schedules/Residential_Service_Optional_Time_of_Day_Rider_Experimental.pdf
# ontario data: https://www.powerstream.ca/customers/rates-support-programs/time-of-use-pricing.html
# charging data: https://pushevs.com/2018/05/21/fast-charging-curves/
import math
import data1
# battery size and max charging rate of a nissan leaf
eBatt_capacity = 40
level1=4
level2=22
def max_delta_e(fullnes):
       if(fullnes/eBatt_capacity<.60):
               return math.floor((level1*2)/3)
       return math.floor(level1/3)
# dictionary holding all possible states
V = [0]*40

for i in range(0,40):
        V[i]=[0]*72


# takes in current state and change in eBatt; gives you next state
def action(eBatt, time, delta_e):
        new_ebatt = eBatt + delta_e
        time = time + 1
        s_prime = (new_ebatt, time)
        return s_prime
def calc(eBatt) :
        x=0
        #print (eBatt-trip[0])
        if(eBatt-trip[0]<=0):
                x= -300
        return x

def termReward(goTime):
        for eBatt in range(0,eBatt_capacity):
                for time in range(goTime,72):
                        x=calc(eBatt)
                        V[eBatt][time]=x
        #print(V)
# returns cost of energy at given time of day
tod_price = [0]*24
for i in range(0, len(tod_price)):
        if(i >= 13*3 and i<= 20*3):
                tod_price[i] = 0.043560
        else:
                tod_price[i] = 0.016334

# returns reward at given state and action 
def reward(state, action):
        eBatt, time = state
        delta_e = action
        # start_hour being when the entire trip starts?
        hour = int(1 + (time/3))
        price = tod_price[hour%24] * delta_e
        return price

         

# fills state dictionary with associated reward 
def value_function():
        max_error=2
        while(max_error>1):
                max_error = 0
                #terminal
                for eBatt in range(0, eBatt_capacity):
                        #t-1
                        for time in range(0, 24*3):
            
                                value = V[eBatt][time]
                                #print (value)
                                best = -100
                                
                                for delta_e in range(0, max_delta_e(value) + 1):
                                        v_eBatt, v_time = action(eBatt, time, delta_e)
                                        if(v_eBatt>39):
                                                break
                                        if(v_time>71):
                                                break
                                        
                                        best = max(best,reward((eBatt, time), delta_e)+ V[v_eBatt][v_time])
                                        
                                         #abs(best)
                                       # best = abs(best)
                                #print (value)
                                max_error =  max(max_error, abs(value-best))
                                V[eBatt][time]=best
                                print(max_error)
                

#home =data1.storecharge()
#print(home)
trip=data1.storeUse()
home = 18
        

termReward(18)
#print(V)
value_function()   
#V[1][1]= action(1,1,1))   
#print(V)




