import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class SimpleTimer:
    def __init__(self, operation='', request_data={}):
        self.operation = operation
        self.steps = [['start', datetime.now()]]
        self.finished = False
        self.sub_timers = []
        self.request = request_data
        self.processing_properties = {}
        logger.info('Running %s: %s', operation, json.dumps(request_data))

    def set_processing_property(self, key, value):
        self.processing_properties[key] = value

    def add_step_done(self, step):
        logger.info(step)
        if not self.finished:
            self.steps.append([step, datetime.now()])
        else:
            logger.warning("The profiler is already finished.")

    def finish(self, last_event='finish'):
        if not self.finished:
            self.steps.append([last_event, datetime.now()])
        else:
            logger.warning("You cannot finish a profiler twice.")

        start_time = self.steps[0][1]
        end_time = self.steps[len(self.steps) - 1][1]

        logger.info("%s started at %s, took total %f", self.operation, start_time, (end_time - start_time).total_seconds())
        logger.info("%s: %s", self.operation, json.dumps(self.request))

        timer_dict = dict(total_seconds=(end_time - start_time).total_seconds())

        last_time = start_time
        for i in range(1, len(self.steps)):
            step = self.steps[i]
            if step[0] == 'finish':
                continue
            logger.info("\t%s at %s, took %f", step[0], step[1], (step[1] - last_time).total_seconds())
            last_time = step[1]
            timer_dict[step[0]] = (step[1] - last_time).total_seconds()
