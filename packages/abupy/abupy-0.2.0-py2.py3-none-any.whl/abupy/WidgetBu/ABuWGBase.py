# -*- encoding:utf-8 -*-
"""股票基本信息图形可视化"""

from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import logging

import ipywidgets as widgets

from abc import ABCMeta, abstractmethod
from IPython.display import display

from ..CoreBu import ABuEnv
from ..CoreBu.ABuFixes import six
from ..UtilBu.ABuStrUtil import to_unicode
from ..MarketBu.ABuSymbol import search_to_symbol_dict

__author__ = '阿布'
__weixin__ = 'abu_quant'

"""基于不同系统的提示框使用partial包装title以及显示log"""
# show_msg_func = partial(show_msg, '提示', log=True)
show_msg_func = logging.info


def browser_down_csv_zip(open_browser=False):
    """浏览器打开教程使用的csv数据百度云地址"""
    try:
        if open_browser:
            import webbrowser
            webbrowser.open('https://pan.baidu.com/s/1geNZgqf', new=0, autoraise=True)
            show_msg_func(u'提取密码: gvtr')
    except:
        pass
    finally:
        logging.info(u'建议直接从百度云下载教程中使用的csv格式美股，A股，港股，币类，期货6年日k数据: ')
        logging.info(u'下载地址: https://pan.baidu.com/s/1geNZgqf')
        logging.info(u'提取密码: gvtr')
        logging.info(u'下载完成后解压zip得到\'csv\'文件夹到\'{}\'目录下'.format(ABuEnv.g_project_data_dir))


# noinspection PyUnresolvedReferences,PyProtectedMember
class WidgetBase(object):
    """界面组件基类，限定最终widget为self.widget"""

    def __call__(self):
        return self.widget

    def display(self):
        """显示使用统一display"""
        display(self.widget)


class WidgetFactorBase(six.with_metaclass(ABCMeta, WidgetBase)):
    """策略可视化基础类"""

    def __init__(self, wg_manager):
        self.wg_manager = wg_manager
        self.widget = None
        self.label_layout = widgets.Layout(width='300px', align_items='stretch')
        self.description_layout = widgets.Layout(height='150px')
        self.widget_layout = widgets.Layout(align_items='stretch', justify_content='space-between')

    @abstractmethod
    def _init_widget(self):
        """子类因子界面设置初始化"""
        pass

    @abstractmethod
    def delegate_class(self):
        """子类因子所委托的具体因子类"""
        pass


