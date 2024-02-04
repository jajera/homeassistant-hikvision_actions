# homeassistant-hikvision_actions

## Project structure
```bash
pip install cookiecutter
mkdir custom_components
cd custom_components
cookiecutter https://github.com/boralyl/cookiecutter-homeassistant-component
cd ..
```

```bash
You've downloaded /home/johna/.cookiecutters/cookiecutter-homeassistant-component before. Is it okay to delete and re-download it? 
[y/n] (y): y
  [1/7] domain (my_component): homeassistant-hikvision_actions                                             
  [2/7] name (My Component): homeassistant-hikvision_actions
  [3/7] docs_url (https://github.com/user/my_component/): https://github.com/jajera/homeassistant-hikvision_actions
  [4/7] owner (@user): @jajera
  [5/7] Select config_flow
    1 - yes
    2 - no
    Choose from [1/2] (1): 1
  [6/7] Select iot_class
    1 - assumed_state
    2 - calculated
    3 - cloud_polling
    4 - cloud_push
    5 - local_polling
    6 - local_push
    Choose from [1/2/3/4/5/6] (1): 5
  [7/7] version (1.0.0):
```

```bash
mkdir .devcontainer
touch .devcontainer/Dockerfile
```

```bash
echo 'FROM mcr.microsoft.com/vscode/devcontainers/python:0-3.11

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Uninstall pre-installed formatting and linting tools
# They would conflict with our pinned versions
RUN \
    pipx uninstall pydocstyle \
    && pipx uninstall pycodestyle \
    && pipx uninstall mypy \
    && pipx uninstall pylint

RUN \
    curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add - \
    && apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        # Additional library needed by some tests and accordingly by VScode Tests Discovery
        bluez \
        ffmpeg \
        libudev-dev \
        libavformat-dev \
        libavcodec-dev \
        libavdevice-dev \
        libavutil-dev \
        libswscale-dev \
        libswresample-dev \
        libavfilter-dev \
        libpcap-dev \
        libturbojpeg0 \
        libyaml-dev \
        libxml2 \
        git \
        cmake \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src

# Setup hass-release
RUN git clone --depth 1 https://github.com/home-assistant/hass-release \
    && pip3 install -e hass-release/

WORKDIR /workspaces

# Install Python dependencies from requirements
COPY requirements.txt ./
COPY homeassistant/package_constraints.txt homeassistant/package_constraints.txt
RUN pip3 install -r requirements.txt
COPY requirements_test.txt requirements_test_pre_commit.txt ./
RUN pip3 install -r requirements_test.txt
RUN rm -rf requirements.txt requirements_test.txt requirements_test_pre_commit.txt homeassistant/

# Set the default shell to bash instead of sh
ENV SHELL /bin/bash' > .devcontainer/Dockerfile
```


```bash
echo '{
  "name": "Home Assistant Dev",
  "context": "..",
  "dockerFile": "Dockerfile",
  "postCreateCommand": "script/setup",
  "postStartCommand": "script/bootstrap",
  "containerEnv": { "DEVCONTAINER": "1" },
  // Port 5683 udp is used by Shelly integration
  "appPort": ["8123:8123", "5683:5683/udp"],
  "runArgs": ["-e", "GIT_EDITOR=code --wait"],
  "customizations": {
    "vscode": {
      "extensions": [
        "charliermarsh.ruff",
        "ms-python.pylint",
        "ms-python.vscode-pylance",
        "visualstudioexptteam.vscodeintellicode",
        "redhat.vscode-yaml",
        "esbenp.prettier-vscode",
        "GitHub.vscode-pull-request-github"
      ],
      // Please keep this file in sync with settings in home-assistant/.vscode/settings.default.json
      "settings": {
        "python.pythonPath": "/usr/local/bin/python",
        "python.testing.pytestArgs": ["--no-cov"],
        "editor.formatOnPaste": false,
        "editor.formatOnSave": true,
        "editor.formatOnType": true,
        "files.trimTrailingWhitespace": true,
        "terminal.integrated.profiles.linux": {
          "zsh": {
            "path": "/usr/bin/zsh"
          }
        },
        "terminal.integrated.defaultProfile.linux": "zsh",
        "yaml.customTags": [
          "!input scalar",
          "!secret scalar",
          "!include_dir_named scalar",
          "!include_dir_list scalar",
          "!include_dir_merge_list scalar",
          "!include_dir_merge_named scalar"
        ],
        "[python]": {
          "editor.defaultFormatter": "charliermarsh.ruff"
        }
      }
    }
  }
}' > .devcontainer/devcontainer.json
```

