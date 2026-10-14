FROM node:24-alpine

WORKDIR /workspace

COPY package.json package-lock.json ./
COPY apps/api/package.json apps/api/package.json
COPY apps/web/package.json apps/web/package.json
RUN npm ci --workspace @weekly-report/api --include-workspace-root=false

COPY apps/api/src apps/api/src

ENV HOST=0.0.0.0
ENV PORT=3001
EXPOSE 3001

CMD ["npm", "run", "start", "--workspace", "@weekly-report/api"]
