#!/usr/bin/env python3
import time
import logging


class SCPI(object):
    """SCPI helper functions."""

    @property
    def SystemErrorQueue(self):
        """SYST:ERR? - System Error Queue.

        :returns: list of error queue items
        """
        responces = []
        # responce = False
        responce = self.query('SYST:ERR?')

        while responce != '+0,"No error"':
            responces.append(responce)
            responce = self.query('SYST:ERR?')
            '''
            responce = self.query('SYST:ERR?')
            if responce != '+0,"No error"':
                responces.append(responce)
            # print(responce)
            '''
        return(responces)
