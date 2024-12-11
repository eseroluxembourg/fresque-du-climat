#!/bin/sh

# Function to determine the full path of the script
get_script_path() {
    # For Bash
    if [ -n "${BASH_SOURCE-}" ]; then
        if [ "${BASH_SOURCE[0]}" != "$0" ]; then
            # Script is being sourced
            echo "$(readlink -f "${BASH_SOURCE[0]}")"
        else
            # Script is being executed
            echo "$(readlink -f "$0")"
        fi

    # For Zsh
    elif [ -n "${ZSH_VERSION-}" ]; then
        case $ZSH_EVAL_CONTEXT in
            *file) echo "$(readlink -f "$0")" ;;    # Script is being executed
            *source) echo "$(readlink -f "${(%):-%N}")" ;;    # Script is being sourced
            *) echo "Unknown execution context in Zsh." ;;
        esac

    # For Ksh
    elif [ -n "${KSH_VERSION-}" ]; then
        if [ "$(basename -- "$0")" = "ksh" ]; then
            # Likely sourced, as $0 is 'ksh'
            echo "$(cd "$(dirname "${.sh.file}")" && pwd)/$(basename "${.sh.file}")"
        else
            # Script is being executed
            echo "$(readlink -f "$0")"
        fi

    # For Dash or other POSIX sh
    elif [ -n "${POSIXLY_CORRECT-}" ] || [ -z "${BASH_VERSION-}" ]; then
        # Detect execution mode
        if [ "$0" = "sh" ] || [ "$0" = "-sh" ]; then
            echo "Source mode detection not supported in pure POSIX shells."
        else
            echo "$(readlink -f "$0")"
        fi

    # Fallback
    else
        echo "Shell not recognized or not supported."
    fi
}

# Function to check if the script is sourced
check_sourced() {
    # For Bash
    if [ -n "${BASH_SOURCE-}" ] && [ "${BASH_SOURCE[0]}" != "$0" ]; then
        echo "This script must be executed, not sourced."
        exit 1
    fi

    # For Zsh
    if [ -n "${ZSH_VERSION-}" ] && [[ "$ZSH_EVAL_CONTEXT" == *source* ]]; then
        echo "This script must be executed, not sourced."
        exit 1
    fi

    # For Ksh
    if [ -n "${KSH_VERSION-}" ] && [ "$(basename -- "$0")" = "ksh" ]; then
        echo "This script must be executed, not sourced."
        exit 1
    fi

    # For POSIX sh and other shells
    if [ "$0" = "sh" ] || [ "$0" = "-sh" ]; then
        echo "Source detection not supported in this shell. Assuming sourced mode."
        exit 1
    fi

    # Default: Assume not sourced
    return 0
}

# Check if the script is sourced
check_sourced

# Check if the script is being run as root
check_root() {
    if [ "$(id -u)" -ne 0 ]; then
        echo "This script must be run as root. Please switch to the root user or use sudo."
        exit 1
    fi
}

# Call the functions
SCRIPT_PATH="$(get_script_path)"
check_root

# Print the full path of the script (if it proceeds)
echo "Script path: $SCRIPT_PATH"
echo "Running with root privileges. Proceeding..."


# Setting up service configuration file
cp $(dirname "$SCRIPT_PATH")/esero-service.service /etc/systemd/system/esero-service.service

# Setting up service configuration file
cp $(dirname "$SCRIPT_PATH")/esero_server_run.sh /usr/local/bin/esero_server_run.sh
chmod +x /usr/local/bin/esero_server_run.sh

echo "
Now, you can perform the following command to enable the service :

sudo systemctl daemon-reload
sudo systemctl enable test-service.service
sudo systemctl start test-service.service

Reboot to see if the service works correctly :
sudo shutdown -r now
"

# To check : watch -n3 "cat /var/log/testservice.txt"
