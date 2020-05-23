import boto3
import click

session = boto3.Session(profile_name='tudi')
ec2 = session.resource('ec2')

@click.group()
def instances():
        """Command for instances"""

@instances.command('list')
@click.option('--project', default=None, help="Only instances for project(tag instanse:<name>)")
def list_instanses(project):
    "List EC2"
    instances = []

    if project:
        filters = [{'Name':'tag:Instanse', 'Values':[project]}]
        instances = ec2.instances.filter(Filters=filters)
    else:
        instances = ec2.instances.all()

    for i in instances:
        tags= {t['Key']: t['Value'] for t in i.tags or [] }
        print(', '.join((
        i.id,
        i.instance_type,
        i.placement['AvailabilityZone'],
        i.state['Name'],
        i.public_dns_name,
        tags.get('Instanse', '<no project>')
        )))
    return

@instances.command('stop')
@click.option('--project', default=None, help="Only instances for project(tag instanse:<name>)")
def stop_instanses(project):
    "Stop EC2"
    instances = []
    if project:
        filters = [{'Name':'tag:Instanse', 'Values':[project]}]
        instances = ec2.instances.filter(Filters=filters)
    else:
        instances = ec2.instances.all()
    for i in instances:
        print("Stopping {0}....".format(i.id))
    return

if __name__ == '__main__':
    instances()
