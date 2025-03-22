# docker buildx build --platform linux/amd64 --tag tab-name:x.x .

FROM ubuntu:22.04

WORKDIR /src
COPY src/ /src

# 必要なパッケージをインストール
RUN apt-get update && apt-get install -y \
    python3.11 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Pythonのバージョンを更新
RUN python3.11 -m pip install --upgrade pip

# 必要なパッケージをインストール
RUN python3.11 -m pip install --no-cache-dir -r requirements.txt

# ポートの公開
EXPOSE 5000

# コンテナ起動時にapp.pyを実行
CMD ["python3.11", "app.py"]