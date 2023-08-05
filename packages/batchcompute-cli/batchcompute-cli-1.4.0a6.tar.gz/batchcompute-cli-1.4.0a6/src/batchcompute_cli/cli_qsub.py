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
    cmd_qsub = Command('qsub', visible=IS_GOD,
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

    # unsupported
    cmd_qsub.option("-z,--zz", '', visible=False)
    cmd_qsub.option("-X,--XX", '', visible=False)
    cmd_qsub.option("-x,--xx", '', visible=False)
    cmd_qsub.option("-W,--additional_attributes [additional_attributes]", '',visible=False)
    cmd_qsub.option("-w,--wpath [path]", '',visible=False)
    cmd_qsub.option("-v,--variable_list [variable_list]", '',visible=False)
    cmd_qsub.option("-u,--user_list [user_list]", '',visible=False)
    cmd_qsub.option("-T,--prescript [pre_script_name]", '',visible=False)
    cmd_qsub.option("-t,--array_request [array_request]", '',visible=False)
    cmd_qsub.option("-S,--path_list [path_list]", '',visible=False)
    cmd_qsub.option("-r,--rerunable [rerunable]", '',visible=False)
    cmd_qsub.option("-q,--queue [destination]", '', visible=False)
    cmd_qsub.option("-P,--proxy_user [proxy_user]", '',visible=False)
    cmd_qsub.option("-p,--priority [priority]", '',visible=False)
    cmd_qsub.option("-M,--mail_user_list [mail_user_list]", '',visible=False)
    cmd_qsub.option("-m,--mail_options [mail_options]", '',visible=False)
    cmd_qsub.option("-k,--keep [keep]", '',visible=False)
    cmd_qsub.option("-I,--interactively", '',visible=False)
    cmd_qsub.option("-h,--hh", '',visible=False)
    cmd_qsub.option("-f,--ff", '',visible=False)
    cmd_qsub.option("-D,--root_path [root_path]", '',visible=False)
    cmd_qsub.option("-C,--directive_prefix", '',visible=False)
    cmd_qsub.option("-c,--checkpoint_options", '',visible=False)
    cmd_qsub.option("-b,--seconds [seconds]", '',visible=False)
    cmd_qsub.option("-A,--account_string [account_string]", '',visible=False)
    cmd_qsub.option("-a,--date_time [date_time]", '',visible=False)



    cmd_qsub.option("-V,--env", MSG['qsub']['option']['V'])
    cmd_qsub.option("--show_json",
                          MSG['qsub']['option']['show_json'])
    cmd_qsub.option("--show_opt",
                    MSG['qsub']['option']['show_opt'], visible=False)
    return cmd_qsub