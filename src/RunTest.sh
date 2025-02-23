ROOT_DIR="/home/gm-svr/Scripts/TwitchOpener"
if [ -z "$ROOT_DIR" ]; then
    ROOT_DIR="$(dirname "$(realpath "$0")")"
fi

if [ ! -d "$ROOT_DIR/venv" ]; then
    python3 -m venv "$ROOT_DIR/venv"
    source "$ROOT_DIR/venv/bin/activate"
    python3 -m ensurepip --upgrade
else
    source "$ROOT_DIR/venv/bin/activate"
fi
python3 -m pip install -r "$ROOT_DIR/requirements.txt"
python3 -u "$ROOT_DIR/WindowArrangerTest.py"