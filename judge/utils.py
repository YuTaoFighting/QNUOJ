import subprocess
import json

from submission.models import JudgeStatus


def run(cmd):
    status, output = subprocess.getstatusoutput(cmd)
    return status, json.loads(output)


def DRAMATIQ_WORKER_ARGS(time_limit=3600_000, max_retries=0, max_age=7200_000):
    return {"max_retries": max_retries, "time_limit": time_limit, "max_age": max_age}


def get_result_id(result):
    if result == 'Accepted':
        return JudgeStatus.ACCEPTED
    elif result == 'Time Limit Exceeded':
        return JudgeStatus.TIME_LIMIT_EXCEEDED
    elif result == 'Compile Error':
        return JudgeStatus.COMPILE_ERROR
    elif result == 'Wrong Answer':
        return JudgeStatus.WRONG_ANSWER
    elif result == 'Presentation Error':
        return JudgeStatus.PRESENTATION_ERROR
    elif result == 'Memory Limit Exceeded':
        return JudgeStatus.MEMORY_LIMIT_EXCEEDED
    elif result == 'Output Limit Exceeded':
        return JudgeStatus.OUTPUT_LIMIT_EXCEEDED
    elif result == 'Runtime Error':
        return JudgeStatus.RUNTIME_ERROR
    elif result == 'Judge Error':
        return JudgeStatus.SYSTEM_ERROR
