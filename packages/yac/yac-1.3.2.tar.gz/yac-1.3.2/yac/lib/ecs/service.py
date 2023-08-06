# stop an ecs service
def stop_ecs_service( cluster_name, service_search_str , time_out_sec=0):

    client = boto3.client('ecs')

    stopped = False

    # get the service requested
    service = find_service_by_name(cluster_name,service_search_str)

    if (service):

        # get the task definition for this service in this cluster
        task_definition=str(service['taskDefinition'])

        print 'Stopping the %s service on the %s cluster  ...'%(service_name,
                          cluster_name )

        # stop the cluster by setting desiredCount to 0
        response = client.update_service(
                        cluster=cluster_name,
                        service=cluster_name,
                        taskDefinition=task_definition,
                        desiredCount=0) 

        if time_out_sec > 0:
            stopped = wait_for_running_count(cluster_name, service_name, 0, timeout_sec)

    return stopped

# start an ecs service
def start_ecs_service( cluster_name, service_search_str , time_out_sec=0):

    client = boto3.client('ecs')

    # get the service requested
    service = find_service_by_name(cluster_name, service_search_str)

    if (service):

        # get the task definition for this service in this cluster
        task_definition=str(service['taskDefinition'])

        print 'Starting the %s service on the %s cluster  ...'%(service_name,
                          cluster_name )

        # start the cluster by setting desiredCount to 1
        response = client.update_service(
                        cluster=cluster_name,
                        service=cluster_name,
                        taskDefinition=task_definition,
                        desiredCount=1) 

        if time_out_sec > 0:
            wait_for_running_count(cluster_name, service_name, 1, timeout_sec)

def find_service_by_name(cluster_name, search_string):

    service = {}

    client = boto3.client('ecs')

    # get the services on this cluster
    services_arns = client.list_services(cluster=cluster_name)

    for services_arn in services_arns['serviceArns']:

        if search_string in services_arn:

            # get a full description of this service
            services = client.describe_services(cluster=cluster_name, services=[services_arn])

            if ( len(services['services'])==1 ):

                return services[0]

    return service

def find_cluster_by_name(search_string):

    cluster = {}

    client = boto3.client('ecs')

    # get all clusters
    clusters = client.list_clusters()

    for cluster in clusters['clusterArns']:

        if search_string in cluster:

            return cluster

    return cluster

def wait_for_running_count(cluster_name, search_string, count, timeout_sec):

    stopped = False

    service = find_service_by_name(cluster_name, search_string)

    if service:

        # get the running count
        runningCount=int(service['runningCount'])

        total_wait_time_sec = 0
        sleep_time = 2

        while (runningCount != count and total_wait_time_sec < timeout_sec):

            # sleep for a few seconds and check again            
            time.sleep(sleep_time)

            total_wait_time_sec = total_wait_time_sec + sleep_time

            service = find_service_by_name(cluster_name, search_string)
            runningCount=int(service['runningCount'])

        if total_wait_time_sec < timeout_sec:
            stopped = True

    return stopped    