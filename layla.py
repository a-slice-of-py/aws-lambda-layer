#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import textwrap
from pathlib import Path

format_code = lambda x: textwrap.dedent(x).strip()

class LayLa:
    """
    LayLa (LAYer LAmbda) implements an easy way to initialize a Lambda layer ready for build and deploy via aws-sam.
    """

    def __init__(
        self,
        layer_name: str,
        contents: list,
        stack_name: str,
        s3_bucket: str = None,
        region_name: str = 'eu-central-1',
        target_dir: str = '.'
        ):
        """Initialize the class.

        Parameters
        ----------
        layer_name : str
            Layer name, will be used for some AWS resources.
        contents : list
            List of Python libraries to be included in the layer.
        stack_name : str
            Name of CloudFormation stack.
        s3_bucket : str, optional
            Name of s3 bucket in which aws-sam artifacts must be stored, by default None.
        region_name : str, optional
            Name of aws region, by default 'eu-central-1'.
        target_dir : str, optional
            Target directory in which layer must be initialized, by default '.'.
        """

        self.layer_name = layer_name
        self.contents = contents
        self.stack_name = stack_name
        self.s3_bucket = s3_bucket
        self.region_name = region_name
        self.target_dir = target_dir
        self.make_app()

    def make_app(self):
        """
        Creates layer directory structure and writes down couple of useful files
        - requirements.txt and layla_lambda.py, which are the actual layer creation trigger
        - samconfig.toml, which contains aws-sam config parameters
        - template.yaml, which is the CloudFormation stack template
        """
        root_dir = f'{self.target_dir}'
        if not Path(root_dir).exists():
            Path(root_dir).mkdir()

        if not Path(f'{root_dir}/contents').exists():
            Path(f'{root_dir}/contents').mkdir()

        p = Path(f'{root_dir}/contents/__init__.py')
        with p.open('w') as f:
            f.close()

        self.newline = "\n"
        static_code = (
            '''
            import json

            def lambda_handler(event, context):
                return {
                    'statusCode': 200,
                    'body': json.dumps('Hello from Layla!')
                }
            '''
            )
        lambda_code = format_code(
            f'''
            {format_code(self.newline.join('import ' + lib for lib in self.contents))}{self.newline}{format_code(static_code)}
            '''
            )
        config_code = format_code(
            f'''
            version = 0.1
            [default]
            [default.deploy]
            [default.deploy.parameters]
            stack_name = "{self.stack_name}"
            s3_bucket = "{self.s3_bucket}"
            s3_prefix = "{self.stack_name}"
            region = "{self.region_name}"
            confirm_changeset = true
            capabilities = "CAPABILITY_IAM"
            '''
            )
        lambda_prefix = 'LaylaLambda'
        safe_name = self.layer_name.title().replace('_','')
        template_code = format_code(
            f'''
            AWSTemplateFormatVersion: '2010-09-09'
            Transform: AWS::Serverless-2016-10-31

            Description: layer description.

            Globals:
                Function:
                    Runtime: python3.6

            Resources:
                {lambda_prefix}{safe_name}:
                    Type: AWS::Serverless::Function
                    Properties:
                        CodeUri: contents/
                        Handler: layla_lambda.lambda_handler
                LaylaLayer{safe_name}:
                    Type: AWS::Serverless::LayerVersion
                    Properties:
                        LayerName: {safe_name}
                        Description: Layer containing custom libraries
                        ContentUri: ./.aws-sam/build/{lambda_prefix}{safe_name}
                        CompatibleRuntimes:
                            - python3.6
                            - python3.7
                        RetentionPolicy: Delete
                    DependsOn: {lambda_prefix}{safe_name}
            '''
            )

        p = Path(f'{root_dir}/contents/layla_lambda.py')
        with p.open('w') as f:
            f.write(lambda_code)
            f.close()

        p = Path(f'{root_dir}/contents/requirements.txt')
        with p.open('w') as f:
            f.write(format_code(self.newline.join(self.contents)))
            f.close()

        p = Path(f'{root_dir}/samconfig.toml')
        with p.open('w') as f:
            f.write(config_code)
            f.close()

        p = Path(f'{root_dir}/template.yaml')
        with p.open('w') as f:
            f.write(template_code)
            f.close()

def main():
    parser = argparse.ArgumentParser(description='Initialize a SAM app to manage a custom Lambda layer.')
    parser.add_argument(
        '-d',
        '--directory',
        action="store",
        dest="target_dir",
        help="the directory in which initialize the app",
        default="."
        )
    parser.add_argument(
        '-n',
        '--layer-name',
        action="store",
        dest="layer_name",
        help="the name of the layer (will be used for root directory and AWS resources)",
        default="hello-world"
        )
    parser.add_argument(
        '-s',
        '--stack-name',
        action="store",
        dest="stack_name",
        help="the name of the AWS stack",
        default="layla-stack"
        )
    parser.add_argument(
        '-c',
        '--contents',
        action="store",
        dest="contents",
        help="the libraries to be included within the layer",
        nargs="+"
        )
    parser.add_argument(
        '-r',
        '--region-name',
        action="store",
        dest="region_name",
        help="the AWS region",
        default="eu-central-1"
        )
    parser.add_argument(
        '-b',
        '--bucket',
        action="store",
        dest="bucket",
        help="the S3 bucket in which store layer contents",
        )
    args = parser.parse_args()
    app = LayLa(
        args.layer_name,
        args.contents,
        args.stack_name,
        s3_bucket=args.bucket,
        region_name=args.region_name,
        target_dir=args.target_dir
        )

if __name__ == '__main__':
    main()