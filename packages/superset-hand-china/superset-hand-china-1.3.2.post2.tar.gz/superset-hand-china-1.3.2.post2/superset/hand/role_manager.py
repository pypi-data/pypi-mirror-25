from flask_appbuilder.security.sqla.manager import SecurityManager
from .role_views import (
    MyRoleViewModel, MyUserViewModel, MyUserStatsChartView,
    MyPermissionViewViewModel)

class MySecurityManager(SecurityManager):
    rolemodelview = MyRoleViewModel
    userdbmodelview = MyUserViewModel
    userstatschartview = MyUserStatsChartView
    permissionviewmodelview  = MyPermissionViewViewModel

