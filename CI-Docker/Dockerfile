# This dockerfile is meant to be personalized, and serves as a template and demonstration.
# Modify it directly, but it is recommended to copy this dockerfile into a new build context (directory),
# modify to taste and modify docker-compose.yml.template to build and run it.

# It is recommended to control docker containers through 'docker-compose' https://docs.docker.com/compose/
# Docker compose depends on a .yml file to control container sets
# rocm-setup.sh can generate a useful docker-compose .yml file
# `docker-compose run --rm <rocm-terminal>`

# If it is desired to run the container manually through the docker command-line, the following is an example
# 'docker run -it --rm -v [host/directory]:[container/directory]:ro <user-name>/<project-name>'.

#FROM ubuntu:18.04
#FROM compute-artifactory.amd.com:5000/rocm-plus-docker/compute-rocm-dkms-no-npi-hipclang:2768-STG1
#FROM compute-artifactory.amd.com:5000/rocm-plus-docker/compute-rocm-dkms-amd-feature-targetid:93-STG1
#FROM compute-artifactory.amd.com:5000/rocm-plus-docker/compute-rocm-dkms-no-npi-hipclang:6311-STG1
# FROM compute-artifactory.amd.com:5000/rocm-plus-docker/compute-rocm-dkms-no-npi-hipclang:6416-STG1
# FROM compute-artifactory.amd.com:5000/rocm-plus-docker/compute-rocm-dkms-no-npi-hipclang:6132-STG1
# FROM compute-artifactory.amd.com:5000/rocm-plus-docker/compute-rocm-dkms-no-npi-hipclang:6665-STG1
FROM compute-artifactory.amd.com:5000/rocm-plus-docker/compute-rocm-rel-4.1:21-STG1

USER root
# Initialize the image
# Modify to pre-install dev tools
RUN apt-get update && \
  DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
  wget \
  sudo \
  gnupg2 \
  libelf1 \
  libnuma-dev \
  build-essential \
  git \
  vim-nox \
  cmake-curses-gui \
  bash-completion \
  exuberant-ctags \
  openssh-server \
  make \
  pkg-config \
  less \
  file \
  screen

# Install ROCm packages from offical repo
#RUN wget -q -O - http://repo.radeon.com/rocm/apt/debian/rocm.gpg.key | sudo apt-key add - && \
#  echo 'deb [arch=amd64] http://repo.radeon.com/rocm/apt/debian/ xenial main' | sudo tee /etc/apt/sources.list.d/rocm.list && \
#  apt-get update && apt-get install -y rocm-dkms && \
#  echo 'export PATH=/opt/rocm/bin:$PATH' >> /root/.bashrc

# run required packages of rocBLAS/Tensile
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
  python3 \
  python3-yaml \
  python3-pip \
  libxml2 \
  libblas-dev \
  liblapack-dev \
  llvm-6.0-dev \
  libomp-dev \
  zlib1g-dev \
  gfortran \
  libboost-program-options-dev \
  libboost-filesystem-dev \
  libmsgpack-dev && apt autoremove

RUN pip3 install --upgrade pip && \
    pip3 install setuptools --upgrade && \
    pip3 install wheel tox pyyaml pytest pylint pyflakes msgpack

# Grant members of 'sudo' group passwordless privileges
# Comment out to require sudo
# COPY sudo-nopasswd /etc/sudoers.d/sudo-nopasswd

# This is meant to be used as an interactive developer container
# Create user rocm-user as member of sudo group
# Append /opt/rocm/bin to the system PATH variable
RUN echo 'root:root' | chpasswd
ENV HOME=/root

# Configure SSH
RUN sed -i 's/\#PasswordAuthentication/PasswordAuthentication/' /etc/ssh/sshd_config
RUN sed -i 's/PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config

RUN git config --global user.email "Yu-cheng.Hsieh@amd.com"
RUN git config --global user.name "yu-hsieh"


# # Increase VSCode file watch count
# #RUN echo 'fs.inotify.max_user_watches=524288' >> /etc/sysctl.conf
# 
# # # The following are optional enhancements for the command-line experience
# # # Uncomment the following to install a pre-configured vim environment based on http://vim.spf13.com/
# # # 1.  Sets up an enhanced command line dev environment within VIM
# # # 2.  Aliases GDB to enable TUI mode by default
# # RUN curl -sL https://j.mp/spf13-vim3 | bash
# # #    echo "alias gdb='gdb --tui'\n" >> ~/.bashrc
# # # COPY colored-prompt.sh /etc/profile.d
# # # COPY .screenrc /root
# # RUN echo 'source /etc/profile' >> /root/.bashrc && \
# #     echo 'filetype plugin indent on' >> /root/.vimrc.local && \
# #     echo 'set tabstop=4' >> /root/.vimrc.local && \
# #     echo 'set shiftwidth=4' >> /root/.vimrc.local && \
# #     echo 'set expandtab' >> /root/.vimrc.local && \
# #     echo 'set mouse=""' >> /root/.vimrc.local && \
# #     echo 'set nospell' >> /root/.vimrc.local && \
# #     echo 'set paste' >> /root/.vimrc.local && \
# #     echo "UnBundle 'scrooloose/syntastic'" >> /root/.vimrc.bundles.local && \
# #     echo 'let g:airline_powerline_fonts = 1' >> /root/.vimrc.before.local && \
# #     echo 'set history save on' >> /root/.gdbinit && \
# #     echo 'layout asm' >> /root/.gdbinit && \
# #     echo 'layout reg' >> /root/.gdbinit
# 
# RUN git config --global alias.lg "log --color --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) ' --abbrev-commit" && \
#     git config --global user.email "Yu-cheng.Hsieh@amd.com" && \
#     git config --global user.name "yu-hsieh"
# 

# Locale and time
RUN apt-get update && apt-get install -y locales && rm -rf /var/lib/apt/lists/* \
    && localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8
ENV LANG en_US.utf8
ENV TZ=Asia/Taipei
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Default to a login shell
CMD service ssh start && bash -l

