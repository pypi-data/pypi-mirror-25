# -*- coding: utf-8 -*-
from terminal import blue
from .externals.command import Command

from . import const,i18n_util
from .action import job_qsub

COMMAND = const.COMMAND
CMD = const.CMD

IMG_ID = 'img-xxxxxx'
INS_TYPE = 'ecs.s3.large'

VERSION = const.VERSION

IS_GOD = const.IS_GOD


# SPLITER = '\n    --%s' + ('-' * 40)

MSG=i18n_util.msg()


def createCommand():
    cmd_qsub = Command('qsub',
                       arguments=['script_name'],
                       detail=MSG['qsub']['detail'],
                       description=MSG['qsub']['description'],
                       usage='''Usage: %s qsub [-d work_path] [-e stderr_path]
                 [-j oe|eo|n] [-l resource_list] [-N job_name]
                 [-o stdout_path] [-V]
                 <script_name>

        Examples:

            1. %s qsub -l select=2:ncpus=2:mem=4gb run.pbs

            ''' % (COMMAND, CMD),

                       func=job_qsub.qsub)

    cmd_qsub.option("-d,--work_path [work_path]", MSG['qsub']['option']['d'])
    cmd_qsub.option("-e,--stderr_path [stderr_path]", MSG['qsub']['option']['e'])
    cmd_qsub.option("-j,--join [join]", MSG['qsub']['option']['j'])
    cmd_qsub.option("-l,--resource_list [resource_list]", MSG['qsub']['option']['l'])
    cmd_qsub.option("-N,--job_name [job_name]", MSG['qsub']['option']['N'])
    cmd_qsub.option("-o,--stdout_path [stdout_path]", MSG['qsub']['option']['o'])
    #cmd_qsub.option("-q,--queue [queue]", MSG['qsub']['option']['q'])
    cmd_qsub.option("-V,--env", MSG['qsub']['option']['V'])
    cmd_qsub.option("--show_json",
                          MSG['qsub']['option']['show_json'])
    cmd_qsub.option("--show_opt",
                    MSG['qsub']['option']['show_opt'], visible=False)
    return cmd_qsub