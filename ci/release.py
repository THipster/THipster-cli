import sys
import anyio
import base
import dagger


async def release(version):

    async with dagger.Connection(dagger.Config(log_output=sys.stderr)) as client:

        src = client.host().directory('.')

        setup = (
            base.pythonBase(client, version)
            .with_exec(['apk', 'add', 'git', 'libgcc'])
            .with_exec(['git', 'config', '--global', 'safe.directory', '*'])
            .with_exec(['pip', 'install', 'python-semantic-release'])
            .with_mounted_directory('/src', src)
            .with_workdir('/src')

        )

        release = setup.with_exec(['semantic-release', 'publish'])
        # execute
        await release.exit_code()

    print('Release succeeded!')

if __name__ == '__main__':
    python_version = '3.11'
    anyio.run(release, python_version)
