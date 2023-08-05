from terminal import red, blue, bold, magenta, white
from .externals.command import Command

from . import const,i18n_util,cli_project,cli_oss
from .action import login, config, info, cluster,events, job, cluster_create, cluster_delete, cluster_update, instance_type \
    , job_delete, job_restart, job_stop, job_update, job_create, log_fetch, job_submit,checker\
    ,image,image_create,image_delete,disk_type,resource_type

import os

COMMAND = const.COMMAND
CMD = const.CMD

IMG_ID = 'img-xxxxxx'
INS_TYPE = 'ecs.s3.large'

VERSION = const.VERSION

IS_GOD = const.IS_GOD


# SPLITER = '\n    --%s' + ('-' * 40)

MSG=i18n_util.msg()


class Cli:
    def __help(self):
        self.program.print_help()

    def __init__(self):
        self.program = Command(COMMAND, version=VERSION,
                          title=bold(magenta('AliCloud BatchCompute CLI')),
                          usage="Usage: %s <command> [option]" % COMMAND,
                          func=self.__help,
                          help_footer=white('  type "%s [command] -h" for more' % CMD))

        # login
        cmd_login = Command('login',
                            description=MSG['login']['description'],
                            func=login.login,
                            spliter='\n    -----%s---------------------------' % blue('config'),
                            arguments=['region', 'accessKeyId', 'accessKeySecret'],
                            usage='''Usage: %s login <region> [accessKeyId] [accessKeySecret] [option]

    Examples:

        1. %s login cn-qingdao kywj6si2hkdfy9 las****bc=
        2. %s login cn-qingdao ''' % (COMMAND, CMD, CMD))
        self.program.action(cmd_login)

        # logout
        cmd_logout = Command('logout',
                                 description=MSG['logout']['description'],
                                 func=login.logout)
        self.program.action(cmd_logout)






        # set config
        cmd_config = Command('config', alias=['me','set'], description=MSG['config']['description'],
                             detail=MSG['config']['detail'],
                             usage='''Usage: %s <command> config|me|set [option]

    Examples:

        1. %s config     # show configurations
        2. %s set -r cn-qingdao -o oss://my-bucket/bcscli/ -l zh_CN
        3. %s set -i %s -t %s ''' % (COMMAND, CMD, CMD,CMD ,IMG_ID, INS_TYPE),
                             func=config.all)
        cmd_config.option('-r,--region [region]', MSG['config']['option']['region'])
        cmd_config.option('-o,--osspath [osspath]', MSG['config']['option']['osspath'] )
        cmd_config.option('-l,--locale [locale]', MSG['config']['option']['locale'])
        cmd_config.option('-i,--image [imageId]', MSG['config']['option']['image'])
        cmd_config.option('-t,--type [instanceType]', MSG['config']['option']['type'])
        cmd_config.option('-s,--ssl [ssl]', MSG['config']['option']['ssl'], visible=IS_GOD)
        cmd_config.option('-v,--version [version]', MSG['config']['option']['version'], visible=IS_GOD)
        cmd_config.option('-g,--god [god]', MSG['config']['option']['god'], visible=IS_GOD)
        self.program.action(cmd_config)

        # info
        cmd_info = Command('info',alias=['about'], description=MSG['info']['description'],
                           visible=IS_GOD,
                             func=info.info)
        self.program.action(cmd_info)

        # resource type
        cmd_resource_type = Command('resource_type', alias=['rt', 'r'],
                                    description=MSG['resource_type']['description'],
                                    usage='''Usage: %s resource_type|rt|r [option]

            Examples:

                1. %s r ''' % (COMMAND, CMD),
                                    spliter='\n    -----%s---------------------------' % blue('query, show'),
                                    func=resource_type.list)
        self.program.action(cmd_resource_type)

        # instance type
        cmd_instance_type = Command('instance_type', alias=['it', 't'],
                                    description=MSG['instance_type']['description'],
                                    usage='''Usage: %s instance_type|it|t [option]

        Examples:

            1. %s it ''' % (COMMAND, CMD),
                                    func=instance_type.list)
        self.program.action(cmd_instance_type)


        # disk type
        cmd_disk_type = Command('disk_type', alias=['d'],
                                    description=MSG['disk_type']['description'],
                                    usage='''Usage: %s disk_type|d [option]

        Examples:

            1. %s d ''' % (COMMAND, CMD),
                                    func=disk_type.list)
        self.program.action(cmd_disk_type)

        # events
        cmd_events = Command('event', alias=['e'],
                                description=MSG['event']['description'],
                                usage='''Usage: %s event|e [option]

            Examples:

                1. %s e ''' % (COMMAND, CMD),
                                func=events.list)
        self.program.action(cmd_events)





        # images
        cmd_images = Command('image', alias=['img','i'],
                               arguments=['imageId'],
                               description=MSG['image']['description'],
                               usage='''Usage: %s image|img|i [imageId|No.] [option]

        Examples:

            list images:
              1. %s i

            get cluster info:
              1. %s i img-6ki4fsea5ldlvsupbrk01q
              2. %s i 1''' % (COMMAND, CMD, CMD, CMD),
                               func=image.all)
        self.program.action(cmd_images)




        ####################################
        ####################################
        ########################################
        # clusters
        cmd_clusters = Command('cluster', alias=['c'],
                               arguments=['clusterId'],
                               description=MSG['cluster']['description'],
                               usage='''Usage: %s cluster|c [clusterId|No.] [option]

    Examples:

        list cluster:
          1. %s c

        get cluster info:
          1. %s c cls-6ki4fsea5ldlvsupbrk01q
          2. %s c 1
          3. %s c 1 -l''' % (COMMAND, CMD, CMD, CMD, CMD),
                               func=cluster.all)
        cmd_clusters.option('-d,--description', MSG['cluster']['option']['description'])
        cmd_clusters.option('-l,--log', MSG['cluster']['option']['oplog'])
        self.program.action(cmd_clusters)




        # jobs
        cmd_job = Command('job', alias=['j'],
                          arguments=['jobId', 'taskName', 'instanceId', 'logType'],
                          description=MSG['job']['description'],
                          usage='''Usage:

    %s job|j [jobId|No.] [taskName|No.] [instanceId] [options]

    Examples:

        list jobs:
          1. %s job|j -t [num] -s [state] -i [jobId] -n [jobName]
          2. %s j                     # show top 10 (default)
          3. %s j -t 50               # show top 50
          4. %s j -a                  # show all
          5. %s j -s Running,Waiting  # show those state is Running or Waiting
          6. %s j -n abc              # show those jobName contains "abc"
          7. %s j -i 0018             # show those jobId contains "0018"

        get job detail:
          1. %s j <jobId>
          2. %s j <jobId> -d          # show job description only
          3. %s j <No.>               # use <No.> instead of <job-id>, this command must run after %s j

        get task detail:
          1. %s j <jobId> <taskName>
          2. %s j <No.> <No.>            #use <No.> instead of <jobId> and <taskName>

        get instance detail:
          1. %s j <jobId> <taskName> <instanceId>
          2. %s j <No.> <No.> <instanceId>         #use <No.> instead of <jobId> and <taskName>''' % (
                          COMMAND, CMD, CMD, CMD,CMD, CMD, CMD, CMD, CMD, CMD, CMD, CMD, CMD, CMD, CMD, CMD),
                          func=job.all)

        cmd_job.option('-t, --top [num]', MSG['job']['option']['top'])
        cmd_job.option('-a, --all', MSG['job']['option']['all'])
        cmd_job.option('-s, --state [state]', MSG['job']['option']['state'])
        cmd_job.option('-i, --id [jobId]', MSG['job']['option']['id'] )
        cmd_job.option('-n, --name [jobName]', MSG['job']['option']['name'] )
        cmd_job.option('-d, --description',  MSG['job']['option']['description'])
        self.program.action(cmd_job)

        # log
        cmd_log = Command('log',alias=['l'],
                          arguments=['jobId', 'taskName', 'instanceId'],
                          description=MSG['log']['description'],
                          usage='''Usage:

            %s log <jobId> [taskName] [instanceId] [options]

          Examples:
              1. %s log <jobId>                                                # show logs for all instances in a job
              2. %s log <jobId> -e                                             # show stderr log only
              3. %s log <jobId> -d /path/to/save/logs/                         # download logs for all instances in a job
              4. %s log <jobId> <taskName> -d /path/to/save/logs/              # download logs for all instances in a task
              5. %s log <jobId> <taskName> <intanceId> -d /path/to/save/logs/  # download logs for a instance
              6. %s log <No.> <No.> <intanceId> -d /path/to/save/logs/         # use <No.> instead of jobId and taskName''' % (
                          COMMAND, CMD, CMD, CMD, CMD, CMD, CMD),
                          func=log_fetch.fetch)
        cmd_log.option('-d, --dir_path [dir_path]', MSG['log']['option']['dir_path'])
        cmd_log.option('-e, --stderr', MSG['log']['option']['stderr'])
        cmd_log.option('-o, --stdout', MSG['log']['option']['stdout'])
        self.program.action(cmd_log)

        ##################################################

        # create image
        cmd_create_image = Command('create_image', alias=['ci'],
                                     description=MSG['create_image']['description'],
                                     arguments=['imageName','ecsImageId'],
                                     usage='''Usage: %s create_image|ci [option] <imageName> <ecsImageId>

            Examples:

                1. %s ci myimage1 m-xxsxxx
                2. %s ci myimage1 m-xxsxxx  -p Linux -d 'this is description' ''' % (COMMAND, CMD, CMD),
                                     spliter='\n    -----%s----------------' % blue('create, update, delete'),
                                     func=image_create.create_image)
        cmd_create_image.option("-p, --platform [platform]", MSG['create_image']['option']['platform'],
                                  resolve=image_create.trans_platform)
        cmd_create_image.option("-d, --description [description]",
                                  MSG['create_image']['option']['description'])
        cmd_create_image.option("--show_json",
                                  MSG['create_image']['option']['show_json'])
        self.program.action(cmd_create_image)


        # delete image
        cmd_del_image = Command('delete_image', alias=['di'],
                                  arguments=['imageId'],
                                  description=MSG['delete_image']['description'],
                                  usage='''Usage: %s delete_image|di [imageId,imageId2,imageId3...] [option]

            Examples:

                1. %s di img-idxxx1                # delete image with imageId
                2. %s di img-idxxx1,img-idxxx2 -y  # delete images in silent mode''' % (COMMAND, CMD, CMD),
                                  func=image_delete.del_image)
        cmd_del_image.option("-y, --yes", MSG['delete_image']['option']['yes'])
        self.program.action(cmd_del_image)



        ##################################################

        # create cluster
        cmd_create_cluster = Command('create_cluster', alias=['cc'],
                                     description=MSG['create_cluster']['description'],
                                     arguments=['clusterName'],
                                     usage='''Usage: %s create_cluster|cc [option] <clusterName>

    Examples:

        1. %s cc cluster1
        2. %s cc cluster2 -n 3
        3. %s cc cluster2 -i %s -t %s -n 1 -d 'this is description' -u key1:value1,k2:v2
        4. %s cc cluster3 --notification_topic my-mns-topic --notification_events OnClusterDeleted,OnInstanceActive --notification_endpoint <your_mns_endpoint>    # set notification
        5. %s cc cluster4 --resource_type Spot  # creating with spot resource type''' % (
                                     COMMAND, CMD, CMD, CMD, IMG_ID, INS_TYPE , CMD, CMD),
                                     spliter=' ',
                                    # spliter='\n    -----%s----------------' % blue('create, update, delete'),
                                     func=cluster_create.create_cluster)
        cmd_create_cluster.option("-i, --image [imageId]", MSG['create_cluster']['option']['image'],
                                  resolve=cluster_create.trans_image)
        cmd_create_cluster.option("-t, --type [instanceType]", MSG['create_cluster']['option']['type'])
        cmd_create_cluster.option("-n, --nodes [instanceCount]", MSG['create_cluster']['option']['nodes'],
                                  resolve=cluster_create.trans_nodes)
        cmd_create_cluster.option("-d, --description [description]",
                                  MSG['create_cluster']['option']['description'])
        cmd_create_cluster.option("-u, --user_data [kv_pairs]",
                                  MSG['create_cluster']['option']['user_data'],
                                  resolve=cluster_create.trans_user_data)

        cmd_create_cluster.option("-e, --env [kv_pairs]", MSG['create_cluster']['option']['env'],resolve=cluster_create.trans_env)
        cmd_create_cluster.option("--disk [disk_configs]",
                                  MSG['create_cluster']['option']['disk'],
                                  resolve=cluster_create.trans_disk)


        cmd_create_cluster.option("--resource_type [resource_type]",
                                  MSG['create_cluster']['option']['resource_type'])

        cmd_create_cluster.option("-m, --mount [kv_pairs]", '(%s) %s' % (red(MSG['changed']),MSG['create_cluster']['option']['mount']),
                                  resolve=cluster_create.trans_mount)
        cmd_create_cluster.option("--nas_access_group [nas_access_group]",
                              MSG['create_cluster']['option']['nas_access_group'])
        cmd_create_cluster.option("--nas_file_system [nas_file_system]", MSG['create_cluster']['option']['nas_file_system'])

        cmd_create_cluster.option("--notification_endpoint [mns_endpoint]",
                              MSG['create_cluster']['option']['notification_endpoint'])
        cmd_create_cluster.option("--notification_topic [mns_topic]", MSG['create_cluster']['option']['notification_topic'])
        cmd_create_cluster.option("--notification_events [cluster_events]", MSG['create_cluster']['option']['notification_events'],
                              resolve=cluster_create.trans_notification_events)
        cmd_create_cluster.option("--no_cache_support",
                                  MSG['create_cluster']['option']['no_cache_support'])

        cmd_create_cluster.option("--vpc_cidr_block [vpc_cidr_block]",
                                  MSG['create_cluster']['option']['vpc_cidr_block'])
        cmd_create_cluster.option("-f, --filePath [filePath]", MSG['create_cluster']['option']['filePath'],
                                  visible=IS_GOD)
        cmd_create_cluster.option("--show_json",
                              MSG['create_cluster']['option']['show_json'])
        self.program.action(cmd_create_cluster)

        # delete cluster
        cmd_del_cluster = Command('delete_cluster', alias=['dc'],
                                  arguments=['clusterId'],
                                  description=MSG['delete_cluster']['description'],
                                  usage='''Usage: %s delete_cluster|dc [clusterId,clusterId2,clusterId3...] [option]

    Examples:

        1. %s dc cls-idxxx1                # delete cluster with clusterId
        2. %s dc cls-idxxx1,cls-idxxx2 -y  # delete clusters in silent mode''' % (COMMAND, CMD, CMD),
                                  func=cluster_delete.del_cluster)
        cmd_del_cluster.option("-y, --yes", MSG['delete_cluster']['option']['yes'])
        self.program.action(cmd_del_cluster)

        # update cluster
        cmd_update_cluster = Command('update_cluster', alias=['uc'],
                                     arguments=['clusterId', 'groupName'],
                                     description=MSG['update_cluster']['description'],
                                     usage='''Usage: %s update_cluster|uc <clusterId> [groupName] [option]

          Examples:

              1. %s uc cls-idxxx1 group -n 2   # update cluster set group.DesiredVMCount=2
              2. %s uc cls-idxxx1 -n 2         # ignore group name when it is 'group' ''' % (COMMAND, CMD, CMD),
                                     func=cluster_update.update)
        cmd_update_cluster.option("-y, --yes",  MSG['update_cluster']['option']['yes'])
        cmd_update_cluster.option("-n, --nodes [desiredVMCount]",  MSG['update_cluster']['option']['nodes'],
                                  resolve=cluster_update.trans_nodes)

        cmd_update_cluster.option("-m, --mount [kv_pairs]", MSG['update_cluster']['option']['mount'],
                                  resolve=cluster_create.trans_mount)
        cmd_update_cluster.option("-i, --image [imageId]", MSG['update_cluster']['option']['image'],
                                  resolve=cluster_update.trans_image)
        cmd_update_cluster.option("-u, --user_data [kv_pairs]",
                                  MSG['update_cluster']['option']['user_data'],
                                  resolve=cluster_update.trans_user_data)
        cmd_update_cluster.option("-e, --env [kv_pairs]", MSG['update_cluster']['option']['env'],
                                  resolve=cluster_update.trans_env)
        cmd_update_cluster.option("--show_json",
                                  MSG['update_cluster']['option']['show_json'])
        self.program.action(cmd_update_cluster)

        ######################


        # create job
        cmd_create_job = Command('create_job', alias=['cj'],
                                 arguments=['jsonString'],
                                 spliter=' ',
                                 description=MSG['create_job']['description'],
                                 usage='''Usage: %s create_job|cj [jsonString] [option]

    Examples:

        1. %s cj "{\\"Name\\":......}"    #create job from json string
        2. %s cj -f /path/to/job.json   #create job from json file path''' % (COMMAND, CMD, CMD),
                                 func=job_create.create)
        cmd_create_job.option("-f, --filePath [filePath]", MSG['create_job']['option']['filePath'])
        self.program.action(cmd_create_job)

        # restart job
        cmd_restart_job = Command('restart_job', alias=['rj'],
                                  arguments=['jobId'],
                                  description=MSG['restart_job']['description'],
                                  usage='''Usage: %s restart_job|rj [jobId,jobId2,jobId3...] [option]

    Examples:

        1. %s rj job-idxxx1             # restart job with jobId
        2. %s rj job-idxxx1,job-idxxx2  # restart job with jobIds''' % (COMMAND, CMD, CMD),
                                  func=job_restart.restart_job)
        cmd_restart_job.option("-y, --yes", MSG['restart_job']['option']['yes'])
        self.program.action(cmd_restart_job)

        # stop job
        cmd_stop_job = Command('stop_job', alias=['sj'],
                               arguments=['jobId'],
                               description=MSG['stop_job']['description'],
                               usage='''Usage: %s stop_job|sj [jobId,jobId2,jobId3...] [option]

    Examples:

        1. %s sj job-idxxx1             # stop job with jobId
        2. %s sj job-idxxx1,job-idxxx2  # stop job with jobIds''' % (COMMAND, CMD, CMD),
                               func=job_stop.stop_job)
        cmd_stop_job.option("-y, --yes", MSG['stop_job']['option']['yes'])
        self.program.action(cmd_stop_job)

        # delete job
        cmd_del_job = Command('delete_job', alias=['dj'],
                              arguments=['jobId'],
                              description=MSG['delete_job']['description'],
                              usage='''Usage: %s delete_job|dj [jobId,jobId2,jobId3...] [option]

    Examples:

        1. %s dj job-idxxx1             # delete job with jobId
        2. %s dj job-idxxx1,job-idxxx2  # delete job with jobIds''' % (COMMAND, CMD, CMD),
                              func=job_delete.del_job)
        cmd_del_job.option("-y, --yes", MSG['delete_job']['option']['yes'])
        self.program.action(cmd_del_job)

        # update job
        cmd_update_job = Command('update_job', alias=['uj'],
                                 arguments=['jobId', 'groupName'],
                                 description=MSG['update_job']['description'],
                                 usage='''Usage: %s update_job|uj <jobId> [option]

    Examples:

        1. %s uj job-idxxx1 -p 2   #update job set priority=2''' % (COMMAND, CMD),
                                 func=job_update.update)
        cmd_update_job.option("-y, --yes",  MSG['update_job']['option']['yes'])
        cmd_update_job.option("-p, --priority <priority>",  MSG['update_job']['option']['priority'])
        self.program.action(cmd_update_job)

        ########################################

        ##############
        def cmd_oss_print_help():
            cmd_oss.print_help()

        # oss
        cmd_oss = Command('oss', alias=['o'],
                          description=MSG['oss']['description'],
                          func=cmd_oss_print_help, spliter='\n    -----%s----------------' % blue('sub command'))
        self.program.action(cmd_oss)

        # sub command for oss
        cli_oss.init(cmd_oss)



        #### project ##
        def cmd_project_print_help():
            cmd_project.print_help()

        # project
        cmd_project = Command('project', alias=['p'],
                              visible=IS_GOD,
                                 description=MSG['project']['description'],
                                 func=cmd_project_print_help )
        self.program.action(cmd_project)


        # sub command for project
        cli_project.init(cmd_project)






        ##############################################

        ##############################################

        # submit job
        cmd_submit_job = Command('submit', alias=['sub'],
                                 arguments=['cmd','job_name'],
                                 description=MSG['submit']['description'],
                                 usage='''Usage: %s submit|sub <cmd> [job_name] [option]

    Examples:

        1. %s sub "echo 'hello'" -n 3 -f                                                    # run this cmd on 3 machines(instances) in force mode
        2. %s sub "echo 'hello'" -c img=%s                                         # use auto cluster, or -i %s
        3. %s sub "python main.py arg1 arg2" job_name -c cls-xxxxx -p ./my_program/         # set job name, use cluster id, pack a folder and upload
        4. %s sub "python /home/admin/test/main.py" -m oss://bucket/a/b/:/home/admin/test/  # mount an oss path to a local path
        5. %s sub "python test.py" -p test.py --docker myubuntu@oss://bucket/dockers/       # run in docker container
        6. %s sub --file job.cfg                    # submit a job from job.cfg
        7. %s sub --notification_topic my-mns-topic --notification_events OnTaskStopped,OnJobFailed  --notification_endpoint <your_mns_endpoint>          # set notification
        ''' % (
                                 COMMAND, CMD, CMD, IMG_ID, IMG_ID, CMD, CMD, CMD, CMD, CMD),
                                 spliter='\n    -----%s----------------' % blue('quick cmd'),
                                 func=job_submit.submit)


        cmd_submit_job.option("-n, --nodes [machine_number]", MSG['submit']['option']['nodes'])
        cmd_submit_job.option("-f, --force", MSG['submit']['option']['force'])
        cmd_submit_job.option("--auto_release", MSG['submit']['option']['auto_release'])
        cmd_submit_job.option("-d, --description [description]", MSG['submit']['option']['description'])

        cmd_submit_job.option("-p, --pack [folder_path]", MSG['submit']['option']['pack'])
        cmd_submit_job.option("--priority [priority]", MSG['submit']['option']['priority'])

        cmd_submit_job.option("--timeout [seconds]", MSG['submit']['option']['timeout'])

        cmd_submit_job.option("-c, --cluster [cluster]", MSG['submit']['option']['cluster'])
        cmd_submit_job.option('-i, --image [imageId]', MSG['submit']['option']['image'])
        cmd_submit_job.option('-t, --type [type]', MSG['submit']['option']['type'])
        cmd_submit_job.option("-e, --env [kv_pairs]", MSG['submit']['option']['env'])
        cmd_submit_job.option("-r, --read_mount [kv_pairs]",  MSG['submit']['option']['read_mount'])
        cmd_submit_job.option("-w, --write_mount [kv_pairs]", MSG['submit']['option']['write_mount'])
        cmd_submit_job.option("-m, --mount [kv_pairs]", '(%s) %s' % (red(MSG['changed']),MSG['submit']['option']['mount']))

        cmd_submit_job.option("--nas_access_group [nas_access_group]",
                              MSG['submit']['option']['nas_access_group'])

        cmd_submit_job.option("--nas_file_system [nas_file_system]", MSG['submit']['option']['nas_file_system'])

        cmd_submit_job.option("--docker [docker]",  MSG['submit']['option']['docker'])
        cmd_submit_job.option("-u,--user_data [kv_pairs]", MSG['submit']['option']['user_data'])

        cmd_submit_job.option("--resource_type [resource_type]",
                                  MSG['submit']['option']['resource_type'])
        cmd_submit_job.option("--disk [disk_configs]",
                                  MSG['submit']['option']['disk'],
                                  resolve=job_submit.trans_disk)
        cmd_submit_job.option("--lock", MSG['submit']['option']['lock'])
        cmd_submit_job.option("--locale [locale]", MSG['submit']['option']['locale'])
        cmd_submit_job.option("--file [file]",  MSG['submit']['option']['file'])
        cmd_submit_job.option("--notification_endpoint [mns_endpoint]",  MSG['submit']['option']['notification_endpoint'])
        cmd_submit_job.option("--notification_topic [mns_topic]", MSG['submit']['option']['notification_topic'])
        cmd_submit_job.option("--notification_events [job_events]", MSG['submit']['option']['notification_events'],
                              resolve=job_submit.trans_notification_events)
        cmd_submit_job.option("--reserve_on_fail", MSG['submit']['option']['reserve_on_fail'])
        cmd_submit_job.option("--no_cache_support", MSG['submit']['option']['no_cache_support'])

        cmd_submit_job.option("--vpc_cidr_block [vpc_cidr_block]",
                                  MSG['submit']['option']['vpc_cidr_block'])

        cmd_submit_job.option("--show_json",
                              MSG['submit']['option']['show_json'])
        cmd_submit_job.option("--show_dag",
                              MSG['submit']['option']['show_dag'])
        self.program.action(cmd_submit_job)


        # check debug
        cmd_check = Command('check', alias=['ch'],
                                 arguments=['jobId'],
                                 description=MSG['check']['description'],
                                 usage='''Usage: %s check|ch <jobId|No.> [option]

    Examples:
        1. %s check job-0000000056D7FE9A0000368000000661
        2. %s ch 2       # use No. instead of jobId''' % (
                                 COMMAND, CMD, CMD),
                                 func=checker.check)
        self.program.action(cmd_check)

        ##############################################
    def go(self, arr=None):
        if os.getenv('DEBUG'):
            self.program.parse(arr)
        else:
            try:
                self.program.parse(arr)
            except Exception as e:
                msg = format(e)
                print(red('\n  ERROR: %s\n' % msg))
                if '()' in msg and 'argument' in msg:
                    print(red('  add "-h" for more information\n'))

def main():

    try:
        Cli().go()
    except KeyboardInterrupt:
        print('\nKeyboardInterrupt')

if __name__ == '__main__':
    main()


