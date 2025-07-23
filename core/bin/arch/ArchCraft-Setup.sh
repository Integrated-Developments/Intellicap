#!/bin/bash
set -euo pipefail

# <!-- [SS-0]: Metadata ----->
Version='0.4.47'
Date='7.20.25'
Dev='AngrySatan666'

# <!-- [SS-1]: Global Variables ----->
# /1.1/ Path Variables
: "${ROOT:=/root}"
: "${BASHRC:=/etc/bash.bashrc}"
: "${INT:=/intellicap}"
: "${CACHE:=$HOME/.cache}"
: "${STATE:=$CACHE/state.build}"
: "${SRC:="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"}"

# /1.2/ Echo $var > file Blocks
DisplayFixBlock='(sleep 2 && \
xrandr --auto && \
nitrogen --restore && \
openbox --restart) &'

Ingress='ingress:
  - hostname: intellicap.org
    service: http://localhost:5050
  - service: http_status:404'

# <!-- [SS-2]: SnippeType Functions ----->
# /2.1/ Readability Scripting
Start () {
    local C="\033[96m"
    local R="\033[0m"
    clear
    echo. && echo.
    echo -e "${C}Version: $Version   Date: $Date   Developer:$Dev${R}"
    sleep 2
    echo "===================================================================================================="
    echo.
    Info "__setup__ Starting${R}"
    sleep 2
    Timer 5
    echo.
}

End () {
    local C="\033[96m"
    local R="\033[0m"
    echo.
    echo "===================================================================================================="
    echo.
    Info "__setup__ Has Finished"
}

# /2.2/ Console Debugging
Error () {
    local C="\033[91m"
    local R="\033[0m"
    for txt in "$@"; do
        echo -e "${C}[ERROR] $txt${R}"
        echo.
        sleep 3
    done
}

Warn () {
    local C="\033[33m"
    local R="\033[0m"
    for txt in "$@"; do
        echo -e "${C}[WARN] $txt${R}"
        echo.
        sleep 1
    done
}

Info () {
    local C="\033[92m"
    local R="\033[0m"
    for txt in "$@"; do
        echo -e "${C}[INFO] $txt${R}"
        echo.
        sleep 1
    done
}

# /2.3/ Cache Config
SetCache () {
    echo "$1" >> "$STATE" || Warn "Failed to Write to State Cache $STATE"
}

Cache () {
    grep -qFx "^$1" "$STATE" 2>/dev/null
}

# /2.4/ Console Controlling
Input () {
    if [[ -n "${answer_count:-}" ]]; then
        for ((i = 1; i<= answer_count; i++)); do
            unset "answer$i"
        done
    fi
    answer_count=$#
    local i=1
    for txt in "$@"; do
        local C="\033[32m"
        local R="\033[0m"
        echo -ne "${C}[INPUT] $txt : ${R}"
        read "answer$i"
        echo.
        ((i++))
    done
}

Timer () {
    local C="\033[35m"
    local R="\033[0m"
    local sec=$1
    while [ "$sec" -gt 0 ]; do
        echo -ne "\r${C}[WAIT] Time Left: ${sec}s${R}"
        sleep 1
        ((sec--))
    done
    echo -e "\r${C}[WAIT] Time Left: 0s${R}"
    echo.
}

