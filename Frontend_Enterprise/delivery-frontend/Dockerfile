# Stage 1: Build Angular
FROM node:18 AS build
WORKDIR /app

# Copy package.json & package-lock.json first
COPY package*.json ./

# Install dependencies (ignore peer issues)
RUN npm cache clean --force && npm install --legacy-peer-deps

# Copy Angular source
COPY . ./

# Build Angular for production
RUN npm run build --prod

# Stage 2: Serve with Nginx
FROM nginx:alpine

# Copy custom nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy compiled Angular build from stage 1
COPY --from=build /app/dist/delivery-frontend /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
