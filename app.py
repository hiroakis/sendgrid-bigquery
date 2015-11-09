from tornado import ioloop, web, gen
from bigquery import get_client
import yaml
import datetime, time, sys, json, hashlib

with open("config/google.yml") as f:
    config = yaml.load(f)

client = get_client(config["auth"]["project_id"],
        service_account=config["auth"]["service_account"],
        private_key_file=config["auth"]["key"],
        readonly=False)

class SendGridEventHandler(web.RequestHandler):

    @gen.coroutine
    def insert_bigquery(self, mails):
        rows = []
        date = datetime.datetime.now()
        unixtimestamp = time.mktime(date.timetuple())
        for mail in mails:
            hashed_email = hashlib.sha256(mail["email"] + config["bigquery"]["salt"]).hexdigest()
            row = {"unixtimestamp": int(unixtimestamp),
                    "datetime": str(date),
                    "sendgrid_timestamp": mail["timestamp"],
                    "email": hashed_email,
                    "event": mail["event"],
                    "reason": mail.get("reason"),
                    "response": mail.get("response")}
            rows.append(row)

        table_name = config["bigquery"]["table_name"] + date.strftime("%Y%m%d")
        success = client.push_rows(config["bigquery"]["dataset"], table_name, rows)
        return success

    @gen.coroutine
    def post(self):
        success = yield self.insert_bigquery(json.loads(self.request.body))
        if success:
            self.set_status(200)
            self.content_type = 'application/json'
            self.finish({"message": "OK"})
        else:
            self.set_status(503)
            self.content_type = 'application/json'
            self.finish({"message": "Service Unavailable: please retry."})

class HealthCheckHandler(web.RequestHandler):

    @gen.coroutine
    def get(self):
        self.set_status(200)
        self.content_type = 'application/json'
        self.finish({"message": "healthy"})


app = web.Application([
    (r"/", SendGridEventHandler),
    (r"/health", HealthCheckHandler),
])

if __name__ == '__main__':
    app.listen(5000)
    ioloop.IOLoop.instance().start()

