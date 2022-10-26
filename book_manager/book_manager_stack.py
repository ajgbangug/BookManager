from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_dynamodb as ddb,
    CfnOutput as cfn_output
)
from constructs import Construct

class BookManagerStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        table = ddb.Table(
            self,
            'Books',
            partition_key={'name': 'isbn', 'type': ddb.AttributeType.STRING},
            billing_mode=ddb.BillingMode.PAY_PER_REQUEST
        )

        table.add_global_secondary_index(
            index_name='authorIndex',
            partition_key={'name': 'authors', 'type': ddb.AttributeType.STRING},
            sort_key={'name': 'title', 'type': ddb.AttributeType.STRING}
        )

        api = _lambda.Function(
            self,
            'API',
            runtime=_lambda.Runtime.PYTHON_3_9,
            code=_lambda.Code.from_asset('api/lambda_function.zip'),
            handler='book_manager.handler',
            environment={
                'TABLE_NAME': table.table_name
            }
        )

        function_url = api.add_function_url(
            auth_type=_lambda.FunctionUrlAuthType.NONE,
            cors={
                'allowed_origins': ['*'],
                'allowed_methods': [_lambda.HttpMethod.ALL],
                'allowed_headers': ['*']
            })

        cfn_output(self, 'APIUrl', value=function_url.url)
        table.grant_read_write_data(api)
