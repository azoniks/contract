#!/usr/bin/env bash

set -Eeuo pipefail

BRANCH="${DEPLOY_BRANCH:-${1:-dev}}"
REMOTE="${DEPLOY_REMOTE:-origin}"
PROJECT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
BACKUP_DIR="${DEPLOY_BACKUP_DIR:-${PROJECT_DIR}/backups}"
LOCK_DIR="${TMPDIR:-/tmp}/contract-deploy.lock"
SERVICE="elena-bucatinschi-backend"

log() {
    printf '\n[%s] %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$*"
}

fail() {
    printf '\nDeploy error: %s\n' "$*" >&2
    exit 1
}

cleanup() {
    rmdir "${LOCK_DIR}" 2>/dev/null || true
}

trap cleanup EXIT

cd "${PROJECT_DIR}"

command -v git >/dev/null 2>&1 || fail "git is not installed"
command -v docker >/dev/null 2>&1 || fail "Docker is not installed"
[[ -f docker-compose.yaml ]] || fail "docker-compose.yaml was not found in ${PROJECT_DIR}"
[[ -f .env ]] || fail ".env was not found in ${PROJECT_DIR}"

if ! mkdir "${LOCK_DIR}" 2>/dev/null; then
    fail "another deploy is already running (${LOCK_DIR})"
fi

if docker compose version >/dev/null 2>&1; then
    COMPOSE=(docker compose)
elif command -v docker-compose >/dev/null 2>&1; then
    COMPOSE=(docker-compose)
else
    fail "Docker Compose is not installed"
fi

git remote get-url "${REMOTE}" >/dev/null 2>&1 || \
    fail "git remote '${REMOTE}' does not exist (set DEPLOY_REMOTE if needed)"

CURRENT_BRANCH="$(git branch --show-current)"
[[ "${CURRENT_BRANCH}" == "${BRANCH}" ]] || \
    fail "current branch is '${CURRENT_BRANCH:-detached HEAD}', expected '${BRANCH}'"

if ! git diff --quiet || ! git diff --cached --quiet; then
    fail "tracked files have local changes; commit or stash them before deploy"
fi

log "Fetching ${REMOTE}/${BRANCH}"
git fetch --prune "${REMOTE}" "${BRANCH}"
git show-ref --verify --quiet "refs/remotes/${REMOTE}/${BRANCH}" || \
    fail "remote branch ${REMOTE}/${BRANCH} was not found"
git merge-base --is-ancestor HEAD "${REMOTE}/${BRANCH}" || \
    fail "local branch has commits absent from ${REMOTE}/${BRANCH}; automatic deploy cancelled"

mkdir -p "${BACKUP_DIR}"
if [[ -f database/db.sqlite3 ]]; then
    BACKUP_FILE="${BACKUP_DIR}/db-$(date '+%Y%m%d-%H%M%S').sqlite3"
    cp -p database/db.sqlite3 "${BACKUP_FILE}"
    log "Database backup created: ${BACKUP_FILE}"
else
    log "Database does not exist yet; backup skipped"
fi

log "Updating project files"
git merge --ff-only "${REMOTE}/${BRANCH}"

log "Building and restarting containers"
"${COMPOSE[@]}" up -d --build --remove-orphans

log "Applying database migrations"
"${COMPOSE[@]}" exec -T "${SERVICE}" python manage.py migrate --no-input

log "Collecting static files"
"${COMPOSE[@]}" exec -T "${SERVICE}" python manage.py collectstatic --no-input

log "Checking Django configuration"
"${COMPOSE[@]}" exec -T "${SERVICE}" python manage.py check

log "Container status"
"${COMPOSE[@]}" ps

log "Deploy completed successfully at commit $(git rev-parse --short HEAD)"
