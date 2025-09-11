FROM node:18-slim

WORKDIR /app

COPY package*.json ./
RUN npm install

# 🟢 Copy env and source code
COPY .env.k8s .env.local
COPY . .

# 🔨 Build your Next.js app
RUN npm run build

EXPOSE 3000

# 🚀 Start the production server
CMD ["npm", "start"]
