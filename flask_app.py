from flask import Flask, redirect, render_template, request, jsonify
import logging
import json
import os

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# URL-konfiguration
SHAREPOINT_URLS = {
    'main': 'https://dynavagroup.sharepoint.com/sites/msteams_7303a6_911413/',
    'case': 'https://dynavagroup.sharepoint.com/sites/msteams_7303a6_911413/_layouts/15/listform.aspx?PageType=8&ListId=%7B7E7F7DF5-2AB4-4CB9-86BA-797C4FFC01F6%7D'
}

# Load configurations from config.json
def load_config():
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logger.error(f"Error loading config.json: {e}")
        return {}

@app.route('/')
def root():
    logger.info("Root route called")
    config = load_config()
    clients = list(config.keys())  # Get list of all configured clients
    return render_template('index.html', 
                          main_url=SHAREPOINT_URLS['main'], 
                          case_url=SHAREPOINT_URLS['case'],
                          clients=clients)

@app.route('/kopparstaden/main')
def main_route():
    logger.info("Main route called")
    return redirect(SHAREPOINT_URLS['main'])

@app.route('/kopparstaden/case')
def case_route():
    logger.info("Case route called")
    return redirect(SHAREPOINT_URLS['case'])

@app.route('/pop')
def pop_route():
    """
    Dynamic route that opens multiple URLs from the config.json file based on client query parameter
    """
    client = request.args.get('client')
    logger.info(f"Pop route called for client: {client}")
    
    if not client:
        return redirect('/')
    
    config = load_config()
    clients = list(config.keys())
    
    # Just render the template - JavaScript will handle the actual URL opening
    return render_template('index.html', 
                          main_url=SHAREPOINT_URLS['main'], 
                          case_url=SHAREPOINT_URLS['case'],
                          clients=clients,
                          pop_client=client)

@app.route('/pop/<client>')
def pop_client_route(client):
    """
    Dynamic route that opens multiple URLs using a cleaner URL format: /pop/client
    """
    logger.info(f"Direct pop route called for client: {client}")
    config = load_config()
    clients = list(config.keys())
    
    # Render the template - JavaScript will handle URL opening and redirection
    return render_template('index.html', 
                          main_url=SHAREPOINT_URLS['main'], 
                          case_url=SHAREPOINT_URLS['case'],
                          clients=clients,
                          pop_client=client)

# New route for client-specific pages
@app.route('/<client>')
def client_route(client):
    """
    Client-specific page that shows only information for this client
    """
    logger.info(f"Client route called for: {client}")
    config = load_config()
    clients = list(config.keys())
    
    # Check if this is a valid client
    if client in clients:
        return render_template('index.html', 
                              main_url=SHAREPOINT_URLS['main'], 
                              case_url=SHAREPOINT_URLS['case'],
                              clients=clients)
    else:
        return redirect('/')

@app.route('/api/urls/<client>')
def get_client_urls(client):
    """API endpoint to get URLs for a specific client"""
    logger.info(f"API request for client URLs: {client}")
    config = load_config()
    
    if client in config and "urls" in config[client]:
        return jsonify({"urls": config[client]["urls"]})
    else:
        logger.warning(f"Client '{client}' not found in configuration or has no URLs")
        return jsonify({"error": f"No URLs found for client '{client}'"}), 404

# Dynamic client action route
@app.route('/<client>/<action>')
def dynamic_client_route(client, action):
    """
    Dynamic route that handles client-specific actions
    """
    logger.info(f"Dynamic route called for client: {client}, action: {action}")
    config = load_config()
    
    if client in config and isinstance(config[client], dict) and action in config[client]:
        return redirect(config[client][action])
    else:
        logger.warning(f"Route '{client}/{action}' not found in configuration")
        return jsonify({"error": f"Route '{client}/{action}' not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=83, debug=True)
else:
    wsgi_app = app.wsgi_app