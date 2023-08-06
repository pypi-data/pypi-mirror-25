#!/usr/bin/env python

from cleo import Command, InputArgument, InputOption
from cleo import Application
from probe.params import SimParams
import logging

root = logging.getLogger()
root.setLevel(logging.DEBUG)
root.addHandler(logging.StreamHandler())


class PrintParamsCommand(Command):
    """
    Print probe params.

    params:print
        {--params-cfg=params.cfg :          file with params}
        {--debye-fraction=10 :         number of grid points in one debye length}
    """

    def handle(self):
        input_arg = self.option('params-cfg')
        debye_fraction = int(self.option('debye-fraction'))
        if debye_fraction:
            debye_fraction = int(debye_fraction)

        sp = SimParams(input_arg, debye_fraction_user=debye_fraction)

        sp.print_params('params')
        sp.print_sparams('sparams')
        sp.print_cparams('cparams')


class PrepareSimCommand(Command):
    """
    Loads params.cfg and creates sim.h5 with common_0000 group set

    params:prepare_sim
        {--cfg=params.cfg :         path to params.cfg}
        {--h5file=sim.h5 :          name of h5 file}
        {--group-number=0 :         number of common group that will be created}
    """

    def handle(self):
        params_cfg = self.option('cfg')
        h5file = self.option('h5file')
        group_number = int(self.option('group-number'))
        sp = SimParams(params_cfg)
        sp.prepare_sim(h5file=h5file, groupno=group_number)


if __name__ == '__main__':
    application = Application()
    application.add(PrintParamsCommand())
    application.add(PrepareSimCommand())
    application.run()
