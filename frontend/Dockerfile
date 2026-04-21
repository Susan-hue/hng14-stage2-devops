FROM node:22-alpine AS builder
WORKDIR /app

COPY package*.json ./

RUN npm ci --only=production

FROM node:22-alpine
WORKDIR /app

RUN apk upgrade --no-cache

COPY --from=builder /app/node_modules ./node_modules

COPY . .

RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:3000/health || exit 1

CMD ["node", "app.js"]