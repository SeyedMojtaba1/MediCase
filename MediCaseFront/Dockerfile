FROM docker.arvancloud.ir/node:20-alpine AS build

WORKDIR /app

# Use Iranian npm mirror for faster access
# RUN npm config set registry https://registry.npmmirror.com
# Alternative Iranian mirrors if the above doesn't work:
# RUN npm config set registry https://mirror.iranserver.com/npm/
# RUN npm config set registry https://npm.irannode.com/
# RUN npm config set registry https://mirror-npm.runflare.com
RUN npm config set registry https://mirror-npm.runflare.com
RUN npm config set strict-ssl false
# Copy package files first (better caching)
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy source code
COPY . .

# Build the application
RUN npx ng build --configuration=production

# Production stage
FROM docker.arvancloud.ir/nginx:stable-perl

# Copy built files from build stage
COPY --from=build /app/dist/MediCaseFront/browser /usr/share/nginx/html

# Copy nginx configuration if needed
# COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]