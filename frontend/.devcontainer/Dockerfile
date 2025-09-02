FROM node:20-alpine

WORKDIR /app

# Install dependencies
COPY package.json package-lock.json* ./
RUN npm ci

# Copy source
COPY . .

EXPOSE 5173

# Vite dev server
CMD ["npm", "run", "dev", "--", "--host"]
