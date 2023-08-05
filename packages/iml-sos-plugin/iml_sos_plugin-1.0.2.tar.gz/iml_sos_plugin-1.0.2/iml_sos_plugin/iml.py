# Copyright (c) 2017 Intel Corporation. All rights reserved.
# Use of this source code is governed by a MIT-style
# license that can be found in the LICENSE file.

from os import path
from datetime import datetime

from sos.plugins import Plugin, RedHatPlugin


class IML(Plugin, RedHatPlugin):
    """IML Framework
    """

    plugin_name = "iml"
    profiles = ('lustre',)
    requires_root = True

    def setup(self):
        limit = self.get_option("log_size", default=0)
        all_logs = self.get_option("all_logs", default=False)

        if all_logs:
            copy_globs = [
                "/var/log/chroma/",
                "/var/log/chroma-agent*",
            ]
        else:
            copy_globs = [
                "/var/log/chroma/*.log",
                "/var/log/chroma-agent*.log",
            ]

        copy_globs = copy_globs + ["/var/lib/chroma/settings/*", "/var/lib/chroma/targets/*"]

        [self.add_copy_spec_limit(x, sizelimit=limit) for x in copy_globs]

        self.add_cmd_output([
            'chroma-agent device_plugin --plugin=linux',
            'chroma-agent detect_scan',
            'chroma-config validate',
            'chroma-agent device_plugin --plugin=linux_network',
            'lctl device_list',
            'lctl_kernel debug_kernel',
            'blkid -s UUID -s TYPE',
            'df --all',
            'ps -ef --forest',
            'cibadmin --query',
        ])

        time_stamp = datetime.now().strftime("%Y%m%dT%H%M%S")
        db_file_name = 'chromadb_%s.sql.gz' % time_stamp
        db_dest = path.join(self.get_cmd_output_path(), db_file_name)

        self.get_command_output(
            'pg_dump -U chroma -F p -Z 9 -w -f %s -T chroma_core_logmessage -T'
            ' chroma_core_series -T chroma_core_sample_* chroma' % db_dest
        )

        self.add_cmd_output(
            "rpm -V chroma-agent chroma-agent-management chroma-manager"
            " chroma-manager-cli chroma-manager-libs",
            suggest_filename="finger-print"
        )

        self.add_cmd_output(
            "rpm -qa",
            suggest_filename="rpm_packges_installed"
        )

        self.add_cmd_output(
            "rabbitmqctl list_queues -p chromavhost",
            suggest_filename="rabbit_queue_status"
        )

# vim: set et ts=4 sw=4 :
