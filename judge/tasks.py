from __future__ import absolute_import

import subprocess, time, os

from billiard import current_process
from celery import shared_task
from celery.task import chord, group
from django.core.cache import cache
from django.db import transaction

from judge.models import Test, TestResult, Solution, UserProblemData,\
                        UserStatts

def get_sol_loc(solution):
    solutionRoot = 'judge/solutions/'
    return solutionRoot + str(solution.pk) + '-run'
def get_box_id():
    return current_process().index
def get_box_loc():
    return '/tmp/box/' + str(get_box_id()) + '/box/'
def get_sandbox():
    return 'judge/isolate'

def compile_solution(solution):
    sourceName = str(solution.pk) + 'source.cpp'
    sourceFile = open(sourceName, 'w')
    sourceFile.write(solution.source)
    sourceFile.close()

    compileArgs = ['g++', '-O2', '--std=c++11',
                    '-o', get_sol_loc(solution), sourceName]

    returnCode = subprocess.call(compileArgs)
    os.remove(sourceName)

    return (returnCode == 0)

def setup_box(solution, test):
    sandbox = get_sandbox()
    boxId = get_box_id()
    subprocess.call([sandbox, '-b', str(boxId), '--init'])
    subprocess.call(['cp', get_sol_loc(solution), 
                    get_box_loc() + 'solution'])

    inFilePath = get_box_loc() + 'std.in'
    inFile = open(inFilePath, 'w')
    inFile.write(test.stdin)
    inFile.close()

def run_solution(test):
    sandbox = get_sandbox()
    boxId = get_box_id()
    time_limit = str(test.time_limit)

    args = [sandbox, '-i', 'std.in', '-o', 'std.out', '-b', str(boxId), 
            '-t', time_limit, '-x', time_limit, '-m', 
            str(test.mem_limit * 1024), '--run', 'solution']

    proc = subprocess.Popen(args, stdout = subprocess.PIPE, 
                            stderr = subprocess.PIPE)
    while proc.poll():
        time.sleep(0.01)

    out, err = proc.communicate()
    return err.decode('utf-8')

def check_output(test):
    outFilePath = get_box_loc() + 'std.out'
    outFile = open(outFilePath, 'r')
    curOut = outFile.read()
    curOut = curOut.replace('\n', '\r\n')
    outFile.close()

    corOut = test.stdout

    return curOut == corOut 

@shared_task
def test_solution(solution):
    if not compile_solution(solution):
        solution.grader_message = 'Compilation error'
        solution.save()
        return
    
    solution.grader_message = 'Testing'
    solution.save()

    taskList = list()
    tests = solution.problem.test_set.all()
    for t in tests:
        curSubTask = run_test.si(solution, t)
        taskList.append(curSubTask)

    print(get_box_id())

    res = chord(group(taskList), save_result.s(solution))
    res.apply_async()

    print('sheduled for testing')

@shared_task
def run_test(solution, test):
    print('seting sandbox')
    boxId = get_box_id()
    
    setup_box(solution, test)
    print('testing')
    sandbox_msg = run_solution(test)
    print('grading')

    score = 0
    time = 'N\\A'

    if sandbox_msg[:2] == 'OK' :
        msg = 'wrong awnser'
        time = sandbox_msg[4:9]
        
        if check_output(test):
            msg = 'correct'
            score = test.score

        sandbox_msg = msg
    
    result = TestResult(message = sandbox_msg, score = score,
                        solution = solution, test = test, exec_time = time)
    print('test passed')
    return result

@shared_task
def save_result(result, solution):
    print('saving results')

    with transaction.atomic():
        for taskRes in result:
            taskRes.save()

        solution.grader_message = 'Tested'
        solution.update_score()
        solution.save()

    try:
        os.remove(get_sol_loc(solution))
    except FileNotFoundError:
        pass

    print('results saved')

@shared_task
def retest_problem(problem):
    solutions = problem.solution_set.all()

    # set_autocommit(False)
    with transaction.atomic():
        UPdata = UserProblemData.objects.filter(problem = problem)

        for data in UPdata:
            if data.maxScore == problem.maxScore:
                statts = UserStatts.objects.get(user = data.user)
                statts.solvedProblems -= 1
                statts.save()

            data.maxScore = 0
            data.save()

        for sol in solutions:
            sol.testresult_set.all().delete()
            sol.score = 0
            sol.grader_message = 'retesting'
            sol.save()

            test_solution.delay(sol)
