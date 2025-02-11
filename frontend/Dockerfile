# Use Nginx as the base image
FROM nginx:alpine

# Set the working directory inside the container
# WORKDIR /usr/share/nginx/html
WORKDIR /var/www/html

# Remove the default Nginx static files
RUN rm -rf ./*

# Copy your frontend files into the container
COPY . .

# Expose port 80 to serve the frontend
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
