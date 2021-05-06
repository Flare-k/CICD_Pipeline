import json
import datetime
import boto3

instance_ID = 'L25004-EC2-Scheduling-TEST'

def lambda_handler(event, context):
    client = boto3.client('ec2')  #ec2 client 불러오기
    response = client.describe_instances() # 계정에 있는 EC2 instance 모두 할당
    
    ec2_list = []       # 타겟 EC2를 저장하기 위한 리스트. start_instances or stop_instances의 경우, 리스트 인자를 필수적으로 할당해줘야 함
    is_Running = False
    
    for ec2 in response['Reservations']:
        for instance in ec2['Instances']:
            for tags in instance['Tags']:
                if tags['Key'] == 'Name':
                    if instance_ID in tags['Value']: # 만약 찾고자 하는 instance가 있는 경우
                        print("\n=== FIND TARGET EC2 ===")
                        print(tags['Value'] + ' : ' + instance['InstanceId'] + '\n')
                        ec2_list.append(instance['InstanceId'])
                            
                        if instance['State']['Code'] == 16: # running(16) # 현재 running 중이면 is_Running을 True로 갱신
                            is_Running = True
                        else :      # 그렇지 않다면 False
                            is_Running = False


    if is_Running == False :    # 현재 EC2가 running 중이지 않으므로 start해준다
        start = client.start_instances(InstanceIds = ec2_list)
        print("=== SERVER START ====")
        return start
    else :                      # 현재 타겟 EC2가 running 중이라면 Stop해준다.
        stop = client.stop_instances(InstanceIds = ec2_list)
        print("=== SERVER STOP ====")
        return stop


'''
### client 내용 설명 ###
client.describe_instances()
return >> https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_instances

### start_instances, stop_instances 함수 인자 설명 ###
start_instances(InstanceIds(list), AdditionalInfo(str), DryRun(boolean))
>> client.start_instances(
    InstanceIds=[
        'string',
    ],
    AdditionalInfo='string',
    DryRun=True|False
)

### instance['State']['Code']의 리턴값. 각 상태에 따라 고유 넘버가 존재함 ###
# code value: 0 (pending), 16 (running), 32 (shutting-down), 48 (terminated), 64 (stopping), and 80 (stopped)

cron(0 9/8 ? * MON-FRI *) 평일 9~17시
'''