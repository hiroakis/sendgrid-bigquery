# sendgrid-bigquery

This is a tool that inserts sendgrid notification to google bigquery.
The tool using Python 2.7 because I'm going to deploy this tool to AWS Lambda. But there is a problem(see TODO section) which I faced with.

## Installation & Preparement

* create google.yml and google.p12

Copy `config/google.yml.example` to `config/google.yml`. And put google.p12 to `config/google.p12`.

* create tables on google bigquery.

```
python manage.py create
```

If you would like to delete dataset, execute `python manage.py delete`.

* run app.py

```
python app.py
```

* configure sendgrid webhook

Visit sendgrid console, then SETTINGS -> Mail Settings -> Event Notification.

## Note

The tool will encrypt email with sha256 and salt before insert to bigquery.
You can obtain hash value as following.

```
python -c "import hashlib; print hashlib.sha256('user@raw.email' + 'SALT').hexdigest()"
```

## TODO

Deploy to AWS Lambda + AWS API Gateway. I tried it, however I faced with following problem.
I couldn't deploy this application to the AWS Lambda.

```
START RequestId: XXXXXXXXXXXX Version: $LATEST
module initialization error: No crypto library available

END RequestId: XXXXXXXXXXXXXXX
REPORT RequestId: XXXXXXXXXX  Duration: 0.35 ms   Billed Duration: 100 ms     Memory Size: 256 MB Max Memory Used: 14 MB  
```

How do I solve this problem?

## License

MIT
