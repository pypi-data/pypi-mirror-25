import os
import time
import json
import click
from tabulate import tabulate

from swag_client.backend import SWAGManager
from swag_client.util import parse_swag_config_options
from swag_client.schemas import v1, v2

from swag_client.migrations import run_migration


def validate_data(data, version=None):
    if version == 1:
        return v1.AccountSchema().load(data)
    else:
        return v2.AccountSchema().load(data)


def create_swag_from_ctx(ctx):
    """Creates SWAG client from the current context."""
    swag_opts = {}
    if ctx.obj['TYPE'] == 'file':
        swag_opts = {
            'swag.type': 'file',
            'swag.data_dir': ctx.obj['DATA_DIR'],
            'swag.data_file': ctx.obj['DATA_FILE']
        }
    elif ctx.obj['TYPE'] == 's3':
        swag_opts = {
            'swag.type': 's3',
            'swag.bucket_name': ctx.obj['BUCKET_NAME'],
            'swag.data_file': ctx.obj['DATA_FILE'],
            'swag.region': ctx.obj['REGION']
        }
    elif ctx.obj['TYPE'] == 'dynamodb':
        swag_opts = {
            'swag.type': 'dynamodb',
            'swag.region': ctx.obj['REGION']
        }
    return SWAGManager(**parse_swag_config_options(swag_opts))


@click.group()
@click.option('--namespace', default='accounts')
@click.pass_context
def cli(ctx, namespace):
    ctx.obj = {'NAMESPACE': namespace}


@cli.group()
@click.option('--region', default='us-east-1', help='Region the table is located in.')
@click.pass_context
def dynamodb(ctx, region):
    ctx.obj['REGION'] = region
    ctx.obj['TYPE'] = 'dynamodb'


@cli.group()
@click.option('--data-dir', help='Directory to store data.', default=os.getcwd())
@click.option('--data-file')
@click.pass_context
def file(ctx, data_dir, data_file):
    """Use the File SWAG Backend"""
    ctx.obj['DATA_DIR'] = data_dir
    ctx.obj['DATA_FILE'] = data_file
    ctx.obj['TYPE'] = 'file'


@cli.group()
@click.option('--bucket-name', help='Name of the bucket you wish to operate on.')
@click.option('--data-file', help='Key name of the file to operate on.')
@click.option('--region', default='us-east-1', help='Region the bucket is located in.')
@click.pass_context
def s3(ctx, bucket_name, data_file, region):
    """Use the S3 SWAG backend."""
    ctx.obj['BUCKET_NAME'] = bucket_name
    ctx.obj['DATA_FILE'] = data_file
    ctx.obj['TYPE'] = 's3'
    ctx.obj['REGION'] = region


@cli.command()
@click.option('--version', default=2, help='Version to validate against.')
@click.pass_context
def validate(ctx, version):
    """Perform validation for SWAG data."""
    data = None

    if ctx.obj['TYPE'] == 'file':
        if ctx.obj['DATA_FILE']:
            file_path = ctx.obj['DATA_FILE']
        else:
            file_path = os.path.join(ctx.obj['DATA_DIR'], ctx.obj['NAMESPACE'] + '.json')

        with open(file_path, 'r') as f:
            data = json.loads(f.read())

    if version == 1:
        data = data['accounts']

    valid = True
    for account in data:
        data, errors = validate_data(account, version=version)
        if errors:
            click.echo(
                click.style('Validation failed. Errors: {errors}'.format(errors=errors), fg='red')
            )
            valid = False

    if valid:
        click.echo(
            click.style('Validation successful.', fg='green')
        )


@cli.command()
@click.pass_context
def list(ctx):
    """List SWAG account info."""
    if ctx.obj.get('NAMESPACE') != 'accounts':
        click.echo(
            click.style('Only account data is available for listing.', fg='red')
        )
        return

    swag = create_swag_from_ctx(ctx)
    accounts = swag.get_all()
    _table = [[result['name'], result.get('id')] for result in accounts]
    click.echo(
        tabulate(_table, headers=["Account Name", "Account Number"])
    )


