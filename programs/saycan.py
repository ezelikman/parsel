# return a list of strings that represnts an action plan to put mug on stall and bread on desk.
def task_plan():
    return put_object_on('mug', 'stall') + put_object_on('bread', 'desk')

# return a list of strings that represnts an action plan to put an object in the place.
def put_object_on(object, place):
    return ["grab " + object, "walk to " + place, "put " + object + " on " + place]



