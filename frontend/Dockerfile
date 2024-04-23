# Use an official Node runtime as a parent image
FROM node:18

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install any needed packages specified in package.json
RUN npm install

# Make port 8081 available to the world outside this container
EXPOSE 8081

# Run npm run serve when the container launches
CMD ["npm", "run", "serve"]
