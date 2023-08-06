import os
from pathlib import Path

import pandas as pd
from flask import Flask, jsonify, request

import debugger


def create_app():
    here = Path(__file__).resolve().parent
    app = Flask(__name__)

    @app.route('/df/<df_id>', methods=['GET'])
    def df_view(df_id):
        df_file = here / 'dataframes' / (str(df_id) + '.dump')
        if df_file.exists():
            df = pd.read_feather(str(df_file))
            return debugger.launch_debugger(df)
        else:
            print(f"[err] No file {df_file}")
            return jsonify({"success": False, "error": f"no DF with id {df_id}"})

    @app.route('/df/<df_id>', methods=['POST'])
    def df_upload(df_id):
        try:
            df_file = here / 'dataframes' / (str(df_id) + '.dump')
            with open(df_file, 'wb') as f:
                while not request.stream.is_exhausted:
                    f.write(request.stream.read(1024 * 100))
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})
        else:
            return jsonify({'success': True, 'message': 'File uploaded'})

    @app.route('/')
    def home():
        return 'no index yet'

    return app


def main():
    os.environ['WERKZEUG_DEBUG_PIN'] = 'off'
    app = create_app()
    app.run(
        host='localhost',
        port=4577,
        debug=True,
        use_reloader=False,
        threaded=True,
    )


if __name__ == '__main__':
    main()
