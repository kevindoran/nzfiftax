FROM python

ARG USER_ID=1001
ARG GROUP_ID=101
RUN addgroup --gid $GROUP_ID app
RUN adduser --disabled-password --gecos '' --uid $USER_ID --gid $GROUP_ID app
WORKDIR /home/app

#RUN apt-get update && apt-get install -y --no-install-recommends \
#	 libsm6 \
#	 rm -rf /var/lib/apt/lists/*

#RUN conda config --add channels conda-forge 

COPY --chown=$USER_ID ./ ./


ENV PATH /home/app/.local/bin:$PATH

# Switching to our new user. Do this at the end, as we need root permissions 
# in order to create folders and install things.
USER app

RUN pip install -r requirements.txt
# Install our own project as a module.
# This is done so the tests can import it.
RUN pip install .

