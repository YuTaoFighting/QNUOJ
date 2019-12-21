import json
import logging
from json.decoder import JSONDecodeError
from uuid import uuid4

import dramatiq
import os

from judge.utils import run, get_result_id
from submission.models import Submission, JudgeStatus
from judge.utils import DRAMATIQ_WORKER_ARGS

logger = logging.getLogger('log')

TESTCASE_ROOT_DIR = '/onlinejudge/data/testcases/'
USER_CODE_ROOT_DIR = '/onlinejudge/data/usercodes/'
SPECIAL_CHECKE_CODE_ROOT_DIR = '/onlinejudge/data/checkcode/'

FILE_TYPE_EXT = {
    'C': '.c',
    'C++': '.cpp',
    'Java': '.java',
    'Python2': '.py',
    'Python3': '.3.py'
}


def push_judge_result(submition_id, final_result):
    submission = Submission.objects.get(pk=submition_id)
    submission.score = final_result['score']
    flag = submission.result == 2
    is_rejudge = submission.result < 9
    submission.result = get_result_id(final_result['result'])
    if submission.result == 2 and not flag:
        submission.problem.add_ac_total()
    elif submission.result != 2 and flag and is_rejudge:
        submission.problem.subject_ac_total()
    submission.use_time_ms = final_result['time']
    submission.use_memory_bytes = final_result['memory']
    submission.point = json.dumps(final_result['point'])
    submission.save()


# def get_pending_submissions():
#     pending_submissions = Submission.objects.filter(result=JudgeStatus.QUEUING)
#     for submission in pending_submissions:
#         judge.send(submission.id)


