# _*_ coding: utf-8 _*_
__author__ = 'kim dong-hun'
from random import randrange
from flask import current_app
from flask_restplus import Resource
from .apis.v1_.rtm import RtmDto
from redis.exceptions import DataError

rtm_a = RtmDto.api
rtm_m = RtmDto.rtm


@rtm_a.route('/')
class AsyncRtm(Resource):
    @rtm_a.doc('create a New Slack RTM')
    @rtm_a.expect(rtm_m)
    @rtm_a.marshal_with(rtm_m, code=201)
    def post(self):
        """
        RTM 수신.
        1.rtm 수신
        2.message 구문 분석
        3.if 구문내 수행 명령 존재 시, async task 요청
        :return:
        """
        import os
        import sys
        sys.path.append(os.getenv('OPBOT_HOME')+"/chatbot")
        import manage

        res_msg = {
            "channel": "opbot",
            "ok": True,
            "message": "success"
        }

        current_app.logger.debug("rtm_a(%r)=<%r>" % (type(rtm_a), rtm_a))
        current_app.logger.debug("rtm_m(%r)=<%r>" % (type(rtm_m), rtm_m))
        current_app.logger.debug("payload(%r)=<%r>" % (type(rtm_a.payload),
                                                       rtm_a.payload))

        rtm_msg = rtm_a.payload

        command_list = current_app.bot.parse_command(rtm_msg['message'])

        recommend_tasks = None

        if len(command_list) <= 0:
            hello_messages = [
                "네, 안녕하세요.",
                "Hi.",
                "안녕하세요."
            ]
            err_messages = [
                "죄송해요. 다시 입력해주세요.",
                "죄송해요. 알수 없는 명령입니다.",
                "뭔 말이여?",
                "Sorry, Please try again.",
                "죄송해요. 이해를 못 했습니다."
            ]
            hello = current_app.bot.say_hello(rtm_msg['message'])

            if len(hello) <= 0:
                current_app.bot.put_broadcast(channel=rtm_msg['channel'],
                                              message=err_messages[randrange(len(err_messages))])
            else:
                current_app.bot.put_broadcast(channel=rtm_msg['channel'],
                                              message=hello_messages[randrange(len(hello_messages))])
        else:
            in_channel_id = current_app.bot.get_in_channel_info(rtm_msg['channel'], 'C')

        for task in command_list:
            current_app.logger.debug("task=<%r>" % task)

            if task == '!조치!':
                # context 상태 변경.
                # todo: code refactoring 필요.
                try:
                    current_app.bot.set_context_s(rtm_msg['channel'],
                                                  current_app.bot.get_current_subjects(rtm_msg['channel']))
                except DataError:
                    msg = "처리할 이벤트가 없습니다."
                    current_app.bot.put_broadcast(channel=rtm_msg['channel'], message=msg)
                    return res_msg, 201
                # 조치 Task
                # 3.분석 task 추천 정보 조회
                anal_tasks = current_app.bot.task_recommend(rtm_msg['channel'])
                current_app.bot.put_chat(channel=rtm_msg['channel'], message=None, tasks=anal_tasks)
            elif task == '!분석!':
                # context 상태 변경.
                # todo: code refactoring 필요.
                try:
                    current_app.bot.set_context_a(rtm_msg['channel'],
                                                  current_app.bot.get_current_subjects(rtm_msg['channel']))
                except DataError:
                    msg = "처리할 이벤트가 없습니다."
                    current_app.bot.put_broadcast(channel=rtm_msg['channel'], message=msg)
                    return res_msg, 201
                anal_tasks = current_app.bot.task_recommend(rtm_msg['channel'])
                current_app.bot.put_chat(channel=rtm_msg['channel'], message=None, tasks=anal_tasks)
            elif task == '!종료!':
                # context 상태 변경.
                # context 삭제.
                # todo: code refactoring 필요.
                try:
                    current_app.bot.del_context(rtm_msg['channel'],
                                                current_app.bot.get_current_subjects(rtm_msg['channel']))
                except DataError:
                    msg = "처리할 이벤트가 없습니다."
                    current_app.bot.put_broadcast(channel=rtm_msg['channel'],
                                                  message=msg)
                    return res_msg, 201

                # 잔여 context 가 있는지 확인
                event_uid, _ = current_app.bot.get_context_one(rtm_msg['channel'])

                current_app.logger.debug("event_uid=<%r>" % event_uid)

                if event_uid is None:
                    # subject 삭제.
                    current_app.bot.del_current_subjects(rtm_msg['channel'])
                    # 종료 처리
                    msg = "상황 종료되었습니다. 감사합니다."
                    # 전체 채널에 공지
                    out_channels = current_app.bot.channel_read(in_channel_id)

                    if len(out_channels) > 0:
                        for channel_info in out_channels:
                            if channel_info[0] == 'B':
                                current_app.bot.put_end(channel=channel_info[1], message=msg)
                            elif channel_info[0] == 'C':
                                current_app.bot.put_end(channel=channel_info[1], message=msg)
                            else:
                                pass
                    break
                else:
                    # 다음 event 처리
                    current_app.bot.set_context_a(rtm_msg['channel'], event_uid)
                    current_app.bot.set_current_subjects(rtm_msg['channel'], event_uid)

                    # 분석 task 추천 정보 조회
                    message = current_app.bot.get_event_message(event_uid)
                    anal_tasks = current_app.bot.task_recommend(rtm_msg['channel'])
                    current_app.bot.put_chat(channel=rtm_msg['channel'], message=message, tasks=anal_tasks)
            elif task == '!mytask!' or task == '!mt!':
                # delete redis data
                current_app.bot.del_c_mytasks(rtm_msg['user'])
                current_app.bot.del_c_user_name(rtm_msg['user'])
                user_name, m_tasks = current_app.bot.get_mytasks(rtm_msg['user'])
                # set redis data
                current_app.bot.set_c_mytasks(rtm_msg['user'], m_tasks)
                current_app.bot.set_c_user_name(rtm_msg['user'], user_name)
                current_app.bot.put_chat4m(channel=rtm_msg['channel'], user=user_name, message=None, tasks=m_tasks)
            elif task.startswith('!mytask,', 0, len('!mytask,')) is True or\
                    task.startswith('!mt,', 0, len('!mt,')) is True:
                task = task.replace('!', '')
                params = task.split(',')

                if len(params) > 1 and params[1] != '':
                    dot_parse = params[1].split('.')

                    if len(dot_parse) == 1:
                        if dot_parse[0].isdigit():
                            current_app.bot.update_c_mytasks(rtm_msg['user'], int(dot_parse[0])-1)
                        else:
                            task_index = current_app.bot.get_c_mytasks_index_by_name(rtm_msg['user'], dot_parse[0])
                            current_app.bot.update_c_mytasks(rtm_msg['user'], task_index)
                        run_index = current_app.bot.get_c_run_mytasks(rtm_msg['user'])
                        run_id, run_nm, run_st = current_app.bot.get_c_mytasks_by_id(rtm_msg['user'], run_index)
                        user_name = current_app.bot.get_c_user_name(rtm_msg['user'])
                        message = "{}님 '{}'를 수행하시겠습니까? (!y! or !n!)".format(user_name, run_nm)
                        current_app.bot.put_broadcast(channel=rtm_msg['channel'], message=message)
                    else:
                        if dot_parse[0].isdigit():
                            current_app.bot.update_c_mytasks(rtm_msg['user'], int(dot_parse[0])-1)
                            run_index = current_app.bot.get_c_run_mytasks(rtm_msg['user'])
                            run_id, run_nm, run_st = current_app.bot.get_c_mytasks_by_id(rtm_msg['user'], run_index)
                            user_name = current_app.bot.get_c_user_name(rtm_msg['user'])
                            message = "{}님 '{}'를 수행하시겠습니까? (!y! or !n!)".format(user_name, run_nm)
                            current_app.bot.put_broadcast(channel=rtm_msg['channel'], message=message)
                        else:
                            user_name, m_tasks = current_app.bot.get_mytasks(rtm_msg['user'])
                            message = "{}님 my task 수행 인자가 올바르지 않습니다.".format(user_name)
                            current_app.bot.put_chat4m(channel=rtm_msg['channel'], user=user_name,
                                                       message=message, tasks=m_tasks)
                else:
                    user_name, m_tasks = current_app.bot.get_mytasks(rtm_msg['user'])
                    message = "{}님 my task 수행 인자가 없습니다.".format(user_name)
                    current_app.bot.put_chat4m(channel=rtm_msg['channel'], user=user_name,
                                               message=message, tasks=m_tasks)
            elif task == '!grouptask!' or task == '!gt!':
                # delete redis data
                current_app.bot.del_c_grouptasks(rtm_msg['user'])
                current_app.bot.del_c_user_name(rtm_msg['user'])
                user_name, g_tasks = current_app.bot.get_grouptasks(rtm_msg['user'])
                # set redis data
                current_app.bot.set_c_grouptasks(rtm_msg['user'], g_tasks)
                current_app.bot.set_c_user_name(rtm_msg['user'], user_name)
                current_app.bot.put_chat4g(channel=rtm_msg['channel'], user=user_name, message=None, tasks=g_tasks)
            elif task.startswith('!grouptask,', 0, len('!grouptask,')) is True or \
                    task.startswith('!gt,', 0, len('!gt,')) is True:
                task = task.replace('!', '')
                params = task.split(',')

                if len(params) > 1 and params[1] != '':
                    dot_parse = params[1].split('.')

                    if len(dot_parse) == 1:
                        if dot_parse[0].isdigit():
                            current_app.bot.update_c_grouptasks(rtm_msg['user'], int(dot_parse[0])-1)
                        else:
                            task_index = current_app.bot.get_c_grouptasks_index_by_name(rtm_msg['user'], dot_parse[0])
                            current_app.bot.update_c_grouptasks(rtm_msg['user'], task_index)
                        run_index = current_app.bot.get_c_run_grouptasks(rtm_msg['user'])
                        run_id, run_nm, run_st = current_app.bot.get_c_grouptasks_by_id(rtm_msg['user'], run_index)
                        user_name = current_app.bot.get_c_user_name(rtm_msg['user'])
                        message = "{}님 '{}'를 수행하시겠습니까? (!y! or !n!)".format(user_name, run_nm)
                        current_app.bot.put_broadcast(channel=rtm_msg['channel'], message=message)
                    else:
                        if dot_parse[0].isdigit():
                            current_app.bot.update_c_grouptasks(rtm_msg['user'], int(dot_parse[0])-1)
                            run_index = current_app.bot.get_c_run_grouptasks(rtm_msg['user'])
                            run_id, run_nm, run_st = current_app.bot.get_c_grouptasks_by_id(rtm_msg['user'], run_index)
                            user_name = current_app.bot.get_c_user_name(rtm_msg['user'])
                            message = "{}님 '{}'를 수행하시겠습니까? (!y! or !n!)".format(user_name, run_nm)
                            current_app.bot.put_broadcast(channel=rtm_msg['channel'], message=message)
                        else:
                            user_name, m_tasks = current_app.bot.get_grouptasks(rtm_msg['user'])
                            message = "{}님 group task 수행 인자가 올바르지 않습니다.".format(user_name)
                            current_app.bot.put_chat4m(channel=rtm_msg['channel'], user=user_name,
                                                       message=message, tasks=m_tasks)
                else:
                    user_name, m_tasks = current_app.bot.get_grouptasks(rtm_msg['user'])
                    message = "{}님 group task 수행 인자가 없습니다.".format(user_name)
                    current_app.bot.put_chat4m(channel=rtm_msg['channel'], user=user_name,
                                               message=message, tasks=m_tasks)
            elif task == '!yes!' or task == '!y!':
                user_name = current_app.bot.get_c_user_name(rtm_msg['user'])

                run_index = current_app.bot.get_c_run_mytasks(rtm_msg['user'])
                run_id, run_nm, run_st = current_app.bot.get_c_mytasks_by_id(rtm_msg['user'], run_index)

                group_run_index = current_app.bot.get_c_run_grouptasks(rtm_msg['user'])
                group_run_id, group_run_nm, group_run_st = current_app.bot.get_c_grouptasks_by_id(rtm_msg['user'],
                                                                                                  group_run_index)

                if run_id is None and group_run_id is None:
                    message = "{}님 수행할 Task가 없습니다.".format(user_name, run_nm)
                    current_app.bot.reset_c_run_mytasks(rtm_msg['user'])
                    current_app.bot.put_broadcast(channel=rtm_msg['channel'], message=message)
                else:
                    # Task 수행 비동기 처리.
                    if run_id is not None:
                        task_name, task_type = current_app.bot.get_task_info(run_id)
                        target_list = current_app.bot.get_target_list(run_id, rtm_msg['channel'])
                        contents = current_app.bot.get_playbook_contents(run_id)
                        result = manage.task_execute.delay(run_id, rtm_msg['channel'], task_name,
                                                           task_type, target_list, contents, exe_type=1)
                        result.wait()
                        current_app.bot.reset_c_run_mytasks(rtm_msg['user'])

                    if group_run_id is not None:
                        task_name, task_type = current_app.bot.get_task_info(group_run_id)
                        target_list = current_app.bot.get_target_list(group_run_id, rtm_msg['channel'])
                        contents = current_app.bot.get_playbook_contents(group_run_id)
                        result = manage.task_execute.delay(group_run_id, rtm_msg['channel'], task_name,
                                                           task_type, target_list, contents, exe_type=1)
                        result.wait()
                        current_app.bot.reset_c_run_grouptasks(rtm_msg['user'])

            elif task == '!no!' or task == '!n!':
                user_name = current_app.bot.get_c_user_name(rtm_msg['user'])

                run_index = current_app.bot.get_c_run_mytasks(rtm_msg['user'])
                run_id, run_nm, run_st = current_app.bot.get_c_mytasks_by_id(rtm_msg['user'], run_index)

                group_run_index = current_app.bot.get_c_run_grouptasks(rtm_msg['user'])
                group_run_id, group_run_nm, group_run_st = current_app.bot.get_c_mytasks_by_id(rtm_msg['user'],
                                                                                               group_run_index)

                if run_id is None and group_run_id is None:
                    message = "{}님 취소할 Task가 없습니다.".format(user_name)
                else:
                    message = "{}님 ".format(user_name)
                    if run_id is not None:
                        message += "'{}'".format(run_nm)
                    if group_run_id is not None:
                        message += "'{}'".format(group_run_nm)
                    message += " 미수행하겠습니다."
                current_app.bot.reset_c_run_mytasks(rtm_msg['user'])
                current_app.bot.put_broadcast(channel=rtm_msg['channel'], message=message)
            else:
                recommend_tasks = current_app.bot.task_recommend(rtm_msg['channel'])
                # current_app.logger.debug("recommend_tasks=<%r>" % recommend_tasks)
                task_id = current_app.bot.get_task_id(recommend_tasks, task)

                if task_id is None:
                    current_app.bot.put_broadcast(channel=rtm_msg['channel'],
                                                  message="죄송해요. 알수 없는 명령입니다.")
                else:
                    # Task 수행 비동기 처리.
                    task_name, task_type = current_app.bot.get_task_info(task_id)
                    target_list = current_app.bot.get_target_list(task_id, rtm_msg['channel'])
                    contents = current_app.bot.get_playbook_contents(task_id)
                    result = manage.task_execute.delay(task_id, rtm_msg['channel'], task_name,
                                                       task_type, target_list, contents)
                    result.wait()
                    # put collector, 비동기 처리.
                    ctx = current_app.bot.get_context(rtm_msg['channel'],
                                                      current_app.bot.get_current_subjects(rtm_msg['channel']))
                    c = manage.put_collector.delay(current_app.bot.get_current_subjects(rtm_msg['channel']),
                                                   task_id,
                                                   ctx)
                    c.wait()

        return res_msg, 201
