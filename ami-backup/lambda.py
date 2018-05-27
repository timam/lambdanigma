mport boto3
import datetime

ec2 = boto3.resource('ec2')
client = boto3.client('ec2')


def lambda_handler(event, context):
    instances = ec2.instances.filter(
        Filters=[{'Name': 'tag-key', 'Values': ['backup', 'Backup']}])

    for instance in instances:
        all_amis = []
        instance_id = instance.id
        print("Instance Type: " + instance.instance_type)

        # Getting Instance Name
        instance_tags = instance.tags
        print(instance_tags)
        instance_name = 'N/A'
        for tags in instance_tags:
            if tags["Key"] == 'Name':
                instance_name = tags["Value"]

        # Date Format
        create_time = datetime.datetime.now()
        create_fmt = create_time.strftime('%Y-%m-%d')

        ami_id = client.create_image(InstanceId=instance_id, Name=instance_name + '_' + instance_id + '_' + create_fmt,
                                     NoReboot=True, DryRun=False)

        all_amis.append(ami_id['ImageId'])

        client.create_tags(
            Resources=all_amis,
            Tags=[
                {'Key': 'Name', 'Value': instance_name + '_' + create_fmt}
            ]
        )
