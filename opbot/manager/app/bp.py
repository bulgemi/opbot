# _*_ coding: utf-8 _*_
__author__ = 'kim dong-hun'


def register_bp(app):
    """
    register a blueprint

    :param app:
    :return:
    """
    # footer
    from .footer.render_about import footer_bp as about
    from .footer.render_sitemap import footer_bp as sitemap
    from .footer.render_contacts import footer_bp as contacts
    app.register_blueprint(about)
    app.register_blueprint(sitemap)
    app.register_blueprint(contacts)
    # login
    from .login.render_login import login_bp as login
    from .login.render_new import login_bp as user_new
    app.register_blueprint(login)
    app.register_blueprint(user_new)
    # task
    from .task.render_new import task_bp as task_new
    from .task.render_list import task_bp as task_list
    app.register_blueprint(task_new)
    app.register_blueprint(task_list)
    # group
    from .group.render_new import group_bp as group_new
    from .group.render_list import group_bp as group_list
    app.register_blueprint(group_new)
    app.register_blueprint(group_list)
    # admin
    from .admin.render_user import admin_bp as admin_user
    from .admin.render_task import admin_bp as admin_task
    from .admin.render_group import admin_bp as admin_group
    app.register_blueprint(admin_user)
    app.register_blueprint(admin_task)
    app.register_blueprint(admin_group)
