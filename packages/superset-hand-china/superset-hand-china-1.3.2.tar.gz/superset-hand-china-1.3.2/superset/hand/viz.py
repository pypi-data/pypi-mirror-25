from superset.viz import BaseViz, viz_types_list, BigNumberTotalViz, BubbleViz, WordCloudViz, FilterBoxViz
from superset import app, utils, cache
from collections import OrderedDict, defaultdict
import simplejson as json

from flask_babel import gettext as __
from flask_babel import lazy_gettext as _

config = app.config

class agGridViz(BaseViz):

    viz_type = 'ag_grid'
    verbose_name = _('ag_grid View')

    def query_obj(self):
        d = super(agGridViz, self).query_obj()
        fd = self.form_data
        # d['startRow'] = fd.get('startRow')
        # d['pageSize'] = fd.get('pageSize')
        # d['currentPageSize'] = fd.get('currentPageSize')
        # d['total'] = fd.get('total')
        # d['viz_type'] = 'ag_grid'
        
        order_by_cols = fd.get('order_by_cols') or []
        d['orderby'] = [json.loads(t) for t in order_by_cols]
        return d

    def get_data(self, df):
        return dict(
            records=df.to_dict(orient="records"),
            columns=list(df.columns),
            total=0,
        )


class echartsBarViz(BaseViz):

    viz_type = 'echarts_bar'
    verbose_name = _('echarts bar View')
    is_timeseries = False

    def query_obj(self):
        d = super(echartsBarViz, self).query_obj()
        fd = self.form_data
        order_by_cols = fd.get('order_by_cols') or []
        d['orderby'] = [json.loads(t) for t in order_by_cols]
        return d

    def get_data(self, df):
        return dict(
            records=df.to_dict(orient='records'),
            columns=list(df.columns),
        )


class FilterBoxTreeViz(echartsBarViz):

    viz_type = "filter_box_tree"
    verbose_name = _("filter box tree View")
    is_timeseries = False  


class FilterBoxCombinationViz(BaseViz):

    viz_type = "filter_box_combination"
    verbose_name = _("filter box combination View")
    is_timeseries = False 

    def get_df(self):
        return True

    def get_data(self, df):
        return None

class FilterBoxCascadeViz(FilterBoxViz):

    viz_type = "filter_box_cascade"
    verbose_name = _("filter box cascade View")
    is_timeseries = False 


class echartsBarHViz(echartsBarViz):
    viz_type = "echarts_bar_h"
    verbose_name = _("echarts bar horizohtal View")
    is_timeseries = False


class echartsLineViz(echartsBarViz):

    viz_type = "echarts_line"
    verbose_name = _("echarts line View")
    is_timeseries = False

class echartsPieMetricsViz(echartsBarViz):

    viz_type = "echarts_pie_m"
    verbose_name = _("echarts Pie Metrics View")
    is_timeseries = False

class echartPieGViz(echartsBarViz):

    viz_type = "echarts_pie_g"
    verbose_name = _("echarts Pie GroupBy View")
    is_timeseries = False

class echartRadarMapViz(echartsBarViz):

    viz_type = "echarts_radar_map"
    verbose_name = _("echarts Radar Map View")
    is_timeseries = False

class echartsBarWaterfallViz(echartsBarViz):

    viz_type = "echarts_bar_waterfall"
    verbose_name = _("echarts bar waterfall View")
    is_timeseries = False

class echartsBigNumberCompareViz(BaseViz):

    viz_type = "echarts_big_number_compare"
    verbose_name = _("echarts Big Number Compare")
    is_timeseries = False

    def query_obj(self):
        d = super(echartsBigNumberCompareViz, self).query_obj()
        fd = self.form_data
        order_by_cols = fd.get('order_by_cols') or []
        d['orderby'] = [json.loads(t) for t in order_by_cols]
        d['metrics'] = [fd.get('metrics_one'), fd.get('metrics_two')]
        return d

    def get_data(self, df):
        return dict(
            records=df.to_dict(orient='records'),
            columns=list(df.columns),
        )


class echartsBarProgressViz(echartsBarViz):
    viz_type = "echarts_bar_progress"
    verbose_name = _("echarts bar horizohtal View")
    is_timeseries = False


class echartsLineBarViz(echartsBarViz):
    viz_type = "echarts_line_bar"
    verbose_name = _("echarts line Bar View")
    is_timeseries = False


