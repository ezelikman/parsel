# For all numbers from n to 2359, run the apps_eval.py script with -p corresponding to the number
# pkill -f Python.app after running this script to kill all the python processes spawned by this script

for i in {3032..5000}
do
    # time out after 45 minutes
    # python apps_eval.py -p $i
    timeout 2700 python apps_eval.py -p $i
    # clean up
    pkill -f Python.app
    pkill -f python
done