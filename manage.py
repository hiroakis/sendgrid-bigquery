from bigquery import get_client
import yaml
import datetime
import sys

with open("config/google.yml") as f:
    config = yaml.load(f)

client = get_client(config["auth"]["project_id"],
        service_account=config["auth"]["service_account"],
        private_key_file=config["auth"]["key"],
        readonly=False)

def create_dataset():
    exists = client.check_dataset(config["bigquery"]["dataset"])
    if not exists:
        print "creating %s" % config["bigquery"]["dataset"]
        client.create_dataset(config["bigquery"]["dataset"],
                friendly_name="sendgrid dataset",
                description="A dataset created by me")

def create_tables():
    now = datetime.datetime.now()
    for i in xrange(0, config["bigquery"]["table_counts"]):
        date = now + datetime.timedelta(days = i)
        table_name = config["bigquery"]["table_name"] + date.strftime("%Y%m%d")
        exists = client.check_table(config["bigquery"]["dataset"], table_name)
        if not exists:
            print "creating table %s" % table_name
            created = client.create_table(config["bigquery"]["dataset"], table_name, config["bigquery"]["schemas"])

def delete_dataset():
    confirmation_message = "You are going to delete '%s' dataset Are you sure? [y/N] " % config["bigquery"]["dataset"]
    confirmation = raw_input(confirmation_message)
    if confirmation == "y":
        exists = client.check_dataset(config["bigquery"]["dataset"])
        if exists:
            print "deleting %s" % config["bigquery"]["dataset"]
            client.delete_dataset(config["bigquery"]["dataset"], delete_contents=True)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "Usage: manage.py create|delete"
        sys.exit(1)

    if sys.argv[1] == "create":
        create_dataset()
        create_tables()
    elif sys.argv[1] == "delete":
        delete_dataset()
    else:
        print "Usage: manage.py create|delete"
