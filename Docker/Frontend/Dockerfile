# Stage 1: Build Angular
FROM node:18 AS build
WORKDIR /app

# Copy Angular project files
COPY ../../Frontend_Enterprise/delivery-frontend/package*.json ./
RUN npm install
COPY ../../Frontend_Enterprise/delivery-frontend/ ./
RUN npm run build --prod

# Stage 2: Nginx
FROM nginx:alpine

# Copy custom Nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy compiled Angular build
COPY --from=build /app/dist/delivery-frontend /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