class echartsPieHViz(echartsBarViz):
    viz_type = "echarts_pie_h"
    verbose_name = _("echarts Pie Hierarchical View")
    is_timeseries = False


class echartPieHGViz(echartsBarViz):
    viz_type = "echarts_pie_h_g"
    verbose_name = _("echarts Pie Hierarchical GroupBy View")
    is_timeseries = False

    def query_obj(self):
        d = super(echartPieHGViz, self).query_obj()
        fd = self.form_data
        order_by_cols = fd.get('order_by_cols') or []
        d['orderby'] = [json.loads(t) for t in order_by_cols]
        d['groupby'] = [fd.get('inner_metrics_one') , fd.get('outer_metrics_one')]
        return d

    def get_data(self, df):
        return dict(
            records=df.to_dict(orient='records'),
            columns=list(df.columns),
        )


class echartsDashboardViz(echartsBarViz):
    viz_type = "echarts_dash_board"
    verbose_name = _("echarts Dashboard View")
    is_timeseries = False

    def query_obj(self):
        d = super(echartsDashboardViz, self).query_obj()
        fd = self.form_data
        order_by_cols = fd.get('order_by_cols') or []
        d['orderby'] = [json.loads(t) for t in order_by_cols]
        d['metrics'] = [fd.get('metric')]
        return d

    def get_data(self, df):
        return dict(
            records=df.to_dict(orient='records'),
            columns=list(df.columns),
        )

class echartsWordCloudViz(WordCloudViz):

    viz_type = "echarts_word_cloud"
    verbose_name = _("echarts Word Cloud")


class echartsTreeMapViz(echartsBarViz):

    viz_type = "echarts_treemap"
    verbose_name = _("Echarts Treemap")
    is_timeseries = False    


class echartsBigNumberViz(BigNumberTotalViz):
    viz_type = "echarts_big_number"
    verbose_name = _("echarts Big Number")
    is_timeseries = False

class echartsBubbleViz(BubbleViz):
    viz_type = "echarts_bubble"
    verbose_name = _("echarts Bubble")
    is_timeseries = False


class echartsQuadrantViz(BaseViz):
    viz_type = "echarts_quadrant"
    verbose_name = _("Echarts Quadrant")
    is_timeseries = False

    def query_obj(self):
        d = super(echartsQuadrantViz, self).query_obj()
        fd = self.form_data
        order_by_cols = fd.get('order_by_cols') or []
        d['groupby'] = [fd.get('series')]
        d['orderby'] = [json.loads(t) for t in order_by_cols]
        d['metrics'] = [fd.get('x_metric'), fd.get('y_metric')]
        return d

    def get_data(self, df):
        return dict(
            records=df.to_dict(orient='records'),
            columns=list(df.columns),
        )
    

class ChinaMapViz(BaseViz):
    viz_type = "echarts_china_map"
    verbose_name = _("Chinaecharts_china_map Map")
    is_timeseries = False

    def query_obj(self):
        d = super(ChinaMapViz, self).query_obj()
        fd = self.form_data
        d['groupby']=[fd.get('groupby_one')]
        return d

    def get_data(self, df):
        return dict(
            records=df.to_dict(orient='records'),
            columns=list(df.columns),
        )


class ChinaCityMapViz(BaseViz):
    viz_type = "china_city_map"
    verbose_name = _("China City Map")
    is_timeseries = False

    def query_obj(self):
        d = super(ChinaCityMapViz, self).query_obj()
        fd = self.form_data
        d['groupby'] = [fd.get('groupby_one')]
        d['metrics'] = [fd.get('metric')]
        return d

    def get_data(self, df):
        return dict(
            records=df.to_dict(orient='records'),
            columns=list(df.columns),
        )

class echartsSankeyViz(BaseViz):
    viz_type = "echarts_sankey"
    verbose_name = _("Echarts Sankey")
    is_timeseries = False

    def query_obj(self):
        d = super(echartsSankeyViz, self).query_obj()
        fd = self.form_data
        order_by_cols = fd.get('order_by_cols') or []
        d['orderby'] = [json.loads(t) for t in order_by_cols]
        d['metrics'] = [fd.get('metric')]
        return d

    def get_data(self, df):
        return dict(
            records=df.to_dict(orient='records'),
            columns=list(df.columns),
        )
