#!/usr/bin/env python

import argparse
import logging
import os
import sys

import sqlalchemy

from .metrics import bunny_containerstats
from .metrics import bunny_postprocess

def get_param(args, param_name):
    if vars(args)[param_name] == None:
        return None
    else:
        return vars(args)[param_name]
    return

def setup_logging(tool_name, args, task_uuid):
    logging.basicConfig(
        filename=os.path.join(task_uuid + '_' + tool_name + '.log'),
        level=args.level,
        filemode='w',
        format='%(asctime)s %(levelname)s %(message)s',
        datefmt='%Y-%m-%d_%H:%M:%S_%Z',
    )
    logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
    logger = logging.getLogger(__name__)
    return logger

def main():
    parser = argparse.ArgumentParser('bunny metrics docker tool')

    # Logging flags.
    parser.add_argument('-d', '--debug',
        action = 'store_const',
        const = logging.DEBUG,
        dest = 'level',
        help = 'Enable debug logging.',
    )
    parser.set_defaults(level = logging.INFO)

    # Required flags.
    parser.add_argument('--metric_name',
                        required = True,
                        help = 'picard tool'
    )
    parser.add_argument('--metric_path',
                        required = False
    )
    parser.add_argument('--task_uuid',
                        required = True,
                        help = 'uuid string',
    )
    parser.add_argument('--slurm_job_id',
                        required = True
    )
    
    # setup required parameters
    args = parser.parse_args()
    metric_name = args.metric_name
    metric_path = args.metric_path
    task_uuid = args.task_uuid
    slurm_job_id = args.slurm_job_id

    logger = setup_logging('bunny_' + metric_name, args, task_uuid)

    sqlite_name = task_uuid + '.db'
    engine_path = 'sqlite:///' + sqlite_name
    engine = sqlalchemy.create_engine(engine_path, isolation_level='SERIALIZABLE')

    if metric_name == 'containerstats':
        bam = get_param(args, 'bam')
        bunny_containerstats.run(metric_name, metric_path, slurm_job_id, task_uuid, engine, logger)
    elif metric_name == 'postprocess':
        bam = get_param(args, 'bam')
        bunny_postprocess.run(metric_name, metric_path, slurm_job_id, task_uuid, engine, logger)
    else:
        sys.exit('No recognized tool was selected')
        
    return

if __name__ == '__main__':
    main()
