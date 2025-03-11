pipeline {
    agent any

    stages {
        stage('Clone Repository') {
            steps {
                git 'https://github.com/hanwangho03/TTKiemThuT5.git'  // 🛠 Đổi URL repo của bạn
            }
        }

        stage('Setup Environment') {
            steps {
                sh 'python -m venv venv'
                sh 'source venv/bin/activate'
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Start Flask Server') {
            steps {
                script {
                    def flask = startFlask()
                }
            }
        }

        stage('Run Selenium Tests') {
            steps {
                sh 'pytest --html=report.html'  // 🛠 Chạy kiểm thử
            }
        }

        stage('Publish Report') {
            steps {
                publishHTML(target: [
                    allowMissing: false,
                    alwaysLinkToLastBuild: true,
                    keepAll: true,
                    reportDir: '.',
                    reportFiles: 'report.html',
                    reportName: 'Selenium Test Report'
                ])
            }
        }
    }
}

def startFlask() {
    sh 'python app.py &'
}
