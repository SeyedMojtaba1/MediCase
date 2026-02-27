FROM docker.arvancloud.ir/node:20-alpine AS build

WORKDIR /app

COPY package*.json ./
RUN npm config set registry https://npm.jamko.ir/
RUN npm install

COPY . .
RUN npm_config_registry=https://npm.jamko.ir/ npm run build --configuration production

FROM docker.arvancloud.ir/nginx:stable-perl

COPY --from=build /app/dist/medi-case-front/browser /usr/share/nginx/html

EXPOSE 80