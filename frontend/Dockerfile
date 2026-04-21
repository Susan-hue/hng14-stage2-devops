FROM node:18-alpine AS builder
WORKDIR /app

COPY package*.json ./

# Install only production dependencies
RUN npm ci --only=production

# ── Final stage ──────────────────────────────────────────
FROM node:18-alpine
WORKDIR /app

# Copy only production node_modules from builder
COPY --from=builder /app/node_modules ./node_modules

# Copy app source (app.js, views, public, etc.)
COPY . .

# Create non-root user (Alpine syntax)
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:3000/health || exit 1

CMD ["node", "app.js"]