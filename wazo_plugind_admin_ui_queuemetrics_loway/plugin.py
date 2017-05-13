# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+


from flask_menu.classy import register_flaskview
from flask_menu.classy import classy_menu_item

from wazo_admin_ui.helpers.plugin import create_blueprint
from wazo_admin_ui.helpers.classful import BaseView
from wazo_admin_ui.helpers.form import BaseForm

from wtforms.fields import SubmitField, StringField
from wtforms.validators import InputRequired, Length, Regexp


queuemetrics = create_blueprint('queuemetrics', __name__)


class Plugin(object):

    def load(self, dependencies):
        core = dependencies['flask']

        QueuemetricsView.service = QueuemetricsService()
        QueuemetricsView.register(queuemetrics, route_base='/queuemetrics')
        register_flaskview(queuemetrics, QueuemetricsView)

        core.register_blueprint(queuemetrics)


class QueuemetricsForm(BaseForm):
    live_id = StringField('Live ID', [InputRequired(), Length(max=128)])
    password = StringField('Password', 
                           [Length(max=80), Regexp(r'^[0-9]+$')],
                           render_kw={'type': 'password',
                                      'data_toggle': 'password'})
    submit = SubmitField('Submit')


class QueuemetricsView(BaseView):

    form = QueuemetricsForm
    resource = 'queuemetrics'

    @classy_menu_item('.queuemetrics', 'Queuemetrics', order=10, icon="bar-chart")
    def index(self):
        return super(QueuemetricsView, self).index()
