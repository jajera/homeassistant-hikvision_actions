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
echo 'FROM mcr.microsoft.com/devcontainers/python:1-3.11-bullseye

RUN apt-get update
RUN apt-get install -y --no-install-recommends \
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
        && pip install --upgrade pip

WORKDIR /workspaces

# Install Python dependencies from requirements
COPY requirements_dev.txt ./
RUN pip3 install -r requirements_dev.txt
COPY requirements_test.txt ./
RUN pip3 install -r requirements_test.txt
RUN rm -rf requirements_dev.txt requirements_test.txt

# Set the default shell to bash instead of sh
ENV SHELL /bin/bash' > .devcontainer/Dockerfile
```

```bash
echo '{
  "name": "Home Assistant Dev",
  "context": "..",
  "dockerFile": "Dockerfile",
  "postCreateCommand": "pip install -r requirements_dev.txt",
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
echo 'homeassistant==2024.1.6
pre-commit==3.3.3
reorder-python-imports==3.10.0
flake8==6.1.0
autoflake==2.2.1' > requirements_dev.txt
```

```bash
echo 'pytest
-r requirements_dev.txt
pytest-homeassistant-custom-component
pytest-asyncio' > requirements_test.txt
```
