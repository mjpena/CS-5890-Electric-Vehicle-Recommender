

def action(eBatt, time, delta_e):
        #something here


    

def reward(eBatt, time, delta_e):
        EV_batt_max = 0
        max_error = 0
        for time in range(0, 24*3):
            for eBatt in range(0, EV_batt_max):
                    V = V[(ebatt, time)]
                    best = -10000000000
                    for delta_e in range(0, max_delta_e + 1):
                            best = max(best, reward(eBatt, time, delta_e)+ V[action(eBatt, time, delta_e)])
                            max_error = max(max_error, abs(V-best))



