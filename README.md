# serverless

how to generate zip file and upload it to s3
ref: https://docs.aws.amazon.com/lambda/latest/dg/python-package.html

```angular2html
# with package
pip install --target ./package boto3
cd package
zip -r ../main.zip .
cd ..
zip main.zip main.py

```

```angular2html
# without package

zip main.zip main.py
```

upload to s3 manually
