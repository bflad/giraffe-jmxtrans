#!/usr/bin/env python

import pprint
import re
import shutil
import os
import yaml

with open('giraffe-jmxtrans.yaml') as configuration_file:
    configuration = yaml.safe_load(configuration_file)
configuration_file.closed

giraffe_dashboard_file = os.path.join(configuration['giraffe']['dashboard'], 'dashboards.js')
graphite_collectd_dir = os.path.join(configuration['graphite']['storage'], configuration['graphite']['prefix'])

def metric_server_target(metric_path):
    return metric_target(os.path.dirname(metric_path))

def metric_target(metric_path):
    return metric_path.replace(configuration['graphite']['storage'] + '/', '').replace('/', '.').replace('.wsp', '')

def metric_type(metric_filename):
    return re.sub('^.*(-|_)', '', metric_filename).replace('.wsp', '')

def connector(metric_dir):
    server_target = metric_server_target(metric_dir)
    metrics = []
    print '\tFound collectd connector metrics'
    for c in os.listdir(metric_dir):
        metrics.append(
            {
                'alias': c + ' connector',
                'targets': [
                    '.'.join([server_target, 'connectors', c, 'currentThreadCount']),
                    '.'.join([server_target, 'connectors', c, 'currentThreadsBusy'])
                ],
                'renderer': 'line',
                'scheme': [
                    '#00ff00',
                    '#ff0000'
                ]
            }
        )
    return metrics

def gc(metric_dir):
    server_target = metric_server_target(metric_dir)
    metrics = []
    print '\tFound collectd gc metrics'
    for c in os.listdir(metric_dir):
        metrics.append(
            {
                'alias': c,
                'targets': [
                    'derivative(' + '.'.join([server_target, 'gc', c, 'CollectionCount']) + ')',
                    'derivative(' + '.'.join([server_target, 'gc', c, 'CollectionTime']) + ')'
                ],
                'renderer': 'line',
                'scheme': [
                    '#00ff00',
                    '#ff0000'
                ]
            }
        )
    return metrics

def memory(metric_dir):
    server_target = metric_server_target(metric_dir)
    print '\tFound collectd memory metric'
    return [
        {
            'alias': 'Heap Memory',
            'targets': [
                '.'.join([server_target, 'memory', 'HeapMemoryUsage_committed']),
                '.'.join([server_target, 'memory', 'HeapMemoryUsage_init']),
                '.'.join([server_target, 'memory', 'HeapMemoryUsage_max']),
                '.'.join([server_target, 'memory', 'HeapMemoryUsage_used'])
            ],
            'renderer': 'line',
            'scheme': [
                '#ffff00',
                '#0000ff',
                '#00ffff',
                '#00ff00'
            ]
        },
        {
            'alias': 'Non-Heap Memory',
            'targets': [
                '.'.join([server_target, 'memory', 'NonHeapMemoryUsage_committed']),
                '.'.join([server_target, 'memory', 'NonHeapMemoryUsage_init']),
                '.'.join([server_target, 'memory', 'NonHeapMemoryUsage_max']),
                '.'.join([server_target, 'memory', 'NonHeapMemoryUsage_used'])
            ],
            'renderer': 'line',
            'scheme': [
                '#ffff00',
                '#0000ff',
                '#00ffff',
                '#00ff00'
            ]
        }
    ]

def memorypool(metric_dir):
    server_target = metric_server_target(metric_dir)
    metrics = []
    print '\tFound collectd memorypool metrics'
    for p in os.listdir(metric_dir):
        metrics.append(
            {
                'alias': p + ' Usage',
                'targets': [
                    '.'.join([server_target, 'memorypool', p, 'Usage_committed']),
                    '.'.join([server_target, 'memorypool', p, 'Usage_init']),
                    '.'.join([server_target, 'memorypool', p, 'Usage_max']),
                    '.'.join([server_target, 'memorypool', p, 'Usage_used'])
                ],
                'renderer': 'line',
                'scheme': [
                    '#ffff00',
                    '#0000ff',
                    '#00ffff',
                    '#00ff00'
                ]
            }
        )
    return metrics

def request(metric_dir):
    server_target = metric_server_target(metric_dir)
    metrics = []
    print '\tFound collectd requests metrics'
    for r in os.listdir(metric_dir):
        metrics.append(
            {
                'alias': r + ' bytes',
                'targets': [
                    '.'.join([server_target, 'requests', r, 'bytesReceived']),
                    '.'.join([server_target, 'requests', r, 'bytesSent'])
                ],
                'renderer': 'line',
                'scheme': [
                    '#00ff00',
                    '#ff0000'
                ]
            }
        )
        metrics.append(
            {
                'alias': r + ' requests',
                'targets': [
                    'derivative(' + '.'.join([server_target, 'requests', r, 'requestCount']) + ')',
                    'derivative(' + '.'.join([server_target, 'requests', r, 'errorCount']) + ')'
                ],
                'renderer': 'line',
                'scheme': [
                    '#00ff00',
                    '#ff0000'
                ]
            }
        )
    return metrics

def threads(metric_dir):
    server_target = metric_server_target(metric_dir)
    print '\tFound collectd threads metric'
    return [
        {
            'alias': 'Threads',
            'targets': [
                '.'.join([server_target, 'threads', 'DaemonThreadCount']),
                '.'.join([server_target, 'threads', 'ThreadCount'])
            ],
            'renderer': 'line',
            'scheme': [
                '#ff0000',
                '#00ff00'
            ]
        }
    ]

dashboards = []
for server in sorted(os.listdir(graphite_collectd_dir)):
    print server
    server_metrics = []
    server_dir = os.path.join(graphite_collectd_dir, server)
    for metric in sorted(os.listdir(server_dir)):
        #print metric
        metric_dir = os.path.join(server_dir, metric)
        if metric == 'connectors':
            server_metrics = server_metrics + connector(metric_dir)
        elif metric == 'gc':
            server_metrics = server_metrics + gc(metric_dir)
        elif metric == 'memory':
            server_metrics = server_metrics + memory(metric_dir)
        elif metric == 'memorypool':
            server_metrics = server_metrics + memorypool(metric_dir)
        elif metric == 'requests':
            server_metrics = server_metrics + request(metric_dir)
        elif metric == 'threads':
            server_metrics = server_metrics + threads(metric_dir)
    dashboards.append({
        "name": server,
        "refresh": configuration['giraffe']['refresh'],
        "metrics": server_metrics
    })

with open(giraffe_dashboard_file + '.tmp', 'w') as f:
    f.write('var graphite_url = "' + configuration['graphite']['url'] + '";\n')
    f.write('var dashboards = \n')
    pp = pprint.PrettyPrinter(indent=2, stream=f)
    pp.pprint(dashboards)
    f.write(';\n')
f.closed
shutil.move(giraffe_dashboard_file + '.tmp', giraffe_dashboard_file)