@dramatiq.actor(**DRAMATIQ_WORKER_ARGS(max_retries=3))
def judge(submission_id):
    submission = Submission.objects.get(pk=submission_id)
    if submission.result >= 9:
        submission.problem.add_submit_total()
    if not os.path.exists(USER_CODE_ROOT_DIR):
        os.makedirs(USER_CODE_ROOT_DIR)
    submition_id = submission.id
    problem_id = submission.problem_id
    source_code = submission.code
    language = submission.language
    time_limit = submission.problem.time_limit
    memory_limit = submission.problem.memory_limit
    is_spj = submission.problem.is_spj

    source_code_filename = USER_CODE_ROOT_DIR + str(uuid4()) + FILE_TYPE_EXT[language]
    with open(source_code_filename, 'w') as f:
        f.write(source_code)
    try:
        testcase_conf_name = TESTCASE_ROOT_DIR + str(problem_id) + '/list.conf'
        testcase_base = TESTCASE_ROOT_DIR + str(problem_id) + '/'
        cmd = ['ljudge', '--max-cpu-time', str(time_limit // 1000), '--max-memory', str(memory_limit) + 'm', '-u',
               source_code_filename]
        score_point = []
        with open(testcase_conf_name, 'r') as f:
            for line in f.readlines():
                line = line.strip().split(' ')
                if len(line) != 0:
                    cmd.append('-i ' + testcase_base + line[0] + '.in')
                    cmd.append('-o ' + testcase_base + line[0] + '.out')
                    score_point.append(int(line[1]))
        if is_spj:
            cmd.append('-c ' + SPECIAL_CHECKE_CODE_ROOT_DIR + str(problem_id) + '.cpp')

        # if language in ['Python3', 'Python2']:
        cmd.append('--keep-stderr')
        # print(cmd)
        # print(score_point)

        final_result = {
            'score': 100,
            'time': 0,
            'msg': '',
            'memory': 0,
            'point': []
        }
        status, output = run(' '.join(cmd))
        logger.info(str(output))
        # print(output)
        # os.remove(source_code_filename)
        if status != 0:
            final_result['result'] = 'Judge Error'
            final_result['score'] = 0
            # update database here
            push_judge_result(submition_id, final_result)
            return None
        else:
            if output['compilation']['success']:
                final_result['msg'] = output['compilation']['log']
                index = 0
                final_status = 'Accepted'
                final_time = 0
                final_memory = 0
                final_score = 0
                final_msg = ''
                for testcase in output['testcases']:
                    point = {
                        'time': 0,
                        'memory': 0,
                        'score': 0,
                        'result': 'Accepted'
                    }
                    if 'memory' in testcase:
                        final_memory = max(testcase['memory'], final_memory)
                        point['memory'] = testcase['memory']
                    if 'time' in testcase:
                        final_time = max(int(testcase['time'] * 1000), final_time)
                        point['time'] = int(testcase['time'] * 1000)
                    if 'stderr' in testcase and testcase['stderr'] != '':
                        final_msg = testcase['stderr']
                        point['msg'] = testcase['stderr']
                    if testcase['result'] == 'TIME_LIMIT_EXCEEDED':
                        if final_status == 'Accepted':
                            final_status = 'Time Limit Exceeded'
                        point['result'] = 'Time Limit Exceeded'
                        final_time = max(time_limit + 1, final_time)
                        point['time'] = max(time_limit + 1, point['time'])
                    elif testcase['result'] == 'NON_ZERO_EXIT_CODE' and language in ['Python3',
                                                                                     'Python2'] and index == 0:
                        final_status = 'Compile Error'
                        final_msg = testcase['stderr']
                        final_time = 0
                        final_memory = 0
                        break
                    elif testcase['result'] == 'MEMORY_LIMIT_EXCEEDED':
                        if final_status == 'Accepted':
                            final_status = 'Memory Limit Exceeded'
                        point['result'] = 'Memory Limit Exceeded'
                        point['memory'] = max(memory_limit + 1, point['memory'])
                        final_memory = max(memory_limit + 1, final_memory)
                    elif testcase['result'] == 'NON_ZERO_EXIT_CODE':
                        if final_status == 'Accepted':
                            final_status = 'Runtime Error'
                        point['result'] = 'Runtime Error'
                    elif testcase['result'] == 'OUTPUT_LIMIT_EXCEEDED':
                        if final_status == 'Accepted':
                            final_status = 'Output Limit Exceeded'
                        point['result'] = 'Output Limit Exceeded'
                    elif testcase['result'] == 'FLOAT_POINT_EXCEPTION':
                        if final_status == 'Accepted':
                            final_status = 'Output Limit Exceeded'
                        point['result'] = 'Output Limit Exceeded'
                    elif testcase['result'] == 'SEGMENTATION_FAULT':
                        if final_status == 'Accepted':
                            final_status = 'Runtime Error'
                        point['result'] = 'Runtime Error'
                    elif testcase['result'] == 'RUNTIME_ERROR':
                        if final_status == 'Accepted':
                            final_status = 'Runtime Error'
                        point['result'] = 'Runtime Error'
                    elif testcase['result'] == 'INTERNAL_ERROR':
                        if final_status == 'Accepted':
                            final_status = 'Runtime Error'
                        point['result'] = 'Runtime Error'
                    elif testcase['result'] == 'PRESENTATION_ERROR':
                        if final_status == 'Accepted':
                            final_status = 'Presentation Error'
                        point['result'] = 'Presentation Error'
                    elif testcase['result'] == 'WRONG_ANSWER':
                        final_status = 'Wrong Answer'
                        point['result'] = final_status
                    elif testcase['result'] == 'ACCEPTED':
                        final_score += score_point[index]
                        point['score'] = score_point[index]
                    index += 1
                    final_result['point'].append(point)
                final_result['result'] = final_status
                final_result['memory'] = final_memory
                final_result['time'] = final_time
                final_result['score'] = final_score
                final_result['msg'] = final_msg
                # update database here
                push_judge_result(submition_id, final_result)
                return None
            else:
                final_result['result'] = 'Compile Error'
                final_result['msg'] = output['compilation']['log']
                final_result['score'] = 0
                # update database here
                push_judge_result(submition_id, final_result)
                return None
    # except Exception as e:
    #     logger.error(e)
    #     os.remove(source_code_filename)
    except JSONDecodeError as e:
        logger.error(e)
        raise JSONDecodeError
    finally:
        os.remove(source_code_filename)
