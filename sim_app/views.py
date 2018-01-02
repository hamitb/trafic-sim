from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from util.server import rpc_service, rpc_call, set_last_notification, get_last_notification, session_exist_with, is_sim_active_for
import json

# Create your views here.
def index(request):
    context = {
        'session_id': request.session.session_key,
        'notification': request.session['notification'] if 'notification' in request.session else '',
    }
    rpc_service(request.session.session_key, quick_start=True)
    return render(request, 'sim_app/index.html', context)

def settings(request, component):
    session = request.session
    
    form = request.POST
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
    elif component == 'add_node':
        node_id = form['node_id']
        node_x = form['node_x']
        node_y = form['node_y']

        req['method'] = 'add_node'
        req['args'] = [int(node_x), int(node_y), int(node_id)]
    elif component == 'add_edge':
        edge_from = form['edge_from']
        edge_to = form['edge_to']
        edge_lanes = form['edge_lanes']
        edge_bidir = form['edge_bidir']

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
        pass

    if(req['method']):
        rpc_json = json.dumps(req)
        rpc_call(rpc_json, session_id)
        request.session['notification'] = notification.format(req['method'], req['args'])

    return HttpResponseRedirect(reverse('sim_app:index'))

def simulation(request):
    context = {}
    session_id = request.session.session_key
    
    if not session_exist_with(session_id):
        context['error_message'] = 'You should create a simulator first, go to settings page'
        return render(request, 'sim_app/simulation.html', context)
    
    if 'tick' in request.POST:
        req = {
            'method': 'tick',
            'args': [],
            'kwargs': {}
        }
        rpc_json = json.dumps(req)
        rpc_call(rpc_json, session_id)
    elif 'start_sim' in request.POST:
        if not is_sim_active_for(session_id):
            req = {
                'method': 'start_simulation',
                'args': [int(request.POST['tick_period'])],
                'kwargs': {}
            }
            rpc_json = json.dumps(req)
            rpc_call(rpc_json, session_id)

            set_last_notification(session_id, "Simulation started, refresh page to get notifications")
            last_notification = get_last_notification(session_id)
            return redirect('/simulation')
    elif 'terminate_sim' in request.POST:
        req = {
            'method': 'terminate_simulation',
            'args': [],
            'kwargs': {}
        }
        rpc_json = json.dumps(req)
        rpc_call(rpc_json, session_id)
        set_last_notification(session_id, "Simulation terminated")

    last_notification = get_last_notification(session_id)
    context['last_notification'] = last_notification
    
    return render(request, 'sim_app/simulation.html', context)