PAK () {
    if ! Cache PakDep; then
        Info "Bootstrapping Arc Packag Recursor"
        pacman -S --noconfirm yq || { Error "Failed to Install yq"; exit 1 }
        SetCache PakDep
    fi
    local env="$1"
    local verify="$2"
    [[ -z "$verify" || "$verify" != "False" ]] && verify="True"
    Info "Installing $env Packages from Requirements.yaml"
    [[ -f "$SRC/Requirements.yaml" ]] || { Error "Requirements.yaml Not Found in $SRC"; exit 1; }
    mapfile -t deps < <(yq eval ".$env[].name" "$SRC/Requirements.yaml" 2>/dev/null | grep -v '^null$')
    [[ ${#deps[@]} -gt 0 ]] || { Error "No Packages Listed Under '$env' in Requirements.yaml"; exit 1; }
    case "$env" in
        arc)
            for pkg in "${deps[@]}"; do
                Info "Installing $pkg"
                pacman -S --noconfirm "$pkg" || { Error "pacman Failed to Install: $pkg"; exit 1; }
                Info "$pkg Installed"
            done
            [[ "$verify" == "True" ]] && for pkg in "${deps[@]}"; do
                pacman -Qe "$pkg" &>/dev/null || { Error "pacman Verification Failed: $pkg Not Explicitly Installed"; exit 1; }
            done
            ;;
        yay)
            for pkg in "${deps[@]}"; do
                Info "Installing $pkg"
                yay -S --noconfirm "$pkg" || { Error "yay Failed to Install: $pkg"; exit 1; }
                Info "$pkg Installed"
            done
            [[ "$verify" == "True" ]] && for pkg in "${deps[@]}"; do
                yay -Qe "$pkg" &>/dev/null || { Error "yay Verification Failed: $pkg Not Explicitly Installed"; exit 1; }
            done
            ;;
        dgd)
            for pkg in "${deps[@]}"; do
                version=$(yq eval ".dgd[] | select(.name == \"$pkg\") | .version" "$SRC/Requirements.yaml")
                [[ -n "$version" ]] || { Error "Missing Version for $pkg in dgd section"; exit 1; }
                Info "Downgrading $pkg to version $version"
                yes | downgrade "$pkg=$version" || { Error "downgrade Failed for $pkg"; exit 1; }
                Info "$pkg downgraded"
            done
            ;;
        pip)
            for pkg in "${deps[@]}"; do
                Info "Installing $pkg"
                pip install "$pkg" || { Error "pip Failed to Install: $pkg"; exit 1; }
                Info "$pkg Installed"
            done
            [[ "$verify" == "True" ]] && for pkg in "${deps[@]}"; do
                pip show "$pkg" &>/dev/null || { Error "pip Verification Failed: $pkg Not Found"; exit 1; }
            done
            ;;
        npm)
            for pkg in "${deps[@]}"; do
                Info "Installing $pkg"
                npm install -g "$pkg" || { Error "npm Failed to Install: $pkg"; exit 1; }
                Info "$pkg Installed"
            done
            [[ "$verify" == "True" ]] && for pkg in "${deps[@]}"; do
                npm list -g --depth=0 "$pkg" &>/dev/null || { Error "npm Verification Failed: $pkg Not Found Globally"; exit 1; }
            done
            ;;
        crg)
            for pkg in "${deps[@]}"; do
                Info "Installing $pkg"
                cargo install "$pkg" || { Error "cargo Failed to Install: $pkg"; exit 1; }
                Info "$pkg Installed"
            done
            [[ "$verify" == "True" ]] && for pkg in "${deps[@]}"; do
                command -v "$pkg" &>/dev/null || { Error "cargo Verification Failed: $pkg Not in PATH"; exit 1; }
            done
            ;;
        mvn|grd|goi)
            for pkg in "${deps[@]}"; do
                Warn "Manual Management Recommended for $env Package: $pkg"
            done
            ;;
        *)
            Warn "Unknown Package Section: [$env]"
            return 0
            ;;
    esac
    Info "$env Packages Installed Successfully"
}

