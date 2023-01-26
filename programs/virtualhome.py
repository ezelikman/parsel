# return a list of strings that represents an action plan to put a mug on the stall and bread on the desk.
def task_plan():
    return put_object_on("mug", "stall") + put_object_on("bread", "desk")

# return a list of strings that represents an action plan to put an object in a place.
def put_object_on(object, place):
    return [
        'find ' + object,
        'grab ' + object,
        'walk to ' + place,
        'put ' + object + ' on ' + place
    ]


from execute_virtual_home import test_script;assert test_script(task_plan())

from execute_virtual_home import test_script;assert test_script(put_object_on("mug", "stall"))
