import sys
import anyio
import base
import dagger


async def release(version):

    async with dagger.Connection(dagger.Config(log_output=sys.stderr)) as client:

        src = client.host().directory('.')

        setup = (
            base.pythonBase(client, version)
            .with_mounted_directory('/src', src)
            .with_workdir('/src')
            .with_exec(['pip', 'install', 'python-semantic-release'])

        )

        release = setup.with_exec(['semantic-release', 'print-version'])
        # execute
        await release.exit_code()

    print('Release succeeded!')

if __name__ == '__main__':
    python_version = '3.11'
    anyio.run(release, python_version)
