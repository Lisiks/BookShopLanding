FROM node:20-alpine

WORKDIR /frontend_app

COPY package.json package-lock.json .

RUN npm install

COPY . .


CMD ["npm", "run", "dev"]