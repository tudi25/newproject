import boto3
import click

session = boto3.Session(profile_name='tudi')
ec2 = session.resource('ec2')

@click.group()
def cli():
        "Manage snapshots"

@cli.group('snapshots')
def snapshots():
        "Command for snapshots"

@snapshots.command('list')
@click.option('--project', default=None, help="Only snapshots for project(tag instanse:<name>)")
def list_volumes(project):
    "List of Snapshots"

    instances = []

    if project:
        filters = [{'Name':'tag:Instanse', 'Values':[project]}]
        instances = ec2.instances.filter(Filters=filters)
    else:
        instances = ec2.instances.all()

    for i in instances:
        for v in i.volumes.all():
            for s in v.snapshots.all():
                print(', '.join((
                    s.id,
                    v.id,
                    i.id,
                    s.state,
                    s.progress,
                    s.start_time.strftime("%c")
                )))
    return
@cli.group('volumes')
def volumes():
        "Command for volumes"

@volumes.command('list')
@click.option('--project', default=None, help="Only instances for project(tag instanse:<name>)")
def list_volumes(project):
    "List of Volumes"

    instances = []

    if project:
        filters = [{'Name':'tag:Instanse', 'Values':[project]}]
        instances = ec2.instances.filter(Filters=filters)
    else:
        instances = ec2.instances.all()

    for i in instances:
        for v in i.volumes.all():
            print(', '.join((
                v.id,
                i.id,
                v.state,
                str(v.size) + "GiB",
                v.encrypted and "Encrypted" or "Not Encrypted"
            )))
    return

@cli.group('instances')
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
    cli()
