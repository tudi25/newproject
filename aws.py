import boto3

session = boto3.Session(profile_name='tudi')
ec2 = session.resource('ec2')

def list_instanses():
    for i in ec2.instances.all():
        print(i)

if __name__ == '__main__':
    list_instanses()
