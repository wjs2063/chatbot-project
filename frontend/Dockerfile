

FROM node:18.18.2-alpine as build-stage

WORKDIR /app

# Copy the working directory

COPY package*.json ./

#install the project

RUN npm install

# Copy Rest of the project files

Copy . .

# Build vue.js application to the production-mode (배포용)

RUN npm run build


