# For all numbers from n to 4000, run the apps_eval.py script with -p corresponding to the number
# pkill -f Python.app after running this script to kill all the python processes spawned by this script

# iterate through a shuffled list of numbers from 3054 to 4000, using 42 as the seed
# skip the first 2
# for i in $(shuf -i 3054-4000 -n 946 --random-source=shuffleseed)
for i in $(shuf -i 3054-4000 -n 946 --random-source=shuffleseed)
# for i in $(shuf -i 3054-4000 -n 946 --random-source=shuffleseed | tail -n +100)
# Iterate through the list [3001, 3012, 3013, 3014, 3016, 3018, 3023]
# for i in 3018 3023 3024 3028 3032 3033 3034 3036 3037 3039 3040 3041 3042 3043 3047 3158 3876 3107 3784 3621 3070 3113 3665 3629 3882
# for i in 3119 3833 3137 3698 3912 3149 3266 3273 3367 3878
do
    # time out after 45 minutes
    # python apps_eval.py -p $i
    # timeout 2700 python apps_eval.py -s -p $i
    # pkill -f apps_sample.sh; pkill -f ".py -s -p"
    timeout 2700 python apps_eval.py -p $i; pkill -f multiprocessing.spawn; pkill -f "apps_eval.py -p"
    # pkill -f apps_eval.sh; pkill -f multiprocessing.spawn; pkill -f ".py -p"
    # { timeout 2700 python apps_eval.py -p $i; pkill -f multiprocessing.spawn; pkill -f "apps_eval.py -p"; } &
done