# <!-- [SS-3]: Directory & Cache ----->
DirCache () {
    # /3.1/ Ensure Terminal at Root Directory "/"
    cd / || { Error "Failed to Change Directory of Terminal to /"; exit 1; }

    # /3.2/ Ensure the "/intellicap" Directory Exists
    if [ ! -d "$HOME" ]; then
        Info "Creating Intellicap Core Directory at $HOME"
        mkdir -p "$HOME" || { Error "Failed to Create Core Directory $HOME"; exit 1; }
        Info "$HOME Directory Created Successfully"
    elif [ -d "$HOME" ]; then
        Info "$HOME Directory Found"
    fi

    # /3.3/ Ensure the "/intellicap/.Cache" Directory Exists
    if [ ! -d "$CACHE" ]; then
        Info "Creating Cache Directory at $CACHE"
        mkdir -p "$CACHE" || { Error "Failed to Create Cache Directory $CACHE"; exit 1; }
        Info "$CACHE Directory Created Successfully"
    elif [ -d "$CACHE" ]; then
        Info "$CACHE Directory Found"
    fi

    # /3.4/ Ensure the state.build Cache Exists
    if [ ! -f "$STATE" ]; then
        Info "Creating Cache state.build"
        touch "$STATE" || { Error "Failed to Create state.build in $CACHE"; exit 1; }
        Info "$STATE Created Successfully"
    elif [ -f "$STATE" ]; then
        Info "$STATE Cache Found"
    fi
}

# <!-- [SS-4]: Install Dependencies ----->
Depends () {
    if ! Cache Deps-Arc; then
		pacman -Syu --noconfirm || { Error "Updating pacman Failed"; exit 1; }
        PAK arc
        PAK yay
        PAK dgd
        SetCache Deps-Arc
    fi
     if ! Cache Deps-Pip; then
        PAK pip
        SetCache Deps-Pip
    fi
    if ! Cache Deps-Java; then
        PAK mvn
        SetCache Deps-Java
    fi
    if ! Cache Deps-Rust; then
        PAK crg
        SetCache Deps-Rust
    fi
    if ! Cache Deps-Npm; then
        PAK npm
        SetCache Deps-Npm
    fi
    if ! Cache Deps-Gradle; then
        PAK grd
        SetCache Deps-Gradle
    fi
    if ! Cache Deps-Go; then
        PAK goi
        SetCache Deps-Go
    fi
}

# <!-- [SS-5]: Config Dependencies ----->
# /5.1/ Bash-Completions
Bash-Comp () {
    # /5.1.1/ Bash-Completion Enabled
    if ! Cache Deps-BashComp; then
        local line='[[ $PS1 && -f /usr/share/bash-completion/bash_completion ]] && . /usr/share/bash-completion/bash_completion'
        grep -Fxq "$line" "$BASHRC" || {
            echo "$line" >> "$BASHRC" || { Error "Failed to Enable Bash-Completion"; exit 1; }
            Info "Enabled Bash-Completion in $BASHRC"
        }
        SetCache Deps-BashComp
    fi

    # /5.1.2/ Add Custom Bash-Completions [NONE TO ADD YET THIS IS JUST A PLACEHOLDER FOR THE FUTURE]

}

# /5.2/ ReSynch-Disp on bash.bashrc 
SynchDisp () {
    if ! Cache Deps-DispSync; then
		Info "Adding Soft Re-Sync of Multi-Monitor Setups to Fix Torn Backgrounds on Boot"
		echo "$DisplayFixBlock" >> "$BASHRC" || { Error "Failed to Append Block to bash.bashrc"; exit 1; }
		Info "Appended RefreshDisplays Block to bash.bashrc"
		SetCache Deps-DispSynch
	fi
}

