FROM node:24-alpine

WORKDIR /workspace

COPY package.json package-lock.json ./
COPY apps/api/package.json apps/api/package.json
COPY apps/web/package.json apps/web/package.json
RUN npm ci --workspace @weekly-report/web --include-workspace-root=false

COPY apps/web apps/web

ENV API_PROXY_TARGET=http://api:3001
EXPOSE 5173

CMD ["npm", "run", "dev", "--workspace", "@weekly-report/web", "--", "--host", "0.0.0.0"]
