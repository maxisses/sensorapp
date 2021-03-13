FROM registry.access.redhat.com/ubi7/nodejs-12

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

WORKDIR /opt/app-root/src

COPY package.json /opt/app-root/src
RUN npm install --only=prod
COPY server /opt/app-root/src/server
COPY views /opt/app-root/src/views
COPY public /opt/app-root/src/public

ENV NODE_ENV production
ENV PORT 3000

EXPOSE 3000

CMD ["npm", "start"]
