import sys
import os
import anyio
import base
import dagger


async def test(version: str):
    """Runs all the automated tests
    """
    async with dagger.Connection(dagger.Config(log_output=sys.stderr)) as client:

        gcp_credentials_content = client.set_secret(
            "gcp-file-secret-content",
            os.environ['GOOGLE_APPLICATION_CREDENTIALS_CONTENT'],
        )

        src = client.host().directory('.')

        setup = (
            base.thipsterBase(client, version)
            .with_mounted_directory('/src', src)
            .with_workdir('/src')
            .with_exec(['pip', 'install', '-e', '.[test]'])
            .with_secret_variable(
                'GOOGLE_APPLICATION_CREDENTIALS_CONTENT', gcp_credentials_content,
            )
        )

        tests = setup.with_exec(['pytest', 'tests'])
        # execute
        await tests.exit_code()

    print('Tests succeeded!')


if __name__ == '__main__':
    python_version = '3.11'
    anyio.run(test, python_version)
