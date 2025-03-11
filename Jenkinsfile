pipeline {
    agent any

    stages {
        stage('Clone Repository') {
            steps {
                git 'https://github.com/hanwangho03/TTKiemThuT5.git' // 🔹 Cập nhật link repo của bạn
            }
        }

        stage('Set Up Environment') {
            steps {
                script {
                    // Cài đặt virtual environment (Linux/Mac)
                    if (isUnix()) {
                        sh 'python3 -m venv venv'
                        sh 'source venv/bin/activate'
                    } else {
                        bat 'python -m venv venv'
                        bat 'venv\\Scripts\\activate'
                    }

                    // Cài đặt dependencies
                    sh 'pip install -r requirements.txt'
                }
            }
        }

        stage('Start Flask Server') {
            steps {
                script {
                    // Chạy Flask server ở background
                    sh 'python app.py &'
                    sleep 5 // Đợi server khởi động
                }
            }
        }

        stage('Run Selenium Tests') {
            steps {
                script {
                    // Chạy test bằng Selenium
                    sh 'python test_todolist.py'
                }
            }
        }

        stage('Cleanup') {
            steps {
                script {
                    // Tắt Flask server sau khi test xong
                    sh 'pkill -f app.py || echo "No process found"'
                }
            }
        }
    }
}
