import sys
import os

print(f"Python 路径: {sys.executable}")
print(f"Python 版本: {sys.version}")

try:
    import pyautogui
    print("PyAutoGUI 已安装")
except ImportError:
    print("PyAutoGUI 未安装")

try:
    from PIL import Image, ImageTk
    print("Pillow 已安装")
except ImportError:
    print("Pillow 未安装")

import tkinter as tk
from tkinter import messagebox, filedialog
import time
from datetime import datetime

class ScreenshotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("定时截屏")
        self.root.geometry("400x300")
        
        # 设置窗口图标
        try:
            icon_path = "nikki.ico"  # 使用之前生成的图标文件
            self.root.iconbitmap(icon_path)
        except:
            print("图标加载失败")
        
        # 创建主框架
        main_frame = tk.Frame(root, padx=20, pady=20)
        main_frame.pack(expand=True, fill='both')
        
        # 间隔时间输入
        interval_frame = tk.Frame(main_frame)
        interval_frame.pack(fill='x', pady=5)
        tk.Label(interval_frame, text="截屏间隔时间（秒）:").pack(side='left')
        self.interval_entry = tk.Entry(interval_frame)
        self.interval_entry.insert(0, "0.5")  # 默认值为0.5秒
        self.interval_entry.pack(side='left', padx=5)
        
        # 截图数量输入
        count_frame = tk.Frame(main_frame)
        count_frame.pack(fill='x', pady=5)
        tk.Label(count_frame, text="截图数量:").pack(side='left')
        self.count_entry = tk.Entry(count_frame)
        self.count_entry.insert(0, "20")  # 默认20张
        self.count_entry.pack(side='left', padx=5)
        
        # 保存路径选择
        path_frame = tk.Frame(main_frame)
        path_frame.pack(fill='x', pady=5)
        self.save_path = os.path.join(os.path.expanduser("~"), "Desktop")
        self.path_label = tk.Label(path_frame, text=f"保存路径: {self.save_path}")
        self.path_label.pack(side='left')
        tk.Button(path_frame, text="选择路径", command=self.choose_path).pack(side='right')
        
        # 开始按钮
        tk.Button(main_frame, text="开始截屏", command=self.on_start, 
                 bg='#4CAF50', fg='white', pady=10).pack(pady=20)

    def choose_path(self):
        path = filedialog.askdirectory(initialdir=self.save_path)
        if path:
            self.save_path = path
            self.path_label.config(text=f"保存路径: {self.save_path}")

    def validate_inputs(self):
        try:
            interval = float(self.interval_entry.get())
            count = int(self.count_entry.get())
            if interval <= 0:
                raise ValueError("间隔时间必须大于0")
            if count <= 0:
                raise ValueError("截图数量必须大于0")
            if interval < 0.3:  # 添加最小间隔限制
                raise ValueError("为了保证稳定性，间隔时间不能小于0.3秒")
            return True
        except ValueError as e:
            messagebox.showerror("输入错误", str(e))
            return False

    def start_screenshot(self, interval, count):
        try:
            time.sleep(0.5)  # 等待0.5秒让窗口完全关闭
            
            current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
            os.makedirs(self.save_path, exist_ok=True)
            
            for i in range(count):
                screenshot = pyautogui.screenshot()
                filename = f'screenshot_{current_time}_{i+1:03d}.png'
                screenshot.save(os.path.join(self.save_path, filename))
                time.sleep(interval)
            
            # 创建更大的结果窗口
            result_window = tk.Tk()
            result_window.title("定时截屏")
            result_window.geometry("500x300")  # 增大窗口尺寸
            
            # 设置结果窗口图标
            try:
                icon_path = "nikki.ico"
                result_window.iconbitmap(icon_path)
            except:
                print("结果窗口图标加载失败")
            
            # 使用Frame来组织内容
            frame = tk.Frame(result_window, padx=20, pady=20)
            frame.pack(expand=True, fill='both')
            
            # 添加完成信息，使用更大的字体
            info_text = f"截屏已成功完成！\n\n" \
                       f"截图信息:\n" \
                       f"- 总张数: {count} 张\n" \
                       f"- 间隔时间: {interval} 秒\n" \
                       f"- 总用时: {interval * (count-1):.1f} 秒\n\n" \
                       f"保存位置:\n{self.save_path}"
            
            tk.Label(frame, 
                    text=info_text,
                    wraplength=460,
                    justify='left',
                    font=('Arial', 12)).pack(padx=10, pady=10)
            
            # 添加确认按钮
            tk.Button(frame, 
                     text="确定",
                     font=('Arial', 11),
                     command=result_window.destroy,
                     width=20).pack(pady=20)
            
            result_window.mainloop()
            
        except Exception as e:
            # 创建错误窗口
            error_window = tk.Tk()
            error_window.title("错误")
            error_window.geometry("400x200")
            
            # 设置错误窗口图标
            try:
                icon_path = "nikki.ico"
                error_window.iconbitmap(icon_path)
            except:
                print("错误窗口图标加载失败")
            
            tk.Label(error_window, 
                    text=f"发生错误:\n{str(e)}",
                    wraplength=360,
                    font=('Arial', 11)).pack(padx=20, pady=20)
            
            tk.Button(error_window, 
                     text="确定",
                     font=('Arial', 11),
                     command=error_window.destroy).pack(pady=10)
            
            error_window.mainloop()

    def on_start(self):
        if not self.validate_inputs():
            return
            
        interval = float(self.interval_entry.get())
        count = int(self.count_entry.get())
        
        if messagebox.askyesno("确认", f"即将开始截屏:\n间隔时间: {interval}秒\n截图数量: {count}张\n是否继续?"):
            self.root.destroy()
            self.start_screenshot(interval, count)

if __name__ == "__main__":
    root = tk.Tk()
    app = ScreenshotApp(root)
    root.mainloop()