# /5.3/ Ranger
Ranger () {
    # /5.3.1/ Ranger Configs Directory
    if ! Cache Deps-RngDir; then
        Info "Configuring Ranger"
        if [ ! -d "$ROOT/.config/ranger" ]; then
            Warn "Ranger config Folder Not Found, Creating it"
            mkdir -p "$ROOT/.config/ranger" || { Error "Failed to Create Ranger Config Dir"; exit 1; }
            Info "Ranger Config Folder Created"
        fi
        SetCache Deps-RngDir
    fi
    
    # /5.3.2/ Check Ranger Config File
    if ! Cache Deps-RngConf; then
        export rc_file="$ROOT/.config/ranger/rc.conf"
        if [ ! -f "$rc_file" ]; then
            Warn "Ranger Configs Not Found, Attempting to Create rc.conf with Ranger"
            if command -v ranger >/dev/null 2>&1; then
                ranger --copy-config=rc || Warn "ranger --copy-config=rc failed"
                if [ -f "$rc_file" ]; then
                    Info "Ranger Configs Created Successfully"
                fi
            else
                Warn "Ranger --copy-config=rc Failed" "Manually creating rc.conf"
                echo "# Default Ranger configuration" > "$rc_file" || { Error "Failed to Manually Create rc.conf"; exit 1; }
            fi
        fi
        SetCache Deps-RngConf
    fi
    
    # /5.3.3/ Set Ranger Configs Show Hidden
    if ! Cache Deps-RSet; then
        if [ -f "$rc_file" ]; then
            local target_line1="set show_hidden false"
            local new_line1="set show_hidden true"
            if grep -q "^$target_line1" "$rc_file"; then
                Info "Editing Target Line Present in rc.conf"
                sed -i "s/^$target_line1.*/$new_line1/" "$rc_file" || { Error "Failed to Edit rc.conf"; exit 1; }
            elif grep -q "^$new_line1" "$rc_file"; then
                Info "Target Line Already Present in rc.conf"
            else
                Warn "Target Line in rc.conf Not Found, Adding it"
                echo "$new_line1" >> "$rc_file" || { Error "Failed to Add Line to rc.conf"; exit 1; }
                Info "Added Target Line to Existing rc.conf"
            fi
            SetCache Deps-RSet
        fi
    fi
    
    # /5.3.4/ Set Ranger Configs Viewmode
    if ! Cache Deps-RSet2; then
        local target_line2="set viewmode miller"
        local new_line2="# set viewmode miller"
        local target_line3="# set viewmode multipane"
        local new_line3="set viewmode multipane"
        if grep -q "^$target_line2" "$rc_file"; then
            Info "Editing Target Line Present in rc.conf"
            sed -i "s/^$target_line2.*/$new_line2/" "$rc_file" || { Error "Failed to Edit rc.conf"; exit 1; }
            sed -i "s/^$target_line3.*/$new_line3/" "$rc_file" || { Error "Failed to Edit rc.conf"; exit 1; }
        elif grep -q "^$new_line2" "$rc_file"; then
            if grep -q "^$new_line3" "$rc_file"; then
                Info "Target Line Already Present in rc.conf"
            fi
        else
            Warn "Target Line in rc.conf Not Found, Adding it"
            echo "$new_line2" >> "$rc_file" || { Error "Failed to Add Line to rc.conf"; exit 1; }
            echo "$new_line3" >> "$rc_file" || { Error "Failed to Add Line to rc.conf"; exit 1; }
            Info "Added Target Line to Existing rc.conf"
        fi
        SetCache Deps-RSet2
    fi
    
    # /5.3.5/ Set Ranger Configs Confirm on Delete
    if ! Cache Deps-RSet4; then
        local target_line4="set confirm_on_delete multiple"
        local new_line4="set confirm_on_delete always"
        if grep -q "^$target_line4" "$rc_file"; then
            Info "Editing Target Line Present in rc.conf"
            sed -i "s/^$target_line4.*/$new_line4/" "$rc_file" || { Error "Failed to Edit rc.conf"; exit 1; }
        elif grep -q "^$new_line4" "$rc_file"; then
            Info "Target Line Already Present in rc.conf"
        else
            Warn "Target Line in rc.conf Not Found, Adding it"
            echo "$new_line4" >> "$rc_file" || { Error "Failed to Add Line to rc.conf"; exit 1; }
            Info "Added Target Line to Existing rc.conf"
        fi
        SetCache Deps-RSet4
    fi
    
    # /5.3.6/ Set Ranger Configs Draw Borders
    if ! Cache Deps-RSet5; then
        local target_line5="set draw_borders none"
        local new_line5="set draw_borders both"
        if grep -q "^$target_line5" "$rc_file"; then
            Info "Target Line Already Present in rc.conf"
            sed -i "s/^$target_line5.*/$new_line5/" "$rc_file" || { Error "Failed to Edit rc.conf"; exit 1; }
        elif grep -q "^$new_line5" "$rc_file"; then
            Info "Target Line Already Present in rc.conf"
        else
            Warn "Target Line in rc.conf Not Found, Adding it"
            echo "$new_line5" >> "$rc_file" || { Error "Failed to add line to rc.conf"; exit 1; }
            Info "Added Target Line to Existing rc.conf"
        fi
        SetCache Deps-RSet5
    fi
    
    # /5.3.7/ Set Ranger Configs Autoupdate Cumulative Size
    if ! Cache Deps-RSet6; then
        local target_line6="set autoupdate_cumulative_size false"
        local new_line6="set autoupdate_cumulative_size true"
        if grep -q "^$target_line6" "$rc_file"; then
            Info "Target Line Already Present in rc.conf"
            sed -i "s/^$target_line6.*/$new_line6/" "$rc_file" || { Error "Failed to Edit rc.conf"; exit 1; }
        elif grep -q "^$new_line6" "$rc_file"; then
            Info "Target Line Already Present in rc.conf"
        else
            Warn "Target Line in rc.conf Not Found, Adding it"
            echo "$new_line6" >> "$rc_file" || { Error "Failed to add line to rc.conf"; exit 1; }
            Info "Added Target Line to Existing rc.conf"
        fi
        SetCache Deps-RSet6
    fi
    
    # /5.3.8/ Set Ranger Configs Wrap Scroll
    if ! Cache Deps-RSet7; then
        local target_line7="set wrap_scroll false"
        local new_line7="set wrap_scroll true"
        if grep -q "^$target_line7" "$rc_file"; then
            Info "Editing Target Line Present in rc.conf"
            sed -i "s/^$target_line7.*/$new_line7/" "$rc_file" || { Error "Failed to Edit rc.conf"; exit 1; }
        elif grep -q "^$new_line7" "$rc_file"; then
            Info "Target Line Already Present in rc.conf"
        else
            Warn "Target Line in rc.conf Not Found, Adding it"
            echo "$new_line7" >> "$rc_file" || { Error "Failed to Add Line to rc.conf"; exit 1; }
            Info "Added Target Line to Existing rc.conf"
        fi
        SetCache Deps-RSet7
    fi
    
    # /5.3.9/ Set Ranger Configs Colorscheme
    if ! Cache Deps-RSet8; then
        local target_line8="set colorscheme default"
        local new_line8="set colorscheme snow"
        if grep -q "^$target_line8" "$rc_file"; then
            Info "Editing Target Line Present in rc.conf"
            sed -i "s/^$target_line8.*/$new_line8/" "$rc_file" || { Error "Failed to Edit rc.conf"; exit 1; }
            sed -i -e '$a\' "$rc_file"
        elif grep -q "^$new_line8" "$rc_file"; then
            Info "Target Line Already Present in rc.conf"
        else
            Warn "Target Line in rc.conf Not Found, Adding it"
            echo "$new_line8" >> "$rc_file" || { Error "Failed to Add Line to rc.conf"; exit 1; }
            sed -i -e '$a\' "$rc_file"
            Info "Added Target Line to Existing rc.conf"
        fi
        SetCache Deps-RSet8
    fi
    
    # /5.3.10/ Set Ranger Configs Ranger/Share
    if ! Cache Deps-RngShare; then
        if [ ! -d "$ROOT/.local/share/ranger" ]; then
            Warn "Rangers Local Configs Folder Not Found" "Manually Creating Ranger Configs file"
            mkdir -p "$ROOT/.local/share/ranger" || { Error "Failed to Add Line to rc.conf"; exit 1; }
            Info "Ranger Local Configs Folder Created"
        fi
        SetCache Deps-RngShare
    fi
    
    # /5.3.11/ Set Ranger Configs Ranger/Bookmarks
    if ! Cache Deps-RngBook; then
        if [ ! -f "$ROOT/.local/share/ranger/bookmarks" ]; then
            Warn "Bookmarks File Not Found" "Manually Creating Bookmarks File"
            echo "':$ROOT/.local/share'" > "$ROOT/.local/share/ranger/bookmarks" || { Error "Failed to Add Line to rc.conf"; exit 1; }
            Info "Bookmarks File Created"
        fi
        SetCache Deps-RngBook
    fi
    
    # /5.3.12/ Set Ranger Configs Add Bookmarks
    if ! Cache Deps-RngRead; then
        if [ -f "$ROOT/.local/share/ranger/bookmarks" ]; then
            Info "Including Locations to Bookmarks File"
            echo "':$ROOT/.local/bin'" >> "$ROOT/.local/share/ranger/bookmarks" || { Error "Failed to Add .local/bin to Bookmarks"; exit 1; }
            Info "Bookmarks Set Successfully"
        fi
        SetCache Deps-RngRead
    fi
    
    # /5.3.13/ Set Ranger Configs Ranger/History
    if ! Cache Deps-RngHist; then
        if [ ! -f "$ROOT/.local/share/ranger/history" ]; then
            Info "Creating Local History Config File"
            echo -n > "$ROOT/.local/share/ranger/history" || { Error "Failed to Create History File"; exit 1; }
            Info "History Config Created"
        fi
        SetCache Deps-RngHist
    fi
    
    # /5.3.14/ Set Ranger Configs Ranger/Tagged
    if ! Cache Deps-RngTag; then
        if [ ! -f "$ROOT/.local/share/ranger/tagged" ]; then
            Info "Creating Local Tagged Config File"
            echo -n > "$ROOT/.local/share/ranger/tagged" || { Error "Failed to Create Tagged File"; exit 1; }
            Info "Tagged Config Created"
        fi
        SetCache Deps-RngTag
    fi
    
    # /5.3.15/ Set Ranger Configs Ranger/GLOBAL
    if ! Cache Deps-RGlobal; then
        if ! grep -q "RANGER_LOAD_DEFAULT_RC" "$BASHRC"; then
            echo 'export RANGER_LOAD_DEFAULT_RC=FALSE' >> "$BASHRC" || { Error "Failed to Set RANGER_LOAD_DEFAULT_RC"; exit 1; }
            Info "Set RANGER_LOAD_DEFAULT_RC=FALSE in bash.bashrc"
        fi
        SetCache Deps-RGlobal
    fi
    Info "Ranger Fully Configured"
    SetCache Deps-Ranger
}
 
