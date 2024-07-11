# Use the official Node.js v14 image as the base image
FROM node:19

# Set the working directory to /app
WORKDIR /app

# Copy the package.json and package-lock.json files to the container
COPY package*.json ./

# Install the dependencies
RUN npm install

# Copy the rest of the application files to the container
COPY ./src ./src
COPY ./public ./public
COPY ./.env ./.env
# Build the React app
RUN npm run build

# Serve the React app with nginx
FROM nginx:1.21.3-alpine
COPY --from=0 /app/build /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
