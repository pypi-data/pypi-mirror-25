from datetime import datetime
import json
import re

import pandas as pd

def run(metric_name, metric_path, slurm_job_id, task_uuid, engine, logger):
    metric_regex = re.compile(r'^\[(.*)\] \[(.*)\] (.*)$')
    job_regex = re.compile(r'(.*)=({.*)')
    job_container_regex = re.compile(r'^(.*) with containerId=(.*)$')
    postprocess_dict_list = list()
    jobid_containerid_dict = dict()
    with open(metric_path, 'r') as f_open:
        for line in f_open:
            postprocess_dict = dict()
            metric_match = metric_regex.search(line)
            if (metric_match and len(metric_match.groups()) == 3):
                metric_datetime = metric_match.group(1)
                metric_log_type = metric_match.group(2)
                metric_value = metric_match.group(3)
                runtime_datetime = datetime.strptime(metric_datetime, '%Y-%m-%d %H:%M:%S.%f')
                runtime_match = job_regex.search(metric_value)
                runtime_metric_type = runtime_match.group(1)
                runtime_metric_jsonstr = runtime_match.group(2)
                if runtime_metric_type == 'RUNTIME-METRICS-containerStats':
                    data_postprocess = json.loads(runtime_metric_jsonstr)
                    postprocess_dict['app'] = data_postprocess['app']
                    postprocess_dict['jobId'] = data_postprocess['id']
                    postprocess_dict['inputs'] = str(data_postprocess['inputs'])
                    postprocess_dict['name'] = data_postprocess['name']
                    postprocess_dict['outputs'] = str(data_postprocess['outputs'])
                    postprocess_dict['parentId'] = data_postprocess['parentId']
                    postprocess_dict['rootId'] = data_postprocess['rootId']
                    postprocess_dict['status'] = data_postprocess['status']
                    postprocess_dict['slurmId'] = slurm_job_id
                    postprocess_dict['taskId'] = task_uuid
                    postprocess_dict_list.append(postprocess_dict)
                if runtime_metric_type == 'RUNTIME-METRICS-started-job':
                    job_container_match = job_container_regex.search(runtime_metric_jsonstr)
                    job_jsonstr = job_container_match.group(1)
                    data_start = json.loads(job_jsonstr)
                    jobId = data_start['id']
                    containerId = job_container_match.group(2)
                    jobid_containerid_dict[jobId] = containerId
    for postprocess_dict in postprocess_dict_list:
        jobId = postprocess_dict['jobId']
        postprocess_dict['containerId'] = jobid_containerid_dict[jobId]
    table_name = 'runtime_bunny_' + metric_name
    df = pd.DataFrame(postprocess_dict_list)
    df.to_sql(table_name, engine, if_exists='append')
    return
