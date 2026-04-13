import os
import logging
from datetime import datetime
from flask import request, jsonify
from werkzeug.utils import secure_filename

from services.validation_service import validate_data
from services.file_service import allowed_file, get_allowed_extensions
from services.database_service import (
    store_validation_result,
    get_validation_result,
    get_domain_statistics,
    get_recent_validations,
    export_validation_data,
    get_database_stats
)

logger = logging.getLogger(__name__)


def register_routes(app):

    # ==================== HEALTH CHECK ====================
    @app.route('/', methods=['GET'])
    def home():
        return jsonify({'message': 'Backend Running'}), 200


    # ==================== FILE UPLOAD ====================
    @app.route('/upload', methods=['POST'])
    def upload_file():
        try:
            # ---- Check file ----
            if 'file' not in request.files:
                return jsonify({'error': 'No file provided'}), 400

            # ---- Check domain ----
            if 'domain' not in request.form:
                return jsonify({'error': 'No domain specified'}), 400

            file = request.files['file']
            domain = request.form.get('domain')

            # ---- Check empty filename ----
            if file.filename == '':
                return jsonify({'error': 'No file selected'}), 400

            # ---- Check extension ----
            if not allowed_file(file.filename):
                allowed_exts = ', '.join(get_allowed_extensions())
                return jsonify({
                    'error': f'File type not allowed. Allowed types: {allowed_exts}'
                }), 400

            # ---- Save file ----
            filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
            filename = timestamp + filename

            upload_folder = 'uploads'
            os.makedirs(upload_folder, exist_ok=True)

            file_path = os.path.join(upload_folder, filename)
            file.save(file_path)

            logger.info(f"File saved: {file_path}")

            # ---- Validate data ----
            result = validate_data(file_path, domain)

            # ---- Store in DB ----
            record_id = store_validation_result(result, domain, file.filename)
            stored = record_id is not None

            # ---- Prepare response ----
            response_data = result.to_dict()
            response_data['record_id'] = record_id
            response_data['stored'] = stored
            response_data['timestamp'] = datetime.now().isoformat()

            return jsonify(response_data), 200

        except Exception as e:
            logger.error(f"Upload error: {str(e)}")
            return jsonify({'error': f'Server error: {str(e)}'}), 500


    # ==================== GET RESULT ====================
    @app.route('/results/<int:record_id>', methods=['GET'])
    def get_result(record_id):
        result = get_validation_result(record_id)

        if result:
            return jsonify(result), 200
        else:
            return jsonify({'error': 'Record not found'}), 404


    # ==================== DOMAIN STATS ====================
    @app.route('/stats/<domain>', methods=['GET'])
    def get_domain_stats(domain):
        stats = get_domain_statistics(domain)

        if stats:
            return jsonify(stats), 200
        else:
            return jsonify({'error': 'No statistics available'}), 404


    # ==================== HISTORY ====================
    @app.route('/history', methods=['GET'])
    def get_history():
        limit = request.args.get('limit', 10, type=int)
        limit = min(limit, 100)

        data = get_recent_validations(limit)

        return jsonify({
            'total': len(data),
            'validations': data
        }), 200


    # ==================== EXPORT ====================
    @app.route('/export', methods=['GET'])
    def export_data():
        domain = request.args.get('domain')
        format_type = request.args.get('format', 'json')

        if format_type not in ['json', 'csv']:
            return jsonify({'error': 'Format must be json or csv'}), 400

        data = export_validation_data(domain, format_type)

        if format_type == 'csv':
            return data, 200, {'Content-Type': 'text/csv'}
        else:
            return data, 200, {'Content-Type': 'application/json'}


    # ==================== DB STATS ====================
    @app.route('/db-stats', methods=['GET'])
    def db_stats():
        stats = get_database_stats()
        return jsonify(stats), 200


    # ==================== ERROR HANDLERS ====================
    @app.errorhandler(413)
    def file_too_large(error):
        return jsonify({'error': 'File too large (max 16MB)'}), 413


    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Endpoint not found'}), 404


    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500