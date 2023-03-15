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
import openai
import numpy as np
import torch
from sentence_transformers import SentenceTransformer
from sentence_transformers import util as st_utils
import json


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
    comm.add_character('chars/Female2', initial_room='kitchen')
    s, g = comm.environment_graph()
    return g

import re

NL_ACTIONS = [['close'], ['cut'], ['drink'], ['drop'], ['eat'], ['find'], ['grab'], ['greet'], ['lie on'], ['look at'], ['move'], ['open'], ['plug in'], ['plug out'], ['point at'], ['pour', 'into'], ['pull'], ['push'], ['put back'], ['take off'], ['put on'], ['put', 'on'], ['put', 'in'], ['read'], ["release"], ['rinse'], ['run to'], ['scrub'], ['sit on'], ['sleep'], ['squeeze'], ['stand up'], ['switch off'], ['switch on'], ['touch'], ['turn to'], ['type on'], ['wake up'], ['walk to'], ['wash'], ['watch'], ['wipe']]
M_ACTIONS = ['[CLOSE]', '[CUT]', '[DRINK]', '[DROP]', '[EAT]', '[FIND]', '[GRAB]', '[GREET]', '[LIE]', '[LOOKAT]', '[MOVE]', '[OPEN]', '[PLUGIN]', '[PLUGOUT]', '[POINTAT]', '[POUR]', '[PULL]', '[PUSH]', '[PUTOBJBACK]', '[PUTOFF]', '[PUTON]', '[PUTBACK]', '[PUTIN]', '[READ]', '[RELEASE]', '[RINSE]', '[RUN]', '[SCRUB]', '[SIT]', '[SLEEP]', '[SQUEEZE]', '[STANDUP]', '[SWITCHOFF]', '[SWITCHON]', '[TOUCH]', '[TURNTO]', '[TYPE]', '[WAKEUP]', '[WALK]', '[WASH]', '[WATCH]', '[WIPE]']

def get_obj_id(obj, graph):
    return 1

def formalize_script(gen_script, graph):
    script = []
    
    for l in gen_script:
        print(l)
        l = " " + l + " "
        has_action = False
        for acts_idx, acts in enumerate(NL_ACTIONS):
            if all([" " + a + " " in l for a in acts]):
                for a in acts:
                    l = l.replace(" " + a + " ", "|")
                objects = l.split("|")[1:]
                objects = list(filter(lambda x : len(x.strip()) > 0, objects ))
                l = M_ACTIONS[acts_idx] + " " + " ".join(["<{}> ({})".format( re.sub(r'[\W_]+','_', obj.lower().strip()), get_obj_id(re.sub(r'[\W_]+','_', obj.lower().strip()), graph)) for obj in objects])
                has_action = True
                break
        assert has_action
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

    try:
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
        return able_to_be_parsed, True, None
    else:
        print(executor.info.get_error_string())
        return able_to_be_parsed, able_to_be_executed, None

def test_script(gen_script, strict = False):    
    gen_script = list(filter(lambda x : len(x.strip()) > 0, gen_script ))
    cache_file = "virtual_home_test_graph_4.json"
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
    script = formalize_script(gen_script, graph)
    if len(script) == 0:
        return False

    print(script)
    ### check soft execution via executor.find_solutions; mainly check whether stuff are possible to parse and execute in any way
    able_to_be_parsed, able_to_be_executed, final_state = check_executability( ", ".join(script), graph)
    
    
    print(able_to_be_parsed, able_to_be_executed)
    # assert able_to_be_parsedå
    # assert able_to_be_executed
    if not (able_to_be_parsed and able_to_be_executed):
        return False
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
            return False
    return True

if __name__ == "__main__":
    
    from programs.saycan import task_plan
    gen_script = task_plan()
    test_script(gen_script, strict=False)

    # correct = 0
    # for i in range(88):
    #     gen_script = [ s.split(":")[1].lower().strip()  for s in  open(f"baseline_vh_generated/eval_{i}.txt").read().split("\n")[:-1]]
    #     try:
    #         # gen_script = ['grab mug']
    #         if test_script(gen_script, strict=False):
    #             correct +=1     
    #     except:
    #         continue
    # print("correct: ",correct)  

    # correct = 0
    # for i in range(88):
    #     try:
    #         plan = __import__(f'vh_generated.eval_test_{i}')
    #         correct +=1
    #     except:
    #         continue
    # print("correct: ",correct)

   