import logging
from datetime import datetime

LOGGING = logging.getLogger(__name__)

from airflow.models import Variable
from airflow.providers.amazon.aws.hooks.base_aws import AwsBaseHook

def airflow_notify_sns(context, **kwargs):
    """ 
    Publish Airflow Error Notification to a SNS Topic

    Parameters:
        context (dict): Airflow task execution context
    
    Returns:
        boto3 sns_client.publish() response
    """
    sns_client = AwsBaseHook(client_type="sns", aws_conn_id='aws_default')
    sns_topic_arn = Variable.get('airflow_notify_sns_arn', None)

    # Make variable required
    if sns_topic_arn is None:
        LOGGING.error("Variable [airflow_notify_sns_arn] not found in Airflow")
        return None


    # Message attributes
    subject = "Airflow task execution failed"
    message = get_message_text(context)

    # Sending message to topic
    LOGGING.info(f"Error message to send: {message}")
    LOGGING.info(f"Sending error message to SNS Topic ARN [{sns_topic_arn}]")
    try:
        response = sns_client.get_conn().publish(
            TopicArn=sns_topic_arn,
            Subject=subject,
            Message=message
        )
        LOGGING.info("Message successfully sent do SNS Topic")
        return response
    except Exception as ex:
        LOGGING.error(f"Error sending message to SNS: [{ex}]")
        return None

    return None

def get_message_text(context):
    return """Airflow task execution failed. 
    *Time*: {time}  
    *Task*: {task}  
    *Dag*: {dag} 
    *Execution Time*: {exec_date}  
    *Log Url*: {log_url} 
    """.format(
        time=datetime.now(),
        task=context.get('task_instance').task_id,
        dag=context.get('task_instance').dag_id,
        ti=context.get('task_instance'),
        exec_date=context.get('execution_date'),
        log_url=context.get('task_instance').log_url,
    )