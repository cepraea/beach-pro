FROM node:22-bookworm-slim

USER root

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       bash \
       bubblewrap \
       ca-certificates \
       curl \
       git \
       jq \
       less \
       passwd \
       procps \
       socat \
       python3 \
       python3-venv \
    && rm -rf /var/lib/apt/lists/*

# CLIs determinísticas para lint/format/type-check.
RUN npm install -g \
    prettier \
    markdownlint-cli2 \
    pyright

# Ferramentas Python isoladas da instalação do sistema.
RUN python3 -m venv /opt/cepraea-tools \
    && /opt/cepraea-tools/bin/pip install --no-cache-dir \
       mypy \
       pydantic

# A imagem Node já possui UID/GID 1000. Renomeie sem conceder sudo.
RUN groupmod -n agent node \
    && usermod -l agent -d /home/agent -m node \
    && install -d -o agent -g agent \
       /home/agent/.local \
       /home/agent/.local/state \
       /home/agent/.cache \
       /home/agent/.claude \
       /home/agent/.codex \
       /home/agent/.local/bin \
       /home/agent/.config/git \
       /home/agent/.config/gh-empty \
       /home/agent/.local/state/cepraea-guards \
       /workspaces/cepraea-beach-pro

RUN install -d -o root -g root \
    /etc/claude-code \
    /etc/codex \
    /usr/local/lib/cepraea-guards

COPY .devcontainer/control-plane/claude-managed-settings.json \
     /etc/claude-code/managed-settings.json

COPY .devcontainer/control-plane/claude-managed-mcp.json \
     /etc/claude-code/managed-mcp.json

COPY .devcontainer/control-plane/codex-requirements.toml \
     /etc/codex/requirements.toml

COPY .devcontainer/guards/ \
     /usr/local/lib/cepraea-guards/

RUN chown -R root:root \
      /etc/claude-code \
      /etc/codex \
      /usr/local/lib/cepraea-guards \
    && chmod 0644 \
      /etc/claude-code/managed-settings.json \
      /etc/claude-code/managed-mcp.json \
      /etc/codex/requirements.toml \
    && chmod 0755 /usr/local/lib/cepraea-guards/*

USER agent

ENV HOME=/home/agent
ENV PATH=/opt/cepraea-tools/bin:/home/agent/.local/bin:$PATH

RUN curl -fsSL https://chatgpt.com/codex/install.sh | sh \
    && curl -fsSL https://claude.ai/install.sh | bash \
    && codex --version \
    && claude --version

WORKDIR /workspaces/cepraea-beach-pro