@cli.command()
@click.option('--start-version', default=1, help='Starting version.')
@click.option('--end-version', default=2, help='Ending version.')
@click.pass_context
def migrate(ctx, start_version, end_version):
    """Transition from one SWAG schema to another."""
    if ctx.obj['TYPE'] == 'file':
        if ctx.obj['DATA_FILE']:
            file_path = ctx.obj['DATA_FILE']
        else:
            file_path = os.path.join(ctx.obj['DATA_DIR'], ctx.obj['NAMESPACE'] + '.json')

        # todo make this more like alemebic and determine/load versions automatically
        with open(file_path, 'r') as f:
            data = json.loads(f.read())

        data = run_migration(data, start_version, end_version)
        with open(file_path, 'w') as f:
            f.write(json.dumps(data))


@cli.command()
@click.pass_context
def propagate(ctx):
    """Transfers SWAG data from one backend to another"""
    data = []
    if ctx.obj['TYPE'] == 'file':
        if ctx.obj['DATA_FILE']:
            file_path = ctx.obj['DATA_FILE']
        else:
            file_path = os.path.join(ctx.obj['DATA_DIR'], ctx.obj['NAMESPACE'] + '.json')

        with open(file_path, 'r') as f:
            data = json.loads(f.read())

    swag_opts = {
        'swag.type': 'dynamodb'
    }

    swag = SWAGManager(**parse_swag_config_options(swag_opts))

    for item in data:
        time.sleep(2)
        swag.create(item)


@cli.command()
@click.pass_context
def create(ctx):
    """Create a new SWAG item."""
    pass


@cli.command()
@click.pass_context
@click.argument('data', type=click.File())
def update(ctx, data):
    """Updates a given record."""
    swag = create_swag_from_ctx(ctx)
    data = json.loads(data.read())

    for account in data:
        account, errors = validate_data(account)

        if errors:
            click.echo(
                json.dumps(account, indent=2)
            )
            click.echo(
                json.dumps(errors)
            )
            continue

        click.echo(click.style(
            'Updated Account. AccountName: {}'.format(account['name']), fg='green')
        )

        swag.update(account)


@cli.command()
@click.argument('data', type=click.File())
@click.pass_context
def seed_aws_data(ctx, data):
    """Seeds SWAG from a list of known AWS accounts."""
    swag = create_swag_from_ctx(ctx)
    for k, v in json.loads(data.read()).items():
        for account in v['accounts']:
            data, errors = validate_data({
                'description': 'This is an AWS owned account used for {}'.format(k),
                'id': account['account_id'],
                'contacts': [],
                'owner': 'aws',
                'provider': 'aws',
                'sensitive': False,
                'email': 'support@amazon.com',
                'name': k + '-' + account['region']
            })

            if errors:
                click.echo(
                    json.dumps(account, indent=2)
                )
                click.echo(
                    json.dumps(errors)
                )

            click.echo(click.style(
                'Seeded Account. AccountName: {}'.format(data['name']), fg='green')
            )

            swag.create(data)


