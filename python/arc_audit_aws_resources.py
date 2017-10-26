import boto3



# def List_instances_with_tag(tagkey, tagvalue):
#     ec2client = boto3.client('ec2', region_name='us-east-1')
#     response = ec2client.describe_instances(Filters=[{'Name': 'tag:'+tagkey,'Values': [tagvalue]}])

#     instancelist = []

#     for reservation in (response["Reservations"]):
#         for instance in reservation["Instances"]:
#             instancelist.append(instance["InstanceId"])
#     return  instancelist



def Instance_without_cost_tag(fid):
    ec2 = boto3.resource('ec2')
    ec2instance = ec2.Instance(fid)
    instancename = ''
    for tags in ec2instance.tags:
        if tags["Key"] == 'Name':
            instancename = tags["Value"]
    print instancename


# INSTANCES = List_instances_with_tag('cost', 'baam')


# print INSTANCES


# for fid in INSTANCES:
#     print 'Now getting the Name of {}'.format(fid)
#     Instance_without_cost_tag(fid)

list1 = ['i-2db8fedd', 'i-1c0e772d' ]

for i in list1:
    print i
    Instance_without_cost_tag(i)
