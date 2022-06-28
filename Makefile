.DEFAULT_GOAL := run
.PHONY: run

install:
	sudo apt update
	sudo apt install libcairo2-dev libpango1.0-dev ffmpeg
	sudo apt install python3-pip
	sudo apt-get install coinor-cbc
	sudo apt-get install -y git pkg-config coinor-libcbc-dev coinor-libosi-dev coinor-libcoinutils-dev coinor-libcgl-dev
	export COIN_INSTALL_DIR=/usr/
	pip3 install --pre cylp
	python3 -m pip install -r requirements.txt

run:
	streamlit run main.py
