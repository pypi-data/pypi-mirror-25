# Copyright 2017 Workonline Communications (Pty) Ltd. All rights reserved.
#
# The contents of this file are licensed under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with the
# License. You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.
"""Looking Glass management commands for djangolg."""

from __future__ import print_function
from __future__ import unicode_literals

from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError

from djangolg import dialects, models


class Command(BaseCommand):
    """Definition of 'lg' management command."""

    help = "Manage Looking Glass Configuration"
    hr = "----"
    commands = [
        "list",
        "show",
        "add",
        "modify",
        "delete",
    ]
    objects = [
        "routers",
        "credentials",
        "locations"
    ]
    credential_types = dict(models.Credential.CRED_TYPE_CHOICES)

    def add_arguments(self, parser):
        """Define command args."""
        parser.add_argument(
            'CMD', choices=self.commands,
            help="Operation to perform"
        )
        parser.add_argument(
            'OBJ', choices=self.objects,
            help="Type of object to manage"
        )
        parser.add_argument(
            '--index', '-I',
            help="Index of the object to manage"
        )
        parser.add_argument(
            '--name', '--hostname', '-n',
            type=str,
            help="Name (or hostname) of object"
        )
        parser.add_argument(
            '--location', '-l',
            type=int,
            help="Index of related location"
        )
        parser.add_argument(
            '--credentials', '-c',
            type=int,
            help="Index of related credentials"
        )
        parser.add_argument(
            '--dialect', '-d',
            choices=dialects.available_dialects(output="list"),
            help="Name of related dialect"
        )
        parser.add_argument(
            '--sitecode', '-s',
            type=str,
            help="Location site code"
        )
        parser.add_argument(
            '--type', '-t',
            type=int,
            choices=self.credential_types.keys(),
            help="Credential type"
        )
        parser.add_argument(
            '--username', '-u',
            type=str,
            help="Credential username"
        )
        parser.add_argument(
            '--password', '-p',
            type=str,
            help="Credential password"
        )
        parser.add_argument(
            '--key', '-k',
            help="Credential key - not yet implemented"
        )

    def handle(self, *args, **options): # noqa
        """Run command."""
        obj = options['OBJ']
        if obj == 'routers':
            cls = models.Router
        elif obj == 'credentials':
            cls = models.Credential
        elif obj == 'locations':
            cls = models.Location
        else:
            raise CommandError("Invalid object type")  # pragma: no cover
        cmd = options['CMD']
        if cmd == 'list':
            self.list(cls)
        elif cmd == 'add':
            inst = self.add(cls, options)
            self.show(inst)
        else:
            if 'index' in options:
                index = options['index']
            else:  # pragma: no cover
                raise CommandError(
                    "Please provide object index argument (--index)")
            try:
                inst = cls.objects.get(id=index)
            except Exception:
                raise CommandError("No %s found with index %s" % (obj, index))
            if cmd == 'show':
                self.show(inst)
            elif cmd == 'modify':
                inst = self.set(inst, options)
                self.show(inst)
            elif cmd == 'delete':
                self.delete(inst)
            else:
                raise CommandError("Invalid command")  # pragma: no cover

    def list(self, cls=None):
        """Run 'list' subcommand."""
        hr = self.hr
        objects = cls.objects.all()
        count = objects.count()
        if cls == models.Router:
            self.stdout.write(hr)
            self.stdout.write("Configured Routers")
            self.stdout.write(hr)
            if count:
                for r in objects:
                    self.stdout.write(
                        "Index: {0}\tHostname: {1}".format(r.id, r.hostname))
            else:
                self.stdout.write("No routers configured")
            self.stdout.write(hr)
        elif cls == models.Credential:
            self.stdout.write(hr)
            self.stdout.write("Configured Credentials")
            self.stdout.write(hr)
            if count:
                for c in objects:
                    self.stdout.write("Index: %s\tName: %s" % (c.id, c.name))
            else:
                self.stdout.write("No credentials configured")
            self.stdout.write(hr)
        elif cls == models.Location:
            self.stdout.write(hr)
            self.stdout.write("Configured Locations")
            self.stdout.write(hr)
            if count:
                for l in objects:
                    self.stdout.write("Index: %s\tName: %s" % (l.id, l.name))
            else:
                self.stdout.write("No locations configured")
            self.stdout.write(hr)

    def show(self, inst=None):
        """Run 'show' subcommand."""
        hr = self.hr
        cls = type(inst)
        if cls == models.Router:
            self.stdout.write(hr)
            self.stdout.write("Router index: %s" % inst.id)
            self.stdout.write(hr)
            self.stdout.write("Hostname: %s" % inst.hostname)
            self.stdout.write("Location: %s" % inst.location)
            self.stdout.write("Credentials: %s" % inst.credentials)
            self.stdout.write("Dialect: %s" % inst.dialect)
            self.stdout.write(hr)
        elif cls == models.Credential:
            self.stdout.write(hr)
            self.stdout.write("Credential index: %s" % inst.id)
            self.stdout.write(hr)
            self.stdout.write("Name: %s" % inst.name)
            self.stdout.write("Type: %s" % self.credential_types[inst.type])
            self.stdout.write("Username: %s" % inst.username)
            self.stdout.write(hr)
        elif cls == models.Location:
            self.stdout.write(hr)
            self.stdout.write("Location index: %s" % inst.id)
            self.stdout.write(hr)
            self.stdout.write("Name: %s" % inst.name)
            self.stdout.write("Site Code: %s" % inst.sitecode)
            self.stdout.write(hr)

    def not_implemented(self, cmd):  # pragma: no cover
        """Raise error on not implemented."""
        msg = "Command %s is not yet implemented" % cmd
        raise CommandError(msg)

    def add(self, cls, options):
        """Run 'add' subcommand."""
        inst = self.set(cls(), options)
        return inst

    def set(self, inst, options): # noqa
        """Run 'set' subcommand."""
        cls = type(inst)
        if cls == models.Router:
            if options['name']:
                inst.hostname = options['name']
            if options['location']:
                location = models.Location.objects.get(id=options['location'])
                inst.location = location
            if options['credentials']:
                credentials = models.Credential.objects.get(
                    id=options['credentials'])
                inst.credentials = credentials
            if options['dialect']:
                inst.dialect = options['dialect']
        elif cls == models.Credential:
            if options['name']:
                inst.name = options['name']
            if options['type'] in self.credential_types:
                inst.type = options['type']
            if options['username']:
                inst.username = options['username']
            if options['password']:
                inst.password = options['password']
        elif cls == models.Location:
            if options['name']:
                inst.name = options['name']
            if options['sitecode']:
                inst.sitecode = options['sitecode']
        try:
            inst.save()
        except IntegrityError:  # pragma: no cover
            raise
        except Exception:  # pragma: no cover
            raise CommandError("Save failed")
        return inst

    def delete(self, inst):
        """Run 'delete' subcommand."""
        try:
            inst.delete()
        except Exception:  # pragma: no cover
            raise CommandError("Delete failed")
