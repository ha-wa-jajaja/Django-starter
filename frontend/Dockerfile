FROM node:20-alpine

WORKDIR /frontend

# Copy package files and install dependencies
COPY package.json package-lock.json* ./
RUN npm install

# Copy the rest of the application code
COPY . .

# Next.js uses port 3000 by default
EXPOSE 3000

# Use npx to ensure we find the next command in node_modules
CMD ["npm", "run", "dev", "--", "-H", "0.0.0.0"]
