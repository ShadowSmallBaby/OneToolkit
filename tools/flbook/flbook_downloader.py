#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
flbook.com.cn PDF下载脚本
作者: Smallbaby
功能: 根据编码下载flbook的PDF文件并自动提取密码
"""

import requests
import re
import json
import base64
from urllib.parse import unquote
from pathlib import Path
from PyPDF2 import PdfReader, PdfWriter


class FlbookDownloader:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })

    def get_op_data(self, code_or_url):
        """
        获取$OP数据
        """
        if code_or_url.startswith('http://') or code_or_url.startswith('https://'):
            url = code_or_url
        else:
            url = f"https://flbook.com.cn/c/{code_or_url}"

        print(f"正在请求: {url}")

        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()

            pattern = r'\$OP\s*=\s*\$\.extend\(JSON\.parse\(\'(.*?)\'\),\s*JSON\.parse\(\'(.*?)\'\)\)'
            match = re.search(pattern, response.text, re.DOTALL)

            if not match:
                pattern2 = r'\$OP\s*=\s*\$\.extend\(JSON\.parse\(\'(.*?)\'\)'
                match = re.search(pattern2, response.text, re.DOTALL)

                if not match:
                    print("未找到$OP数据，请检查页面结构")
                    return None

            try:
                op_data = json.loads(match.group(1))
                print("成功解析$OP数据")
                return op_data
            except json.JSONDecodeError as e:
                print(f"JSON解析错误: {e}")
                return None

        except requests.RequestException as e:
            print(f"请求错误: {e}")
            return None

    def get_filename(self, op_data):
        """
        获取文件名
        """
        filename = op_data.get('introduce') or op_data.get('journal')

        if filename:
            filename = unquote(filename)
            filename = re.sub(r'[\\/*?:"<>|]', '', filename)
            return filename

        return "unknown"

    def get_pdf_url(self, op_data):
        """
        获取PDF文件地址
        """
        pdf_url = op_data.get('pdfcreateurl')

        if pdf_url:
            pdf_url = unquote(pdf_url)
            if not pdf_url.startswith('http'):
                pdf_url = f"https://img2.flbook.com.cn/{pdf_url}"

        return pdf_url

    def get_password(self, userid):
        """
        生成密码
        """
        try:
            userid_str = str(userid)
            password = base64.b64encode(userid_str.encode('utf-8')).decode('utf-8')
            return password
        except Exception as e:
            print(f"密码生成错误: {e}")
            return None

    def get_file_extension(self, url):
        """
        从URL中提取文件扩展名
        """
        filename = url.split('/')[-1].split('?')[0]

        if '.' in filename:
            ext = filename.split('.')[-1].lower()
            return f".{ext}"

        return ".pdf"

    def decrypt_pdf(self, input_path, output_path, password):
        """
        使用PyPDF2解密PDF文件
        """
        print(f"正在检查PDF加密状态: {input_path}")

        try:
            # 读取PDF检查加密状态
            reader = PdfReader(str(input_path))

            # 检查是否已加密
            if not reader.is_encrypted:
                print("⚠ PDF未加密，无需解密")
                return False

            decrypt_result = reader.decrypt(password)

            if decrypt_result == 1:
                print("✓ PDF已加密，正在解密...")
                writer = PdfWriter()
                for page in reader.pages:
                    writer.add_page(page)

                with open(output_path, 'wb') as output_file:
                    writer.write(output_file)

                print(f"✓ 解密成功: {output_path.name}")
                return True
            else:
                print("✗ 密码错误，解密失败")
                return False

        except Exception as e:
            print(f"✗ 解密错误: {e}")
            return False

    def download_file(self, url, filename, password):
        """
        下载文件，并为PDF生成解密版本
        """
        if not url:
            print("PDF地址为空，无法下载")
            return False

        ext = self.get_file_extension(url)
        full_filename = f"{filename}{ext}"
        download_dir = Path(r".\\flbook_downloads")
        download_dir.mkdir(exist_ok=True)
        save_path = download_dir / full_filename

        print(f"开始下载: {url}")
        print(f"保存路径: {save_path}")
        print(f"文件密码: {password}")

        try:
            response = self.session.get(url, stream=True, timeout=60)
            response.raise_for_status()
            total_size = int(response.headers.get('content-length', 0))

            # 下载文件
            with open(save_path, 'wb') as f:
                downloaded = 0
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)

                        if total_size > 0:
                            percent = (downloaded / total_size) * 100
                            print(f"\r下载进度: {percent:.1f}% ({downloaded}/{total_size} bytes)", end='')

            print(f"\n下载完成: {full_filename}")

            # 如果是PDF文件，尝试生成解密版本
            if ext.lower() == '.pdf':
                print("\n正在处理PDF解密...")
                decrypted_filename = f"{filename}_解密版.pdf"
                decrypted_path = download_dir / decrypted_filename

                if self.decrypt_pdf(save_path, decrypted_path, password):
                    print(f"✓ 解密版本已保存: {decrypted_filename}")
                else:
                    print("⚠ PDF未加密或解密失败，无需生成未加密版本")

            # 保存密码到文本文件（仅当PDF被解密时）
            password_file = download_dir / f"{filename}_密码.txt"
            with open(password_file, 'w', encoding='utf-8') as f:
                f.write(f"文件名: {full_filename}\n")
                if ext.lower() == '.pdf':
                    f.write(f"密码: {password}\n")

            print(f"密码已保存到: {password_file}")
            return True

        except Exception as e:
            print(f"\n下载失败: {e}")
            return False

    def process(self, code_or_url):
        """
        主处理流程
        """
        display_id = code_or_url
        if code_or_url.startswith('http'):
            display_id = code_or_url.split('/')[-1].split('?')[0]

        print(f"\n{'='*50}")
        print(f"flbook下载器 - 输入: {display_id}")
        print(f"{'='*50}\n")

        # 1. 获取数据
        op_data = self.get_op_data(code_or_url)
        if not op_data:
            return False

        # 2. 提取信息
        filename = self.get_filename(op_data)
        pdf_url = self.get_pdf_url(op_data)
        userid = op_data.get('userid')

        if not userid:
            print("未找到userid，无法生成密码")
            return False

        password = self.get_password(userid)

        # 3. 显示信息
        print(f"文件名: {filename}")
        print(f"PDF地址: {pdf_url}")
        print(f"用户ID: {userid}")
        print(f"密码: {password}")

        # 4. 下载文件
        if pdf_url:
            return self.download_file(pdf_url, filename, password)
        else:
            print("未找到PDF地址")
            return False


def main():
    """主函数"""
    downloader = FlbookDownloader()

    while True:
        print("\n" + "="*50)
        print("flbook.com.cn PDF下载工具")
        print("="*50)
        print("支持输入:")
        print("  - 编码: code")
        print("  - 完整URL: https://flbook.com.cn/c/code")
        print("输入 'q' 退出")
        print("-"*50)

        input_str = input("请输入编码或URL: ").strip()

        if input_str.lower() == 'q':
            print("退出程序")
            break

        if not input_str:
            print("输入不能为空")
            continue

        downloader.process(input_str)

        print("\n" + "="*50)
        input("按回车键继续...")


if __name__ == "__main__":
    main()