from superset.views.core import Superset
from superset.views.base import BaseSupersetView
from flask_appbuilder.security.decorators import has_access_api, has_access
from flask_appbuilder import BaseView
from flask_appbuilder.widgets import ListWidget
from flask_appbuilder import expose
from superset import (
    appbuilder, cache, db, viz, utils, app,
    sm, sql_lab, results_backend, security
)
from flask import (
    g, request, redirect, flash, Response, render_template, Markup,
    abort, url_for)
from flask_appbuilder.models.sqla.interface import SQLAInterface
from sqlalchemy import asc, and_, desc, select
from flask import request
from . import models
import superset.models.core as superset_models
import superset.models.sql_lab as sql_models
from superset.hand.mail import Mail
from superset.hand.scheduler import Scheduler

from superset.views.base import (
    api, SupersetModelView, BaseSupersetView, DeleteMixin,
    SupersetFilter, get_user_roles, json_error_response, get_error_msg
)
import json
import re
import time
import logging
from flask_babel import gettext as __
from flask_babel import lazy_gettext as _
import logging
from flask import  request,g
from flask_login import current_user
from superset.connectors.sqla.models import SqlaTable


class PortalFilter(SupersetFilter):
    def apply(self, query, func):  # noqa
        if self.has_all_datasource_access():
            return query
        portal_perms = self.get_view_menus('portal_access')
        query = query.filter(models.Portal.portal_name.in_(portal_perms))
        return query


class PortalModelView(SupersetModelView, DeleteMixin):  # noqa
    datamodel = SQLAInterface(models.Portal)
    list_title = _("List Portal")
    show_title = _("Show Portal")
    add_title = _("Add Portal")
    edit_title = _("Edit Portal")
    list_columns = [
        'portal_link', 'description', 'creator', 'modified', 'portal_link2']
    edit_columns = [
        'portal_name', 'description', 'title', 
        'footer', 'portal_href']
    add_columns = edit_columns
    show_columns = add_columns
    base_filters = [['portal_name', PortalFilter, lambda: []]]
    order_columns = ['portal_link', 'description', 'modified']
    page_size = 10
    search_columns = ['portal_name', 'title', 'portal_href', 'changed_on']
    label_columns = {
        'portal_link': _("portal_name"),
        'portal_link2': _("Manage"),
        'portal_name': _("portal_name"),
        'description': _("Description"),
        'creator': _("Creator"),
        'modified': _("Modified"),
        'title': _("title"),
        'footer': _("footer"),
        'portal_href': _("portal_href"),
    }
 
appbuilder.add_view(
    PortalModelView,
    "Portal",
    label=__("Portal"),
    icon="fa-university",
    category="",
    category_icon='',
)


