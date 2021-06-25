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

#ENV PATH /home/app/.local/bin:$PATH

COPY --chown=$USER_ID requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY --chown=$USER_ID ./ ./

RUN pip install .

# Switching to our new user. Do this at the end, as we need root permissions 
# in order to create folders and install things.
USER app

# Install our own project as a module.
# This is done so the tests can import it.


