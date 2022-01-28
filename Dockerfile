FROM condaforge/miniforge3:4.10.3-10

WORKDIR /app
RUN apt-get --allow-releaseinfo-change update && apt-get -y install gcc

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get install -y python3-opencv

RUN conda create -n Boardgame python=3.8
#RUN /opt/conda/envs/Boardgame/bin/pip install torch==1.8.1 torchvision==0.9.1 torchaudio==0.8.1
#RUN /opt/conda/envs/Boardgame/bin/pip install torch==1.8.0 torchvision==0.9.1 torchaudio==0.10.0

COPY env.yml .
RUN conda env update --name Boardgame --file env.yml

COPY . .
CMD conda run -n Boardgame /bin/bash -c "python BoardGameAssistant.py &"
