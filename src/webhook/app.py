"""
Flask webhook handler for WhatsApp messages.
Minimal version for initial deployment.
"""
from flask import Flask, request, jsonify
import logging
import os

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key')


@app.route('/')
def index():
    """Root endpoint - bot info"""
    return jsonify({
        "bot": "Notion Pangeia V2",
        "version": "2.0.0",
        "status": "online",
        "instance": "pangeiabot"
    })


@app.route('/health')
def health():
    """Health check endpoint for Railway"""
    return jsonify({
        "status": "healthy",
        "service": "notion-pangeia-v2"
    }), 200


@app.route('/webhook/whatsapp', methods=['POST'])
def webhook_whatsapp():
    """
    Webhook endpoint for Evolution API messages.
    Minimal version - will be expanded in next phase.
    """
    try:
        data = request.json
        logger.info(f"Received webhook: {data}")

        # Extract message info
        event = data.get('event')
        instance = data.get('instance')

        if event == 'messages.upsert':
            message_data = data.get('data', {})
            key = message_data.get('key', {})
            message = message_data.get('message', {})

            # Ignore messages from bot itself
            if key.get('fromMe'):
                logger.info("Ignoring message from bot")
                return jsonify({"status": "ignored", "reason": "fromMe"}), 200

            # Extract text
            text = (
                message.get('conversation') or
                message.get('extendedTextMessage', {}).get('text') or
                ''
            )

            phone = key.get('remoteJid', '').split('@')[0]

            logger.info(f"Message from {phone}: {text}")

            # TODO: Process command and send response
            # This will be implemented in Phase 5

        return jsonify({"status": "received"}), 200

    except Exception as e:
        logger.error(f"Webhook error: {e}", exc_info=True)
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
