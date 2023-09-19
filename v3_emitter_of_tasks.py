"""
Version 3 - RabbitMQ Task Emitter

This program sends messages to a RabbitMQ queue by reading tasks from a CSV file.
It demonstrates the use of RabbitMQ for distributing tasks to multiple workers.

Author: Kim Leach
Date: 09/18/20203

"""


# Import necessary libraries
import pika
import sys
import webbrowser
import csv

def offer_rabbitmq_admin_site():
    """
    Offer to open the RabbitMQ Admin website if show_offer is True.
    RabbitMQ Admin allows monitoring of RabbitMQ queues.
    Modify the 'show_offer' variable to control this feature.

    """
    show_offer = True  # Set to True to offer opening the admin site, False to skip
    if show_offer:
        webbrowser.open_new("http://localhost:15672/#/queues")

def send_message(host: str, queue_name: str, message: str):
    """
    Creates and sends a message to the queue each execution.
    
    Parameters:
        host (str): the host name or IP address of the RabbitMQ server
        queue_name (str): the name of the queue
        message (str): the message to be sent to the queue
    
    """
import pika
import sys
import webbrowser
import csv
import time

# Define the CSV file as a variable
csv_file = 'tasks.csv'

def offer_rabbitmq_admin_site():
    """Offer to open the RabbitMQ Admin website"""
    ans = input("Would you like to monitor RabbitMQ queues? y or n ")
    print()
    if ans.lower() == "y":
        webbrowser.open_new("http://localhost:15672/#/queues")
        print()

def send_message(host: str, queue_name: str, message: str):
    """
    Creates and sends a message to the queue each execution.
    This process runs and finishes.

    Parameters:
        host (str): the host name or IP address of the RabbitMQ server
        queue_name (str): the name of the queue
        message (str): the message to be sent to the queue
    """

    try:
        # create a blocking connection to the RabbitMQ server
        conn = pika.BlockingConnection(pika.ConnectionParameters(host))
        # use the connection to create a communication channel
        ch = conn.channel()
        # use the channel to declare a durable queue
        # a durable queue will survive a RabbitMQ server restart
        # and help ensure messages are processed in order
        # messages will not be deleted until the consumer acknowledges
        ch.queue_declare(queue=queue_name, durable=True)
        # use the channel to publish a message to the queue
        # every message passes through an exchange
        ch.basic_publish(exchange="", routing_key=queue_name, body=message)
        # print a message to the console for the user
        print(f" [x] Sent {message}")
    except pika.exceptions.AMQPConnectionError as e:
        print(f"Error: Connection to RabbitMQ server failed: {e}")
        sys.exit(1)
    finally:
        # close the connection to the server
        conn.close()

if __name__ == "__main__":
    # ask the user if they'd like to open the RabbitMQ Admin site
    offer_rabbitmq_admin_site()

    # Read tasks from the CSV file
    tasks = []
    with open(csv_file, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            tasks.append(row[0])  # Assuming the tasks are in the first column of the CSV

    # Loop through the tasks and send them to the queue with a delay based on the number of periods
    for task in tasks:
        message = task.rstrip('.')  # Remove trailing periods
        num_periods = len(task) - len(message)
        send_message("localhost", "task_queue2", message)
        
        # Delay based on the number of periods (one second per period)
        time.sleep(num_periods)
