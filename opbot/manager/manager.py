# _*_ coding: utf-8 _*_
__author__ = 'kim dong-hun'
import uuid
from app import create_app, db
from app.models import ChannelInfo
from app.models import TargetList
from app.models import TaskInfo, TaskPlaybook, TaskManagement
from app.models import UserInfo
from app.models import GroupInfo, GroupManagement

app, manager = create_app()


@manager.command
def seed():
    """
    init db data.
    :return:
    """
    moss = app.config['MOSS']

    print("Add seed data to the database.")
    ChannelInfo.query.delete()

    seed_data = ChannelInfo(in_channel_id='swing',
                            out_channel_type='B',
                            out_channel_id='#swing',
                            out_channel_name='SWING OPBOT')
    db.session.add(seed_data)

    seed_data = ChannelInfo(in_channel_id='swing',
                            out_channel_type='C',
                            out_channel_id='#opbot_swing',
                            out_channel_name='SWING OPBOT')
    db.session.add(seed_data)
    db.session.commit()

    TargetList.query.delete()

    print("(%d)[%s]" % (len(moss.enc('localhost')), moss.enc('localhost')))
    seed_data = TargetList(task_id='DB_상태_분석',
                           host='localhost',
                           port=22,
                           user='tester',
                           passwd=moss.enc('!tester56#'),
                           out_channel_id='#opbot_swing',
                           adapter_type=0)
    db.session.add(seed_data)

    seed_data = TargetList(task_id='EAI/MCG_상태_분석',
                           host='localhost',
                           port=22,
                           user='tester',
                           passwd=moss.enc('!tester56#'),
                           out_channel_id='#opbot_swing',
                           adapter_type=0)
    db.session.add(seed_data)

    seed_data = TargetList(task_id='시스템_상태_분석',
                           host='localhost',
                           port=22,
                           user='tester',
                           passwd=moss.enc('!tester56#'),
                           out_channel_id='#opbot_swing',
                           adapter_type=0)
    db.session.add(seed_data)

    seed_data = TargetList(task_id='TP_상태_분석',
                           host='localhost',
                           port=22,
                           user='tester',
                           passwd=moss.enc('!tester56#'),
                           out_channel_id='#opbot_swing',
                           adapter_type=0)
    db.session.add(seed_data)

    seed_data = TargetList(task_id='DB_Session_Lock_제거',
                           host='localhost',
                           port=22,
                           user='tester',
                           passwd=moss.enc('!tester56#'),
                           out_channel_id='#opbot_swing',
                           adapter_type=0)
    db.session.add(seed_data)

    seed_data = TargetList(task_id='EAI_Queue_Purge',
                           host='localhost',
                           port=22,
                           user='tester',
                           passwd=moss.enc('!tester56#'),
                           out_channel_id='#opbot_swing',
                           adapter_type=0)
    db.session.add(seed_data)

    seed_data = TargetList(task_id='TP_재기동',
                           host='localhost',
                           port=22,
                           user='tester',
                           passwd=moss.enc('!tester56#'),
                           out_channel_id='#opbot_swing',
                           adapter_type=0)
    db.session.add(seed_data)

    db.session.commit()

    TaskInfo.query.delete()

    seed_data = TaskInfo(task_id='t_41750ee0-6ffe-11ea-8634-d0abd5335702',
                         task_name='DB_상태_분석',
                         task_type=2,
                         owner_id='u_425690ee-6fff-11ea-8634-d0abd5335702',
                         action_type='A',
                         status_code=1,
                         create_time='20200327164920',
                         update_time='20200327164920',
                         audit_id='u_425690ee-6fff-11ea-8634-d0abd5335702')
    db.session.add(seed_data)

    seed_data = TaskInfo(task_id='t_e355d1c6-6fff-11ea-8634-d0abd5335702',
                         task_name='EAI/MCG_상태_분석',
                         task_type=2,
                         owner_id='u_425690ee-6fff-11ea-8634-d0abd5335702',
                         action_type='A',
                         status_code=1,
                         create_time='20200327164920',
                         update_time='20200327164920',
                         audit_id='u_425690ee-6fff-11ea-8634-d0abd5335702')
    db.session.add(seed_data)

    seed_data = TaskInfo(task_id='t_213ffe8a-7000-11ea-8634-d0abd5335702',
                         task_name='시스템_상태_분석',
                         task_type=2,
                         owner_id='u_425690ee-6fff-11ea-8634-d0abd5335702',
                         action_type='A',
                         status_code=1,
                         create_time='20200327164920',
                         update_time='20200327164920',
                         audit_id='u_425690ee-6fff-11ea-8634-d0abd5335702')
    db.session.add(seed_data)

    seed_data = TaskInfo(task_id='t_8ef98bda-7000-11ea-8634-d0abd5335702',
                         task_name='TP_상태_분석',
                         task_type=2,
                         owner_id='u_425690ee-6fff-11ea-8634-d0abd5335702',
                         action_type='A',
                         status_code=1,
                         create_time='20200327164920',
                         update_time='20200327164920',
                         audit_id='u_425690ee-6fff-11ea-8634-d0abd5335702')
    db.session.add(seed_data)

    seed_data = TaskInfo(task_id='t_cbe83f46-7000-11ea-8634-d0abd5335702',
                         task_name='DB_Session_Lock_제거',
                         task_type=2,
                         owner_id='u_425690ee-6fff-11ea-8634-d0abd5335702',
                         action_type='S',
                         status_code=1,
                         create_time='20200327164920',
                         update_time='20200327164920',
                         audit_id='u_425690ee-6fff-11ea-8634-d0abd5335702')
    db.session.add(seed_data)

    seed_data = TaskInfo(task_id='t_0749d202-7001-11ea-8634-d0abd5335702',
                         task_name='EAI_Queue_Purge',
                         task_type=2,
                         owner_id='u_425690ee-6fff-11ea-8634-d0abd5335702',
                         action_type='S',
                         status_code=1,
                         create_time='20200327164920',
                         update_time='20200327164920',
                         audit_id='u_425690ee-6fff-11ea-8634-d0abd5335702')
    db.session.add(seed_data)

    seed_data = TaskInfo(task_id='t_7983cf08-7001-11ea-8634-d0abd5335702',
                         task_name='TP_재기동',
                         task_type=2,
                         owner_id='u_425690ee-6fff-11ea-8634-d0abd5335702',
                         action_type='S',
                         status_code=1,
                         create_time='20200327164920',
                         update_time='20200327164920',
                         audit_id='u_425690ee-6fff-11ea-8634-d0abd5335702')
    db.session.add(seed_data)

    seed_data = TaskInfo(task_id='t_d54bb2e2-7001-11ea-8634-d0abd5335702',
                         task_name='잠겨진_태스크',
                         task_type=2,
                         owner_id='u_425690ee-6fff-11ea-8634-d0abd5335702',
                         action_type='S',
                         status_code=2,
                         create_time='20200327164920',
                         update_time='20200327164920',
                         audit_id='u_425690ee-6fff-11ea-8634-d0abd5335702')
    db.session.add(seed_data)

    seed_data = TaskInfo(task_id='t_13c5e862-7002-11ea-8634-d0abd5335702',
                         task_name='비정상_태스크',
                         task_type=2,
                         owner_id='u_425690ee-6fff-11ea-8634-d0abd5335702',
                         action_type='S',
                         status_code=0,
                         create_time='20200327164920',
                         update_time='20200327164920',
                         audit_id='u_425690ee-6fff-11ea-8634-d0abd5335702')
    db.session.add(seed_data)

    seed_data = TaskPlaybook(task_id='t_41750ee0-6ffe-11ea-8634-d0abd5335702',
                             task_seq=0,
                             contents=moss.enc("cat /home/tester/db_stat.txt"),
                             cause="DB 상태 분석 용도",
                             create_time='20200327164920',
                             update_time='20200327164920',
                             audit_id='u_425690ee-6fff-11ea-8634-d0abd5335702')
    db.session.add(seed_data)

    seed_data = TaskPlaybook(task_id='t_e355d1c6-6fff-11ea-8634-d0abd5335702',
                             task_seq=0,
                             contents=moss.enc("cat /home/tester/eai_stat.txt"),
                             cause="EAI/MCG 상태 분석 용도",
                             create_time='20200327164920',
                             update_time='20200327164920',
                             audit_id='u_425690ee-6fff-11ea-8634-d0abd5335702')
    db.session.add(seed_data)

    seed_data = TaskPlaybook(task_id='t_213ffe8a-7000-11ea-8634-d0abd5335702',
                             task_seq=0,
                             contents=moss.enc("top -n 1 -b"),
                             cause="시스템 상태 분석 용도",
                             create_time='20200327164920',
                             update_time='20200327164920',
                             audit_id='u_425690ee-6fff-11ea-8634-d0abd5335702')
    db.session.add(seed_data)

    seed_data = TaskPlaybook(task_id='t_8ef98bda-7000-11ea-8634-d0abd5335702',
                             task_seq=0,
                             contents=moss.enc("cat /home/tester/tp_stat.txt"),
                             cause="TP 상태 분석 용도",
                             create_time='20200327164920',
                             update_time='20200327164920',
                             audit_id='u_425690ee-6fff-11ea-8634-d0abd5335702')
    db.session.add(seed_data)

    seed_data = TaskPlaybook(task_id='t_cbe83f46-7000-11ea-8634-d0abd5335702',
                             task_seq=0,
                             contents=moss.enc("cat /home/tester/db_solution.txt"),
                             cause="DB Session Lock 제거 용도",
                             create_time='20200327164920',
                             update_time='20200327164920',
                             audit_id='u_425690ee-6fff-11ea-8634-d0abd5335702')
    db.session.add(seed_data)

    seed_data = TaskPlaybook(task_id='t_0749d202-7001-11ea-8634-d0abd5335702',
                             task_seq=0,
                             contents=moss.enc("cat /home/tester/eai_solution.txt"),
                             cause="EAI 적체 제거 용도",
                             create_time='20200327164920',
                             update_time='20200327164920',
                             audit_id='u_425690ee-6fff-11ea-8634-d0abd5335702')
    db.session.add(seed_data)

    seed_data = TaskPlaybook(task_id='t_7983cf08-7001-11ea-8634-d0abd5335702',
                             task_seq=0,
                             contents=moss.enc("cat /home/tester/tp_solution.txt"),
                             cause="TP 재기동 용도",
                             create_time='20200327164920',
                             update_time='20200327164920',
                             audit_id='u_425690ee-6fff-11ea-8634-d0abd5335702')
    db.session.add(seed_data)

    seed_data = TaskPlaybook(task_id='t_d54bb2e2-7001-11ea-8634-d0abd5335702',
                             task_seq=0,
                             contents=moss.enc("cat /home/tester/tp_solution.txt"),
                             cause="잠겨진 태스크 테스트 용도",
                             create_time='20200327164920',
                             update_time='20200327164920',
                             audit_id='u_425690ee-6fff-11ea-8634-d0abd5335702')
    db.session.add(seed_data)

    seed_data = TaskPlaybook(task_id='t_13c5e862-7002-11ea-8634-d0abd5335702',
                             task_seq=0,
                             contents=moss.enc("cat /home/tester/tp_solution.txt"),
                             cause="비정상 태스크 테스트 용도",
                             create_time='20200327164920',
                             update_time='20200327164920',
                             audit_id='u_425690ee-6fff-11ea-8634-d0abd5335702')
    db.session.add(seed_data)

    seed_data = TaskManagement(owner_id='u_425690ee-6fff-11ea-8634-d0abd5335702',
                               task_id='t_41750ee0-6ffe-11ea-8634-d0abd5335702',
                               owner_type=0,
                               create_time='20200327164920',
                               update_time='20200327164920',
                               audit_id='u_425690ee-6fff-11ea-8634-d0abd5335702')
    db.session.add(seed_data)

    seed_data = TaskManagement(owner_id='u_425690ee-6fff-11ea-8634-d0abd5335702',
                               task_id='t_e355d1c6-6fff-11ea-8634-d0abd5335702',
                               owner_type=0,
                               create_time='20200327164920',
                               update_time='20200327164920',
                               audit_id='u_425690ee-6fff-11ea-8634-d0abd5335702')
    db.session.add(seed_data)

    seed_data = TaskManagement(owner_id='u_425690ee-6fff-11ea-8634-d0abd5335702',
                               task_id='t_213ffe8a-7000-11ea-8634-d0abd5335702',
                               owner_type=0,
                               create_time='20200327164920',
                               update_time='20200327164920',
                               audit_id='u_425690ee-6fff-11ea-8634-d0abd5335702')
    db.session.add(seed_data)

    seed_data = TaskManagement(owner_id='u_425690ee-6fff-11ea-8634-d0abd5335702',
                               task_id='t_8ef98bda-7000-11ea-8634-d0abd5335702',
                               owner_type=0,
                               create_time='20200327164920',
                               update_time='20200327164920',
                               audit_id='u_425690ee-6fff-11ea-8634-d0abd5335702')
    db.session.add(seed_data)

    seed_data = TaskManagement(owner_id='u_425690ee-6fff-11ea-8634-d0abd5335702',
                               task_id='t_cbe83f46-7000-11ea-8634-d0abd5335702',
                               owner_type=0,
                               create_time='20200327164920',
                               update_time='20200327164920',
                               audit_id='u_425690ee-6fff-11ea-8634-d0abd5335702')
    db.session.add(seed_data)

    seed_data = TaskManagement(owner_id='u_425690ee-6fff-11ea-8634-d0abd5335702',
                               task_id='t_0749d202-7001-11ea-8634-d0abd5335702',
                               owner_type=0,
                               create_time='20200327164920',
                               update_time='20200327164920',
                               audit_id='u_425690ee-6fff-11ea-8634-d0abd5335702')
    db.session.add(seed_data)

    seed_data = TaskManagement(owner_id='u_425690ee-6fff-11ea-8634-d0abd5335702',
                               task_id='t_7983cf08-7001-11ea-8634-d0abd5335702',
                               owner_type=0,
                               create_time='20200327164920',
                               update_time='20200327164920',
                               audit_id='u_425690ee-6fff-11ea-8634-d0abd5335702')
    db.session.add(seed_data)

    seed_data = TaskManagement(owner_id='u_425690ee-6fff-11ea-8634-d0abd5335702',
                               task_id='t_d54bb2e2-7001-11ea-8634-d0abd5335702',
                               owner_type=0,
                               create_time='20200327164920',
                               update_time='20200327164920',
                               audit_id='u_425690ee-6fff-11ea-8634-d0abd5335702')
    db.session.add(seed_data)

    seed_data = UserInfo(user_id='u_425690ee-6fff-11ea-8634-d0abd5335702',
                         user_name='김동훈',
                         email='donghun_kim@sk.com',
                         passwd=moss.enc('1234567890'),
                         status_code=1,
                         role_code=0,
                         slack_id='',
                         create_time='20200327164920',
                         update_time='20200327164920')
    db.session.add(seed_data)

    seed_data = GroupInfo(group_id='g_aa3d71fa-7009-11ea-8634-d0abd5335702',
                          group_name='솔루션개발Cell',
                          owner_id='u_425690ee-6fff-11ea-8634-d0abd5335702',
                          create_time='20200327164920',
                          update_time='20200327164920',
                          audit_id='u_425690ee-6fff-11ea-8634-d0abd5335702')
    db.session.add(seed_data)

    seed_data = GroupManagement(user_id='u_425690ee-6fff-11ea-8634-d0abd5335702',
                                group_id='g_aa3d71fa-7009-11ea-8634-d0abd5335702',
                                task_id='t_7983cf08-7001-11ea-8634-d0abd5335702',
                                create_time='20200327164920',
                                update_time='20200327164920',
                                audit_id='u_425690ee-6fff-11ea-8634-d0abd5335702')
    db.session.add(seed_data)

    db.session.commit()


if __name__ == '__main__':
    manager.run()
