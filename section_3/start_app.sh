#!/bin/bash

# Section 3: Cursor AI应用开发启动脚本

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印带颜色的消息
print_message() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${BLUE}================================${NC}"
    echo -e "${BLUE}  Cursor AI应用开发环境启动${NC}"
    echo -e "${BLUE}================================${NC}"
}

# 检查Python版本
check_python() {
    print_message "检查Python版本..."
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
        print_message "Python版本: $PYTHON_VERSION"
    else
        print_error "未找到Python3，请先安装Python 3.8+"
        exit 1
    fi
}

# 创建虚拟环境
create_venv() {
    print_message "创建Python虚拟环境..."
    if [ ! -d "venv" ]; then
        python3 -m venv venv
        print_message "虚拟环境创建成功"
    else
        print_message "虚拟环境已存在"
    fi
}

# 激活虚拟环境
activate_venv() {
    print_message "激活虚拟环境..."
    source venv/bin/activate
    print_message "虚拟环境已激活"
}

# 安装依赖
install_dependencies() {
    print_message "安装项目依赖..."
    pip install --upgrade pip
    pip install -r requirements.txt
    print_message "依赖安装完成"
}

# 检查环境变量
check_env() {
    print_message "检查环境变量配置..."
    if [ ! -f ".env" ]; then
        print_warning "未找到.env文件，创建示例配置文件..."
        cat > .env << EOF
# AI模型API配置
OPENAI_API_KEY=your_openai_api_key_here
DEEPSEEK_API_KEY=your_deepseek_api_key_here
DASHSCOPE_API_KEY=your_dashscope_api_key_here

# 应用配置
APP_ENV=development
DEBUG=True
PORT=8501

# 数据库配置（可选）
DATABASE_URL=sqlite:///app.db
EOF
        print_message "示例.env文件已创建，请根据实际情况修改配置"
    else
        print_message ".env文件已存在"
    fi
}

# 启动开发服务器
start_dev_server() {
    print_message "启动开发服务器..."
    print_message "访问地址: http://localhost:8501"
    print_message "按 Ctrl+C 停止服务器"
    
    # 启动Streamlit应用
    streamlit run app.py --server.port 8501 --server.address 0.0.0.0
}

# 显示帮助信息
show_help() {
    echo "使用方法: $0 [选项]"
    echo ""
    echo "选项:"
    echo "  setup      - 初始设置（创建虚拟环境、安装依赖）"
    echo "  start      - 启动开发服务器"
    echo "  install    - 安装依赖"
    echo "  check      - 检查环境"
    echo "  help       - 显示帮助信息"
    echo ""
    echo "示例:"
    echo "  $0 setup   - 首次使用时的环境设置"
    echo "  $0 start   - 启动应用"
}

# 主函数
main() {
    print_header
    
    case "${1:-start}" in
        "setup")
            check_python
            create_venv
            activate_venv
            install_dependencies
            check_env
            print_message "环境设置完成！"
            ;;
        "start")
            check_python
            activate_venv
            check_env
            start_dev_server
            ;;
        "install")
            activate_venv
            install_dependencies
            ;;
        "check")
            check_python
            check_env
            print_message "环境检查完成"
            ;;
        "help"|"-h"|"--help")
            show_help
            ;;
        *)
            print_error "未知选项: $1"
            show_help
            exit 1
            ;;
    esac
}

# 执行主函数
main "$@" 