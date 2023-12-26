# backupscan 备份文件扫描

## 安装依赖

```bash
pip3 install -r requirements.txt
```

## 使用

```bash
python3 back_scan.py -h         
```

```text
    ____             __                  _____                
   / __ )____ ______/ /____  ______     / ___/_________ _____ 
  / __  / __ `/ ___/ //_/ / / / __ \    \__ \/ ___/ __ `/ __ \
 / /_/ / /_/ / /__/ ,< / /_/ / /_/ /   ___/ / /__/ /_/ / / / /
/_____/\__,_/\___/_/|_|\__,_/ .___/   /____/\___/\__,_/_/ /_/ 
                           /_/                                
                     __                   __    _       __              
                    / /_  __  __   ____  / /_  (_)___  / /_  __  ______ 
                   / __ \/ / / /  /_  / / __ \/ /_  / / __ \/ / / / __ \
                  / /_/ / /_/ /    / /_/ / / / / / /_/ / / / /_/ / /_/ /
                 /_.___/\__, /    /___/_/ /_/_/ /___/_/ /_/\__,_/\____/ 
                       /____/                                           

usage: back_scan.py [-h] [-u URL] [-f [URL_FILE]] [-t THREADS] [-o [OUTPUT]]
                    [-tm [TIMEOUT]] [-d [DEBUG]]

Backup Scan by zhizhuo

optional arguments:
  -h, --help            show this help message and exit
  -u URL, -url URL      单个url检测，输入样例http://www.baidu.com
  -f [URL_FILE], -file [URL_FILE]
                        多个url检测，以txt文件形式存储,文件中的url格式为http://www.baidu.com或者www
                        .baidu.com
  -t THREADS, -T THREADS
                        线程数量，默认是50线程
  -o [OUTPUT], -output [OUTPUT]
                        结果输出文件
  -tm [TIMEOUT], -timeout [TIMEOUT]
                        结果输出文件
  -d [DEBUG], -debug [DEBUG]
                        开启debug模式

```

## 结束

如果遇到问题请提交issue，会及时修复。