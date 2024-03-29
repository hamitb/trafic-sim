from django.shortcuts import render, redirect
from django.http import JsonResponse
from util.server import rpc_service, rpc_call, is_sim_active_for, get_map_state_for, delete_controller_for
import json

# Create your views here.
def index(request):
    if not request.session.session_key:
        request.session.save()

    rpc_service(request.session.session_key, quick_start=False)

    return render(request, 'sim_app/index.html')

def settings(request, component):
    session = request.session
    
    form = request.POST
    print(form)
    session_id = session.session_key
    req = {
            'method': '',
            'args': [],
            'kwargs': {}
        }
    notification = "executed {} with parameters: {}"

    if component == 'load_map':
        map_name = form['map_name']
        
        req['method'] = 'load_map'
        req['args'] = [map_name]
    elif component == 'save_map':
        map_name = form['map_name']

        req['method'] = 'save_map'
        req['args'] = [map_name]
    elif component == 'add_node':
        node_id = form['node_id']
        node_x = form['node_x']
        node_y = form['node_y']

        req['method'] = 'add_node'
        req['args'] = [int(node_x), int(node_y), int(node_id)]
    elif component == 'delete_node':
        node_id = form['node_id']

        req['method'] = 'delete_node'
        req['args'] = [int(node_id)]
    elif component == 'add_edge':
        edge_from = form['edge_from']
        edge_to = form['edge_to']
        edge_lanes = form['edge_lanes']
        edge_bidir = True if 'edge_bidir' in form else False

        req['method'] = 'add_road'
        req['args'] = [int(edge_from), int(edge_to), int(edge_lanes), bool(edge_bidir)]
    elif component == 'add_gen':
        gen_source = list(map(lambda x:int(x), form['gen_source'].split(',')))
        gen_target = list(map(lambda x:int(x), form['gen_target'].split(',')))
        period = int(form['gen_period'])
        count = int(form['gen_count'])

        req['method'] = 'add_generator'
        req['args'] = [gen_source, gen_target, period, count]
    elif component == 'debug_level':
        debug_level = form.getlist('debug_level')

        req['method'] = 'set_debug_level'
        req['args'] = [debug_level]
    elif component == 'restart_sim':
        quickstart = 'quickstart' in form
        delete_controller_for(session_id)
        rpc_service(request.session.session_key, quick_start=quickstart)
        map_state = get_map_state_for(session_id)
        notification = "Simulation restarted"
        return JsonResponse({"result": "success", "notification": notification, "map_state": map_state});

    if(req['method']):
        rpc_json = json.dumps(req)
        try:
            rpc_call(rpc_json, session_id)
            notification = notification.format(req['method'], req['args'])
            map_state = get_map_state_for(session_id)
            return JsonResponse({"result": "success", "notification": notification, "map_state": map_state})
        except Exception as err:
            print(err)
            notification = "Some bad things happened"
            return JsonResponse({"result": "danger", "notification": notification});

def simulation(request):
    session_id = request.session.session_key
    notification = ""
    result = "success"

    if 'tick' in request.POST:
        req = {
            'method': 'tick',
            'args': [],
            'kwargs': {}
        }
        rpc_json = json.dumps(req)
        rpc_call(rpc_json, session_id)
        notification = "Tick!"
        result = "success"
    elif 'start-sim' in request.POST:
        if not is_sim_active_for(session_id):
            req = {
                'method': 'start_simulation',
                'args': [int(request.POST['tick_period'])],
                'kwargs': {}
            }
            rpc_json = json.dumps(req)
            rpc_call(rpc_json, session_id)

            notification = "Simulation started!"
            result = "success"
    elif 'terminate-sim' in request.POST:
        req = {
            'method': 'terminate_simulation',
            'args': [],
            'kwargs': {}
        }
        rpc_json = json.dumps(req)
        rpc_call(rpc_json, session_id)
        result = "success"
        notification = "Terminated"

    resp = {
        "result": result,
        "notification": notification,
    }
    
    return JsonResponse(resp)

def map_state(request):
    session_id = request.session.session_key;

    map_state = get_map_state_for(session_id);

    return JsonResponse({'map_state': map_state});