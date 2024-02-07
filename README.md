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

RUN \
    pipx uninstall pydocstyle \
    && pipx uninstall pycodestyle \
    && pipx uninstall mypy \
    && pipx uninstall pylint

RUN \
    curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add - \
    && apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
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

RUN git clone --depth 1 https://github.com/home-assistant/hass-release \
    && pip3 install -e hass-release/

WORKDIR /workspaces

COPY requirements.txt ./
COPY homeassistant/package_constraints.txt homeassistant/package_constraints.txt
RUN pip3 install -r requirements.txt
COPY requirements_test.txt requirements_test_pre_commit.txt ./
RUN pip3 install -r requirements_test.txt
RUN rm -rf requirements.txt requirements_test.txt requirements_test_pre_commit.txt homeassistant/

ENV SHELL /bin/bash' > .devcontainer/Dockerfile
```

```bash
echo '{
  "name": "Home Assistant Dev",
  "context": "..",
  "dockerFile": "Dockerfile",
  // "postCreateCommand": "container setup && npm add",
  "containerEnv": { "DEVCONTAINER": "1" },
  "appPort": ["8123:8123", "5683:5683/udp"],
  "containerUser": "vscode",
  "remoteUser": "vscode",
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
        "GitHub.vscode-pull-request-github",
        "ms-azuretools.vscode-docker"
      ],
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
echo 'homeassistant==2024.1.6
pre-commit==3.3.3
reorder-python-imports==3.10.0
flake8==6.1.0
autoflake==2.2.1' > requirements.txt
```

```bash
echo 'pytest
-r requirements.txt
pytest-homeassistant-custom-component
pytest-asyncio' > requirements_test.txt
```
