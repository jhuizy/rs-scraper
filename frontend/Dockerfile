FROM node

RUN npm install -g yarn

WORKDIR /app

COPY package.json .
COPY yarn.lock .
RUN yarn

COPY . .
EXPOSE 3000

CMD ["yarn", "start"]
