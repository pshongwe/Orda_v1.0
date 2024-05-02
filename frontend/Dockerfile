# Use an official Node runtime as a parent image
FROM node:18

# Install Bun
RUN curl https://bun.sh/install | bash

# Add bun to PATH
ENV PATH="/root/.bun/bin:${PATH}"

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install any needed packages specified in package.json using Bun
RUN bun install

# Make port 8081 available to the world outside this container
EXPOSE 8082

# Run bun run serve when the container launches
CMD ["bun", "run", "serve"]
