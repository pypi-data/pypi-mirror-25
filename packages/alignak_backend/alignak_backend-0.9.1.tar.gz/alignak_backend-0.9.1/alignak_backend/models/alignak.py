#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Resource information of Alignak
"""


def get_name(friendly=False):
    """Get name of this resource

    :return: name of this resource
    :rtype: str
    """
    if friendly:  # pragma: no cover
        return "Alignak configuration"
    return 'alignak'


def get_doc():  # pragma: no cover
    """Get documentation of this resource

    :return: rst string
    :rtype: str
    """
    return """
    The ``alignak`` model is used to store the global configuration of an Alignak instance.

    """


def get_schema():
    """Schema structure of this resource

    Some fields are defined  but this resource allows to store some other fields that may be some
    macros definition.

    Note that the `name` field is 1) not unique, 2) used as a reference for the Arbiter match.

    The configuration for an Alignak Arbiter named as 'arbiter-master' may be dispatched into
    several items in this collection with the same name field.

    :return: schema dictionary
    :rtype: dict
    """
    return {
        'allow_unknown': True,
        'schema': {
            'name': {
                "title": "Alignak name",
                "comment": "Alignak instance name. This will be compared to the Alignak arbiter "
                           "instance name to get the correct configuration.",
                'type': 'string',
                'required': True,
                'unique': False,
                'empty': False,
            },
            'alias': {
                "title": "Alias",
                "comment": "Element friendly name used by the Web User Interface.",
                'type': 'string',
                'default': ''
            },
            'notes': {
                "title": "Notes",
                "comment": "Element notes. Free text to store element information.",
                'type': 'string',
                'default': ''
            },
            'notes_url': {
                "title": "Notes URL",
                "comment": "Element notes URL. Displayed in the Web UI as some URL to be "
                           "navigatesd. Note that a very specific text format must be used for "
                           "this field, see the Web UI documentation.",
                'type': 'string',
                'default': ''
            },

            # Global Alignak status
            'instance_name': {
                "title": "Instance name",
                "comment": "Reporting daemon name",
                'type': 'string'
            },
            'instance_id': {
                "title": "Instance identifier",
                "comment": "Reporting daemon identifier",
                'type': 'string'
            },

            'pid': {
                "title": "Instance PID",
                "comment": "Reporting daemon PID",
                'type': 'integer',
                'default': 0
            },

            'program_start': {
                "title": "Program start time",
                "comment": "Date/time the Alignak scheduler started/restarted",
                'type': 'integer',
                'default': 0
            },
            'last_alive': {
                "title": "Last time alive",
                "comment": "Date/time of this status report",
                'type': 'integer',
                'default': 0
            },

            # Global Alignak configuration
            'interval_length': {
                "title": "Application interval length",
                "comment": "Default is 60 seconds for one minute",
                'type': 'integer',
                'default': 60
            },
            'use_timezone': {
                "title": "Alignak time zone",
                "comment": "",
                'type': 'string',
                'default': ''
            },
            'illegal_macro_output_chars': {
                "title": "Illegal macros output characters",
                "comment": "",
                'type': 'string',
                'default': ''
            },
            'illegal_object_name_chars': {
                "title": "Illegal objects name characters",
                "comment": "",
                'type': 'string',
                'default': """`~!$%^&*"|'<>?,()="""
            },
            'cleaning_queues_interval': {
                "title": "Scheduler queues cleaning interval",
                "comment": "Default is 15 minutes (900 seconds)",
                'type': 'integer',
                'default': 900
            },
            'max_plugins_output_length': {
                "title": "Maximum check output length",
                "comment": "Default is 8192 bytes",
                'type': 'integer',
                'default': 8192
            },
            'enable_environment_macros': {
                "title": "Enable environment macros",
                "comment": "Enable to provide environment variables as macros to the "
                           "launched commands. Default is disabled.",
                'type': 'boolean',
                'default': False
            },

            # Monitoring logs configuration
            'log_initial_states': {
                "title": "Log objects initial states",
                "comment": "Create a monitoring log event for this event",
                'type': 'boolean',
                'default': True
            },
            'log_active_checks': {
                "title": "Log objects active checks",
                "comment": "Create a monitoring log event for this event",
                'type': 'boolean',
                'default': True
            },
            'log_host_retries': {
                "title": "Log hosts checks retries",
                "comment": "Create a monitoring log event for this event",
                'type': 'boolean',
                'default': True
            },
            'log_service_retries': {
                "title": "Log services checks retries",
                "comment": "Create a monitoring log event for this event",
                'type': 'boolean',
                'default': True
            },
            'log_passive_checks': {
                "title": "Log objects passive checks",
                "comment": "Create a monitoring log event for this event",
                'type': 'boolean',
                'default': True
            },
            'log_notifications': {
                "title": "Log notifications",
                "comment": "Create a monitoring log event for this event",
                'type': 'boolean',
                'default': True
            },
            'log_event_handlers': {
                "title": "Log objects event handlers",
                "comment": "Create a monitoring log event for this event",
                'type': 'boolean',
                'default': True
            },
            'log_external_commands': {
                "title": "Log external commands",
                "comment": "Create a monitoring log event for this event",
                'type': 'boolean',
                'default': True
            },
            'log_flappings': {
                "title": "Log objects states flapping",
                "comment": "Create a monitoring log event for this event",
                'type': 'boolean',
                'default': True
            },
            'log_snapshots': {
                "title": "Log objects snapshots",
                "comment": "Create a monitoring log event for this event",
                'type': 'boolean',
                'default': True
            },

            # Notifications configuration
            'enable_notifications': {
                "title": "Notifications enabled",
                "comment": "Raising notifications is enabled. Default is True",
                'type': 'boolean',
                'default': True
            },
            'notification_timeout': {
                "title": "Notification commands timeout",
                "comment": "Default is 30 seconds",
                'type': 'integer',
                'default': 30
            },
            'timeout_exit_status': {
                "title": "Command timeout exit status",
                "comment": "Default is 2 (CRITICAL)",
                'type': 'integer',
                'default': 2
            },

            # Active checks configuration
            'execute_host_checks': {
                "title": "Active host checks enabled",
                "comment": "",
                'type': 'boolean',
                'default': True
            },
            'max_host_check_spread': {
                "title": "Maximum hosts checks spread",
                "comment": "Default is 30 seconds",
                'type': 'integer',
                'default': 30
            },
            'host_check_timeout': {
                "title": "Hosts checks commands timeout",
                "comment": "Default is 30 seconds",
                'type': 'integer',
                'default': 30
            },
            'check_for_orphaned_hosts': {
                "title": "Check for orphaned hosts",
                "comment": "",
                'type': 'boolean',
                'default': True
            },
            'execute_service_checks': {
                "title": "Active service checks enabled",
                "comment": "",
                'type': 'boolean',
                'default': True
            },
            'max_service_check_spread': {
                "title": "Maximum services checks spread",
                "comment": "Default is 30 seconds",
                'type': 'integer',
                'default': 30
            },
            'service_check_timeout': {
                "title": "Services checks commands timeout",
                "comment": "Default is 60 seconds",
                'type': 'integer',
                'default': 60
            },
            'check_for_orphaned_services': {
                "title": "Check for orphaned services",
                "comment": "",
                'type': 'boolean',
                'default': True
            },

            # Flapping configuration
            'flap_detection_enabled': {
                "title": "Flapping detection enabled",
                "comment": "",
                'type': 'boolean',
                'default': True
            },
            'flap_history': {
                "title": "Flapping history",
                "comment": "Number of states for flapping computing",
                'type': 'integer',
                'default': 20
            },
            'low_host_flap_threshold': {
                "title": "Host low flapping threshold",
                "comment": "",
                'type': 'integer',
                'default': 20
            },
            'high_host_flap_threshold': {
                "title": "Host high flapping threshold",
                "comment": "",
                'type': 'integer',
                'default': 30
            },
            'low_service_flap_threshold': {
                "title": "Service low flapping threshold",
                "comment": "",
                'type': 'integer',
                'default': 20
            },
            'high_service_flap_threshold': {
                "title": "Service high flapping threshold",
                "comment": "",
                'type': 'integer',
                'default': 30
            },

            # Event handlers
            'event_handlers_enabled': {
                "title": "Event handlers enabled",
                "comment": "",
                'type': 'boolean',
                'default': True
            },
            'event_handler_timeout': {
                "title": "Event handlers commands timeout",
                "comment": "Default is 30 seconds",
                'type': 'integer',
                'default': 30
            },
            'no_event_handlers_during_downtimes': {
                "title": "Event handlers launched when object is in a downtime period",
                "comment": "",
                'type': 'boolean',
                'default': False
            },
            'global_host_event_handler': {
                "title": "Global host event handler",
                "comment": "Command that will be used as an event handler "
                           "if none is specified for a specific host/service.",
                'type': 'string',
                'default': 'None'
            },
            'global_service_event_handler': {
                "title": "Global service event handler",
                "comment": "Command that will be used as an event handler "
                           "if none is specified for a specific host/service.",
                'type': 'string',
                'default': 'None'
            },

            # Performance data - deprecate this
            'process_performance_data': {
                "title": "Process performance data",
                "comment": "Enable / disable the performance data extra management",
                'type': 'boolean',
                'default': True
            },
            'host_perfdata_command': {
                "title": "Host performance data command",
                "comment": "Command that will be run for the performance data of an host.",
                'type': 'string',
                'default': 'None'
            },
            'service_perfdata_command': {
                "title": "Service performance data command",
                "comment": "Command that will be run for the performance data of a service.",
                'type': 'string',
                'default': 'None'
            },

            # Passive/Freshness check
            'accept_passive_host_checks': {
                "title": "Passive host checks enabled",
                "comment": "Accept passive hosts checks. Default is True",
                'type': 'boolean',
                'default': True
            },
            'check_host_freshness': {
                "title": "Host checks freshness check",
                "comment": "Host checks freshness is enabled/disabled. Default is True",
                'type': 'boolean',
                'default': True
            },
            'host_freshness_check_interval': {
                "title": "Host freshness check interval",
                "comment": "Default is one hour (3600 seconds)",
                'type': 'integer',
                'default': 3600
            },
            'accept_passive_service_checks': {
                "title": "Passive service checks enabled",
                "comment": "Accept passive services checks",
                'type': 'boolean',
                'default': True
            },
            'check_service_freshness': {
                "title": "Passive service checks enabled",
                "comment": "Accept passive services checks",
                'type': 'boolean',
                'default': True
            },
            'service_freshness_check_interval': {
                "title": "Service freshness check interval",
                "comment": "Default is one hour (3600 seconds)",
                'type': 'integer',
                'default': 30
            },
            'additional_freshness_latency': {
                "title": "Additional freshness latency",
                "comment": "Extra time for the freshness check - default is 15 seconds",
                'type': 'integer',
                'default': 15
            },

            # External commands
            'check_external_commands': {
                "title": "Check external commands",
                "comment": "Enable / disable the external commands management",
                'type': 'boolean',
                'default': True
            },

            '_realm': {
                'type': 'objectid',
                'data_relation': {
                    'resource': 'realm',
                    'embeddable': True
                },
                'required': True,
            },
            '_sub_realm': {
                'type': 'boolean',
                'default': True
            },
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
            },
        }
    }