```bash
echo 'default_config:

logger:
  default: info
  logs:
    custom_components.tapo: debug
# If you need to debug uncommment the line below (doc: https://www.home-assistant.io/integrations/debugpy/)
# debugpy:

debugpy:
  start: true
  wait: false

scene:
  - id: "1682456037783"
    name: 3 Office pinks
    entities:
      light.striscia_luminosa_smart:
        min_color_temp_kelvin: 2500
        max_color_temp_kelvin: 6500
        min_mireds: 153
        max_mireds: 400
        effect_list:
          - bubblingcauldron
          - aurora
          - candycane
          - christmas
          - flicker
          - christmaslight
          - hanukkah
          - hauntedmansion
          - icicle
          - lightning
          - ocean
          - rainbow
          - raindrop
          - spring
          - sunrise
          - sunset
          - valentines
        supported_color_modes:
          - brightness
          - color_temp
          - hs
          - onoff
        friendly_name: Office kallax
        supported_features: 4
        color_mode: hs
        brightness: 255
        hs_color:
          - 295
          - 99
        rgb_color:
          - 233
          - 2
          - 255
        xy_color:
          - 0.357
          - 0.142
        state: "on"
    metadata:
      light.striscia_luminosa_smart:
        entity_only: true
    icon: mdi:desktop-classic
  - id: "1682456224579"
    name: 2 Office White
    entities:
      light.striscia_luminosa_smart:
        min_color_temp_kelvin: 2500
        max_color_temp_kelvin: 6500
        min_mireds: 153
        max_mireds: 400
        effect_list:
          - bubblingcauldron
          - aurora
          - candycane
          - christmas
          - flicker
          - christmaslight
          - hanukkah
          - hauntedmansion
          - icicle
          - lightning
          - ocean
          - rainbow
          - raindrop
          - spring
          - sunrise
          - sunset
          - valentines
        supported_color_modes:
          - brightness
          - color_temp
          - hs
          - onoff
        color_mode: color_temp
        brightness: 255
        color_temp_kelvin: 6535
        color_temp: 153
        hs_color:
          - 54.768
          - 1.6
        rgb_color:
          - 255
          - 254
          - 250
        xy_color:
          - 0.326
          - 0.333
        friendly_name: Office kallax
        supported_features: 4
        state: "on"
    metadata:
      light.striscia_luminosa_smart:
        entity_only: true
    icon: mdi:desktop-classic
  - id: "1697651778268"
    name: 1 Office Streamin
    entities:
      light.striscia_luminosa_smart:
        min_color_temp_kelvin: 2500
        max_color_temp_kelvin: 6500
        min_mireds: 153
        max_mireds: 400
        effect_list:
          - bubblingcauldron
          - aurora
          - candycane
          - christmas
          - flicker
          - christmaslight
          - hanukkah
          - hauntedmansion
          - icicle
          - lightning
          - ocean
          - rainbow
          - raindrop
          - spring
          - sunrise
          - sunset
          - valentines
        supported_color_modes:
          - brightness
          - color_temp
          - hs
          - onoff
        friendly_name: Office kallax
        supported_features: 4
        color_mode: color_temp
        brightness: 255
        color_temp_kelvin: 2500
        color_temp: 400
        hs_color:
          - 28.874
          - 72.522
        rgb_color:
          - 255
          - 159
          - 70
        xy_color:
          - 0.546
          - 0.389
        effect: Rainbow
        state: "on"
    icon: mdi:desktop-classic
    metadata:
      light.striscia_luminosa_smart:
        entity_only: true
  - id: "1687783375727"
    name: Studio Light Warm 100%
    entities:
      light.striscia_luminosa_smart:
        effect_list:
          - bubblingcauldron
          - aurora
          - candycane
          - christmas
          - flicker
          - christmaslight
          - hanukkah
          - hauntedmansion
          - icicle
          - lightning
          - ocean
          - rainbow
          - raindrop
          - spring
          - sunrise
          - sunset
          - valentines
        supported_color_modes:
          - brightness
          - hs
          - onoff
        color_mode: hs
        brightness: 128
        hs_color:
          - 30
          - 94
        rgb_color:
          - 255
          - 135
          - 15
        xy_color:
          - 0.6
          - 0.381
        friendly_name: Studio Right Strip
        supported_features: 4
        state: "on"
        icon: mdi:globe-light
        metadata: {}' > .devcontainer/configuration.yaml
```

```bash
echo '# linters such as pylint should be pinned, as new releases
# make new things fail. Manually update these pins when pulling in a
# new version

# types-* that have versions roughly corresponding to the packages they
# contain hints for available should be kept in sync with them

-c homeassistant/package_constraints.txt
-r requirements_test_pre_commit.txt
astroid==3.0.1
coverage==7.4.1
freezegun==1.3.1
mock-open==1.4.0
mypy==1.8.0
pre-commit==3.6.0
pydantic==1.10.12
pylint==3.0.3
pylint-per-file-ignores==1.2.1
pipdeptree==2.13.2
pytest-asyncio==0.23.4
pytest-aiohttp==1.0.5
pytest-cov==4.1.0
pytest-freezer==0.4.8
pytest-socket==0.6.0
pytest-test-groups==1.0.3
pytest-sugar==0.9.7
pytest-timeout==2.1.0
pytest-unordered==0.5.2
pytest-picked==0.5.0
pytest-xdist==3.3.1
pytest==7.4.4
requests-mock==1.11.0
respx==0.20.2
syrupy==4.6.0
tqdm==4.66.1
types-aiofiles==23.2.0.20240106
types-atomicwrites==1.4.5.1
types-croniter==1.0.6
types-beautifulsoup4==4.12.0.20240106
types-caldav==1.3.0.20240106
types-chardet==0.1.5
types-decorator==5.1.8.20240106
types-paho-mqtt==1.6.0.20240106
types-pillow==10.2.0.20240111
types-protobuf==4.24.0.20240106
types-psutil==5.9.5.20240106
types-python-dateutil==2.8.19.20240106
types-python-slugify==8.0.0.3
types-pytz==2023.3.1.1
types-PyYAML==6.0.12.12
types-requests==2.31.0.3
types-xmltodict==0.13.0.3' > requirements_dev.txt
```

```bash
echo 'pytest
pytest-cov==2.9.0
pytest-homeassistant-custom-component' > requirements_test.txt
```

```bash
echo '# Automatically generated from .pre-commit-config.yaml by gen_requirements_all.py, do not edit

codespell==2.2.2
ruff==0.1.15
yamllint==1.32.0' > requirements_test_pre_commit.txt
```

