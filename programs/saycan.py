# return a list of strings that represnts an action plan to put mug on stall and bread on desk.
def task_plan():
    return put_object_on('mug', 'stall') + put_object_on('bread', 'desk')
# return a list of strings that represnts an action plan to put an object in the place.
def put_object_on(object, place):
    """
    :param object: the object to be put on the place
    :param place: the place to put the object on
    :return: a list of strings that represnts an action plan to put an object in the place
    """
    return ["grab " + object, "put " + object + " on " + place]


from execute_virtual_home import test_script;assert test_script(task_plan())

from execute_virtual_home import test_script;assert test_script(put_object_on("mug", "stall"))
