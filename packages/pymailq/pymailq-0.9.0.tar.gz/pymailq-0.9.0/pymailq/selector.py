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

import gc
from functools import wraps
from datetime import datetime
from pymailq import debug


class MailSelector(object):
    """
    Mail selector class to request mails from store matching criterias.

    The :class:`~selector.MailSelector` instance provides the following
    attributes:

        .. attribute:: mails

            Currently selected :class:`~store.Mail` objects :func:`list`

        .. attribute:: store

            Linked :class:`~store.PostqueueStore` at the
            :class:`~selector.MailSelector` instance initialization.

        .. attribute:: filters

            Applied filters :func:`list` on current selection. Filters list
            entries are tuples containing ``(function.__name__, args, kwargs)``
            for each applied filters. This list is filled by the
            :meth:`~selector.MailSelector.filter_registration` decorator while
            calling filtering methods. It is possible to replay registered
            filter using :meth:`~selector.MailSelector.replay_filters` method.
    """
    def __init__(self, store):
        """Init method"""
        self.mails = []
        self.store = store
        self.filters = []

        self.reset()

    def filter_registration(function):
        """
        Decorator to register applied filter.

        This decorated is used to wrap selection methods ``lookup_*``. It
        registers a ``(function.__name__, args, kwargs)`` :func:`tuple` in
        the :attr:`~MailSelector.filters` attribute.
        """
        @wraps(function)
        def wrapper(self, *args, **kwargs):
            filterinfo = (function.__name__, args, kwargs)
            self.filters.append(filterinfo)
            return function(self, *args, **kwargs)
        return wrapper

    def reset(self):
        """
        Reset mail selector with initial store mails list.

        Selected :class:`~store.Mail` objects are deleted and the
        :attr:`~MailSelector.mails` attribute is removed for memory releasing
        purpose (with help of :func:`gc.collect`). Attribute
        :attr:`~MailSelector.mails` is then reinitialized a copy of
        :attr:`~MailSelector.store`'s :attr:`~PostqueueStore.mails` attribute.

        Registered :attr:`~MailSelector.filters` are also emptied.
        """
        del self.mails
        gc.collect()

        self.mails = [mail for mail in self.store.mails]
        self.filters = []

    def replay_filters(self):
        """
        Reset selection with store content and replay registered filters.

        Like with the :meth:`~selector.MailSelector.reset` method, selected
        :class:`~store.Mail` objects are deleted and reinitialized with a copy
        of :attr:`~MailSelector.store`'s :attr:`~PostqueueStore.mails`
        attribute.

        However, registered :attr:`~MailSelector.filters` are kept and replayed
        on resetted selection. Use this method to refresh your store content
        while keeping your filters.
        """
        del self.mails
        gc.collect()

        self.mails = [mail for mail in self.store.mails]
        filters = [entry for entry in self.filters]
        for filterinfo in filters:
            name, args, kwargs = filterinfo
            getattr(self, name)(*args, **kwargs)
        self.filters = filters

    def get_mails_by_qids(self, qids):
        """
        Get mails with specified IDs.

        This function is not registered as filter.

        :param list qids: List of mail IDs.
        :return: List of newly selected :class:`~store.Mail` objects
        :rtype: :func:`list`
        """
        return [mail for mail in self.mails
                if mail.qid in qids]

    @debug
    @filter_registration
    def lookup_qids(self, qids):
        """
        Lookup mails with specified IDs.

        :param list qids: List of mail IDs.
        :return: List of newly selected :class:`~store.Mail` objects
        :rtype: :func:`list`
        """
        self.mails = self.get_mails_by_qids(qids)
        return self.mails

    @debug
    @filter_registration
    def lookup_status(self, status):
        """
        Lookup mails with specified postqueue status.

        :param list status: List of matching status to filter on.
        :return: List of newly selected :class:`~store.Mail` objects
        :rtype: :func:`list`
        """
        self.mails = [mail for mail in self.mails
                      if mail.status in status]

        return self.mails

    @debug
    @filter_registration
    def lookup_sender(self, sender, exact=True):
        """
        Lookup mails send from a specific sender.

        Optionnal parameter ``partial`` allow lookup of partial sender like
        ``@domain.com`` or ``sender@``. By default, ``partial`` is ``False``
        and selection is made on exact sender.

        .. note::

            Matches are made against :attr:`Mail.sender` attribute instead of
            real mail header :mailheader:`Sender`.

        :param str sender: Sender address to lookup in :class:`~store.Mail`
                           objects selection.
        :param bool exact: Allow lookup with partial or exact match
        :return: List of newly selected :class:`~store.Mail` objects
        :rtype: :func:`list`
        """
        if exact is False:
            self.mails = [mail for mail in self.mails
                          if sender in mail.sender]
        else:
            self.mails = [mail for mail in self.mails
                          if sender == mail.sender]

        return self.mails

    @debug
    @filter_registration
    def lookup_recipient(self, recipient, exact=True):
        """
        Lookup mails send to a specific recipient.

        Optionnal parameter ``partial`` allow lookup of partial sender like
        ``@domain.com`` or ``sender@``. By default, ``partial`` is ``False``
        and selection is made on exact sender.

        .. note::

            Matches are made against :attr:`Mail.recipients` attribute instead
            of real mail header :mailheader:`To`.

        :param str recipient: Recipient address to lookup in
                              :class:`~store.Mail` objects selection.
        :param bool exact: Allow lookup with partial or exact match
        :return: List of newly selected :class:`~store.Mail` objects
        :rtype: :func:`list`
        """
        if exact is False:
            selected = []
            for mail in self.mails:
                for value in mail.recipients:
                    if recipient in value:
                        selected += [mail]
            self.mails = selected
        else:
            self.mails = [mail for mail in self.mails
                          if recipient in mail.recipients]

        return self.mails

    @debug
    @filter_registration
    def lookup_error(self, error_msg):
        """
        Lookup mails with specific error message (message may be partial).

        :param str error_msg: Error message to filter on
        :return: List of newly selected :class:`~store.Mail` objects`
        :rtype: :func:`list`
        """
        self.mails = [mail for mail in self.mails
                      if True in [True for err in mail.errors
                                  if error_msg in err]]
        return self.mails

    @debug
    @filter_registration
    def lookup_date(self, start=None, stop=None):
        """
        Lookup mails send on specific date range(s).

        :param datetime.date start: Start date (Default: None)
        :param datetime.date stop: Stop date (Default: None)

        :return: List of newly selected :class:`~store.Mail` objects
        :rtype: :func:`list`
        """
        if start is None:
            start = datetime(1970, 1, 1)
        if stop is None:
            stop = datetime.now()

        self.mails = [mail for mail in self.mails
                      if start <= mail.date <= stop]

        return self.mails

    @debug
    @filter_registration
    def lookup_size(self, smin=0, smax=0):  # TODO: documentation
        """
        Lookup mails send with specific size.

        Both arguments ``smin`` and ``smax`` are optionnal and default is set
        to ``0``. Maximum size is ignored if setted to ``0``. If both ``smin``
        and ``smax`` are setted to ``0``, no filtering is done and the entire
        :class:`~store.Mail` objects selection is returned.

        :param int smin: Minimum size (Default: ``0``)
        :param int smax: Maximum size (Default: ``0``)
        :return: List of newly selected :class:`~store.Mail` objects
        :rtype: :func:`list`
        """
        if smin == 0 and smax == 0:
            return self.mails

        if smax > 0:
            self.mails = [mail for mail in self.mails if mail.size <= smax]
        self.mails = [mail for mail in self.mails if mail.size >= smin]

        return self.mails
