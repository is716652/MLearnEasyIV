### ### 基于Ubuntu22.04 的镜像

> 基于Dockerfile构建机制
>
> 1. 各种网络工具的安装
> 2. SSH 支持root登录
> 3. Python3.12环境
> 4. 支持 jupyter

```dockerfile
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
    pytest

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
```

### start_services.sh 启动脚本

```bash
#!/bin/bash

# 启动SSH服务
/usr/sbin/sshd -D &

# 启动Jupyter Notebook
jupyter notebook \
  --notebook-dir=${JUPYTER_DIR} \
  --ip=0.0.0.0 \
  --port=${JUPYTER_PORT} \
  --no-browser \
  --allow-root \
  --NotebookApp.token='' \
  --NotebookApp.password=''

# 保持容器运行
wait
```

### 构建和运行命令

1. **构建镜像**：
```bash
docker build -t ubuntu-base-tools-22.04  .
```

2. **运行容器**：
```bash
docker run -d \
  -p 9000:9000 \
  -v $(pwd)/jupyter_files:/root/jupyter_files \
  --name ubuntu-tools-22.04-python3.12 \
  ubuntu-base-tools-22.04:v1
```

### 功能说明

1. **SSH访问**：
   - 端口：2222 (映射到容器22端口)
   - 用户名：root
   - 密码：password
   - 连接命令：`ssh root@localhost -p 2222`

2. **Jupyter Notebook**：
   - 访问地址：`http://localhost:9000`
   - 工作目录：`/root/jupyter_files` (挂载到宿主机的./jupyter_files)
   - 无需密码直接访问

3. **文件持久化**：
   - Jupyter文件会保存在宿主机的`./jupyter_files`目录
   - 即使容器删除，文件也不会丢失

4. **同时运行**：
   - SSH和Jupyter服务会同时启动
   - 都可以从宿主机访问





---



### 1. 基于ubuntu-base-tools-22.04  构建新的镜像

> #### 1. 继承原有的镜像功能
>
> #### 2. 新增F1-App 代码自动执行网页版
>
> #### 3. 开放9200端口
>
> - #### http://0.0.0.0:9200   访问
>
> #### 4. 开放2222端口模拟22端口
>
> 

---

```bash
docker run -d \
  -p 9000:9000 \    # Jupyter Notebook 端口
  -p 9200:9200 \    # 新增的 9200 端口映射
  -p 2222:22 \      # SSH 端口映射（容器内 22 → 主机 2222）
  -v $(pwd)/jupyter_files:/root/jupyter_files \
  --name ubuntu-tools-22.04-python3.12-jupyter-f1app \
  ubuntu-base-jupyter-f1app:v2
  
docker run -d  -p 9000:9000 -p 9200:9200 -p 2222:22 -v $(pwd)/jupyter_files:/root/jupyter_files --name ubuntu-tools-22.04-python3.12-jupyter-f1app ubuntu-base-jupyter-f1app:v2
```





