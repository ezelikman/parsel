import glob
from sys import platform
import sys
from PIL import Image
import matplotlib.pyplot as plt
from tqdm import tqdm
import os
import virtualhome
from unity_simulator.comm_unity import UnityCommunication
from unity_simulator import utils_viz
import json
from virtualhome.simulation.evolving_graph.check_programs import ScriptParseException
from virtualhome.simulation.evolving_graph.scripts import read_script_from_string
from virtualhome.simulation.evolving_graph.execution import ScriptExecutor
from virtualhome.simulation.evolving_graph.environment import EnvironmentGraph
from virtualhome.simulation.evolving_graph import utils

def add_node(graph, n):
    graph['nodes'].append(n)

def add_edge(graph, fr_id, rel, to_id):
    graph['edges'].append({'from_id': fr_id, 'relation_type': rel, 'to_id': to_id})


def find_nodes(graph, **kwargs):
    if len(kwargs) == 0:
        return None
    else:
        k, v = next(iter(kwargs.items()))
        return [n for n in graph['nodes'] if n[k] == v]

def setup():
    mode = 'auto' # auto / manual
    if mode == 'auto':
        if platform == 'darwin':
            exec_file = 'macos_exec.v2.3.0*'
        else:
            exec_file = 'linux_exec*.x86_64'
        file_names = glob.glob(exec_file)
        if len(file_names) > 0:
            file_name = file_names[0]
            comm = UnityCommunication(file_name=file_name, port="8082", x_display="0")
        else:
            print("Error: executable path not found.")
    else:
        comm = UnityCommunication()
    return comm

def init_graph(comm, graph):

    sofa = find_nodes(graph, class_name='sofa')[-2]

    # add_node(graph, {'class_name': 'cat', 
    #                 'category': 'Animals', 
    #                 'id': 1000, 
    #                 'properties': [], 
    #                 'states': []})
    # add_edge(graph, 1000, 'ON', sofa['id'])

    add_node(graph, {'class_name': 'bread', 
                    'id': 1000, 
                    'properties': [], 
                    'states': []})

    floor = find_nodes(graph, class_name='floor')[1]

    add_node(graph, {'class_name': 'table', 
                    'id': 1001, 
                    'properties': [], 
                    'states': []}) ## somehow this just refuses to be added ...

    add_edge(graph, 1000, 'ON', sofa['id'])
    add_edge(graph, 1001, 'ON', floor['id'])

    # add_node(graph, {'class_name': 'desk', 
    #                 'id': 1003, 
    #                 'properties': [], 
    #                 'states': []})
    # add_edge(graph, 1003, 'ON', floor['id'])

    # add_node(graph, {'class_name': 'donut', 
    #                 'id': 1002, 
    #                 'properties': ['GRABBABLE',], 
    #                 'states': []})

    # add_edge(graph, 1002, 'ON', sofa['id'])
    


    success, message = comm.expand_scene(graph)
    assert success
    comm.add_character('chars/Female2', initial_room='kitchen')
    # s, g = comm.environment_graph()

    # script = ['<char0> [Walk] <sofa> ({})'.format(sofa['id']),
    #       '<char0> [Find] <donut> ({})'.format(get_obj_id("donut", g))]

    # success, message = comm.render_script(script=script,
    #                             processing_time_limit=60,
    #                             find_solution=False,
    #                             image_width=320,
    #                             image_height=240,  
    #                             skip_animation=True,
    #                             recording=False,
    #                             save_pose_data=False,
    #                             file_name_prefix='relax')
    # print(success, message)

    s, g = comm.environment_graph()
    return g

import re

NL_ACTIONS = [['close'], ['cut'], ['drink'], ['drop'], ['eat'], ['find'], ['grab'], ['greet'], ['lie on'], ['look at'], ['move'], ['open'], ['plug in'], ['plug out'], ['point at'], ['pour', 'into'], ['pull'], ['push'], ['put', 'on'], ['put', 'in'], ['put back'], ['take off'], ['put on'], ['read'], ["release"], ['rinse'], ['run to'], ['scrub'], ['sit on'], ['sleep'], ['squeeze'], ['stand up'], ['switch off'], ['switch on'], ['touch'], ['turn to'], ['type on'], ['wake up'], ['walk to'], ['wash'], ['watch'], ['wipe']]
M_ACTIONS = ['[CLOSE]', '[CUT]', '[DRINK]', '[DROP]', '[EAT]', '[FIND]', '[GRAB]', '[GREET]', '[LIE]', '[LOOKAT]', '[MOVE]', '[OPEN]', '[PLUGIN]', '[PLUGOUT]', '[POINTAT]', '[POUR]', '[PULL]', '[PUSH]', '[PUTBACK]', '[PUTIN]', '[PUTOBJBACK]', '[PUTOFF]', '[PUTON]', '[READ]', '[RELEASE]', '[RINSE]', '[RUN]', '[SCRUB]', '[SIT]', '[SLEEP]', '[SQUEEZE]', '[STANDUP]', '[SWITCHOFF]', '[SWITCHON]', '[TOUCH]', '[TURNTO]', '[TYPE]', '[WAKEUP]', '[WALK]', '[WASH]', '[WATCH]', '[WIPE]']

