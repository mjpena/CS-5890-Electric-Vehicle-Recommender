# peak schedule: https://www.rockymountainpower.net/ya/po/otou.html
# prices per kwh: https://www.rockymountainpower.net/content/dam/rocky_mountain_power/doc/About_Us/Rates_and_Regulation/Utah/Approved_Tariffs/Rate_Schedules/Residential_Service_Optional_Time_of_Day_Rider_Experimental.pdf
# ontario data: https://www.powerstream.ca/customers/rates-support-programs/time-of-use-pricing.html
# nissan leaf specs: https://www.evbox.com/electric-cars/nissan/nissan-leaf-2018

#need eBatt_max value
eBatt_max = 2

# dictionary holding all possible combinations of battery charge at an hour
"""V = []
for time in range(0, 2):
        V[time] = V.get(time, {})
        for eBatt in range(0, eBatt_max):
                V[time][eBatt] =  0
                print(V[time, eBatt])
   """ 

# takes in current state and change in eBatt; gives you next state
def action(eBatt, time, delta_e):
        new_ebatt = eBatt + delta_e
        time = time + 1
        s_prime = (new_ebatt, time)
        return s_prime
        

# returns 
def reward(state, action):
        eBatt_capacity = 40
        curr_eBatt, curr_time = state
        next_eBatt, next_time = action

        # no charging occurs, no reward
        if(curr_eBatt >= next_eBatt):
                return 0

        # day is split up into 72(24*3) sections or 20 minute intervals so divide back into just hours
        curr_hours = curr_time / 3
        next_hours = next_time /3
        # hours_charging = abs(curr_hours - next_hours)
        price = 0.0

        for time in range(curr_hours, next_hours):          
                # 1pm to 8pm is onpeak, any other time is off peak; not taking into account weekends or holidays
                if(time >= 13 & time <= 20):
                        price = price + 0.043560
                else:
                                price = price + 0.016334
                
        #if overcharging occurs
        if(next_eBatt > eBatt_capacity):
                return -100


        


# possible reward for making it through the day
"""def V(eBatt, time, delta_e):
        EV_batt_max = 0
        max_error = 0
        for time in range(0, 24*3):
            for eBatt in range(0, EV_batt_max):
                    V = V[(eBatt, time)]
                    best = -10000000000
                    for delta_e in range(0, max_delta_e + 1):
                            best = max(best, reward(eBatt, time, delta_e)+ V[action(eBatt, time, delta_e)])
                            max_error = max(max_error, abs(V-best))

"""

