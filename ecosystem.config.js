module.exports = {
    apps: [
        {
            name: 'XIRA Speech To Text',
            script: 'gunicorn',
            args: '-w 6 -b 0.0.0.0:3600 -k gthread --threads 5 Whiper:app',
            cwd: '/home/ubuntu/xira_speech_to_text/',
            interpreter: '/home/ubuntu/xira_speech_to_text/.venv/bin/python3',
            instances: '1',
            exec_mode: 'fork',
            autorestart: true,
            max_restarts: 10,
            max_memory_restart: '8G',
            log_date_format: 'YYYY-MM-DDTHH:mm:ssZ',
            watch: ['./'],
            watch_delay: 1000,
            watch_options: { followSymlinks: false },
            error_file: '~/.pm2/logs/XIRA Speech To Text-err.log',
            out_file: '~/.pm2/logs/XIRA Speech To Text-out.log',
            log_file: '~/.pm2/logs/XIRA Speech To Text-combined.log',
            cron_restart: '0 0 * * *',
            env: {
                "MODEL_SIZE" : "medium",
                "DEVICE" : "cuda",
                "COMPUTER_TYPE" : "float16"
            }
        },
    ]
}
