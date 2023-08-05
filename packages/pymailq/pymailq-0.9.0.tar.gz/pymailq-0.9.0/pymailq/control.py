# coding: utf-8
#
#    Postfix queue control python tool (pymailq)
#
#    Copyright (C) 2014 Denis Pompilio (jawa) <denis.pompilio@gmail.com>
#
#    This file is part of pymailq
#
#    This program is free software; you can redistribute it and/or
#    modify it under the terms of the GNU General Public License
#    as published by the Free Software Foundation; either version 2
#    of the License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, see <http://www.gnu.org/licenses/>.

import time
import subprocess
from pymailq import CONFIG, debug


class QueueControl(object):
    """
    Postfix queue control using postsuper command.

    The :class:`~control.QueueControl` instance defines the following
    attributes:

        .. attribute:: use_sudo

            Boolean to control the use of `sudo` to invoke Postfix command.
            Default is ``False``

        .. attribute:: postsuper_cmd

            Postfix command and arguments :func:`list` for mails queue
            administrative operations. Default is ``["postsuper"]``

        .. attribute:: known_operations

            Known Postfix administrative operations :class:`dict` to associate
            operations to command arguments. Known associations are::

                 delete: -d
                   hold: -h
                release: -H
                requeue: -r

            .. warning::

                Default known associations are provided for the default mails
                queue administrative command `postsuper`_.

        .. seealso::

            Postfix manual:
                `postsuper`_ -- Postfix superintendent
    """

    @staticmethod
    def get_operation_cmd(operation):
        """Get operation related command from configuration

        This method use Postfix administrative commands defined
        in :attr:`pymailq.CONFIG` attribute under the key 'list_queue'.
        Command and arguments list is build on call with the configuration data.

        Command keys are built with the ``operation`` argument suffixed with
        ``_message``. Example: ``hold_message`` for the hold command.

        :param str operation: Operation name
        :return: Command and arguments as :class:`list`

        :raise KeyError: Operation is unknown

        .. seealso::

            :ref:`pymailq-configuration`
        """
        cmd = CONFIG['commands'][operation + '_message']
        if CONFIG['commands']['use_sudo']:
            cmd.insert(0, 'sudo')
        return cmd

    @debug
    def _operate(self, operation, messages):
        """
        Generic method to lead operations messages from postfix mail queue.

        Operations can be one of Postfix known operations stored in
        PyMailq module configuration.

        :param str operation: Known operation from :attr:`pymailq.CONFIG`.
        :param list messages: List of :class:`~store.Mail` objects targetted
                              for operation.
        :return: Command's *stderr* output lines
        :rtype: :func:`list`
        """
        # validate that object's attribute "qid" exist. Raise AttributeError.
        for msg in messages:
            getattr(msg, "qid")

        # We may modify this part to improve security.
        # It should not be possible to inject commands, but who knows...
        # https://www.kevinlondon.com/2015/07/26/dangerous-python-functions.html
        # And consider the use of sh module: https://amoffat.github.io/sh/
        operation_cmd = self.get_operation_cmd(operation) + ['-']
        try:
            child = subprocess.Popen(operation_cmd,
                                     stdin=subprocess.PIPE,
                                     stderr=subprocess.PIPE)
        except EnvironmentError as exc:
            command_str = " ".join(operation_cmd)
            error_msg = "Unable to call '%s': %s" % (command_str, str(exc))
            raise RuntimeError(error_msg)

        # If permissions error, the postsuper process takes ~1s to teardown.
        # Wait this delay and raise error message if process has stopped.
        time.sleep(1.1)
        child.poll()
        if child.returncode:
            raise RuntimeError(child.communicate()[1].strip().decode())

        try:
            for msg in messages:
                child.stdin.write((msg.qid+'\n').encode())
            stderr = child.communicate()[1].strip()
        except BrokenPipeError:
            raise RuntimeError("Unexpected error: child process has crashed")

        return [line.strip() for line in stderr.decode().split('\n')]

    def delete_messages(self, messages):
        """
        Delete several messages from postfix mail queue.

        This method is a :func:`~functools.partial` wrapper on
        :meth:`~control.QueueControl._operate`. Passed operation is ``delete``
        """
        return self._operate('delete', messages)

    def hold_messages(self, messages):
        """
        Hold several messages from postfix mail queue.

        This method is a :func:`~functools.partial` wrapper on
        :meth:`~control.QueueControl._operate`. Passed operation is ``hold``
        """
        return self._operate('hold', messages)

    def release_messages(self, messages):
        """
        Release several messages from postfix mail queue.

        This method is a :func:`~functools.partial` wrapper on
        :meth:`~control.QueueControl._operate`. Passed operation is ``release``
        """
        return self._operate('release', messages)

    def requeue_messages(self, messages):
        """
        Requeue several messages from postfix mail queue.

        This method is a :func:`~functools.partial` wrapper on
        :meth:`~control.QueueControl._operate`. Passed operation is ``requeue``
        """
        return self._operate('requeue', messages)
