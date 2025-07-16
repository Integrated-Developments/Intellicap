Code_Install () {
    apt install curl -y
    curl -fsSL https://code-server.dev/install.sh | sh
    code-server
    if [ -f ~/.config/code-server/config.yaml ]; then
        sed -i '/^password:/d' ~/.config/code-server/config.yaml
        sed -i 's/^auth:.*/auth: none/' ~/.config/code-server/config.yaml
    fi
}

User_Add () {
    usr="$1"
    useradd -r -s /bin/bash "$usr"
    passwd -d "$usr"
    mkdir -p '/etc/systemd/system/getty@tty1.service.d'
    echo -n > '/etc/systemd/system/getty@tty1.service.d/override.conf'
    echo '[Service]' >> '/etc/systemd/system/getty@tty1.service.d/override.conf'
    echo 'ExecStart=' >> '/etc/systemd/system/getty@tty1.service.d/override.conf'
    echo 'ExecStart=-/sbin/agetty --noclear %I $TERM' >> '/etc/systemd/system/getty@tty1.service.d/override.conf'
    echo '$TERM' >> '/etc/systemd/system/getty@tty1.service.d/override.conf'
    systemctl daemon-reexec
    systemctl daemon-reload
    systemctl restart getty@tty1.service
}