def get_obj_id(obj, graph):
    print(obj)
    # import pdb;pdb.set_trace()
    return [node['id'] for node in graph['nodes'] if node['class_name'] == obj][0]

def formalize_script(gen_script, graph):
    # with open("language-planner/src/available_actions.json") as f:
    #     available_actions = json.load(f)
    # pass
    script = []
    
    for l in gen_script:
        # for obj in objects:
        #     if obj in l:
        #         l = l.replace(obj, "<{}> ({})".format(obj, objects[obj]))
        for acts_idx, acts in enumerate(NL_ACTIONS):
            if all([a in l for a in acts]):
                for a in acts:
                    l = l.replace(a + " ", "|")
                objects = l.split("|")[1:]
                l = M_ACTIONS[acts_idx] + " " + " ".join(["<{}> ({})".format( obj.strip(), get_obj_id(obj.strip(), graph)) for obj in objects])
                break
        script.append(l)
    return script


def check_executability(string, graph_dict):
    able_to_be_parsed = False
    able_to_be_executed = False

    try:
        script = read_script_from_string(string)
        able_to_be_parsed = True
    except ScriptParseException:
        return able_to_be_parsed, able_to_be_executed, None

    graph = EnvironmentGraph(graph_dict)
    name_equivalence = utils.load_name_equivalence()
    executor = ScriptExecutor(graph, name_equivalence)

    # executable, final_state, _ = executor.execute(script)
    try:
        # executable, final_state, _ = executor.execute(script) sometimes errors out for bad reasons??
        state_enum = executor.find_solutions(script)
        executable = state_enum is not None
    except AttributeError:
        print("Attribute error")
        print("Program:")
        programs = string.split(', ')
        for p in programs:
            print(p)
        return able_to_be_parsed, able_to_be_executed, None
    except:
        print("Unexpected error:", sys.exc_info()[0])
        print("Program:")
        programs = string.split(', ')
        for p in programs:
            print(p)
        return able_to_be_parsed, able_to_be_executed, None

    if executable:
        able_to_be_executed = True
        return able_to_be_parsed, True, state_enum
    else:
        print(executor.info.get_error_string())
        return able_to_be_parsed, able_to_be_executed, None

def test_script(gen_script, strict = False):    
    cache_file = "virtual_home_test_graph.json"
    if os.path.exists(cache_file) and not strict:
        with open(cache_file, 'r') as f:
            graph = json.load(f)
    else:
        comm = setup()
        comm.reset(4)
        success, graph = comm.environment_graph()

        graph = init_graph(comm, graph)
        with open(cache_file, 'w') as f:
            json.dump(graph, f)
    

    print(gen_script)
    # gen_script = ['grab cup', 'put cup on table', 'grab bread', 'put bread on desk']
    script = formalize_script(gen_script, graph)

    print(script)
    ### check soft execution via executor.find_solutions; mainly check whether stuff are possible to parse and execute in any way
    able_to_be_parsed, able_to_be_executed, final_state = check_executability( ", ".join(script), graph)
    
    
    print(able_to_be_parsed, able_to_be_executed)
    # assert able_to_be_parsed
    # assert able_to_be_executed
    if not (able_to_be_parsed and able_to_be_executed):
        return "not executable"
    if strict:
        ### execution check; too expensive for on the fly
        script = ["<char0> " + s for s in script]
        print(script)
        success, message = comm.render_script(script=script,
                                    processing_time_limit=60,
                                    find_solution=False,
                                    image_width=320,
                                    image_height=240,  
                                    skip_animation=True,
                                    recording=False,
                                    save_pose_data=False,
                                    file_name_prefix='relax')
        print(message)
        if not success:
            return "not executable"
    return "executable"

if __name__ == "__main__":
    
    
    from programs.saycan import task_plan
    gen_script = task_plan()
    # gen_script = ['grab mug']
    gen_script = gen_script
    test_script(gen_script, strict = True)            

   