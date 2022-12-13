# -*- coding: utf-8 -*- #
# Copyright 2022 Google LLC. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Command to show fleet information."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from googlecloudsdk.api_lib.container.fleet import client
from googlecloudsdk.calliope import base
from googlecloudsdk.command_lib.container.fleet import resources


@base.Hidden
@base.ReleaseTracks(base.ReleaseTrack.ALPHA)
class Describe(base.DescribeCommand):
  """Show fleet namespace info.

  This command can fail for the following reasons:
  * The project specified does not exist.
  * The namespace specified does not exist in the project.
  * The caller does not have permission to access the namespace.

  ## EXAMPLES

  To print metadata for the namespace `test-ns` in project `foo-bar-1`,
  run:

    $ {command} test-ns --project=foo-bar-1
  """

  @staticmethod
  def Args(parser):
    resources.AddRBACResourceArg(
        parser,
        api_version='v1alpha',
        rbacrb_help=('Name of the RBAC RoleBinding to be created. '
                     'Must comply with RFC 1123 (up to 63 characters, '
                     'alphanumeric and \'-\')'))

  def Run(self, args):
    fleetclient = client.FleetClient(release_track=base.ReleaseTrack.ALPHA)
    return fleetclient.GetRBACRoleBinding(resources.RBACResourceName(args))