# /5.4/ CloudFlared
CloudFlare () {
	# /5.4.1/ Login to CloudFlared CLI
	if ! Cache Cloudflare-Login; then
        Info "Running Cloudflared Login Will Require Browser + Input"
        if ! [ -d "$ROOT/.cloudflared" ]; then
			mkdir -p "$ROOT/.cloudflared" || { Error "Failed to Create Cloudflared Config Dir"; exit 1; }
		fi
        cloudflared login || { Error "Cloudflared Login Failed"; exit 1; }
        SetCache Cloudflare-Login
        Info "Cloudflare Login Successful"
    fi
	
	# /5.4.2/ Create the Flask Tunnel to Domain
	Info "Creating Tunnel in Cloudflared"
	if ! Cache Cloudflare-Tunnel; then
        Info "Creating Named Tunnel for Flask App"
        local before=($(ls -1 "$ROOT/.cloudflared"))
        cloudflared tunnel create Flask-Tunnel || { Error "Tunnel creation failed"; exit 1; }
        local after=($(ls -1 "$ROOT/.cloudflared"))
        for f in "${after[@]}"; do
			if [[ ! " ${before[*]} " =~ " $f " ]]; then
				local new="$f"
				break
			fi
		done
		[[ -z "$new" ]] || { Error "Failed to Locate Tunnel Credentials File"; exit 1 }
        SetCache Cloudflare-Tunnel
        Info "Tunnel 'Flask-Tunnel' Created"
    fi
    
	# /5.4.3/ Correct Paths in Config
	Info "Setting Cloudflared Tunnel Configs"
	if ! Cache Cloudflare-Routes; then
		[[ -f "$ROOT/.cloudflared/$new" ]] || { Error "Tunnel credentials file missing"; exit 1; }
		cfg="$ROOT/.cloudflared/config.yml"
		sed -i "/^tunnel:/d" "$cfg" || { Error "Failed to remove 'tunnel:' line"; exit 1; }
		sed -i "/^credentials-file:/d" "$cfg" || { Error "Failed to remove 'credentials-file:' line"; exit 1; }
		echo "tunnel: Flask-Tunnel" >> "$cfg" || { Error "Failed to write 'tunnel:' line"; exit 1; }
		echo "credentials-file: /root/.cloudflared/$new" >> "$cfg" || { Error "Failed to write 'credentials-file:' line"; exit 1; }
		sed -i '/^ingress:/,$d' "$cfg" || { Error "Failed to clear ingress block"; exit 1; }
		echo "$Ingress" >> "$cfg" || { Error "Failed to append ingress block"; exit 1; }
		Info "Cloudflared Tunnel Config Installed to $cfg"
		SetCache Cloudflare-Routes
	fi

	# /5.4.4/ Setup Systemd Service
	Info "Installing Cloudflare-Service"
	if ! Cache Cloudflare-Service; then
        cloudflared service install || { Error "Cloudflared Systemd Install Failed"; exit 1; }
        SetCache Cloudflare-Service
        Info "Cloudflared Systemd Service Installed"
    fi
	
	# /5.4.5/ Enable Tunnel
	Info "Enabeling Cloudflare Service"
	if ! Cache Cloudflare-Enable; then
		if ! systemctl is-enabled cloudflared 2>/dev/null; then
			systemctl enable cloudflared || { Error "Failed to Enable Cloudflared Service"; exit 1; }
		fi
		SetCache Cloudflare-Enable
		Info "Cloudflared Set to Autostart"
	fi
}