class echartsFunnel(BaseViz):
    viz_type = "echarts_funnel"
    verbose_name = _("Echarts Funnel")
    is_timeseries = False
    
    def query_obj(self):
        d = super(echartsFunnel, self).query_obj()
        fd = self.form_data
        order_by_cols = fd.get('order_by_cols') or []
        d['orderby'] = [json.loads(t) for t in order_by_cols]
        d['groupby'] = [fd.get('groupby_one')]
        d['metrics'] = [fd.get('metric')]
        return d
    def get_data(self, df):
        return dict(
            records=df.to_dict(orient='records'),
            columns=list(df.columns),
        )

class echartsChinaCityMapMigrationViz(BaseViz):
    viz_type = "echarts_china_city_map_migration"
    verbose_name = _("Echarts China City Map Migration")
    is_timeseries = False

    def query_obj(self):
        d = super(echartsChinaCityMapMigrationViz, self).query_obj()
        fd = self.form_data
        order_by_cols = fd.get('order_by_cols') or []
        d['orderby'] = [json.loads(t) for t in order_by_cols]
        d['metrics'] = [fd.get('metric')]
        return d

    def get_data(self, df):
        return dict(
            records=df.to_dict(orient='records'),
            columns=list(df.columns),
        )


class echartsAreaStack(echartsBarViz):

    viz_type = "echarts_area_stack"
    verbose_name = _("Echarts Area Stack View")
    is_timeseries = False


class bigNumberViz(BaseViz):

    viz_type = "big_number_viz"
    verbose_name = _("Big Number")
    is_timeseries = False

    def query_obj(self):
        d = super(bigNumberViz, self).query_obj()
        fd = self.form_data
        order_by_cols = fd.get('order_by_cols') or []
        d['orderby'] = [json.loads(t) for t in order_by_cols]
        d['metrics'] = [fd.get('metric')]
        return d

    def get_data(self, df):
        return dict(
            records=df.to_dict(orient='records'),
            columns=list(df.columns),
        )  


class bigNumberTwoViz(BaseViz):

    viz_type = "big_number_two_viz"
    verbose_name = _("Big Number Two")
    is_timeseries = False

    def query_obj(self):
        d = super(bigNumberTwoViz, self).query_obj()
        fd = self.form_data
        order_by_cols = fd.get('order_by_cols') or []
        d['orderby'] = [json.loads(t) for t in order_by_cols]
        metric = [fd.get('metric'), fd.get('metrics_one'), fd.get('metrics_two')]
        d['metrics'] = list(set(metric))
        return d

    def get_data(self, df):
        return dict(
            records=df.to_dict(orient='records'),
            columns=list(df.columns),
        )  
    

class bigNumberThreeViz(BaseViz):

    viz_type = "big_number_three_viz"
    verbose_name = _("Big Number Three")
    is_timeseries = False

    def query_obj(self):
        d = super(bigNumberThreeViz, self).query_obj()
        fd = self.form_data
        order_by_cols = fd.get('order_by_cols') or []
        d['orderby'] = [json.loads(t) for t in order_by_cols]
        d['metrics'] = [fd.get('metric')]
        return d

    def get_data(self, df):
        return dict(
            records=df.to_dict(orient='records'),
            columns=list(df.columns),
        )  



viz_types_list += [
    agGridViz,
    FilterBoxTreeViz,
    FilterBoxCombinationViz,
    FilterBoxCascadeViz,
    echartsBarViz,
    echartsBarHViz,
    echartsBarProgressViz,
    echartsLineBarViz,
    echartsPieHViz,
    echartPieHGViz,
    echartsDashboardViz,
    echartsBigNumberViz,
    echartsBubbleViz,
    echartsQuadrantViz,
    echartsLineViz,
    echartsPieMetricsViz,
    echartPieGViz,
    echartRadarMapViz,
    echartsBarWaterfallViz,
    echartsBigNumberCompareViz,
    echartsWordCloudViz,
    echartsTreeMapViz,
    ChinaMapViz,
    ChinaCityMapViz,
    echartsSankeyViz,
    echartsFunnel,
    echartsAreaStack,
    bigNumberViz,
    echartsChinaCityMapMigrationViz,
    bigNumberTwoViz,
    bigNumberThreeViz,
]
        
viz_types = OrderedDict([(v.viz_type, v) for v in viz_types_list
                         if v.viz_type not in config.get('VIZ_TYPE_BLACKLIST')])