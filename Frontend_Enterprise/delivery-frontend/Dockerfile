# Stage 1: Build Angular
FROM node:18 AS build
WORKDIR /app

# Copy package.json & package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

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

# Expose port
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
