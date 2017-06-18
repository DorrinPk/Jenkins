# python script to create
# task definition
# service


import boto3
import sys

ecs = boto3.client('ecs', region_name='us-east-1')

name = sys.argv[1]       # main name for everything
env = sys.argv[2]         # which cluster

image = "<account number>.dkr.ecr.us-east-1.amazonaws.com/"+name+":latest"

## see if the service exists

services = ecs.describe_services(
    cluster= env,
    services=[
        name+"-service",
    ]
)

## create task definition
def createtask():
    response = ecs.register_task_definition(
    family= name,
    containerDefinitions=[
        {
            'name': name+"-task",
            'image': image,
            'memory': 128,
            'memoryReservation': 128,
            'logConfiguration': {
                'logDriver': 'fluentd',
                'options': {
                    'fluentd-address': '127.0.0.1:24224'
                }
            }
        },
    ],

)

def describetask():
    global revision
    describetaskresponse = ecs.describe_task_definition(
    taskDefinition=name
)
    revision = describetaskresponse['taskDefinition']['revision']

def deregistertask():
    fulltask=name+":"+ str(revision)
    updatedtaskresponse = ecs.deregister_task_definition(
    taskDefinition= fulltask
)

def createservice():
    serviceresponse = ecs.create_service(
    cluster= env,
    serviceName= name+"-service",
    taskDefinition= name,
    desiredCount=1,
    deploymentConfiguration={
        'maximumPercent': 200,
        'minimumHealthyPercent': 50
    },
    placementStrategy=[
        {
            'type': 'binpack',
            'field': 'memory'
        },
    ]
)

def updateservice():
    updateresponse = ecs.update_service(
    cluster = env,
    service = name+"-service",
    desiredCount=1,
    taskDefinition = name
    )

def main():
    existing_service = services.get("services")
    if existing_service == []:
        print "creating service . . . "
        createtask()
        createservice()
    else:
        print "updating service . . . "
        describetask()
        deregistertask()
        createtask()
        updateservice()

main()
