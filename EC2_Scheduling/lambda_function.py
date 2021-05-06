import json
import datetime
import boto3

instance_ID = 'L25004-EC2-Scheduling-TEST'

def lambda_handler(event, context):
    client = boto3.client('ec2')  #ec2 client �ҷ�����
    response = client.describe_instances() # ������ �ִ� EC2 instance ��� �Ҵ�
    
    ec2_list = []       # Ÿ�� EC2�� �����ϱ� ���� ����Ʈ. start_instances or stop_instances�� ���, ����Ʈ ���ڸ� �ʼ������� �Ҵ������ ��
    is_Running = False
    
    for ec2 in response['Reservations']:
        for instance in ec2['Instances']:
            for tags in instance['Tags']:
                if tags['Key'] == 'Name':
                    if instance_ID in tags['Value']: # ���� ã���� �ϴ� instance�� �ִ� ���
                        print("\n=== FIND TARGET EC2 ===")
                        print(tags['Value'] + ' : ' + instance['InstanceId'] + '\n')
                        ec2_list.append(instance['InstanceId'])
                            
                        if instance['State']['Code'] == 16: # running(16) # ���� running ���̸� is_Running�� True�� ����
                            is_Running = True
                        else :      # �׷��� �ʴٸ� False
                            is_Running = False


    if is_Running == False :    # ���� EC2�� running ������ �����Ƿ� start���ش�
        start = client.start_instances(InstanceIds = ec2_list)
        print("=== SERVER START ====")
        return start
    else :                      # ���� Ÿ�� EC2�� running ���̶�� Stop���ش�.
        stop = client.stop_instances(InstanceIds = ec2_list)
        print("=== SERVER STOP ====")
        return stop


'''
### client ���� ���� ###
client.describe_instances()
return >> https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_instances

### start_instances, stop_instances �Լ� ���� ���� ###
start_instances(InstanceIds(list), AdditionalInfo(str), DryRun(boolean))
>> client.start_instances(
    InstanceIds=[
        'string',
    ],
    AdditionalInfo='string',
    DryRun=True|False
)

### instance['State']['Code']�� ���ϰ�. �� ���¿� ���� ���� �ѹ��� ������ ###
# code value: 0 (pending), 16 (running), 32 (shutting-down), 48 (terminated), 64 (stopping), and 80 (stopped)

cron(0 9/8 ? * MON-FRI *) ���� 9~17��
'''