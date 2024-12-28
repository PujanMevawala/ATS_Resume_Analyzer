mkdir -p ~/.streamlit

# Install poppler-utils (required for pdf2image)
apt-get update && apt-get install -y poppler-utils

# Ensure that Streamlit runs in headless mode
echo "[server]" > ~/.streamlit/config.toml
echo "headless = true" >> ~/.streamlit/config.toml
echo "port = 8501" >> ~/.streamlit/config.toml
