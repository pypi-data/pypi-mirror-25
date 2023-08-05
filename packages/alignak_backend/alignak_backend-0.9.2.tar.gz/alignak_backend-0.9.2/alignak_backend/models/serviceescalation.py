#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Resource information of serviceescalation
"""


def get_name(friendly=False):
    """Get name of this resource

    :return: name of this resource
    :rtype: str
    """
    if friendly:
        return "Service escalation"
    return 'serviceescalation'


def get_doc():  # pragma: no cover
    """Get documentation of this resource

    :return: rst string
    :rtype: str
    """
    return """
    The ``serviceescalation`` model is used to define escalated notifications for the hosts.

    See the Alignak documentation regarding the escalations to discover all the features
    and the possibilities behind this Alignak feature.
    """


def get_schema():
    """Schema structure of this resource

    :return: schema dictionary
    :rtype: dict
    """
    return {
        'schema': {
            # Importation source
            'imported_from': {
                "title": "Imported from",
                "comment": "Item importation source (alignak-backend-import, ...)",
                'type': 'string',
                'default': 'unknown'
            },
            'definition_order': {
                "title": "Definition order",
                "comment": "Priority level if several elements have the same name",
                'type': 'integer',
                'default': 100
            },

            # Old and to be deprecated stuff...
            # todo: To be deprecated
            'first_notification': {
                "title": "First notification count",
                "comment": "Nagios legacy. Number of the first notification this "
                           "escalation will be used. **Note** that this property "
                           "will be deprecated in favor of the ``first_notification_time``.",
                'type': 'integer',
            },
            'last_notification': {
                "title": "Last notification count",
                "comment": "Nagios legacy. Number of the last notification this "
                           "escalation will not be used anymore. **Note** that this property "
                           "will be deprecated in favor of the ``last_notification_time``.",
                'type': 'integer',
            },

            # Identity
            'name': {
                "title": "Service escalation name",
                "comment": "Unique service escalation name",
                'type': 'string',
                'required': True,
                'empty': False,
                'unique': True,
            },
            'alias': {
                "title": "Alias",
                "comment": "Element friendly name used by the Web User Interface.",
                'type': 'string',
                'default': '',
            },
            'notes': {
                "title": "Notes",
                "comment": "Element notes. Free text to store element information.",
                'type': 'string',
                'default': '',
            },

            # Concerned items: services, hosts or hosts groups
            'services': {
                "title": "Services",
                "comment": "List of the services concerned by the escalation.",
                'type': 'list',
                'schema': {
                    'type': 'objectid',
                    'data_relation': {
                        'resource': 'service',
                        'embeddable': True,
                    }
                }
            },
            'hosts': {
                "title": "Hosts",
                "comment": "List of the hosts concerned by the escalation.",
                'type': 'list',
                'schema': {
                    'type': 'objectid',
                    'data_relation': {
                        'resource': 'host',
                        'embeddable': True,
                    }
                }
            },
            'hostgroups': {
                "title": "Hosts groups",
                "comment": "List of the hosts groups concerned by the escalation.",
                'type': 'list',
                'schema': {
                    'type': 'objectid',
                    'data_relation': {
                        'resource': 'hostgroup',
                        'embeddable': True,
                    }
                }
            },

            # Escalated notification sent-out time
            'first_notification_time': {
                "title": "First notification time",
                "comment": "Duration in minutes before sending the first escalated notification.",
                'type': 'integer',
                'default': 60
            },
            'last_notification_time': {
                "title": "Last notification time",
                "comment": "Duration in minutes before sending the last escalated notification. "
                           "Escalated notifications will be sent-out between the "
                           "first_notification_time and last_notification_time period.",
                'type': 'integer',
                'default': 240
            },
            'escalation_period': {
                "title": "Escalation time period",
                "comment": "No escalation notifications will be sent-out "
                           "except during this time period.",
                'type': 'objectid',
                'data_relation': {
                    'resource': 'timeperiod',
                    'embeddable': True
                }
            },
            'escalation_options': {
                "title": "Escalation options",
                "comment": "List of the notifications types this escalation is concerned with. "
                           "This escalation will be used only if the host is in one of the "
                           "states specified in this property.",
                'type': 'list',
                'default': ['w', 'c', 'x', 'r'],
                'allowed': ['w', 'c', 'x', 'r']
            },
            'notification_interval': {
                "title": "Notifications interval",
                "comment": "Number of minutes to wait before re-sending the escalated "
                           "notifications if the problem is still present. If you set this "
                           "value to 0, only one notification will be sent out.",
                'type': 'integer',
                'default': 60
            },

            # Notified users / users groups
            'users': {
                "title": "Escalation users",
                "comment": "List of the users concerned by this escalation.",
                'type': 'list',
                'schema': {
                    'type': 'objectid',
                    'data_relation': {
                        'resource': 'user',
                        'embeddable': True,
                    }
                },
                'required': True
            },
            'usergroups': {
                "title": "Escalation users groups",
                "comment": "List of the users groups concerned by this escalation.",
                'type': 'list',
                'schema': {
                    'type': 'objectid',
                    'data_relation': {
                        'resource': 'usergroup',
                        'embeddable': True,
                    }
                },
                'required': True
            },

            # Realm
            '_realm': {
                "title": "Realm",
                "comment": "Realm this element belongs to.",
                'type': 'objectid',
                'data_relation': {
                    'resource': 'realm',
                    'embeddable': True
                },
                'required': True,
            },
            '_sub_realm': {
                "title": "Sub-realms",
                "comment": "Is this element visible in the sub-realms of its realm?",
                'type': 'boolean',
                'default': True
            },

            # Users CRUD permissions
            '_users_read': {
                'type': 'list',
                'schema': {
                    'type': 'objectid',
                    'data_relation': {
                        'resource': 'user',
                        'embeddable': True,
                    }
                },
            },
            '_users_update': {
                'type': 'list',
                'schema': {
                    'type': 'objectid',
                    'data_relation': {
                        'resource': 'user',
                        'embeddable': True,
                    }
                },
            },
            '_users_delete': {
                'type': 'list',
                'schema': {
                    'type': 'objectid',
                    'data_relation': {
                        'resource': 'user',
                        'embeddable': True,
                    }
                },
            }
        }
    }
