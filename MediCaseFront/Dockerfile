FROM docker.arvancloud.ir/node:20-alpine AS build

WORKDIR /app

RUN sed -i 's/deb.debian.org/mirror.arvancloud.ir/g' /etc/apt/sources.list.d/debian.sources || \
    sed -i 's/deb.debian.org/mirror.arvancloud.ir/g' /etc/apt/sources.list

COPY package*.json ./
RUN npm config set registry https://registry.npmjs.org/
RUN npm install

COPY . .
RUN npx ng build --configuration=production

FROM docker.arvancloud.ir/nginx:stable-perl

COPY --from=build /app/dist/MediCaseFront/browser /usr/share/nginx/html
EXPOSE 80