# <!-- [SS-6]: Aliases in bash.bashrc
Alias () {
    if ! Cache Alias-ListAll; then
        echo "alias ls='ls -a'" >> "$BASHRC" || { Error "Failed to Set Alias ls on bash.bashrc"; exit 1; }
		SetCache Alias-ListAll
    fi
    if ! Cache Alias-SyncDis; then
		echo "alias syncdis='openbox --restart'" >> "$BASHRC" || { Error "Failed to Set Alias syncdis on bash.bashrc"; exit 1; }
		SetCache Alias-SyncDis
	fi
	if ! Cache Alias-Intellicap; then
		echo "alias server.start='cloudflared tunnel run Flask-Tunnel" >> "$BASHRC" || { Error "Failed to Set Alias server.start on bash.bashrc"; exit 1; }
		echo "alias server.stop=\"pkill -f 'cloudflared tunnel run Flask-Tunnel'\"" >> "$BASHRC" || { Error "Failed to Set Alias server.start on bash.bashrc"; exit 1; }
		echo "alias server.reboot='server.stop && sleep 1 && server.start'" >> "$BASHRC" || { Error "Failed to Set Alias server.start on bash.bashrc"; exit 1; }
		SetCache Alias-Intellicap
	fi
}

# <!-- [SS-8]: Configure Root Profile
SirRoot () {
    # /8.1/ Root Gui Access & No DPMS
    if ! Cache Root-Gui; then
		[[ -f "$SRC/openbox.zip" ]] || { Error "Openbox Config Zip Not Found in Source"; exit 1; }
		mkdir -p "$ROOT/.config" || { Error "Failed to Create /root/.config/"; exit 1; }
        unzip -oq "$SRC/openbox.zip" -d "$ROOT/.config/" || { Error "Failed to Extract Openbox Config"; exit 1; }
		SetCache Root-Gui
	fi
	
	# /8.2/ Desktop Pretty
	if ! Cache Root-Pretty; then
		local src="$SRC/dsktop"
		[[ -d "$ROOT/.icons" ]] || { Error "Icons Dir Not Found in Source"; exit 1; }
		mkdir -p "$ROOT/.icons" || { Error "Failed to Create /root/.config/"; exit 1; }
		cp -r "$src/icons/." "$ROOT/.icons" || { Error "Failed to Create Root .icons"; exit 1; }
		cp -r "$src/Img/." "$ROOT/Pictures" || { Error "Failed to Create Root Pictures"; exit 1; }
		cp -r "$src/Music/." "$ROOT/Music" || { Error "Failed to Create Root Music"; exit 1; }
		cp -r "$src/Documents/." "$ROOT/Documents" || { Error "Failed to Create Root Documents"; exit 1; }
		cp -r "$src/Notifications/." "$ROOT/.notifications" || { Error "Failed to Create Root .notifications"; exit 1; }
		cp -f "$src/creds.ini" "$ROOT/.local/creds.ini" || { Error "Failed to Create Root Service Credentials"; exit 1; }
		SetCache Root-Pretty
		Info "Desktop Accessories Installed to Root"
	fi
	
    # /8.3/ Autologin Root
    if ! Cache Root-Auto; then
        Info "Enabling Root Autologin on tty1"
        mkdir -p "/etc/systemd/system/getty@tty1.service.d" || { Error "Failed to Create Autologin File"; exit 1;} 
        cp "$SRC/assets/override-root-login.conf" "/etc/systemd/system/getty@tty1.service.d/override.conf" || { Error "Failed to Set Autologin Override"; exit 1; }
        systemctl daemon-reexec || { Error "Systemctl daemon-reexec Exited with an Error"; exit 1; }
        systemctl daemon-reload || { Error "Systemctl daemon-reload Exited with an Error"; exit 1; }
        SetCache Root-Auto
        Info "Root Autologin Configured Successfully"
    fi
    if ! Cache Root-NoPass; then
        Info "Clearing Root Password"
        passwd -d root || { Error "Failed to Clear Root Password"; exit 1; }
        SetCache Root-NoPass
        Info "Root Password Cleared"
    fi
    if ! Cache Root-Login; then
        Info "Persisting Root to Auto-Login"
        cp "$SRC/assets/bash_profile" "/root/.bash_profile" || { Error "Failed to Copy .bash_profile"; exit 1; }
        SetCache Root-Login
        Info "Root Fully Set to Auto Login"
    fi
    
    # /8.4/ Root/.local/bin to Path and chmod +x Contents
    if ! Cache Root-LocalBin; then
		Info "PATHing Root/.local/bin"
		echo 'export PATH="$PATH:/root/.local/bin"' >> "$BASHRC" || { Error "Failed to Copy to Bashrc"; exit 1; }
		echo 'find /root/.local/bin -type f -exec chmod +x {} \;' >> || "$BASHRC" { Error "Failed to Copy to Bashrc"; exit 1; }
		echo 'export ROOT=/root' >> "$BASHRC" || { Error "Failed to Copy to Bashrc"; exit 1; }
		SetCache Root-LocalBin
		Info "Root/.local/bin in PATH and Executable"
	fi
}
    
Start
DirCache
Depends
Bash-Comp
SynchDisp
Ranger
CloudFlare
Alias
SirRoot
End
