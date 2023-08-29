"""Release a python package on pypi and GitHub."""
import os
import re
import sys

import anyio
import base
import dagger


async def release(python_version):
    """Run python semantic-release."""
    async with dagger.Connection(dagger.Config(log_output=sys.stderr)) as client:
        src = client.host().directory('.')

        cr_pat = client.set_secret('password', os.environ['CR_PAT'])

        setup = await src.file('setup.py').contents()
        cli_version = re.findall(
            r"__version__ = '([0-9]+\.[0-9]+\.[0-9]+)'",
            setup,
        )[0]

        image = (
            base.thipster_base(client, python_version)
            .with_workdir('/tmp')
            .with_exec(['pip', 'install', f'thipstercli=={cli_version}'])
            .with_entrypoint(['thipster'])
            .with_label(
                'org.opencontainers.image.source',
                'https://github.com/THipster/THipster-cli',
            )
        )

        address = await (
            image.with_registry_auth('ghcr.io', 'rcattin', cr_pat)
            .publish(f'ghcr.io/thipster/cli:{cli_version}')
        )

    print(f'Image published at {address} ')

if __name__ == '__main__':
    python_version = '3.11'
    anyio.run(release, python_version)
