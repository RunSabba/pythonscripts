#https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/instances.html
import boto3
from datetime import datetime, timedelta, timezone
region = "us-east-1"
ec2 = boto3.resource('ec2',region_name=region)
cloudwatch = boto3.client('cloudwatch', region_name=region)

def list_instances_and_metrics():
    instance_filter = {"Name":"instance-state-name", "Values": ["running"]}
    instances = list(ec2.instances.filter(Filters=[instance_filter]))
    if instances:
        for instance in instances:
            try:
                print(f"\nEC2 instance: {instance.id} is running in {region} region.")
                get_cpu_utilization(instance)
            except Exception as e:
                print(f"Unable to poll the {instance.id} instance in the {region} region. {e}")
    else:
        print(f" No EC2 instances are running in the {region} region.")


def get_cpu_utilization(instance):
    cpu_stats = cloudwatch.get_metric_statistics(
        Namespace='AWS/EC2',
        MetricName = 'CPUUtilization',
        Dimensions = [{'Name': 'InstanceId', 'Value': instance.id}],
        StartTime = datetime.now(timezone.utc) - timedelta(minutes=10),
        EndTime = datetime.now(timezone.utc),
        Period = 60,
        Statistics = ['Average']
    )

    if cpu_stats['Datapoints']:
        average_cpu = cpu_stats['Datapoints'][0]['Average']
        print(f"The average CPU Utilization for {instance.id}: {average_cpu}")
        if average_cpu > 70:
            ec2_high_util_alert(instance.id, average_cpu)
    else:
        print(f"No CPU Utilization stats available for {instance.id} at the moment.") 

def ec2_high_util_alert(instance_id,average_cpu):
    print(f"CLOUDWATCH ALERT: Instance {instance_id} is currently using {average_cpu} CPU, which exceeds the threshold set.")
    #complete the rest of the sns topic tomorrow.

list_instances_and_metrics()