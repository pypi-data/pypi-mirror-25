# -*- coding: utf-8 -*-
#########################################################################
#
# Copyright (C) 2016 OSGeo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
#########################################################################

from geonode import settings

THUNDERFOREST = {
    'maps': {
        'cycle': {
            'enabled': True,
            'name': 'Thunderforest OpenCycleMap',
            'visibility': False,
        },
        'transport': {
            'enabled': True,
            'name': 'Thunderforest Transport',
            'visibility': False,
        },
        'transport-dark': {
            'enabled': True,
            'name': 'Thunderforest Transport Dark',
            'visibility': False,
        },
        'spinal-map': {
            'enabled': True,
            'name': 'Thunderforest Spinal Map',
            'visibility': False,
        },
        'landscape': {
            'enabled': True,
            'name': 'Thunderforest Landscape',
            'visibility': False,
        },
        'outdoors': {
            'enabled': True,
            'name': 'Thunderforest Outdoors',
            'visibility': False,
        },
        'pioneer': {
            'enabled': True,
            'name': 'Thunderforest Pioneer',
            'visibility': False,
        }
    }
}
ATTRIBUTION = ('&copy; <a href="http://www.thunderforest.com/">Thunderforest</'
               'a>, &copy; <a href="http://www.openstreetmap.org/copyright">Op'
               'enStreetMap</a>')
for k, v in THUNDERFOREST['maps'].items():
    URL = 'http://a.tile.thunderforest.com/%s/${z}/${x}/${y}.png' % k
    if v['enabled']:
        BASEMAP = {
            'source': {
                'ptype': 'gxp_olsource'
            },
            'type': 'OpenLayers.Layer.XYZ',
            "args": [
                '%s' % v['name'],
                [URL],
                {
                    'transitionEffect': 'resize',
                    'attribution': '%s' % ATTRIBUTION,
                }
            ],
            'fixed': True,
            'visibility': v['visibility'],
            'group': 'background'
        }
        settings.MAP_BASELAYERS.append(BASEMAP)
