# _*_ coding: utf-8 _*_
__author__ = 'kim dong-hun'
from app import create_app, db
from app.models import ChannelInfo

app, manager = create_app()


@manager.command
def seed():
    print("Add seed data to the database.")
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


if __name__ == '__main__':
    manager.run()
