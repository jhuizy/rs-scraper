FROM node

RUN npm install -g yarn

WORKDIR /app

COPY package.json .
COPY yarn.lock .
RUN yarn

CMD ["yarn", "start"]