class WidgetFactorManagerBase(six.with_metaclass(ABCMeta, WidgetBase)):
    """策略管理可视化基础类"""

    def __init__(self):
        self.factor_dict = {}
        self.factor_wg_array = []
        # 策略候选池可x轴左右滚动
        self.factor_layout = widgets.Layout(overflow_x='scroll',
                                            flex_direction='row',
                                            display='flex')
        self.selected_factors = widgets.SelectMultiple(
            options=[],
            description=u'已添加的全局策略:',
            disabled=False,
            layout=widgets.Layout(width='100%', align_items='stretch')
        )
        # 已添加的全局策略可点击删除
        self.selected_factors.observe(self.remove_factor, names='value')
        # 全局策略改变通知接收序列
        self.selected_factors_obs = set()
        self.factor_box = None
        # 默认不启动可滚动因子界面，因为对外的widget版本以及os操作系统不统一
        self.scroll_factor_box = False
        # 构建具体子类的界面构建
        self._init_widget()
        if self.factor_box is None:
            raise RuntimeError('_init_widget must build factor_box!')
        self.widget = widgets.VBox([self.factor_box, self.selected_factors])

    def _sub_children(self, children, n_split):
        """将children每n_split个为一组，组装子children_group序列"""
        sub_children_cnt = int(len(children) / n_split)
        if sub_children_cnt == 0:
            sub_children_cnt = 1
        group_adjacent = lambda a, k: zip(*([iter(a)] * k))
        children_group = list(group_adjacent(children, sub_children_cnt))
        residue_ind = -(len(children) % sub_children_cnt) if sub_children_cnt > 0 else 0
        if residue_ind < 0:
            children_group.append(children[residue_ind:])
        return children_group

    def register_subscriber(self, observe):
        """注册已选策略池更新通知与BFSubscriberMixin共同作用"""
        self.selected_factors_obs.add(observe)

    def unregister_subscriber(self, observe):
        """解除注册已选策略池更新通知与BFSubscriberMixin共同作用"""
        self.selected_factors_obs.remove(observe)

    def notify_subscriber(self):
        """通知已选策略池发生改变的observe"""
        for observe in self.selected_factors_obs:
            if hasattr(observe, 'notify_subscriber'):
                observe.notify_subscriber()

    @abstractmethod
    def _init_widget(self):
        """子类因子界面设置初始化, 内部需要构建self.factor_box"""
        pass

    def refresh_factor(self):
        """已选策略池刷新，通知其它更新"""
        self.selected_factors.options = list(self.factor_dict.keys())
        self.notify_subscriber()

    def remove_factor(self, select):
        """点击从策略池中删除已选择的策略"""
        for st_key in list(select['new']):
            self.factor_dict.pop(st_key)
        self.selected_factors.options = list(self.factor_dict.keys())
        # 通知其它需要一起更新的界面进行更新
        self.notify_subscriber()

    def add_factor(self, factor_dict, factor_desc_key):
        """根据具体策略提供的策略字典对象和策略描述构建上层策略序列"""
        if factor_desc_key in self.factor_dict:
            msg = u'{} 策略已经添加过，重复添加！'.format(factor_desc_key)
            show_msg_func(msg)
            return
        self.factor_dict[factor_desc_key] = factor_dict
        self.selected_factors.options = list(self.factor_dict.keys())
        # 通知其它需要一起更新的界面进行更新
        self.notify_subscriber()


class WidgetSearchBox(WidgetBase):
    """搜索框ui界面"""

    # noinspection PyProtectedMember
    def __init__(self, search_result_callable):
        """构建股票池选股ui界面"""
        if not callable(search_result_callable):
            raise TypeError('search_result_select_func must callable!')
        # symbol搜索框构建
        self.search_bt = widgets.Button(description=u'搜索:', layout=widgets.Layout(height='10%', width='7%'))
        self.search_input = widgets.Text(
            value='',
            placeholder=u'交易代码/公司名称/拼音首字母',
            description='',
            disabled=False
        )
        self.search_input.observe(self._search_input_change, names='value')

        # symbol搜索结果框
        self.search_result = widgets.SelectMultiple(
            options=[],
            description=u'搜索结果:',
            disabled=False,
            layout=widgets.Layout(width='300px', align_items='stretch', justify_content='space-between')
        )
        self.search_result.observe(search_result_callable, names='value')
        self.search_bt.on_click(self._do_search)

        # 搜索框 ＋ 按钮 ＋ 结果框 box拼接
        sc_hb = widgets.HBox([self.search_bt, self.search_input])
        self.widget = widgets.VBox([sc_hb, self.search_result])

    # noinspection PyUnusedLocal
    def _do_search(self, bt):
        """搜索框搜索执行函数"""
        result_dict = search_to_symbol_dict(self.search_input.value)
        result_options = [u'{}:{}'.format(to_unicode(result_dict[symbol]), to_unicode(symbol))
                          for symbol in result_dict]
        self.search_result.options = result_options

    def _search_input_change(self, change):
        """当搜索输入框文字大于1个进行自动搜索"""
        search_word = change['new']
        if len(search_word) > 1:
            # 和_do_search不同这里使用fast_mode
            result_dict = search_to_symbol_dict(self.search_input.value, fast_mode=True)
            result_options = [u'{}:{}'.format(to_unicode(result_dict[symbol]), to_unicode(symbol))
                              for symbol in result_dict]
            self.search_result.options = result_options
