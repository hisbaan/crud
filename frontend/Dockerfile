# syntax=docker/dockerfile:1
FROM node:17.3.0-alpine
WORKDIR /frontend
ENV PATH /frontend/node_modules/.bin:$PATH
COPY package.json .
COPY package-lock.json .
RUN npm install --silent
RUN npm install react-scripts -g --silent
EXPOSE 3000
COPY . .
CMD ["npm", "start"]
