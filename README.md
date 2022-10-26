
# Book Manager

A CRUP API that stores information about books. Most of the code here was influenced by [this](https://github.com/pixegami/todo-list-api) project. It is a Lambda function written in Python that uses FastAPI. A Function URL is used in order to expose the application. Data storage is done via DynamoDB. The infrastructure is managed via Python CDK.

# How to setup

Create virtualenv using the following command.

```
$ python3 -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

Run the following commands to build the archive for the lambda function.

```bash
# From the root of the project
$ cd api
$ ./package_for_lambda.sh
```

At this point you can now synthesize the CloudFormation template for this code.

```bash
# From the root of the project
$ cdk bootstrap  # Bootstrap CDK if needed
$ cdk synth
$ cdk deploy
```

# How to run the intergration tests

Once the stack has been deployed, update the `ENDPOINT` variable in the `api/test/api_integration_test.py` file to the one that is in the output of the `cdk deploy` run.

Install additional packages for the test using the following commands.

```
$ cd api
$ pip install -r requirements-dev.txt
```

Once the packages are installed, you can now run the tests.

```
$ pytest
```

# How to access the API documentation page

An OpenAPI documentation page is available via a `/docs` URL.

```
<ENDPOINT URL>/docs
```

# Assumptions/Constrains

* The only web interface that is available is the OpenAPI specification page provided by FastAPI.
* ISBN is a unique attribute.
* Search can only be done via using the full name of the `authors` and then an optional `title` query that matches the beginning of the string.
* In order to do an update, you must provide all attributes and not just the once that have changed.
