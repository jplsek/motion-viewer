FROM node

WORKDIR /app

# Copy package json first to cache yarn install for future builds
COPY package.json yarn.lock ./

RUN yarn install

# Now copy everything else
COPY . .

RUN yarn build

ENV HOST=0.0.0.0
ENV ROOT=/motion

CMD ["yarn", "start"]