# NEON AI (TM) SOFTWARE, Software Development Kit & Application Framework
# All trademark and other rights reserved by their respective owners
# Copyright 2008-2022 Neongecko.com Inc.
# Contributors: Daniel McKnight, Guy Daniels, Elon Gasper, Richard Leeds,
# Regina Bloomstine, Casimiro Ferreira, Andrii Pernatii, Kirill Hrymailo
# BSD-3 License
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from this
#    software without specific prior written permission.
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
# CONTRIBUTORS  BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA,
# OR PROFITS;  OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE,  EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import click

from click_default_group import DefaultGroup
from neon_utils.packaging_utils import get_package_version_spec
from neon_utils.configuration_utils import init_config_dir
from ovos_config.config import Configuration


@click.group("neon-audio", cls=DefaultGroup,
             no_args_is_help=True, invoke_without_command=True,
             help="Neon Audio Commands\n\n"
                  "See also: neon COMMAND --help")
@click.option("--version", "-v", is_flag=True, required=False,
              help="Print the current version")
def neon_audio_cli(version: bool = False):
    if version:
        click.echo(f"neon_audio version "
                   f"{get_package_version_spec('neon_audio')}")


@neon_audio_cli.command(help="Start Neon Audio module")
@click.option("--module", "-m", default=None,
              help="TTS Plugin to configure")
@click.option("--package", "-p", default=None,
              help="TTS package spec to install")
@click.option("--force-install", "-f", default=False, is_flag=True,
              help="Force pip installation of configured module")
def run(module, package, force_install):
    init_config_dir()
    from neon_audio.__main__ import main
    if force_install or module or package:
        install_plugin(module, package, force_install)
    if module:
        audio_config = Configuration()
        if module != audio_config["tts"]["module"]:
            from neon_audio.utils import patch_config
            click.echo("Updating config with module and package")
            package = package or audio_config["tts"].get("package_spec")
            patch_config({"tts": {"module": module,
                                  "package_spec": package}})
    click.echo("Starting Audio Client")
    main()
    click.echo("Audio Client Shutdown")


@neon_audio_cli.command(help="Install a TTS Plugin")
@click.option("--module", "-m", default=None,
              help="TTS Plugin to configure")
@click.option("--package", "-p", default=None,
              help="TTS package spec to install")
@click.option("--force-install", "-f", default=False, is_flag=True,
              help="Force pip installation of configured module")
def install_plugin(module, package, force_install):
    from neon_audio.utils import install_tts_plugin
    audio_config = Configuration()

    if force_install and not (package or module):
        click.echo("Installing TTS plugin from configuration")
        module = module or audio_config["tts"]["module"]
        package = package or audio_config["tts"].get("package_spec")

    if module:
        install_tts_plugin(package or module)
        if not module:
            click.echo("Plugin specified without module")


@neon_audio_cli.command(help="Install a TTS Plugin")
@click.option("--plugin", "-p", default=None,
              help="TTS module to init")
def init_plugin(plugin):
    from neon_audio.utils import init_tts_plugin
    plugin = plugin or Configuration()["tts"]["module"]
    init_tts_plugin(plugin)
