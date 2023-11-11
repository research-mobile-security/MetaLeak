from confluent_kafka import Consumer, KafkaError
import subprocess
from confluent_kafka.admin import AdminClient, NewTopic
from confluent_kafka import KafkaException
import time
from time import sleep
from confluent_kafka import Producer
import os
import psutil
########################### Kafka consumer configuration ###########################
conf = {
    'bootstrap.servers': 'localhost:9092',  #Kafka IP
    'group.id': 'my_consumer_group',  # Consumer group ID
    'auto.offset.reset': 'latest',  # Start consuming from the latest offset
    'max.poll.interval.ms': 86400000 # Maximum poll interval of 24 hours
}
########################### Function ###########################
# 1. Create topic = metadta if not exist
def check_create_topic(topic_name):
    bootstrap_servers = 'localhost:9092'  # Replace with your Kafka bootstrap servers
    admin_client = AdminClient({'bootstrap.servers': bootstrap_servers})
    topic_exists = False

    try:
        # Create the topic
        topic_config = {'num_partitions': 1, 'replication_factor': 1}
        topic = NewTopic(topic_name, **topic_config)
        admin_client.create_topics([topic])
        print(f"Topic '{topic_name}' created.")
        
        # Introduce a small delay for topic metadata propagation
        time.sleep(1)

        # Check if the topic exists again
        topic_metadata = admin_client.list_topics(timeout=5).topics
        if topic_name in topic_metadata:
            topic_exists = True
            print(f"Topic '{topic_name}' exists.")
    except KafkaException as e:
        print(f"Error creating or checking topic '{topic_name}': {e}")
# 2. Process when receive messaage
def process_message(message):
    value = message.value().decode('utf-8')
    print('Received message: {}'.format(value))
    
    if value == 'start':
        run_script(web_port,listen_port,tester_name)
    elif value == 'stop':
        stop_script(tester_name)
# 3. Run the script
def run_script(web_port,listen_port,tester_name):
    #subprocess.Popen(['mitmweb', '-s', '/root/metadata-gdpr-server/save_image_request.py', '--web-host', '0.0.0.0', '--web-port', '8081'])
    command = [
        'mitmweb',
        '-s', '/root/metadata-gdpr-server-'+tester_name+'/save_image_request_optimize.py',
        '--web-host', '0.0.0.0',
        '--web-port', str(web_port),#'8081', # change with each user
        '--listen-port', str(listen_port) #'8080' # change with each user
    ]
    try:
        subprocess.Popen(command)
    except FileNotFoundError:
        print("mitmweb command not found")
# 4. Push data to kafka topic
def send_files_to_kafka(directory, topic, bootstrap_servers):
    producer = Producer({'bootstrap.servers': bootstrap_servers})
    for file_name in os.listdir(directory):
        print("-----Send file name "+str(file_name)+"-----")
        file_path = os.path.join(directory, file_name)
        if os.path.isfile(file_path):
            with open(file_path, 'rb') as file:
                file_content = file.read()
                producer.produce(topic, value=file_content)
                producer.flush()
        time.sleep(2)
# 5. Stop the script
def stop_script(tester_name):
    topic_data = "bytes-"+tester_name
    check_create_topic(topic_name)
    time.sleep(7)
    remove_empty_files(data_path)
    time.sleep(5)
    send_files_to_kafka(data_path, topic_data, "localhost:9092")
    time.sleep(5)
    delete_files_in_directory(data_path)
    time.sleep(5)
    #subprocess.Popen(['pkill', '-f', 'mitmweb'])
    kill_service_by_port(listen_port)
    #pass
# 5. Remove all bytes file
def delete_files_in_directory(directory):
    file_list = os.listdir(directory)
    for file_name in file_list:
        file_path = os.path.join(directory, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)
# 6. Kill service based on port
def kill_service_by_port(port):
    try:
        # Get a list of all running processes
        for process in psutil.process_iter(['pid', 'name', 'connections']):
            for conn in process.info['connections']:
                if conn.laddr.port == port:
                    # Terminate the process
                    process.terminate()
                    print(f"Terminated process running on port {port}")
                    return
        print(f"No process found on port {port}")
    except psutil.NoSuchProcess as e:
        print(f"Error killing service: {e}")
# 7. Remove empty file
def remove_empty_files(directory_path):
    min_file_size_kb=5 # remove file < 5kb
     # Convert the minimum file size from KB to bytes
    min_file_size_bytes = min_file_size_kb * 1024
    # Get a list of all files in the directory
    file_list = os.listdir(directory_path)

    # Loop through each file
    for file_name in file_list:
        file_path = os.path.join(directory_path, file_name)

        # Check file size 
        if os.path.isfile(file_path) and os.path.getsize(file_path) < min_file_size_bytes:
            try:
                # Remove the file
                os.remove(file_path)
                print(f"Removed empty file: {file_path}")
            except OSError as e:
                print(f"Error removing file: {file_path}, {e}")
# 8. Check path exist:
def checkFileOrDirectoryExist(path):
    if os.path.exists(path):
        return True
    else:
        return False
########################### Main ###########################
# Static
web_port = 8081
listen_port = 8080
# Create Kafka topic
tester_name = "lam"
topic_name = "metadata-"+tester_name
data_path = "/root/metadata-gdpr-server-"+tester_name+"/bytes/"
check_create_topic(topic_name)
# Create Kafka consumer instance
consumer = Consumer(conf)
# Subscribe to the 'metadata' topic
consumer.subscribe([topic_name])
# Start consuming messages
while True:
    message = consumer.poll(1.0)  # Poll for new messages every 1 second

    if message is None:
        continue
    if message.error():
        if message.error().code() == KafkaError._PARTITION_EOF:
            continue
        else:
            print('Error: {}'.format(message.error()))
            break

    # Process the latest received message
    process_message(message)

# Close the consumer
consumer.close()
