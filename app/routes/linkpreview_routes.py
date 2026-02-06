from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
import requests
import os

bp = Blueprint('linkpreview_bp', __name__, url_prefix='/linkpreview')

@bp.route('/fetch', methods=['POST', 'OPTIONS'])
@cross_origin(supports_credentials=True)
def fetch_link_preview():
    """fetch metadata from url using LinkPreview API"""
    if request.method == 'OPTIONS':
        return '', 200
    
    request_data = request.get_json()
    url = request_data.get('url')
    
    if not url:
        return jsonify({'error': 'URL is required'}), 400
    
    api_key = os.getenv('LINKPREVIEW_API_KEY')
    if not api_key:
        return jsonify({'error': 'LinkPreview API key not configured'}), 500
    
    try:
        response = requests.post(
            'https://api.linkpreview.net',
            headers={'X-Linkpreview-Api-Key': api_key,
                    'Cache-Control': 'no-cache'},
            json={'q': url},
            timeout=10
        )
        
        if response.status_code == 425:
            import time
            time.sleep(1) # Brief cooldown
            response = requests.post(
                'https://api.linkpreview.net',
                headers={'X-Linkpreview-Api-Key': api_key},
                json={'q': url},
                timeout=10
            )
            
        if response.status_code != 200:
            return jsonify({'error': f'LinkPreview API error: {response.status_code}'}), response.status_code
        
        data = response.json()
        
        # return only the fields we need
        return jsonify({
            'title': data.get('title', ''),
            'description': data.get('description', ''),
            'image': data.get('image', ''),
            'url': data.get('url', url)
        }), 200
        
    except requests.exceptions.Timeout:
        return jsonify({'error': 'Request timeout'}), 504
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Request failed: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Unexpected error: {str(e)}'}), 500
