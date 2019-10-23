# _*_ coding: utf-8 _*_
__author__ = 'kim dong-hun'
from app import create_app, db
from app.models import ChannelInfo, TargetList, TaskInfo

app, manager = create_app()


@manager.command
def seed():
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

    seed_data = TargetList(task_id='DB_상태_분석',
                           host='localhost',
                           port=22,
                           user='tester',
                           passwd='!tester56#',
                           out_channel_id='#opbot_swing',
                           adapter_type=0)
    db.session.add(seed_data)

    seed_data = TargetList(task_id='EAI/MCG_상태_분석',
                           host='localhost',
                           port=22,
                           user='tester',
                           passwd='!tester56#',
                           out_channel_id='#opbot_swing',
                           adapter_type=0)
    db.session.add(seed_data)

    seed_data = TargetList(task_id='시스템_상태_분석',
                           host='localhost',
                           port=22,
                           user='tester',
                           passwd='!tester56#',
                           out_channel_id='#opbot_swing',
                           adapter_type=0)
    db.session.add(seed_data)

    seed_data = TargetList(task_id='TP_상태_분석',
                           host='localhost',
                           port=22,
                           user='tester',
                           passwd='!tester56#',
                           out_channel_id='#opbot_swing',
                           adapter_type=0)
    db.session.add(seed_data)

    seed_data = TargetList(task_id='DB_Session_Lock_제거',
                           host='localhost',
                           port=22,
                           user='tester',
                           passwd='!tester56#',
                           out_channel_id='#opbot_swing',
                           adapter_type=0)
    db.session.add(seed_data)

    seed_data = TargetList(task_id='EAI_Queue_Purge',
                           host='localhost',
                           port=22,
                           user='tester',
                           passwd='!tester56#',
                           out_channel_id='#opbot_swing',
                           adapter_type=0)
    db.session.add(seed_data)

    seed_data = TargetList(task_id='TP_재기동',
                           host='localhost',
                           port=22,
                           user='tester',
                           passwd='!tester56#',
                           out_channel_id='#opbot_swing',
                           adapter_type=0)
    db.session.add(seed_data)

    db.session.commit()

    TaskInfo.query.delete()

    seed_data = TaskInfo(task_id='DB_상태_분석',
                         task_type='c',
                         script_seq=0,
                         script="cat /home/tester/db_stat.txt")
    db.session.add(seed_data)

    seed_data = TaskInfo(task_id='EAI/MCG_상태_분석',
                         task_type='c',
                         script_seq=0,
                         script="cat /home/tester/eai_stat.txt")
    db.session.add(seed_data)

    seed_data = TaskInfo(task_id='시스템_상태_분석',
                         task_type='c',
                         script_seq=0,
                         script="top -n 1 -b")
    db.session.add(seed_data)

    seed_data = TaskInfo(task_id='TP_상태_분석',
                         task_type='c',
                         script_seq=0,
                         script="cat /home/tester/tp_stat.txt")
    db.session.add(seed_data)

    seed_data = TaskInfo(task_id='DB_Session_Lock_제거',
                         task_type='c',
                         script_seq=0,
                         script="cat /home/tester/db_solution.txt")
    db.session.add(seed_data)

    seed_data = TaskInfo(task_id='EAI_Queue_Purge',
                         task_type='c',
                         script_seq=0,
                         script="cat /home/tester/eai_solution.txt")
    db.session.add(seed_data)

    seed_data = TaskInfo(task_id='TP_재기동',
                         task_type='c',
                         script_seq=0,
                         script="cat /home/tester/tp_solution.txt")
    db.session.add(seed_data)

    db.session.commit()


if __name__ == '__main__':
    manager.run()