@cli.command()
@click.pass_context
def modifying_secondary_approver(ctx):
    data = [{'googleGroup': 'awssg-aws_dataeng_dr_finance-915405021214',
             'secondaryApprover': 'capacity-planning-finance@netflix.com',
             'roleName': 'aws_dataeng_dr_finance',
             'id': 'aws_dataeng_dr_finance',
             'policyUrl': 'https://stash.corp.netflix.com/projects/CLDSEC/repos/rolliepollie_templates/browse/roles/finance.json'},
            {'googleGroup': 'awssg-aws_dvd_prod_finance-164354612399',
             'secondaryApprover': 'capacity-planning-finance@netflix.com',
             'roleName': 'aws_dvd_prod_finance',
             'id': 'aws_dvd_prod_finance',
             'policyUrl': 'https://stash.corp.netflix.com/projects/CLDSEC/repos/rolliepollie_templates/browse/roles/finance.json'},
            {'googleGroup': 'awssg-aws_dvd_test_finance-967129535581',
             'secondaryApprover': 'capacity-planning-finance@netflix.com',
             'roleName': 'aws_dvd_test_finance',
             'id': 'aws_dvd_test_finance',
             'policyUrl': 'https://stash.corp.netflix.com/projects/CLDSEC/repos/rolliepollie_templates/browse/roles/finance.json'},
            {'googleGroup': 'awssg-aws_ob_test_alpha_admin-713714578568',
             'secondaryApprover': None,
             'roleName': 'aws_ob_test_alpha_admin',
             'id': 'aws_ob_test_alpha_admin',
             'policyUrl': 'https://stash.corp.netflix.com/projects/CLDSEC/repos/rolliepollie_templates/browse/roles/admin.json'},
            {'googleGroup': 'awssg-aws_ob_test_alpha_finance-713714578568',
             'secondaryApprover': 'capacity-planning-finance@netflix.com',
             'roleName': 'aws_ob_test_alpha_finance',
             'id': 'aws_ob_test_alpha_finance',
             'policyUrl': 'https://stash.corp.netflix.com/projects/CLDSEC/repos/rolliepollie_templates/browse/roles/finance.json'},
            {'googleGroup': 'awssg-aws_ob_test_beta_admin-108039169430',
             'secondaryApprover': None,
             'roleName': 'aws_ob_test_beta_admin',
             'id': 'aws_ob_test_beta_admin',
             'policyUrl': 'https://stash.corp.netflix.com/projects/CLDSEC/repos/rolliepollie_templates/browse/roles/admin.json'},
            {'googleGroup': 'awssg-aws_ob_test_beta_finance-108039169430',
             'secondaryApprover': 'capacity-planning-finance@netflix.com',
             'roleName': 'aws_ob_test_beta_finance',
             'id': 'aws_ob_test_beta_finance',
             'policyUrl': 'https://stash.corp.netflix.com/projects/CLDSEC/repos/rolliepollie_templates/browse/roles/finance.json'},
            {'googleGroup': 'awssg-awscontentplatform_finance-267481021547',
             'secondaryApprover': 'capacity-planning-finance@netflix.com',
             'roleName': 'awscontentplatform_finance',
             'id': 'awscontentplatform_finance',
             'policyUrl': 'https://stash.corp.netflix.com/projects/CLDSEC/repos/rolliepollie_templates/browse/roles/finance.json'},
            {'googleGroup': 'awssg-awseur_finance-406704945546',
             'secondaryApprover': 'capacity-planning-finance@netflix.com',
             'roleName': 'awseur_finance',
             'id': 'awseur_finance',
             'policyUrl': 'https://stash.corp.netflix.com/projects/CLDSEC/repos/rolliepollie_templates/browse/roles/finance.json'},
            {'googleGroup': 'awssg-awseurtest_finance-156292793330',
             'secondaryApprover': 'capacity-planning-finance@netflix.com',
             'roleName': 'awseurtest_finance',
             'id': 'awseurtest_finance',
             'policyUrl': 'https://stash.corp.netflix.com/projects/CLDSEC/repos/rolliepollie_templates/browse/roles/finance.json'},
            {'googleGroup': 'awssg-awsoss_finance-awssg-751929122243',
             'secondaryApprover': 'capacity-planning-finance@netflix.com',
             'roleName': 'awsoss_finance',
             'id': 'awsoss_finance',
             'policyUrl': 'https://stash.corp.netflix.com/projects/CLDSEC/repos/rolliepollie_templates/browse/roles/finance.json'},
            {'googleGroup': 'awssg-awsprod_soxaudit-149510111645',
             'secondaryApprover': 'secops@netflix.com',
             'roleName': 'awsprod_soxaudit',
             'id': 'awsprod_soxaudit',
             'policyUrl': 'https://stash.corp.netflix.com/projects/CLDSEC/repos/rolliepollie_templates/browse/roles/soxaudit.json'},
            {'googleGroup': 'awssg-awsseg_finance-443032226508',
             'secondaryApprover': 'secops@netflix.com',
             'roleName': 'awsseg_finance',
             'id': 'awsseg_finance',
             'policyUrl': 'https://stash.corp.netflix.com/projects/CLDSEC/repos/rolliepollie_templates/browse/roles/finance.json'},
            {'googleGroup': 'awssg-awsuswest_finance-286456577209',
             'secondaryApprover': 'capacity-planning-finance@netflix.com',
             'roleName': 'awsuswest_finance',
             'id': 'awsuswest_finance',
             'policyUrl': 'https://stash.corp.netflix.com/projects/CLDSEC/repos/rolliepollie_templates/browse/roles/finance.json'},
            {'googleGroup': 'awssg-awsuswesttest_finance-766713286350',
             'secondaryApprover': 'capacity-planning-finance@netflix.com',
             'roleName': 'awsuswesttest_finance',
             'id': 'awsuswesttest_finance',
             'policyUrl': 'https://stash.corp.netflix.com/projects/CLDSEC/repos/rolliepollie_templates/browse/roles/finance.json'},
            {'googleGroup': 'awssg-beenops_finance-826986664462',
             'secondaryApprover': 'capacity-planning-finance@netflix.com',
             'roleName': 'beenops_finance',
             'id': 'beenops_finance',
             'policyUrl': 'https://stash.corp.netflix.com/projects/CLDSEC/repos/rolliepollie_templates/browse/roles/finance.json'},
            {'googleGroup': 'awssg-cmpses1_finance-904048622432',
             'secondaryApprover': 'capacity-planning-finance@netflix.com',
             'roleName': 'cmpses1_finance',
             'id': 'cmpses1_finance',
             'policyUrl': 'https://stash.corp.netflix.com/projects/CLDSEC/repos/rolliepollie_templates/browse/roles/finance.json'},
            {'googleGroup': 'awssg-cmpses2_finance-151019314534',
             'secondaryApprover': 'capacity-planning-finance@netflix.com',
             'roleName': 'cmpses2_finance',
             'id': 'cmpses2_finance',
             'policyUrl': 'https://stash.corp.netflix.com/projects/CLDSEC/repos/rolliepollie_templates/browse/roles/finance.json'},
            {'googleGroup': 'awssg-cmpses3_finance-932133054308',
             'secondaryApprover': 'capacity-planning-finance@netflix.com',
             'roleName': 'cmpses3_finance',
             'id': 'cmpses3_finance',
             'policyUrl': 'https://stash.corp.netflix.com/projects/CLDSEC/repos/rolliepollie_templates/browse/roles/finance.json'},
            {'googleGroup': 'awssg-cmpses4_finance-880975198854',
             'secondaryApprover': 'capacity-planning-finance@netflix.com',
             'roleName': 'cmpses4_finance',
             'id': 'cmpses4_finance',
             'policyUrl': 'https://stash.corp.netflix.com/projects/CLDSEC/repos/rolliepollie_templates/browse/roles/finance.json'},
            {'googleGroup': 'awssg-cmpses5_finance-270300451856',
             'secondaryApprover': 'capacity-planning-finance@netflix.com',
             'roleName': 'cmpses5_finance',
             'id': 'cmpses5_finance',
             'policyUrl': 'https://stash.corp.netflix.com/projects/CLDSEC/repos/rolliepollie_templates/browse/roles/finance.json'},
            {'googleGroup': 'awssg-dataeng_test_finance-060543065565',
             'secondaryApprover': 'capacity-planning-finance@netflix.com',
             'roleName': 'dataeng_test_finance',
             'id': 'dataeng_test_finance',
             'policyUrl': 'https://stash.corp.netflix.com/projects/CLDSEC/repos/rolliepollie_templates/browse/roles/finance.json'},
            {'googleGroup': 'awssg-dlcme_finance-157314514760',
             'secondaryApprover': 'capacity-planning-finance@netflix.com',
             'roleName': 'dlcme_finance',
             'id': 'dlcme_finance',
             'policyUrl': 'https://stash.corp.netflix.com/projects/CLDSEC/repos/rolliepollie_templates/browse/roles/finance.json'},
            {'googleGroup': 'awssg-encodingops_cde-662787462842',
             'secondaryApprover': None,
             'roleName': 'encodingops_cde',
             'id': 'encodingops_cde',
             'policyUrl': 'https://stash.corp.netflix.com/projects/CLDSEC/repos/rolliepollie_templates/browse/roles/cde.json'},
            {'googleGroup': 'awssg-itops_prod_soxaudit-788777746278',
             'secondaryApprover': 'secops@netflix.com',
             'roleName': 'itops_prod_soxaudit',
             'id': 'itops_prod_soxaudit',
             'policyUrl': 'https://stash.corp.netflix.com/projects/CLDSEC/repos/rolliepollie_templates/browse/roles/soxaudit.json'},
            {'googleGroup': 'awssg-lab_automation_prod_finance-774845362322',
             'secondaryApprover': 'capacity-planning-finance@netflix.com',
             'roleName': 'lab_automation_prod_finance',
             'id': 'lab_automation_prod_finance',
             'policyUrl': 'https://stash.corp.netflix.com/projects/CLDSEC/repos/rolliepollie_templates/browse/roles/finance.json'},
            {'googleGroup': 'awssg-lab_automation_test_finance-927658505930',
             'secondaryApprover': 'capacity-planning-finance@netflix.com',
             'roleName': 'lab_automation_test_finance',
             'id': 'lab_automation_test_finance',
             'policyUrl': 'https://stash.corp.netflix.com/projects/CLDSEC/repos/rolliepollie_templates/browse/roles/finance.json'},
            {'googleGroup': 'awssg-litigation_finance-847046755941',
             'secondaryApprover': 'capacity-planning-finance@netflix.com',
             'roleName': 'litigation_finance',
             'id': 'litigation_finance',
             'policyUrl': 'https://stash.corp.netflix.com/projects/CLDSEC/repos/rolliepollie_templates/browse/roles/finance.json'},
            {'googleGroup': 'awssg-mechanicalturk_finance-329823569757',
             'secondaryApprover': 'capacity-planning-finance@netflix.com',
             'roleName': 'mechanicalturk_finance',
             'id': 'mechanicalturk_finance',
             'policyUrl': 'https://stash.corp.netflix.com/projects/CLDSEC/repos/rolliepollie_templates/browse/roles/finance.json'},
            {'googleGroup': 'awssg-mediapipelinedev_finance-412549767277',
             'secondaryApprover': 'capacity-planning-finance@netflix.com',
             'roleName': 'mediapipelinedev_finance',
             'id': 'mediapipelinedev_finance',
             'policyUrl': 'https://stash.corp.netflix.com/projects/CLDSEC/repos/rolliepollie_templates/browse/roles/finance.json'},
            {'googleGroup': 'awssg-microsites_prod_finance-561684337804',
             'secondaryApprover': 'capacity-planning-finance@netflix.com',
             'roleName': 'microsites_prod_finance',
             'id': 'microsites_prod_finance',
             'policyUrl': 'https://stash.corp.netflix.com/projects/CLDSEC/repos/rolliepollie_templates/browse/roles/finance.json'},
            {'googleGroup': 'awssg-microsites_test_finance-245210267489',
             'secondaryApprover': 'capacity-planning-finance@netflix.com',
             'roleName': 'microsites_test_finance',
             'id': 'microsites_test_finance',
             'policyUrl': 'https://stash.corp.netflix.com/projects/CLDSEC/repos/rolliepollie_templates/browse/roles/finance.json'},
            {'googleGroup': 'awssg-persistence_prod_soxaudit-031606205351',
             'secondaryApprover': 'secops@netflix.com',
             'roleName': 'persistence_prod_soxaudit',
             'id': 'persistence_prod_soxaudit',
             'policyUrl': 'https://stash.corp.netflix.com/projects/CLDSEC/repos/rolliepollie_templates/browse/roles/soxaudit.json'},
            {'googleGroup': 'awssg-pnetest_finance-170547834535',
             'secondaryApprover': 'capacity-planning-finance@netflix.com',
             'roleName': 'pnetest_finance',
             'id': 'pnetest_finance',
             'policyUrl': 'https://stash.corp.netflix.com/projects/CLDSEC/repos/rolliepollie_templates/browse/roles/finance.json'},
            {'googleGroup': 'awssg-project_baldr_coffin_finance-359026904398',
             'secondaryApprover': 'capacity-planning-finance@netflix.com',
             'roleName': 'project_baldr_coffin_finance',
             'id': 'project_baldr_coffin_finance',
             'policyUrl': 'https://stash.corp.netflix.com/projects/CLDSEC/repos/rolliepollie_templates/browse/roles/finance.json'},
            {'googleGroup': 'awssg-sitc_prod_finance-103255076389',
             'secondaryApprover': 'capacity-planning-finance@netflix.com',
             'roleName': 'sitc_prod_finance',
             'id': 'sitc_prod_finance',
             'policyUrl': 'https://stash.corp.netflix.com/projects/CLDSEC/repos/rolliepollie_templates/browse/roles/finance.json'},
            {'googleGroup': 'awssg-sitc_test_finance-678292567210',
             'secondaryApprover': 'capacity-planning-finance@netflix.com',
             'roleName': 'sitc_test_finance',
             'id': 'sitc_test_finance',
             'policyUrl': 'https://stash.corp.netflix.com/projects/CLDSEC/repos/rolliepollie_templates/browse/roles/finance.json'},
            {'googleGroup': 'awssg-travelawsworkspaces_finance-339553139927',
             'secondaryApprover': 'capacity-planning-finance@netflix.com',
             'roleName': 'travelawsworkspaces_finance',
             'id': 'travelawsworkspaces_finance',
             'policyUrl': 'https://stash.corp.netflix.com/projects/CLDSEC/repos/rolliepollie_templates/browse/roles/finance.json'},
            {'googleGroup': 'awssg-turtle_finance-867241597532',
             'secondaryApprover': 'capacity-planning-finance@netflix.com',
             'roleName': 'turtle_finance',
             'id': 'turtle_finance',
             'policyUrl': 'https://stash.corp.netflix.com/projects/CLDSEC/repos/rolliepollie_templates/browse/roles/finance.json'}]

    swag = create_swag_from_ctx(ctx)
    for account in swag.get_all():
        for service in account['services']:
            if service.get('name') == 'console':
                for d in data:
                    if account['id'] in d['googleGroup']:
                        service['roles'].append(d)
        swag.update(account)


@cli.command()
@click.pass_context
def access_logs(ctx):
    swag = create_swag_from_ctx(ctx)
    for account in swag.get_all():
        for service in account['services']:
            if service.get('name') == 's3':
                service['metadata'].update({'accessLogs': {'enabled': True, 'special': False}})

        swag.update(account)


file.add_command(list)
file.add_command(validate)
file.add_command(migrate)
file.add_command(propagate)
file.add_command(create)
file.add_command(seed_aws_data)
file.add_command(update)
dynamodb.add_command(modifying_secondary_approver)
dynamodb.add_command(access_logs)
dynamodb.add_command(list)
dynamodb.add_command(create)
dynamodb.add_command(update)
dynamodb.add_command(seed_aws_data)
s3.add_command(list)
s3.add_command(create)
s3.add_command(update)
s3.add_command(seed_aws_data)
