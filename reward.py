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
               return math.floor((level2*2)/3)
       return math.floor(level2/3)
# dictionary holding all possible states
V = [0]*40

for i in range(0,40):
        V[i]=[0]*72


# takes in current state and change in eBatt; gives you next state
def action(eBatt, time, delta_e):
        if(home[time]<=0):
                return (eBatt,time)
        new_ebatt = eBatt + delta_e
        time = time + 1
        s_prime = (new_ebatt, time)
        day[eBatt][time]=new_ebatt
        return s_prime
        

# returns reward at given state and action 
def reward(state,action):
        reward =0
        curr_eBatt, curr_time = state
        next_eBatt= action
        #if overcharging occur, negative reward
        if(next_eBatt > eBatt_capacity):
                return -100000
                # no charging occurs, no reward
        if(curr_eBatt >= next_eBatt):
                return 1
        
        if(next_eBatt-trip[curr_time]<0):
                return curr_eBatt-trip[curr_time]
        else:
                return -10000
        # day is split up into 72(24*3) sections or 20 minute intervals so divide back into just hours
        curr_hours = curr_time / 3
        next_hours = (curr_time+1) / 3
        
        for time in range(math.floor(curr_hours), math.floor(next_hours)):
               # off_peak_price = 0.016334
               # on_peak_price = 0.043560
                off_peak_price = 16
                on_peak_price = 44
                best_price = abs(curr_hours-next_hours) * off_peak_price
                actual_price = 0 

                # 1pm to 8pm is onpeak, any other time is off peak; not taking into account weekends or holidays
                if(time >= 13 & time <= 20):
                        actual_price += on_peak_price
                else:
                        actual_price += off_peak_price
                reward = math.floor(abs(best_price - actual_price))
        
        return reward
         

# fills state dictionary with associated reward 
def value_function():
        max_error=2
        while(max_error>1):
                max_error = 0
                #terminal
                for eBatt in range(0, eBatt_capacity):
                        for time in range(0, 24*3):
            
                                value = V[eBatt][time]
                                #print (value)
                                best = -100
                                #V[eBatt][time]=abs(best)
                                for delta_e in range(0, max_delta_e(value) + 1):
                                        v_eBatt, v_time = action(eBatt, time, delta_e)
                                        if(v_eBatt>39):
                                                break
                                        if(v_time>71):
                                                break
                                        best = max(best,reward((eBatt, time), delta_e)+ V[v_eBatt][v_time])
                                        V[eBatt][time]=abs(best)
                                        max_error = max(max_error, abs(value-best))
                print (max_error)

home =data1.storecharge()
#print(home)
trip=data1.storeUse()
day =[10]*40
for i in range(0,40):
        day[i]=[trip[i]*-1]*72
        


value_function()   
#V[1][1]= action(1,1,1))   
#print(V)

   



