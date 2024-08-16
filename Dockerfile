FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Essential installs; one RUN command to keep layers to a minimum
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    wget bzip2 ca-certificates git stow zsh locales curl gpg && \
    wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh && \
    bash Miniconda3-latest-Linux-x86_64.sh -b -p /opt/conda && \
    rm Miniconda3-latest-Linux-x86_64.sh && \
    /opt/conda/bin/conda init && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --no-cache-dir pipx && \
    pipx ensurepath && \
    pipx install poetry==1.8.3 && \
    git clone https://github.com/mclevey/dotfiles.git /root/dotfiles && \
    cd /root/dotfiles && \
    stow zsh && \
    curl -sS https://starship.rs/install.sh | sh -s -- --yes && \
    echo 'eval "$(starship init zsh)"' >> ~/.zshrc && \
    chsh -s /bin/zsh && \
    echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && \
    locale-gen && \
    echo 'export LC_ALL=en_US.UTF-8' >> ~/.zshrc && \
    echo 'export LANG=en_US.UTF-8' >> ~/.zshrc && \
    echo 'export LANGUAGE=en_US.UTF-8' >> ~/.zshrc && \
    mkdir -p /etc/apt/keyrings && \
    wget -qO- https://raw.githubusercontent.com/eza-community/eza/main/deb.asc | gpg --dearmor -o /etc/apt/keyrings/gierens.gpg && \
    echo "deb [signed-by=/etc/apt/keyrings/gierens.gpg] http://deb.gierens.de stable main" | tee /etc/apt/sources.list.d/gierens.list && \
    chmod 644 /etc/apt/keyrings/gierens.gpg && \
    apt-get update && \
    apt-get install -y eza && \
    apt-get install -y zoxide

# Add conda and pipx venvs to PATH
ENV PATH="/opt/conda/bin:/root/.local/bin:/root/.local/pipx/venvs/poetry/bin:${PATH}"

COPY pyproject.toml poetry.lock ./
ENV PATH="/root/.local/bin:/root/.local/pipx/venvs/poetry/bin:${PATH}"
RUN poetry install --no-root

# Default command to keep the container running
CMD ["zsh", "-c", "zsh"]
