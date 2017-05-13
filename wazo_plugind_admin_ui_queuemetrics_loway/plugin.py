# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+


import json
from urlparse import urlparse

from flask_menu.classy import register_flaskview
from flask_menu.classy import classy_menu_item

from wazo_admin_ui.helpers.plugin import create_blueprint
from wazo_admin_ui.helpers.classful import BaseView
from wazo_admin_ui.helpers.form import BaseForm

from wtforms.fields import SubmitField, StringField
from wtforms.validators import InputRequired, Length, Regexp


queuemetrics = create_blueprint('queuemetrics', __name__)
configfile = '/etc/uniloader/uniloader.json'

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
                           [Length(max=80)],
                           render_kw={'type': 'password',
                                      'data_toggle': 'password'})
    submit = SubmitField('Submit')


class QueuemetricsView(BaseView):

    form = QueuemetricsForm
    resource = 'queuemetrics'

    @classy_menu_item('.queuemetrics', 'Queuemetrics', order=10, icon="bar-chart")
    def index(self):
        return super(QueuemetricsView, self).get(None)

    def _map_resources_to_form(self, resource):
        o = urlparse(resource[0].get('uri'))
        live_id = o.path.split('/')[1]
        data = {
            'live_id': live_id,
            'password': resource[0].get('pass')
        }
        form = self.form(data=data)
        return form


class QueuemetricsService(object):

    def get(self, arg):
        return self._read_config()

    def update(self, resource):
        config = self._read_config()
        config[0]['uri'] = 'https://my.queuemetrics-live.com/{}'.format(resource.get('live_id'))
        config[0]['pass'] = resource.get('password')

        with open(configfile, 'w') as outfile:
            json.dump(config, outfile, indent = 4)
        return True

    def _read_config(self):
        with open(configfile) as json_data:
            return json.load(json_data)
