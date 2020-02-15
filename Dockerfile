FROM python:3.6-slim

RUN apt-get update && apt-get install -y curl

RUN curl -sL https://deb.nodesource.com/setup_13.x | bash - && apt-get install -y git nodejs cloc

WORKDIR /usr/jquery-data

COPY prep.py .

COPY jquery_releases.csv .

RUN python prep.py

RUN rm -rf jquery_releases.csv

WORKDIR /usr

COPY jsinspect jsinspect

RUN npm install -g ./jsinspect

# Increase the amount of memory nodejs can allocate, this
# prevents JsInspect from running into the GC issues. 
ENV NODE_OPTIONS=--max-old-space-size=4000

WORKDIR /usr/jquery-data

# Open a bash prompt, such that you can execute commands 
# such as `cloc`. 
ENTRYPOINT ["bash"]