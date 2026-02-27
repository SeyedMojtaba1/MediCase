FROM docker.arvancloud.ir/node:20-alpine AS build

WORKDIR /app

COPY package*.json ./
RUN npm config set registry https://registry.npmjs.org/
RUN npm install

COPY . .
RUN npm_config_registry=https://mirror-npm.runflare.com/ npm run build --configuration production

FROM docker.arvancloud.ir/nginx:stable-perl

COPY --from=build /app/dist/medi-case-front/browser /usr/share/nginx/html

EXPOSE 80