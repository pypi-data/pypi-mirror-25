Help on package batchcompute:

NAME
    batchcompute - A simple implementation for BatchCompute service SDK.

FILE
    /apsarapangu/disk1/batchcompute_ecs_python_sdk/src/batchcompute/__init__.py

PACKAGE CONTENTS
    client (package)
    core (package)
    resources (package)
    utils (package)

CLASSES
    __builtin__.object
        batchcompute.client.client.Client
    exceptions.Exception(exceptions.BaseException)
        batchcompute.core.exceptions.ClientError
        batchcompute.core.exceptions.FieldError
        batchcompute.core.exceptions.JsonError
        batchcompute.core.exceptions.ValidationError
        batchcompute.utils.functions.ConfigError
    
    class Client(__builtin__.object)
     |  Implementation of client to use BatchCompute service.
     |  
     |  Methods defined here:
     |  
     |  __init__(self, region, access_key_id, access_key_secret, security_token='', security_conn=False, human_readable=False, **headers)
     |      @params `region`: service region.
     |      @type `region`: import `region` from batchcompute root package, [
     |          CN_QINGDAO, CN_SHENZHEN] allowed.
     |      
     |      @params `access_key_id`: access key id in Aliyun.
     |      @type `access_key_id`: usually a {str}. 
     |      
     |      @params `access_key_secret`: access secret key in Aliyun.
     |      @type `access_key_secret`: usually a {str}. 
     |      
     |      @params `security_token`: STS token.
     |      @type `security_token`: a {str} STS token.
     |      
     |      @params `security_conn`: use HTTPS.
     |      @parames `security_conn`: {bool}, default False.
     |      
     |      @params `human_readable`: unused now.
     |      @type `human_readable`: {bool}, default: False.
     |  
     |  change_cluster_desired_vm_count(self, cluster, **kwargs)
     |      Change the desired vm count of a existing cluster. 
     |      
     |      @params `cluster`: a batchcompute cluster.
     |      @type `cluster`: a 'cls-' started {str} or a CreateResponse object.
     |      
     |      @params `kwargs`: some key-word pair like group_name=desired_vm_count.
     |      @type `kwargs`: desired_vm_count must be a positive {int} value;
     |      
     |      @example:
     |          >>> client = Client(region, id, key)
     |          ... cluster_id = client.create_cluster(... 
     |          ... client.change_cluster_desired_vm_count(cluster_id, group1=3, group2=4)
     |  
     |  change_job_priority(self, job, priority)
     |      Change the priority of a given job.
     |      
     |      @Notice:
     |          Only stopped jobs' priority can be changed.
     |      
     |      @params `job`: a batchcompute job.
     |      @type `job`: a 'job-' started {str} or a CreateResponse object.
     |      
     |      @params `priority`: priority number.
     |      @type `priority`: a {int} between 0~999.
     |      
     |      @example:
     |          >>> client = Client(region, id, key)
     |          ... job_id = 'job-xxxx' 
     |          ... client.stop_job(job_id)
     |          ... assert client.get_job(job_id).State == 'Stopped'
     |          ... client.change_job_priority(job_id, 99)
     |          ... client.start_job(job_id)
     |          ... assert client.get_job_description(job_id).Priority == 99
     |  
     |  create_cluster(self, cluster_desc, token='')
     |      Create a new cluster in server. 
     |      
     |      @params `cluster_desc`: a object descripts a cluster.
     |      @type `cluster_desc`: a json {str}, a {dict} object, or a 
     |          {ClusterDescription} object.  
     |      
     |      @params `token`: idempotent token.
     |      @type `token`: a {str} specified by user.
     |      
     |      @return: a {CreateResponse} object.
     |      
     |      @example:
     |      
     |          >>> from batchcompute import Cient, ClientError
     |          ... from batchcompute.resources import ClusterDescription, GroupDescription 
     |          ... # some other codes here
     |          ... Client = Client(REGION, id, key)
     |          ... 
     |          ... try: 
     |          ...     cluster_desc = ClusterDescription()
     |          ...     group_desc = GroupDescription()
     |      
     |          ...     group_desc.DesiredVMCount = 1
     |          ...     group_desc.InstanceType = 'ecs.t1.small'
     |          ...     cluster_desc.add_group('group1', group_desc)
     |          ...     cluster_desc.Name = "BatchcomputePythonSDK" 
     |          ...     # image_id is a image created in batchcompute service before.
     |          ...     cluster_desc.ImageId = image_id
     |          ...    
     |          ...     print client.create_cluster(cluster_desc).Id
     |          ... except ClientError, e:
     |          ...     print (e.get_status_code(), e.get_code(), e.get_requestid(), e.get_msg())
     |  
     |  create_image(self, image_desc, token='')
     |      Create a new image in server. 
     |      
     |      @params `image_desc`: a object descripts a image.
     |      @type `image_desc`: a json {str}, a {dict} object, or a 
     |          {ImageDescription} object.  
     |      
     |      @params `token`: idempotent token.
     |      @type `token`: a {str} specified by user.
     |      
     |      @return: a {CreateResponse} object.
     |      
     |      @example:
     |      
     |          >>> from batchcompute import Cient, ClientError
     |          ... from batchcompute.resources import ImageDescription
     |          ... # some other codes here
     |          ... Client = Client(REGION, id, key)
     |          ... 
     |          ... try: 
     |          ...     image_desc = ImageDescription()
     |      
     |          ...     image_desc.Name = "PythonSDKImage"
     |          ...     image_desc.Description = "PythonSDKImage"
     |          ...     image_desc.EcsImageId = "m-xxxx"
     |          ...     image_desc.Platform = "Linux" # or Windows
     |          ...    
     |          ...     print client.create_image(image_desc).Id
     |          ... except ClientError, e:
     |          ...     print (e.get_status_code(), e.get_code(), e.get_requestid(), e.get_msg())
     |  
     |  create_job(self, job_desc, token='')
     |      Create a new job in server.
     |      
     |              @param `job_desc`: a object descripts a job.
     |              @type `job_desc`: a json {str}, a {dict} object, or a {Job} object.  
     |      
     |              @param `token`: idempotent token.
     |              @type `token`: a {str} specified by user.
     |      
     |              @example:
     |      
     |                  >>> from batchcompute import Cient, ClientError
     |                  ... from batchcompute import CN_QINGDAO as REGION 
     |                  ... from batchcompute.resources import JobDescription, TaskDescription, DAG
     |                  ... # some other codes here
     |                  ... access_key_id = ... # your_access_key_id
     |                  ... access_key_secret = ... # your_access_key_secret
     |                  ... cluster_id = ... # ID of cluster created before
     |                  ... Client = Client(REGION, access_key_id, access_key_secret)
     |                  ... 
     |                  ... try: 
     |                  ...     job_desc = JobDescription()
     |                  ...     map_task = TaskDescription()
     |      
     |                  ...     # Create map task.
     |                  ...     map_task.Parameters.Command.CommandLine = "ping -n 3 127.0.0.1"
     |                  ...     map_task.Parameters.Command.PackagePath = ""
     |                  ...     map_task.Parameters.StdoutRedirectPath = "oss://xxx/xxx/" 
     |                  ...     map_task.Parameters.StderrRedirectPath = "oss://xxx/xxx/" 
     |                  ...     map_task.InstanceCount = 3
     |                  ...     # cluster_id is a cluster created in batchcompute service before.
     |                  ...     map_task.ClusterId = cluster_id
     |      
     |                  ...     # Create task dag.
     |                  ...     task_dag = DAG()
     |                  ...     task_dag.add_task(task_name='Map', task=map_task)
     |      
     |                  ...     # Create job description.
     |                  ...     job_desc.DAG = task_dag
     |                  ...     job_desc.Priority = 99
     |                  ...     job_desc.Name = 'PythonSDKDemo' 
     |                  ...     job_desc.JobFailOnInstanceFail = True
     |                  ...
     |                  ...     job_id = client.create_job(job_desc).Id
     |                  ...     # Wait job finished.
     |                  ...     errs = client.poll(job_id)
     |                  ...     if errs: print ('
     |      '.join(errs))
     |                  ... except ClientError, e:
     |                  ...     print (e.get_status_code(), e.get_code(), e.get_requestid(), e.get_msg())
     |  
     |  delete_cluster(self, cluster)
     |      Release a cluster from batchcompute service.
     |      
     |      @params `cluster`: cluster id info.
     |      @type `cluster`: a `cls-` started {str} or a {CreateResponse} object.
     |      
     |      @example:
     |          >>> client = Client(region, id, key)
     |          ... cluster_id = 'cls-xxxx' 
     |          ... client.delete_cluster(job_id)
     |  
     |  delete_cluster_instance(self, cluster_id, group_name, instance_id)
     |      Recreate a existing instance in cluster.
     |      
     |      @params `cluster_id`: a batchcompute cluster.
     |      @type `cluster_id`: a 'cls-' started {str} or a CreateResponse object.
     |      
     |      @params `group_name`: group name.
     |      @type `group_name`: a {str}.
     |      
     |      @params `instance_id`: id of a instance.
     |      @type `instance_id`: a {str}.
     |      
     |      @example:
     |          >>> client = Client(region, id, key)
     |          ... cluster_id = 'cls-xxxx' 
     |          ... group_name = 'group1' 
     |          ... instance_id = 'i-xxxxxx' 
     |          ... client.delete_cluster_instance(cluster_id, group_name, instance_id)
     |  
     |  delete_image(self, image)
     |      Release a image. 
     |      
     |      @params `image`: a batchcompute image.
     |      @type `image`: a {str} or a CreateResponse object.
     |      
     |      @example:
     |          >>> client = Client(region, id, key)
     |          ... image_id = 'm-xxxx' 
     |          ... client.delete_image(image_id)
     |  
     |  delete_job(self, job)
     |      Release a job. 
     |      
     |      @Notice:
     |          Only Failed, Stopped, Finished job can be deleted.
     |      
     |      @params `job`: a batchcompute job.
     |      @type `job`: a 'job-' started {str} or a CreateResponse object.
     |      
     |      @example:
     |          >>> client = Client(region, id, key)
     |          ... job_id = 'job-xxxx' 
     |          ... client.delete_job(job_id)
     |  
     |  easy_list(self, resource_type, *resource_info, **filters)
     |      List all items with filters. 
     |      
     |      @param `resource_type`: the resource type.
     |      @type `resource_type`: a {str}, only ['jobs', 'clusters', 'images',
     |          'tasks', 'instances'] allowed now.
     |      
     |      @param `resource_info`: position arguments which needed to indicate 
     |          which job's or task's information is interested.
     |      
     |      @param `filters`: key-value arguments which needed to filter interested
     |          items from all other items of a given `resource_type`. 
     |      
     |      @return: A {list} of all items meet the requirements information given
     |           by `filters` parameter.
     |      
     |      @exmaples:
     |          >>> client = Client(region, id, key)
     |          ... for job in client.easy_list('jobs', Name='PythonSDK', Description='test list job') 
     |          ...     print (job.Name, job.Description)
     |          ...
     |          ... job_filters = {
     |          ...     'Name': 'PythonSDK',
     |          ...     'Description': 'test list job'
     |          ... }
     |          ... for job in client.easy_list('jobs', **job_filters):
     |          ...     print (job.Name, job.Description) 
     |          ...
     |          ... for job in client.easy_list('jobs', State=['Waiting', 'Running']):
     |          ...     print (job.Name, job.Description) 
     |          ...
     |          ... state_filter = lambda state: state in ['Waiting', 'Running']
     |          ... for job in client.easy_list('jobs', State=state_filter):
     |          ...     print (job.Name, job.Description) 
     |          ...
     |          ... job_id = 'job-xxx' 
     |          ... client.easy_list('tasks', job_id, State='Running')
     |          ...
     |          ... job_id = 'job-xxx' 
     |          ... task_name = 'Map'
     |          ... client.easy_list('instances', job_id, task_name, State='Running')
     |  
     |  get_cluster(self, cluster)
     |      Get the running status of a cluster. 
     |      
     |      @params `cluster`: cluster id info.
     |      @type `cluster`: a `cls-` started {str} or a {CreateResponse} object.
     |      
     |      @example:
     |          >>> client = Client(region, id, key)
     |          ... cluster_id = 'cls-xxxx' 
     |          ... cluster_status = client.get_cluster(cluster_id)
     |          ... print (cluster_status.State)
     |  
     |  get_cluster_instance(self, cluster_id, group_name, instance_id)
     |      Get running information a instance in cluster.
     |      
     |      @params `cluster_id`: a batchcompute cluster.
     |      @type `cluster_id`: a 'cls-' started {str} or a CreateResponse object.
     |      
     |      @params `group_name`: group name.
     |      @type `group_name`: a {str}.
     |      
     |      @params `instance_id`: id of a instance.
     |      @type `instance_id`: a {str}.
     |      
     |      @example:
     |          >>> client = Client(region, id, key)
     |          ... cluster_id = 'cls-xxxx' 
     |          ... group_name = 'group1' 
     |          ... instance_id = 'i-xxxxxx' 
     |          ... instance_status = client.get_cluster_instance(cluster_id, group_name, instance_id)
     |          ... print (instance_status.InstanceState)
     |  
     |  get_image(self, image)
     |      Get the running status of a image. 
     |      
     |      @params `image`: a batchcompute image.
     |      @type `image`: a {str} or a CreateResponse object.
     |      
     |      @example:
     |          >>> client = Client(region, id, key)
     |          ... image_id = 'm-xxxx' 
     |          ... image_status = client.get_image(image_id)
     |          ... print (image_status.Name)
     |          ... print (image_status.Id)
     |  
     |  get_instance(self, job, task_name, instance_id)
     |      Get instance running information of a task.
     |      
     |      @params `job`: a batchcompute job.
     |      @type `job`: a 'job-' started {str} or a CreateResponse object.
     |      
     |      @params `task_name`: task name.
     |      @type `task_name`: a {str}.
     |      
     |      @params `instance_id`: instance id.
     |      @type `instance_id`: a {int}.
     |      
     |      @example:
     |          >>> client = Client(region, id, key)
     |          ... job_id = 'job-xxxx' 
     |          ... task_name = 'Map' 
     |          ... instance_id = 1 
     |          ... instance_status = client.get_instance(job_id, task_name, instance_id)
     |          ... print (instance_status.State)
     |  
     |  get_job(self, job)
     |      Get the running status of a job. 
     |      
     |      @params `job`: a batchcompute job.
     |      @type `job`: a 'job-' started {str} or a CreateResponse object.
     |      
     |      @example:
     |          >>> client = Client(region, id, key)
     |          ... job_id = 'job-xxxx' 
     |          ... job_status = client.get_job(job_id)
     |          ... print (job_status.State)
     |          ... print (job_status.Id)
     |  
     |  get_job_description(self, job)
     |      Get the description of a job. 
     |      
     |      @params `job`: a batchcompute job.
     |      @type `job`: a 'job-' started {str} or a CreateResponse object.
     |      
     |      @example:
     |          >>> client = Client(region, id, key)
     |          ... job_id = 'job-xxxx' 
     |          ... job_desc = client.get_job_description(job_id)
     |          ... print (job_desc.Description) 
     |          ... print (job_desc.Priority)
     |  
     |  get_task(self, job, task_name)
     |      Get running information of a task.
     |      
     |      @params `job`: a batchcompute job.
     |      @type `job`: a 'job-' started {str} or a CreateResponse object.
     |      
     |      @params `task_name`: task name.
     |      @type `task_name`: a {str}.
     |      
     |      @example:
     |          >>> client = Client(region, id, key)
     |          ... job_id = 'job-xxxx' 
     |          ... task_name = 'Map' 
     |          ... task_status = client.get_task(job_id, task_name)
     |          ... print (task_status.State)
     |  
     |  get_version(self)
     |      Get api version number.
     |      
     |      Return the api version number string.
     |  
     |  list_cluster_instances(self, cluster_id, group_name, marker, max_item_count)
     |      List cluster instances in a specified group.
     |      
     |      @params `cluster_id`: a batchcompute cluster.
     |      @type `cluster_id`: a 'cls-' started {str} or a CreateResponse object.
     |      
     |      @params `group_name`: group name.
     |      @type `group_name`: a {str}.
     |      
     |      @params `marker`: start point of this list action.
     |      @type `marker`: a {str}, usually the content of `NextMarker` property
     |          of the latest list action response, empty {str} triggers another
     |          series of list actions.
     |      
     |      @params `max_item_count`: max item number returned by a single list 
     |          invacation.
     |      @type `max_item_count`: a {int} number. 
     |      
     |      @return: a {ListResponse} object. 
     |      
     |      @example:
     |          >>> client = Client(region, id, key)
     |          ... cluster_id = 'cls-xxxx' 
     |          ... group_name = 'group1' 
     |          ...
     |          ... marker = ''
     |          ... max_item_count = 100
     |          ... cluster_instances = client.list_clusters_instances(cluster_id, group_name, marker, max_item_count)
     |          ... # NextMarker is used to indicate the start point of next list action.
     |          ... print cluster_instances.NextMarker 
     |          ... for instance in cluster_instances.Items:
     |          ...     print (instance.State)
     |  
     |  list_clusters(self, marker, max_item_count)
     |      List clusters with paging enabled.
     |      
     |      @params `marker`: start point of this list action.
     |      @type `marker`: a {str}, usually the content of `NextMarker` property
     |          of the latest list action response, empty {str} triggers another
     |          series of list actions.
     |      
     |      @params `max_item_count`: max item number returned by a single list 
     |          invacation.
     |      @type `max_item_count`: a {int} number. 
     |      
     |      @return: a {ListResponse} object. 
     |      
     |      @example:
     |          >>> client = Client(region, id, key)
     |          ... marker = ''
     |          ... max_item_count = 100
     |          ... clusters = client.list_clusters(marker, max_item_count)
     |          ... # NextMarker is used to indicate the start point of next list action.
     |          ... print clusters.NextMarker 
     |          ... for cluster in clusters.Items:
     |          ...     print (cluster.Name)
     |  
     |  list_images(self, marker, max_item_count)
     |      List images with paging enabled.
     |      
     |      @params `marker`: start point of this list action.
     |      @type `marker`: a {str}, usually the content of `NextMarker` property
     |          of the latest list action response, empty {str} triggers another
     |          series of list actions.
     |      
     |      @params `max_item_count`: max item number returned by a single list 
     |          invacation.
     |      @type `max_item_count`: a {int} number. 
     |      
     |      @return: a {ListResponse} object. 
     |      
     |      @example:
     |          >>> client = Client(region, id, key)
     |          ... marker = ''
     |          ... max_item_count = 100
     |          ... images = client.list_images(marker, max_item_count)
     |          ... # NextMarker is used to indicate the start point of next list action.
     |          ... print (images.NextMarker)
     |          ... for image in images.Items:
     |          ...     print (image.Name)
     |  
     |  list_instances(self, job, task_name, marker, max_item_count)
     |      List instances of a task with paging enabled.
     |      
     |      @params `job`: a batchcompute job.
     |      @type `job`: a 'job-' started {str} or a CreateResponse object.
     |      
     |      @params `task_name`: task name.
     |      @type `task_name`: a {str}.
     |      
     |      @params `marker`: start point of this list action.
     |      @type `marker`: a {str}, usually the content of `NextMarker` property
     |          of the latest list action response, empty {str} triggers another
     |          series of list actions.
     |      
     |      @params `max_item_count`: max item number returned by a single list 
     |          invacation.
     |      @type `max_item_count`: a {int} number. 
     |      
     |      @return: a {ListResponse} object. 
     |      
     |      @example:
     |          >>> client = Client(region, id, key)
     |          ... marker = ''
     |          ... max_item_count = 100
     |          ... job_id = 'job-xxxx' 
     |          ... task_name = 'Map' 
     |          ... instances = client.list_instances(job_id, task_name, marker, max_item_count)
     |          ... # NextMarker is used to indicate the start point of next list action.
     |          ... print (instances.NextMarker)
     |          ... for instance in instances.Items:
     |          ...     print (instance.State)
     |  
     |  list_jobs(self, marker, max_item_count)
     |      A method to list jobs with paging enabled.
     |      
     |      @params `marker`: start point of this list action. 
     |      @type `marker`: a {str}, usually the content of `NextMarker` property
     |          of the latest list action response, empty {str} triggers another
     |          series of list actions.
     |      
     |      @params `max_item_count`: max item number returned by a single list 
     |          invocation.
     |      @type `max_item_count`: a {int} number between 1~100.
     |      
     |      @return: a {ListResponse} object. 
     |      
     |      @example:
     |          >>> client = Client(region, id, key)
     |          ... marker = ''
     |          ... max_item_count = 100
     |          ... jobs = client.list_jobs(marker, max_item_count)
     |          ... # NextMarker is used to indicate the start point of next list action.
     |          ... print jobs.NextMarker 
     |          ... for job in jobs.Items:
     |          ...     print (job.State)
     |  
     |  list_tasks(self, job, marker, max_item_count)
     |      List tasks of a specified job with paging enabled.
     |      
     |      @params `marker`: start point of this list action..
     |      @type `marker`: a {str}, usually the content of `NextMarker` property
     |          of the latest list action response, empty {str} triggers another
     |          series of list actions.
     |      
     |      @params `max_item_count`: max item number returned by a single list 
     |          invocation.
     |      @type `max_item_count`: a {int} number between 1~100. 
     |      
     |      @return: a {ListResponse} object. 
     |      
     |      @example:
     |          >>> client = Client(region, id, key)
     |          ... marker = ''
     |          ... max_item_count = 100
     |          ... job_id = 'job-xxxx' 
     |          ... tasks = client.list_tasks(job_id, marker, max_item_count)
     |          ... # NextMarker is used to indicate the start point of next list action.
     |          ... print (tasks.NextMarker)
     |          ... for task in tasks.Items:
     |          ...     print (task.TaskName, task.State)
     |  
     |  poll(self, job_ids, timeout=86400, interval=3)
     |      Wait for all jobs transist to 'Finished' state.
     |      
     |      @param `job_ids`: job ids for polling. 
     |      @type `job_ids`: a {str}, a {unicode}, a {list} or a {tuple}
     |      
     |      @param `timeout`: timeout value for polling. 
     |      @type verbose: {int}
     |      
     |      @return: A {list} of {str} indicating the errors when polling, for ex-
     |          ample: 'Failed' or 'Stopped' job occurs or timeout, you should ch-
     |          eck whether it is empty ensuring all jobs 'Terminated'.
     |      
     |      @example:
     |          >>> client = Client(region, id, key)
     |          ... job_ids = ['job-xxx', 'job-xxx', 'job-xxx']
     |          ... errs = client.poll(job_ids)
     |          ... if errs:
     |          ...     print ('Some jobs mustbe Failed or Stopped', errs)
     |  
     |  recreate_cluster_instance(self, cluster_id, group_name, instance_id)
     |      Recreate a existing instance in cluster.
     |      
     |      @params `cluster_id`: a batchcompute cluster.
     |      @type `cluster_id`: a 'cls-' started {str} or a CreateResponse object.
     |      
     |      @params `group_name`: group name.
     |      @type `group_name`: a {str}.
     |      
     |      @params `instance_id`: id of a instance.
     |      @type `instance_id`: a {str}.
     |      
     |      @example:
     |          >>> client = Client(region, id, key)
     |          ... cluster_id = 'cls-xxxx' 
     |          ... group_name = 'group1' 
     |          ... instance_id = 'i-xxxxxx' 
     |          ... client.recreate_cluster_instance(cluster_id, group_name, instance_id)
     |  
     |  set_version(self, value)
     |      Set api version number.
     |      
     |      @param `value`: api version number will be sent to batchcompute
     |          service.
     |      @type `value`: a {str} as `2015-11-11`
     |  
     |  start_job(self, job)
     |      Restart a stopped job.
     |      
     |      @Notice:
     |          Only stopped jobs can be restart.
     |      
     |      @params `job`: a batchcompute job.
     |      @type `job`: a 'job-' started {str} or a CreateResponse object.
     |      
     |      @example:
     |          >>> client = Client(region, id, key)
     |          ... job_id = 'job-xxxx' 
     |          ... client.start_job(job_id)
     |  
     |  stop_job(self, job)
     |      Stop a running or waiting job. 
     |      
     |      @Notice:
     |          Only running or waiting jobs can be stopped.
     |      
     |      @params `job`: a batchcompute job.
     |      @type `job`: a 'job-' started {str} or a CreateResponse object.
     |      
     |      @example:
     |          >>> client = Client(region, id, key)
     |          ... job_id = 'job-xxxx' 
     |          ... client.stop_job(job_id)
     |  
     |  ----------------------------------------------------------------------
     |  Static methods defined here:
     |  
     |  get_regions()
     |  
     |  register_region(region_name, url, port=8888)
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)
     |  
     |  version
     |      api version
    
    class ClientError(exceptions.Exception)
     |  Method resolution order:
     |      ClientError
     |      exceptions.Exception
     |      exceptions.BaseException
     |      __builtin__.object
     |  
     |  Methods defined here:
     |  
     |  __init__(self, status, code, request_id, msg)
     |  
     |  __str__(self)
     |  
     |  get_code(self)
     |  
     |  get_msg(self)
     |  
     |  get_requestid(self)
     |  
     |  get_status_code(self)
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)
     |  
     |  ----------------------------------------------------------------------
     |  Data and other attributes inherited from exceptions.Exception:
     |  
     |  __new__ = <built-in method __new__ of type object at 0x7f804c685ca0>
     |      T.__new__(S, ...) -> a new object with type S, a subtype of T
     |  
     |  ----------------------------------------------------------------------
     |  Methods inherited from exceptions.BaseException:
     |  
     |  __delattr__(...)
     |      x.__delattr__('name') <==> del x.name
     |  
     |  __getattribute__(...)
     |      x.__getattribute__('name') <==> x.name
     |  
     |  __getitem__(...)
     |      x.__getitem__(y) <==> x[y]
     |  
     |  __getslice__(...)
     |      x.__getslice__(i, j) <==> x[i:j]
     |      
     |      Use of negative indices is not supported.
     |  
     |  __reduce__(...)
     |  
     |  __repr__(...)
     |      x.__repr__() <==> repr(x)
     |  
     |  __setattr__(...)
     |      x.__setattr__('name', value) <==> x.name = value
     |  
     |  __setstate__(...)
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors inherited from exceptions.BaseException:
     |  
     |  __dict__
     |  
     |  args
     |  
     |  message
     |      exception message
    
    class ConfigError(exceptions.Exception)
     |  Method resolution order:
     |      ConfigError
     |      exceptions.Exception
     |      exceptions.BaseException
     |      __builtin__.object
     |  
     |  Methods defined here:
     |  
     |  __init__(self, msg)
     |  
     |  __str__(self)
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)
     |  
     |  ----------------------------------------------------------------------
     |  Data and other attributes inherited from exceptions.Exception:
     |  
     |  __new__ = <built-in method __new__ of type object at 0x7f804c685ca0>
     |      T.__new__(S, ...) -> a new object with type S, a subtype of T
     |  
     |  ----------------------------------------------------------------------
     |  Methods inherited from exceptions.BaseException:
     |  
     |  __delattr__(...)
     |      x.__delattr__('name') <==> del x.name
     |  
     |  __getattribute__(...)
     |      x.__getattribute__('name') <==> x.name
     |  
     |  __getitem__(...)
     |      x.__getitem__(y) <==> x[y]
     |  
     |  __getslice__(...)
     |      x.__getslice__(i, j) <==> x[i:j]
     |      
     |      Use of negative indices is not supported.
     |  
     |  __reduce__(...)
     |  
     |  __repr__(...)
     |      x.__repr__() <==> repr(x)
     |  
     |  __setattr__(...)
     |      x.__setattr__('name', value) <==> x.name = value
     |  
     |  __setstate__(...)
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors inherited from exceptions.BaseException:
     |  
     |  __dict__
     |  
     |  args
     |  
     |  message
     |      exception message
    
    class FieldError(exceptions.Exception)
     |  Method resolution order:
     |      FieldError
     |      exceptions.Exception
     |      exceptions.BaseException
     |      __builtin__.object
     |  
     |  Methods defined here:
     |  
     |  __init__(self, key)
     |  
     |  __str__(self)
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)
     |  
     |  ----------------------------------------------------------------------
     |  Data and other attributes inherited from exceptions.Exception:
     |  
     |  __new__ = <built-in method __new__ of type object at 0x7f804c685ca0>
     |      T.__new__(S, ...) -> a new object with type S, a subtype of T
     |  
     |  ----------------------------------------------------------------------
     |  Methods inherited from exceptions.BaseException:
     |  
     |  __delattr__(...)
     |      x.__delattr__('name') <==> del x.name
     |  
     |  __getattribute__(...)
     |      x.__getattribute__('name') <==> x.name
     |  
     |  __getitem__(...)
     |      x.__getitem__(y) <==> x[y]
     |  
     |  __getslice__(...)
     |      x.__getslice__(i, j) <==> x[i:j]
     |      
     |      Use of negative indices is not supported.
     |  
     |  __reduce__(...)
     |  
     |  __repr__(...)
     |      x.__repr__() <==> repr(x)
     |  
     |  __setattr__(...)
     |      x.__setattr__('name', value) <==> x.name = value
     |  
     |  __setstate__(...)
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors inherited from exceptions.BaseException:
     |  
     |  __dict__
     |  
     |  args
     |  
     |  message
     |      exception message
    
    class JsonError(exceptions.Exception)
     |  Method resolution order:
     |      JsonError
     |      exceptions.Exception
     |      exceptions.BaseException
     |      __builtin__.object
     |  
     |  Methods defined here:
     |  
     |  __init__(self, msg)
     |  
     |  __str__(self)
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)
     |  
     |  ----------------------------------------------------------------------
     |  Data and other attributes inherited from exceptions.Exception:
     |  
     |  __new__ = <built-in method __new__ of type object at 0x7f804c685ca0>
     |      T.__new__(S, ...) -> a new object with type S, a subtype of T
     |  
     |  ----------------------------------------------------------------------
     |  Methods inherited from exceptions.BaseException:
     |  
     |  __delattr__(...)
     |      x.__delattr__('name') <==> del x.name
     |  
     |  __getattribute__(...)
     |      x.__getattribute__('name') <==> x.name
     |  
     |  __getitem__(...)
     |      x.__getitem__(y) <==> x[y]
     |  
     |  __getslice__(...)
     |      x.__getslice__(i, j) <==> x[i:j]
     |      
     |      Use of negative indices is not supported.
     |  
     |  __reduce__(...)
     |  
     |  __repr__(...)
     |      x.__repr__() <==> repr(x)
     |  
     |  __setattr__(...)
     |      x.__setattr__('name', value) <==> x.name = value
     |  
     |  __setstate__(...)
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors inherited from exceptions.BaseException:
     |  
     |  __dict__
     |  
     |  args
     |  
     |  message
     |      exception message
    
    class ValidationError(exceptions.Exception)
     |  Method resolution order:
     |      ValidationError
     |      exceptions.Exception
     |      exceptions.BaseException
     |      __builtin__.object
     |  
     |  Methods defined here:
     |  
     |  __init__(self, key)
     |  
     |  __str__(self)
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)
     |  
     |  ----------------------------------------------------------------------
     |  Data and other attributes inherited from exceptions.Exception:
     |  
     |  __new__ = <built-in method __new__ of type object at 0x7f804c685ca0>
     |      T.__new__(S, ...) -> a new object with type S, a subtype of T
     |  
     |  ----------------------------------------------------------------------
     |  Methods inherited from exceptions.BaseException:
     |  
     |  __delattr__(...)
     |      x.__delattr__('name') <==> del x.name
     |  
     |  __getattribute__(...)
     |      x.__getattribute__('name') <==> x.name
     |  
     |  __getitem__(...)
     |      x.__getitem__(y) <==> x[y]
     |  
     |  __getslice__(...)
     |      x.__getslice__(i, j) <==> x[i:j]
     |      
     |      Use of negative indices is not supported.
     |  
     |  __reduce__(...)
     |  
     |  __repr__(...)
     |      x.__repr__() <==> repr(x)
     |  
     |  __setattr__(...)
     |      x.__setattr__('name', value) <==> x.name = value
     |  
     |  __setstate__(...)
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors inherited from exceptions.BaseException:
     |  
     |  __dict__
     |  
     |  args
     |  
     |  message
     |      exception message

DATA
    CN_BEIJING = 'batchcompute.cn-beijing.aliyuncs.com'
    CN_HANGZHOU = 'batchcompute.cn-hangzhou.aliyuncs.com'
    CN_QINGDAO = 'batchcompute.cn-qingdao.aliyuncs.com'
    CN_SHENZHEN = 'batchcompute.cn-shenzhen.aliyuncs.com'
    __all__ = ['Client', 'ClientError', 'FieldError', 'ValidationError', '...
    __author__ = 'crisish'
    __version__ = '2.0.7a2'

VERSION
    2.0.7a2

AUTHOR
    crisish


