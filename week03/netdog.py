import os
import re
import json
# import queue
import socket
import logging
# import requests
import argparse
import threading
import subprocess
import multiprocessing
from multiprocessing import cpu_count
# ip address
# port range option
# osi layer three sniffing or osi layer four sniffing main
# use multiprocess or threading main
# current process or thread count
# result stdout & persist local json file
# script excute time option main

logger = logging.getLogger("netdog")
logger.setLevel(logging.INFO)
from logging.handlers import RotatingFileHandler
log_path = f"{os.path.expanduser('~')}/netdog.log"
handler = RotatingFileHandler(log_path, maxBytes=102400, backupCount=5)
handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s [(module)s] - %(levelname)s %(funcName)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


class NetDog:
    # 不考虑掩码类地址段表达形式, 按照题目要求，掩码为24位(偷懒...)，用正则捕获网络位和主机位地址段
    ip_address_compile = re.compile(r'((?:\d+\.){3})(\d+)(?:-(?:\d+\.){3}(\d+))?')
    def __init__(self, ip_addr: str,p_count: int, port="1-1024"):
        self.p_count = p_count
        self.port = port
        self.address_field = False
        # 判断地址格式
        match_result = self.ip_address_compile.fullmatch(ip_addr)
        if not match_result:
            raise Exception("地址格式错误")
        # 捕获网络位、主机位
        self.capture_elem = match_result.groups()
        if all(self.capture_elem):
            self.address_field = True

    def ip_handler(self):
        network_field, start, end = self.capture_elem
        if self.address_field:
            ip = (f"{network_field}{i}" for i in range(int(start), int(end)+1))
        else:
            ip = f"{network_field}{start}"
        return ip

    def address_handler(self, ip):
        start, end = self.port.split("-")
        return ((ip, i) for i in range(int(start), int(end)+1))

    def osi_layer_three(self, ip: str) -> str:
        # ping命令支持wait超时选项，这里用subprocess.run的参数设置超时，捕获异常
        cmd = "ping {} -c 1"
        try:
            output = subprocess.run(cmd.format(ip), shell=True, capture_output=True, timeout=3)
            if output.returncode == 0:
                print(f"侦测到地址{ip}")
                return ip
        except subprocess.TimeoutExpired:
            pass
        except:
            logger.error(f"ERROR 侦测地址{ip}连通性发生异常", exc_info=True)

    def osi_layer_four(self, address) -> int:
        try:
            with socket.socket() as tcp:
                stauts_code = tcp.connect_ex(address)
            if stauts_code == 0:
                print(f"{address[0]} TCP端口:{address[1]} 对外开放")
                return address
        except:
            logging.error(f"ERROR 侦测地址{address}发生异常", exc_info=True)

    def use_thread(self, func, *args) -> 'map object':
        from concurrent.futures import ThreadPoolExecutor
        with ThreadPoolExecutor(self.p_count) as executor:
            r = executor.map(func, *args)
        return r

    def use_process(self, func, *args) -> 'map object':
        from concurrent.futures import ProcessPoolExecutor
        with ProcessPoolExecutor(self.p_count) as executor:
            r = executor.map(func, *args)
        return r

    def local_persistance(self, name: str, gen: 'generator', data_type: str=None, path=os.path.expanduser("~")):
        data = {}
        try:
            if data_type == "ping":
                data["Activities_ip"] = list(filter(None, gen))
            if data_type == "tcp":
                from collections import defaultdict
                address = defaultdict(list)
                for k,v in filter(None, gen):
                    address[k].append(v)
                data["Activities_address"] = address
            serialize = json.dumps(data)
            abs_path = f"{path}/{name}"
            with open(abs_path, "w", encoding="utf-8") as f:
                f.write(serialize)
            return abs_path
        except:
            logger.error("数据持久化至本地发生异常", exc_info=True)
            return False

if __name__ == "__main__":
    net_dog_parser = argparse.ArgumentParser(description='简易网络嗅探工具, v0.0.1')
    net_dog_parser.add_argument("-n", dest="concurrent", type=int, default=cpu_count(), help="指定并发任务数量，默认与cpu内核数量一致")
    net_dog_parser.add_argument("-f", dest="sniffing_type", choices=["ping", "tcp"], required=True,
                                help="指定探测类型，支持传入ping或tcp。若传入tcp则通过选项-ip需传入单一的ip地址。")
    net_dog_parser.add_argument("-ip", dest="ip", type=str, required=True,
                                help="需要进行探测的单一地址或地址段，地址段表示方式为: 192.168.1.1-192.168.1.100")
    net_dog_parser.add_argument("-w", dest="persistance", default=None, help="数据持久化至本地后的文件名称，路径为执行文件用户家目录")
    net_dog_parser.add_argument("-m", dest="model_type", choices=["proc", "thread"], default="thread",
                                help="指定使用多进程或多线程模型加速扫描，支持proc和thread。默认为thread")
    net_dog_parser.add_argument("-v", dest="performance", action="store_true", help="启用性能测试，会打印命令执行耗时，一般为调试命令时使用")
    args = net_dog_parser.parse_args()

    concurrent = args.concurrent
    sniffing_type = args.sniffing_type
    ip = args.ip
    persistance = args.persistance
    model_type = args.model_type
    performance = args.performance

    from time import time
    start_time = time()

    result = None
    net_dog = NetDog(ip, concurrent)
    method = {
        "proc": ["多进程", net_dog.use_process],
        "thread": ["多线程", net_dog.use_thread],
    }
    info, model = method[model_type]
    print(f"*** 开始进行嗅探工作(模型: {info}, 并发任务数量: {concurrent}) ***")
    ip = net_dog.ip_handler()
    if sniffing_type == "tcp":
        address = net_dog.address_handler(ip
        result = model(net_dog.osi_layer_four, address)
    if sniffing_type == "ping":
        result = model(net_dog.osi_layer_three, ip)
    print("*** 嗅探结束 ***")
    if performance:
        print(f"*** 执行时间: {time() - start_time:.2f} ***")
    if persistance and result:
        write_result = net_dog.local_persistance(persistance, result, data_type=sniffing_type,)
        if not write_result:
            print(f"*** 数据持久化本地发生异常，请查看错误日志，日志路径: {log_path} ***")
        else:
            print(f"*** 数据持久化至本地路径: {write_result} ***")

