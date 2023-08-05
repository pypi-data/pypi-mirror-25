from datetime import datetime
import json
import re

import pandas as pd


import sqlalchemy
metric_path = 'runtime_nohup.out'
metric_name = 'containerstats'
slurm_job_id = 16444
task_uuid = "00104-e1230-1f2305-12234gh"
sqlite_name = task_uuid + '.db'
engine_path = 'sqlite:///' + sqlite_name
engine = sqlalchemy.create_engine(engine_path, isolation_level='SERIALIZABLE')

def run(metric_name, metric_path, slurm_job_id, task_uuid, engine, logger):
    metric_regex = re.compile(r'^\[(.*)\] \[(.*)\] (.*)$')
    job_regex = re.compile(r'^RUNTIME-METRICS-containerStats=(.*)$')
    containerstats_regex = re.compile(r'^(.*) for containerId=(.*)$')
    data_dict_list = list()
    jobid_containerid_dict = dict()
    with open(metric_path, 'r') as f_open:
        for line in f_open:
            data_dict = dict()
            metric_match = metric_regex.search(line)
            if (metric_match and len(metric_match.groups()) == 3):
                metric_datetime = metric_match.group(1)
                metric_log_type = metric_match.group(2)
                metric_value = metric_match.group(3)
                runtime_datetime = datetime.strptime(metric_datetime, '%Y-%m-%d %H:%M:%S.%f')
                runtime_match = job_regex.search(metric_value)
                if runtime_match is not None:
                    runtime_metric_str = runtime_match.group(1)
                    containerstats_match = containerstats_regex.search(runtime_metric_str)
                    containerstats_str = containerstats_match.group(1)
                    containerId = containerstats_match.group(2)
                    if containerstats_str == 'null':
                        data_dict['containerId'] = containerId
                        data_dict['log_datetime'] = runtime_datetime.isoformat()
                        data_dict['slurmId'] = slurm_job_id
                        data_dict['taskId'] = task_uuid
                        data_dict['read'] = None
                        data_dict['network'] = None
                        data_dict['networks'] = None
                        data_dict['memory_stats'] = None
                        data_dict['blkio_stats'] = None
                        data_dict['cpu_stats'] = None
                        alreadyContainer = False
                    else:
                        data = json.loads(containerstats_str)
                        data_dict['containerId'] = containerId
                        data_dict['log_datetime'] = runtime_datetime.isoformat()
                        data_dict['slurmId'] = slurm_job_id
                        data_dict['taskId'] = task_uuid
                        data_dict['blkio_stats'] = str(data['blkio_stats'])
                        data_dict['cpu_stats'] = str(data['cpu_stats'])
                        data_dict['memory_stats'] = str(data['memory_stats'])
                        data_dict['network'] = str(data['network'])
                        data_dict['networks'] = str(data['networks'])
                        data_dict['read'] = data['read']
                    alreadyContainer = False
                    for stored_data_dict in data_dict_list:
                        if stored_data_dict['containerId'] == containerId:
                            logger.info('already: %s' % containerId)
                            alreadyContainer = True
                    if not alreadyContainer:
                        data_dict_list.append(data_dict)
    table_name = 'runtime_bunny_' + metric_name
    df = pd.DataFrame(data_dict_list)
    df.to_sql(table_name, engine, if_exists='append')
    return
