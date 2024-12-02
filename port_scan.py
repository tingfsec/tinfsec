import socket
import threading

# 创建锁
lock = threading.Lock()


def print_colored_text():
    green = "\033[32m"
    reset = "\033[0m"

    a = f"""{green} _____   _   __   _   _____   _____   __   _   _____   _____   _____   _____  
|_   _| | | |  \ | | |  ___| | ____| |  \ | | /  ___| /  ___/ | ____| /  ___| 
  | |   | | |   \| | | |__   | |__   |   \| | | |     | |___  | |__   | |     
  | |   | | | |\   | |  __|  |  __|  | |\   | | |  _  \___  \ |  __|  | |     
  | |   | | | | \  | | |     | |___  | | \  | | |_| |  ___| | | |___  | |___  
  |_|   |_| |_|  \_| |_|     |_____| |_|  \_| \_____/ /_____/ |_____| \_____|   Author:TingFengSec Github:https://github.com/tingfsec/tinfsec{reset}
"""
    print(a)



def port_scan(ip, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        s.connect((ip, port))
        # 使用锁来确保每次只有一个线程能打印信息
        with lock:
            print('[+]:{}端口是开放的'.format(port))
        s.close()  # 关闭socket连接
    except Exception as e:
        pass  # 如果端口不可达或者超时，忽略异常


def scan_ports(ip, port_range, thread_count):
    try:
        # 解析端口范围
        if '-' in port_range:
            start, end = map(int, port_range.split('-'))
        elif ':' in port_range:
            start, end = map(int, port_range.split(':'))
        else:
            print("您输入的格式不正确,正确格式为起始端口-结束端口,或起始端口:结束端口")
            return

        if start > end:
            raise ValueError("起始端口不能大于结束端口")  # 抛出异常

        # 创建线程池
        threads = []
        for port in range(start, end + 1):  # 遍历端口范围
            t = threading.Thread(target=port_scan, args=(ip, port))  # 创建线程
            threads.append(t)

        # 限制线程数量，确保不超过用户输入的数量
        max_threads = int(thread_count)
        for i in range(0, len(threads), max_threads):
            for t in threads[i:i + max_threads]:
                t.start()  # 启动线程
            for t in threads[i:i + max_threads]:
                t.join()  # 等待所有线程结束

    except ValueError as e:
        print(e)
    except Exception as e:
        print(f"发生了错误: {e}")


if __name__ == '__main__':
    print_colored_text()
    ip = input("请输入要扫描的IP地址: ")
    port_range = input("请输入要扫描的端口范围(格式:起始端口-结束端口,或起始端口:结束端口): ")
    thread_count = input("请输入要使用的线程数: 1-100: ")

    # 检查线程数是否合法
    if not thread_count.isdigit() or not (1 <= int(thread_count) <= 100):
        print("请输入一个合法的线程数（1-100）")
    else:
        scan_ports(ip, port_range, thread_count)
        print("端口扫描完成。")
