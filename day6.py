input  = """Time:        57     72     69     92
Distance:   291   1172   1176   2026"""

times_string, distances_string = input.split('\n')
times_string = times_string.split(':')[1]
distances_string = distances_string.split(':')[1]
time = int(times_string.replace(' ',''))
distance = int(distances_string.replace(' ',''))

print(time)
print(distance)

def check_if_we_won(press_time, target_distance):
    speed = press_time
    time_left = time-press_time
    distance_covered = speed*time_left
    if distance_covered > target_distance:
        return True
    return False

# find where we swap from not making it to making it by bisecting
last_fail = 0
first_success = int(time/2)

# let's just check we do have a success and a fail
if check_if_we_won(0, distance):
    print("Erm, expected to fail at 0?!?")
if not check_if_we_won(first_success, distance):
    print(f"Erm, expected to succeed at {first_success}")   

while(first_success-last_fail>1) :
    print(last_fail)
    print(first_success)
    next_try = int((first_success+last_fail)/2)
    if check_if_we_won(next_try, distance):
        first_success = next_try
    else:
        last_fail = next_try

num_wins = time - last_fail - last_fail - 1
print(num_wins)

       