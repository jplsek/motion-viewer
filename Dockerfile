FROM node

COPY . /app

WORKDIR /app

RUN yarn install

RUN yarn build

ENV HOST=0.0.0.0
ENV ROOT=/motion

CMD ["yarn", "start"]