class Hand(BaseSupersetView):

    # 获取所有的切片
    @has_access
    # @csrf.exempt
    @expose("/explore/getSlices", methods=['GET', 'POST'])
    def getSlices(self):
        d = {}
        slices = db.session.query(superset_models.Slice).all()
        for slice in slices:
            d[str(slice.id)] = slice.slice_name
        return json.dumps(d)

    # 获取所有的仪表盘
    @has_access
    @expose("/explore/getDashboards", methods=['GET', 'POST'])
    def getDashboards(self):
        d = {}
        dashboards = db.session.query(superset_models.Dashboard).all()
        for dashboard in dashboards:
            d[str(dashboard.id)] = dashboard.dashboard_title
        return json.dumps(d)

    # 根据sliceId查询slice名称
    @has_access
    @expose("/explore/getSliceName/<slice_id>", methods=['GET', 'POST'])
    def getSliceName(self, slice_id):
        if slice_id != 'undefined':
            slice = db.session.query(superset_models.Slice).filter_by(id=slice_id).one()
            return slice.slice_name
        else: 
            return 'slice'

    # 根据给定的sliceIds获取slice详情（提示器组合获取子切片及对应数据源）
    @has_access
    @expose("/getSliceData/", methods=['GET', 'POST'])
    def getSliceData(self):
        sliceIds = request.args.get('sliceIds')
        # print(sliceIds)
        slices = []
        datasources = set()
        for slice_id in sliceIds.split(','):
            slice = db.session.query(superset_models.Slice).filter_by(id=slice_id).one()
            datasource = slice.datasource
            if datasource:
                datasources.add(datasource)
            # print(slice.data)
            sliceJson = slice.data
            # the filter_box_combination's children
            sliceJson['form_data']['is_child'] = True
            slices.append(sliceJson)
        return json.dumps({ "dashboard_data": {"slices": slices},
            "datasources": {ds.uid: ds.data for ds in datasources},
            "common": self.common_bootsrap_payload() })

    # 获取提示器组合所有子切片id及名称
    @has_access
    @expose("/getFilterBoxs/", methods=['GET', 'POST'])
    def getFilterBoxs(self):
        filterBoxs = db.session.query(superset_models.Slice) \
            .filter(superset_models.Slice.viz_type.in_(['filter_box', 'filter_box_tree', 'filter_box_cascade'])) \
            .all()
        filters = []
        for f in filterBoxs:
            filters.append({
                'id': f.id,
                'slice_name': f.slice_name
            })
        return json.dumps(filters)

    # 设置提示器缺省值（sql查询设置）
    @has_access
    @expose("/prompt/query", methods=['GET', 'POST'])
    def propmtQuery(self):
        try:
            sql = request.form.get('sql')
            # parse database name from sql
            regex = '[\w_-]+\.[\w_-]+\.[\w_-]+'
            pattern = re.compile(regex)
            list = pattern.findall(sql)
            database_name = list[0].split('.')[0]
            sql = sql.replace(list[0], list[0][(list[0].find('.') + 1):])
            # print(sql)
            session = db.session()
            mydb = session.query(superset_models.Database).filter_by(database_name=database_name).first()
            client_id = str(time.time()).replace('.', '')[2:13]
            query = sql_models.Query(
                database_id=int(mydb.id),
                limit=int(app.config.get('SQL_MAX_ROW', None)),
                sql=sql,
                user_id=int(g.user.get_id()),
                client_id=client_id,
            )
            session.add(query)
            session.commit()
            query_id = query.id

            result = sql_lab.get_sql_results(query_id, return_results=True)
            return json.dumps(result['data'])
        except Exception as e:
            return utils.error_msg_from_exception(e)

    @expose("/rest/api/sliceUrl", methods=['GET', 'POST'])
    def sliceUrl(self):
        sliceId = request.args.get('sliceId')
        if sliceId:
            slc = db.session.query(superset_models.Slice).filter_by(id=sliceId).one()
            return json.dumps({
                'url': slc.slice_url,
                'title': slc.slice_name
            })
        else:
            return False

    @expose("/rest/api/dashboardUrl", methods=['GET', 'POST'])
    def dashboardUrl(self):
        title = request.form['title']
        # groupby = request.form['groupby']
        # group = groupby.split(',')
        slcs = []
        if title:
            dash = db.session.query(superset_models.Dashboard).filter_by(id=title).one()
            for slice in dash.slices:
                if slice.viz_type == 'filter_box' or slice.viz_type == 'filter_box_tree':
                    param = json.loads(slice.params)
                    groupby = None
                    if slice.viz_type == 'filter_box':
                        groupby = param['groupby']
                    else:
                        groupby = [param['filter_name'].split('-')[1]]
                    cols = []
                    for col in groupby:
                        cols.append({
                            'extCol': col
                        })
                    slcs.append({
                        'sliceId': slice.id,
                        'columns': cols
                    })
                elif slice.viz_type == 'filter_box_combination':
                    filter_combination = db.session.query(superset_models.Slice).filter_by(id=slice.id).one()
                    filterIds = json.loads(filter_combination.params)['filter_combination']
                    for filterId in filterIds:
                        filter = db.session.query(superset_models.Slice).filter_by(id=filterId).one()
                        param = json.loads(filter.params)
                        groupby = None
                        if filter.viz_type == 'filter_box':
                            groupby = param['groupby']
                        else:
                            groupby = [param['filter_name'].split('-')[1]]
                        cols = []
                        for col in groupby:
                            cols.append({
                                'extCol': col
                            })
                        slcs.append({
                            'sliceId': filter.id,
                            'columns': cols
                        })                  
            return json.dumps({
                'url': dash.url,
                'title': dash.dashboard_title,
                'slcs': slcs
            })
        else:
            return False

    @has_access
    @expose("/portal/<portal_id>/<operate>", methods=['GET', 'POST'])
    def portal(self, portal_id, operate):
        portal = db.session.query(models.Portal)\
                    .filter_by(id = portal_id).one()
        # query all menu by protal_id
        menus = db.session.query(models.PortalMenu)\
                    .filter_by(portal_id = portal_id).all()
        showHeader = 'true'
        d = {
            'portal': (portal.id, portal.portal_name, portal.title, portal.width, portal.logo, portal.footer, portal.portal_href),
            'menus':  [(m.id, m.menu_name, m.parent_id, m.dashboard_href, m.open_way, m.is_index, m.icon) for m in menus],
            'edit': 'false',
            'dashboards': None,
        }
        if operate == 'edit':
            d['edit'] = 'true'
            dashobards = db.session.query(superset_models.Dashboard).all()
            d['dashboards'] = [(d.id, d.dashboard_title) for d in dashobards]
            return self.render_template(
                'hand/portalManage.html',
                bootstrap_data=json.dumps(d, default=utils.json_iso_dttm_ser)
            )
        if operate == 'show':
            # get user info
            d['roles'] =str(current_user.roles)
            d['username'] = current_user.username
            # get portals
            portals = db.session.execute('select id, portal_name from portal').fetchall()
            portalList = []
            for p in portals:
                portalList.append([p[0], p[1]])
            d['portals'] = portalList
            return self.render_template(
                'hand/portalShow.html',
                bootstrap_data=json.dumps(d, default=utils.json_iso_dttm_ser)
            )
    
    @has_access
    @expose("/menu/<operate>", methods=['GET', 'POST'])
    def addMenu(self, operate):
        data = json.loads(request.form.get('data'))
        try:
            if data['is_index'] == 'true':
                db.session.query(models.PortalMenu) .filter_by(portal_id = str(data['portal_id'])).update({models.PortalMenu.is_index : 'null'})
                # db.session.execute('update portal_menu set is_index = null where portal_id = ' + str(data['portal_id']))
            if operate == 'add':
                addMenu = models.PortalMenu(
                    portal_id=data['portal_id'],
                    menu_name=data['menuName'],
                    parent_id=data['parentSelector'],
                    dashboard_href=data['dashboard_href'],
                    icon=data['picSelector'],
                    is_index =data['is_index'])
                db.session.add(addMenu)
            elif operate == 'modify':
                menu = models.PortalMenu(
                    id =data['id'],
                    portal_id=data['portal_id'],
                    menu_name=data['menuName'],
                    parent_id=data['parentSelector'],
                    dashboard_href=data['dashboard_href'],
                    icon=data['picSelector'],
                    is_index =data['is_index'])
                db.session.query(models.PortalMenu).filter_by(id=menu.id).update(
                    {
                        models.PortalMenu.portal_id: menu.portal_id,
                        models.PortalMenu.menu_name: menu.menu_name,
                        models.PortalMenu.parent_id: menu.parent_id,
                        models.PortalMenu.is_index: menu.is_index,
                        models.PortalMenu.dashboard_href: menu.dashboard_href,
                        models.PortalMenu.icon: menu.icon
                    }
                )
            else:
                menu = models.PortalMenu(id =data['id'])
                db.session.query(models.PortalMenu).filter_by(id=menu.id).delete()
            db.session.commit()
            return 'true'
        except Exception as e:
            logging.exception(e)
            return 'false'

    @has_access
    @expose("/upload/logo", methods=['GET', 'POST'])
    def uploadLogo(self):
        try:
            file = request.files['file']
            filename = 'logo_' + request.form['portal_id'] + '_' + request.form['time'] + '.png'
          
            # write portal_logo to db
            # db.session.execute("update portal set logo = '%s' where id = %s" %(request.form['time'], request.form['portal_id']))
            db.session.query(models.Portal).filter_by(id = request.form['portal_id']).update({models.Portal.logo : request.form['time']})
            db.session.commit()
            import os
            if not os.path.exists(os.path.abspath(os.path.join(os.path.dirname(__file__),os.path.pardir)) + '/assets/resrouces/portalManage/logo'):
                os.mkdir(os.path.abspath(os.path.join(os.path.dirname(__file__),os.path.pardir)) + '/assets/resrouces/portalManage/logo')
            file.save(os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__),os.path.pardir)) + '/assets/resrouces/portalManage/logo/', filename))
            return 'true'
        except Exception as e:
            logging.exception(e)
            return 'false'

    @has_access
    @expose("/logo/del/<id>", methods=['GET', 'POST'])
    def delLogo(self, id):
        try:
            # db.session.execute("update portal set logo = null where id = %s" %(id))
            db.session.query(models.Portal).filter_by(id = id).update({models.Portal.logo : "null"})
            db.session.commit()
            return 'true'
        except Exception as e:
            logging.exception(e)
            return 'false'

    @has_access
    @expose("/portal/getTheme", methods=['GET', 'POST'])
    def getPortalTheme(self):                                            
        try:
            # theme = db.session.execute("select * from portal_theme where user_id = " + g.user.get_id()).fetchone()
            theme = db.session.query(models.PortalTheme).filter_by(user_id = g.user.get_id()).all()
            if theme == []:
                # init this user theme
                # db.session.execute("insert into portal_theme (user_id, color, theme_style, layout, header, top_menu, sidebar_mode, sidebar_menu, sidebar_style, sidebar_position, footer) values (%s, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')"
                #                     %(g.user.get_id(), 'blue', 'square', 'fluid', 'fixed', 'light', 'default', 'accordion', 'default', 'left', 'default'))
                addTheme = models.PortalTheme(
                    user_id = g.user.get_id(),
                    color = "blue",
                    theme_style = "square",
                    layout = "fluid",
                    header = "fixed",
                    top_menu = "light",
                    sidebar_mode = 'default',
                    sidebar_menu = 'accordion',
                    sidebar_style = 'default',
                    sidebar_position = 'left',
                    footer = 'default',)
                
                db.session.add(addTheme)
                db.session.commit()
                # theme = db.session.execute("select * from portal_theme where user_id = " + g.user.get_id()).fetchone()
                theme = db.session.query(models.PortalTheme).filter_by(user_id = g.user.get_id()).all()
            return json.dumps({
                'color': theme[0].color, 'themeStyle': theme[0].theme_style, 'layout': theme[0].layout,
                'header': theme[0].header, 'top_menu': theme[0].top_menu, 'sidebar_mode': theme[0].sidebar_mode,
                'sidebar_menu': theme[0].sidebar_menu, 'sidebar_style': theme[0].sidebar_style, 'sidebar_position': theme[0].sidebar_position, 'footer': theme[0].footer
            })
        except Exception as e:
            logging.exception(e)
            return 'fail'
    @has_access
    @expose("/portal/updateTheme", methods=['GET', 'POST'])
    def updatePortalTheme(self):
        try:
            # db.session.execute("update portal_theme set color = '%s', theme_style = '%s', layout = '%s', header = '%s', top_menu = '%s', sidebar_mode = '%s', sidebar_menu = '%s', sidebar_style = '%s', sidebar_position = '%s', footer = '%s' where user_id = %s"
            #                 %(request.form['color'], request.form['theme_style'], request.form['layout'], request.form['header'], request.form['top_menu'], request.form['sidebar_mode'], 
            #                 request.form['sidebar_menu'], request.form['sidebar_style'], request.form['sidebar_position'], request.form['footer'], g.user.get_id()) )
            db.session.query(models.PortalTheme).filter_by(user_id = g.user.get_id()).update({
                models.PortalTheme.color : request.form['color'],
                models.PortalTheme.theme_style : request.form['theme_style'],
                models.PortalTheme.layout : request.form['layout'],
                models.PortalTheme.header : request.form['header'],
                models.PortalTheme.top_menu : request.form['top_menu'],
                models.PortalTheme.sidebar_mode : request.form['sidebar_mode'],
                models.PortalTheme.sidebar_menu : request.form['sidebar_menu'],
                models.PortalTheme.sidebar_style : request.form['sidebar_style'],
                models.PortalTheme.sidebar_position : request.form['sidebar_position'],
                models.PortalTheme.footer : request.form['sidebar_position']
            })
            db.session.commit()
            return 'success'
        except Exception as e:
            logging.exception(e)
            return 'fail'
    
    @has_access
    @expose("/portal/getUserInfo", methods=['GET'])
    def getUserInfo(self):
        user = {
            'username': current_user.username,
            'first_name': current_user.first_name,
            'last_name': current_user.last_name,
            'active': current_user.active,
            'roles': str(current_user.roles),
            'login_count': current_user.login_count,
            'email': current_user.email
        }
        return json.dumps(user)

    @has_access
    @expose("/portal/updatePassword", methods=['GET', 'POST'])
    def updatePassword(self):
        try:
            from werkzeug.security import generate_password_hash
            current_user.password = generate_password_hash(request.form['newPassword'])
            # print(current_user.__dict__)
            db.session.add(current_user)
            db.session.commit()
            return 'success'
        except Exception as e:
            logging.exception(e)
            return 'fail'

    @has_access
    @expose("/portal/updateUserInfo", methods=['GET', 'POST'])
    def updateUserInfo(self):
        try:
            current_user.first_name = request.form['firstName']
            current_user.last_name = request.form['lastName']
            current_user.email = request.form['email']
            # print(current_user.__dict__)
            db.session.add(current_user)
            db.session.commit()
            return 'success'
        except Exception as e:
            logging.exception(e)
            return 'fail'
        

    appbuilder.add_link(
        'My Email',
        href='/hand/email/show',
        category_icon="fa-flask",
        icon="fa-flask",
        category='Warn'
    )

    appbuilder.add_link(
        'My Scheduler',
        href='/hand/mySchedulers/list/1',
        icon="fa-search",
        category_icon="fa-flask",
        category='Warn'
    )


    @has_access
    @expose("/testMail", methods=['GET', 'POST'])
    def testMail(self):
        return Mail.testConn(request.form['smtp_server'], request.form['port'], request.form['email'], request.form['password'])
    
    @has_access
    @expose("/resetMailPassword", methods=['GET', 'POST'])
    def resetMailPassword(self):
        db.session.query(models.Mail).filter_by(id=request.form['id']).update({
            'password': request.form['password']
        })
        db.session.commit()
        return 'true'

    @has_access
    @expose("/email/<operate>", methods=['GET', 'POST'])
    def email(self, operate):
        if operate == 'show':
            try:
                mail = db.session.query(models.Mail).filter_by(user_id=g.user.get_id()).one()
                m = mail.__dict__
                del(m['_sa_instance_state'])
            except Exception as e:
                m = None
            d = {
                'mailPage': 'true',
                'mail': m
            }
            return self.render_template(
                'hand/scheduler.html',
                entry='scheduler',
                bootstrap_data=json.dumps(d, default=utils.json_iso_dttm_ser),
            )
        else:
            data = {}
            try:
                if operate == 'add':
                    add_email = models.Mail(
                        user_id = g.user.get_id(),
                        smtp_server = request.form['smtp_server'],
                        port = request.form['port'],
                        email = request.form['email'],
                        password = request.form['password']
                    )
                    db.session.add(add_email)
                elif operate == 'modify':
                    modify_email = {
                        'smtp_server': request.form['smtp_server'],
                        'port': request.form['port'],
                        'email': request.form['email'],
                    }
                    db.session.query(models.Mail).filter_by(id=request.form['id']).update(modify_email)
                db.session.commit()
                data['status'] = 'true'
            except Exception as e:
                logging.exception(e)
                data['status'] = 'false'
            return json.dumps(data)

    @has_access
    @expose("/mySchedulers/<operate>/<id>", methods=['GET', 'POST'])
    def getMySchedulers(self, operate, id):
        # get all dashboards, slices and metrics
        newDashboards = []
        sendSlices = []
        if operate == 'add' or operate == 'modify':
            for s in db.session.query(superset_models.Slice).all():
                try:
                    try:
                        metrics = json.loads(s.params)['metrics']
                    except Exception as e:
                        metrics = [json.loads(s.params)['metric']]
                    sendSlices.append({
                        'id': s.id,
                        'name': s.slice_name,
                        'metrics': metrics,
                    })
                except Exception as e:
                    # has no metric or metrics
                    pass
            for dashboard in db.session.query(superset_models.Dashboard).all():
                newSlices = []
                for s in dashboard.slices:
                    
                    newSlices.append({
                        'id': s.id,
                        'name': s.slice_name,
                    })

                newDashboards.append({
                    'id': dashboard.id,
                    'name': dashboard.dashboard_title,
                    'slices': newSlices
                })
            # print(sendSlices)
            # print(newDashboards)

        if operate == 'list':
            schedulers = db.session.query(models.Scheduler).filter_by(user_id=g.user.get_id()).all()
            ss = []
            for scheduler in schedulers:
                s = scheduler.__dict__
                if len(scheduler.condition) > 0:
                    s['description'] = scheduler.condition[0].description
                    del(s['_sa_instance_state'])
                    del(s['condition'])
                    ss.append(s)
            d = {
                'schedulers': ss,
                'type': 'list',
            }
        elif operate == 'add':
            d = {
                'type': 'add',
                'dashboards': newDashboards,
                'slices': sendSlices,
            }
        elif operate == 'modify':
            scheduler = db.session.query(models.Scheduler).filter_by(id=id).one()
            condition = scheduler.condition[0]

            s = scheduler.__dict__
            c = condition.__dict__
            del(s['_sa_instance_state'])
            del(s['condition'])
            del(c['_sa_instance_state'])

            d = {
                'type': 'modify',
                'scheduler': s,
                'condition': c,
                'dashboards': newDashboards,
                'slices': sendSlices,
            }

        return self.render_template(
            'hand/scheduler.html',
            entry='scheduler',
            bootstrap_data=json.dumps(d, default=utils.json_iso_dttm_ser),
        )

    @has_access
    @expose("/job/<operate>/<id>", methods=['GET'])
    def operateJob(self, operate, id):
        # scheduler = db.session.query(models.Scheduler).filter_by(id = id).one()
        if operate == 'active':
            try:
                # update is_active and is_running
                modify_scheduler = {
                    'is_active': True,
                    'is_running': True,
                }
                db.session.query(models.Scheduler).filter_by(id=id).update(modify_scheduler)
                Scheduler.add(id)
                db.session.commit()
                return 'true'
            except Exception as e:
                logging.exception(e)
                db.session.rollback()
                return 'false'
        elif operate == 'delete':
            try:
                try:
                    Scheduler.delete(id)
                except Exception as e:
                    logging.exception(e)
                # delete table(scheduler and condition)
                db.session.query(models.Condition).filter_by(warn_scheduler_id=id).delete()
                db.session.query(models.Scheduler).filter_by(id=id).delete()
                db.session.commit()
                return 'true'
            except Exception as e:
                logging.exception(e)
                db.session.rollback()
                return 'false'
        elif operate == 'resume':
            db.session.query(models.Scheduler).filter_by(id=id).update({ 'is_running': True})
            Scheduler.resume(id)
            db.session.commit()
            return 'true'
        elif operate == 'pause':
            db.session.query(models.Scheduler).filter_by(id=id).update({ 'is_running': False})
            Scheduler.pause(id)
            db.session.commit()
            return 'true'

    @has_access
    @expose('/insertOrModifyScheduler/<operate>', methods=['POST'])
    def insertOrModifyScheduler(self, operate):
        data = {}
        try:
            if request.form['mode'] == 'cron':
                # example: month='6-8,11-12', day='3rd fri', hour='0-3'
                cron_year = cron_month = cron_day = cron_week = cron_day_of_week = cron_hour = cron_minute = cron_second = start_date = end_date = None
                cronArray = request.form['expr'].split('&&')
                for cron in cronArray:
                    key = cron.split('=')[0].strip()
                    value = cron.split('=')[1].strip()
                    if value[0] == "'" and value[len(value)-1] == "'":
                        value = value[1: -1]
                    if key == 'year':
                        cron_year = value
                    elif key == 'month':
                        cron_month = value
                    elif key == 'day':
                        cron_day = value
                    elif key == 'week':
                        cron_week = value
                    elif key == 'day_of_week':
                        cron_day_of_week = value
                    elif key == 'hour':
                        cron_hour = value
                    elif key == 'minute':
                        cron_minute = value
                    elif key == 'second':
                        cron_second = value
                    elif key == 'start_date':
                        start_date = value
                    elif key == 'end_date':
                        end_date = value
                if operate == 'insert':
                    add_scheduler = models.Scheduler(
                        user_id = g.user.get_id(),
                        mode = request.form['mode'],
                        cron_year = cron_year,
                        cron_month = cron_month,
                        cron_day = cron_day,
                        cron_week = cron_week,
                        cron_day_of_week = cron_day_of_week,
                        cron_hour = cron_hour,
                        cron_minute = cron_minute,
                        cron_second = cron_second,
                        start_date = start_date,
                        end_date = end_date,
                        is_active = False,
                        is_running = False,
                    )
                    db.session.add(add_scheduler)
                elif operate == 'modify':
                    modify_scheduler = {
                        'mode': request.form['mode'],
                        'cron_year': cron_year,
                        'cron_month': cron_month,
                        'cron_day': cron_day,
                        'cron_week': cron_week,
                        'cron_day_of_week': cron_day_of_week,
                        'cron_hour': cron_hour,
                        'cron_minute': cron_minute,
                        'cron_second': cron_second,
                        'start_date': start_date,
                        'end_date': end_date,
                    }
                    db.session.query(models.Scheduler).filter_by(id=request.form['id']).update(modify_scheduler)
            elif request.form['mode'] == 'interval':
                # example: hours=2, start_date='2017-3-20'
                interval_expr = start_date = end_date = None
                exprArray = request.form['expr'].split('&&')
                for expr in exprArray:
                    key = expr.split('=')[0].strip()
                    value = expr.split('=')[1].strip()
                    if value[0] == "'" and value[len(value)-1] == "'":
                        value = value[1: -1]
                    if key == 'start_date':
                        start_date = value
                    elif key == 'end_date':
                        end_date = value
                    else:
                        interval_expr = expr.strip()
                if operate == 'insert':
                    add_scheduler = models.Scheduler(
                        user_id = g.user.get_id(),
                        mode = request.form['mode'],
                        interval_expr = interval_expr,
                        start_date = start_date,
                        end_date = end_date,
                        is_active = False,
                        is_running = False,
                    )
                    db.session.add(add_scheduler)
                elif operate == 'modify':
                    modify_scheduler = {
                        'mode': request.form['mode'],
                        'interval_expr': interval_expr,
                        'start_date': start_date,
                        'end_date': end_date,
                    }
                    db.session.query(models.Scheduler).filter_by(id=request.form['id']).update(modify_scheduler)
            else:
                # example: run_date='2017-3-20 12:00:00'
                date_run_date = request.form['expr'].split('=')[1].strip()[1: -1]
                if operate == 'insert':
                    add_scheduler = models.Scheduler(
                        user_id = g.user.get_id(),
                        mode = request.form['mode'],
                        date_run_date = date_run_date,
                        is_active = False,
                        is_running = False,
                    )
                    db.session.add(add_scheduler)
                elif operate == 'modify':
                    modify_scheduler = {
                        'mode': request.form['mode'],
                        'date_run_date': date_run_date,
                    }
                    db.session.query(models.Scheduler).filter_by(id=request.form['id']).update(modify_scheduler)
            db.session.commit()
            data['status'] = 'true'
            if operate == 'insert':
                scheduler = db.session.query(models.Scheduler).order_by(models.Scheduler.created_on.desc()).first()
                data['schedulerId'] = scheduler.id
        except Exception as e:
            logging.exception(e)
            data['status'] = 'false'
        return json.dumps(data)

    @has_access
    @expose('/insertOrModifyCondition/<operate>', methods=['POST'])
    def insertOrModifyCondition(self, operate):
        data = {}
        try:
            if operate == 'insert':
                add_condition = models.Condition(
                    warn_scheduler_id = request.form['scheduler_id'],
                    dashboard_id = request.form['dashboard_id'],
                    slice_id = request.form['slice_id'],
                    metric = request.form['metric'],
                    expr = request.form['expr'],
                    receive_address = request.form['receive_address'],
                    send_slice_id = request.form['send_slice_id'],
                    description = request.form['description'],
                )
                db.session.add(add_condition)
            elif operate == 'modify':
                modify_condition = {
                    'dashboard_id': request.form['dashboard_id'],
                    'slice_id': request.form['slice_id'],
                    'metric': request.form['metric'],
                    'expr': request.form['expr'],
                    'receive_address': request.form['receive_address'],
                    'send_slice_id': request.form['send_slice_id'],
                    'description': request.form['description'],
                }
                db.session.query(models.Condition).filter_by(id=request.form['id']).update(modify_condition)
            db.session.commit()
            data['status'] = 'true'
        except Exception as e:
            logging.exception(e)
            data['status'] = 'false'
        return json.dumps(data)
    # 查询漏斗图排序类型
    @has_access
    @expose("/queryForFunnel", methods=[ 'GET','POST'])
    def queryForFunnel(self):
        try:
            # 获取参数
            datasource = request.form.get('datasource')
            groupby = request.form.get('groupby')
            datasource =datasource.split('_')
            #获取数据ID
            data = datasource[0]
            session = db.session()
            mydb = session.query(SqlaTable.sql).filter_by(id=data).one()
            ty = 'select temp.%s from ( %s) as temp ' % (groupby,mydb.sql)
            query =  db.session.execute(ty).fetchall()
            db.session.commit()
            results = []
            for r in query:
                results.append(r[0])
                
            return json.dumps((',').join(results))

        except Exception as e:
            return utils.error_msg_from_exception(e)

    @has_access
    @expose('/addQueryHistory', methods=['GET', 'POST'])
    def addQueryHistory(self):
        try:
            add_query = models.DownloadQuery(
                slice_id = request.form['slice_id'],
                query_json_url = request.form['query_json_url'],
                export_json_url = request.form['export_json_url'],
                sql = request.form['sql'],
                columns = request.form['columns'],
            )
            db.session.add(add_query)
            db.session.commit()
            return 'SUCCESS'
        except Exception as e:
            logging.exception(e)
            return 'FAIL'

    @has_access
    @expose("/getDownloadQueryHistory/<slice_id>", methods=['GET', 'POST'])
    def query(self, slice_id):
        def f(obj):
            return {
                'sql': obj.sql,
                'query_json_url': obj.query_json_url,
                'export_json_url': obj.export_json_url,
                'columns': obj.columns,
                'query_time': obj.created_on.strftime("%Y-%m-%d %H:%M:%S")
            }
        querys = db.session.query(models.DownloadQuery).filter_by(slice_id=slice_id).order_by(models.DownloadQuery.created_on.desc()).all()
        results = list(map(f, querys))
        return json.dumps(results)

    @has_access
    @expose("/queryCascadeData", methods=['GET', 'POST'])
    def queryCascadeData(self):
        datasource = request.form.get('datasource')
        groupby = request.form.get('groupby').split(',')
        table = db.session.query(SqlaTable.sql).filter_by(id=datasource.split('__')[0]).one()
        result = {}
        for g in groupby:
            sql = 'select distinct(temp.%s) from (%s) as temp' % (g, table.sql)
            query =  db.session.execute(sql).fetchall()
            db.session.commit()
            data = []
            for r in query:
                data.append(r[0])
            result[g] = data
        return json.dumps(result)

appbuilder.add_view_no_menu(Hand)
