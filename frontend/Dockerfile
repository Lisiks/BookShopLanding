FROM node:22-alpine AS builder

WORKDIR /frontend_app

COPY package.json package-lock.json .

RUN npm install

COPY . .


CMD ["npm", "run", "dev"]