import boto3
import click

session = boto3.Session(profile_name='shotty')
ec2 = session.resource('ec2')

@click.command()
@click.option('--project', default=None,
    help="Only instances for project (tag Project:<name>)")
def list_instances():
    "List EC2 instances"
    intances = []

    if project:
        filters = [{'Name':'tag:Project', 'Values':[project]}]
        instances = ec2.instances.filter(Filters=filters)
    else:
        instances = ec2.instances.all()

    for i in ec2.instances.all():
        tags = { t['Key']: t['Value'] for t in i.tags or [] }
        print(','.join((
            i.id,
            i.instance_type,
            i.placement['AvailabilityZone'],
            i.state['Name'],
            i.public_dns_name,
            tags.get('Project', '<no project>')
            )))

    return

if __name__ == '__main__':
    list_instances()

    ##something in lines 20-34 is going wrong, don't know what
