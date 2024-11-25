# Dependencies: arduino-cli

usage() {
    echo "Usage: $0 <sketch-dir> <board-pattern>"
    echo
    echo "Arguments:"
    echo "  <sketch-dir>    Specify arduino sketch directory."
    echo "  <board-pattern> Specify the board pattern to upload to."
    echo "                  Search for the pattern in arduino-cli board list."
}

if [ $# -ne 2 ]; then
    usage
    exit 1
fi

dir="$1"
board="$2"

board_info=$(arduino-cli board list | grep -m1 "$board") || {
    echo "No boards found."
    exit 1
}

echo "$board_info"
echo "Board found by '$board'"
echo

port=$(echo "$board_info" | awk '{print $1}')
fqbn=$(echo "$board_info" | awk '{print $(NF-1)}')
core=$(echo "$board_info" | awk '{print $(NF)}')

if [ -d "$dir" ]; then
    arduino-cli board attach -p "$port" -b "$fqbn" "$dir"
    exit 0
fi

echo "creating new sketch"
arduino-cli sketch new "$dir"

arduino-cli core update-index

arduino-cli core install "$core"

arduino-cli board attach -p "$port" -b "$fqbn" "$dir"
