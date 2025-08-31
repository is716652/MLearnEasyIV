# 使用Ubuntu 22.04作为基础镜像
FROM ubuntu:22.04

# 设置环境变量
ENV DEBIAN_FRONTEND=noninteractive \
    PIP_INDEX_URL=https://mirrors.aliyun.com/pypi/simple \
    JUPYTER_PORT=9000 \
    JUPYTER_DIR=/root/jupyter_files

# 更新系统并安装基础工具
RUN apt-get update && apt-get install -y \
    sudo \
    curl \
    wget \
    git \
    net-tools \
    iputils-ping \
    dnsutils \
    htop \
    vim \
    openssh-server \
    software-properties-common \
    build-essential \
    zlib1g-dev \
    libncurses5-dev \
    libgdbm-dev \
    libnss3-dev \
    libssl-dev \
    libreadline-dev \
    libffi-dev \
    libsqlite3-dev \
    libbz2-dev \
    iptables \
    iproute2 \
    lsof \
    strace \
    tcpdump \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# 设置SSH（允许root登录）
RUN mkdir /var/run/sshd && \
    echo 'root:password' | chpasswd && \
    sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config && \
    sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config && \
    sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd

ENV NOTVISIBLE="in users profile"
RUN echo "export VISIBLE=now" >> /etc/profile

# 复制本地Python源码到容器
COPY Python-3.12.4.tar.xz /tmp/

# 安装Python 3.12
RUN cd /tmp && \
    tar -xvf Python-3.12.4.tar.xz && \
    cd Python-3.12.4 && \
    ./configure --enable-optimizations && \
    make -j$(nproc) && \
    make install && \
    cd / && \
    rm -rf /tmp/Python-3.12.4* && \
    python3 --version

# 配置pip阿里云镜像源并更新pip
RUN python3 -m ensurepip --upgrade && \
    python3 -m pip install --upgrade pip && \
    pip config set global.index-url https://mirrors.aliyun.com/pypi/simple && \
    pip config set install.trusted-host mirrors.aliyun.com

# 安装Jupyter和其他Python工具
RUN pip install --no-cache-dir \
    numpy \
    pandas \
    matplotlib \
    seaborn \
    scipy \
    scikit-learn \
    jupyter \
    ipython \
    virtualenv \
    requests \
    flask \
    django \
    pytest \
    aiohttp \
    asyncio \
    selenium \
    scrapy


# 创建符号链接
RUN ln -sf /usr/local/bin/python3 /usr/local/bin/python && \
    ln -sf /usr/local/bin/pip3 /usr/local/bin/pip

# 创建Jupyter工作目录
RUN mkdir -p ${JUPYTER_DIR} && \
    chmod -R 777 ${JUPYTER_DIR}

# 设置工作目录
WORKDIR /workspace

# 暴露端口
EXPOSE 22 ${JUPYTER_PORT}

# 启动脚本
COPY start_services.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/start_services.sh
CMD ["start_services.sh"]
