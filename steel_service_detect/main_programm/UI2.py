import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, Toplevel, scrolledtext
from tkinter import ttk
import cv2
import os
import requests
from datetime import datetime

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("车辆零部件表面缺陷检测系统")
        self.geometry("1200x900")
        self.current_user = None
        self.configure_style()
        self.create_widgets()
        self.images = []

    def configure_style(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TButton', font=('微软雅黑', 12), padding=8)
        self.style.configure('TLabel', background='#f0f0f0', font=('微软雅黑', 12))
        self.style.map('TButton',
            foreground=[('active', '!disabled', 'white'), ('pressed', 'white')],
            background=[('active', '#0052cc'), ('pressed', '#0052cc')])

    def create_widgets(self):
        # 主界面
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        title_label = ttk.Label(self.main_frame, 
                              text="车辆零部件表面缺陷检测系统",
                              font=('微软雅黑', 20, 'bold'),
                              foreground='#1a237e')
        title_label.pack(pady=30)

        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(pady=20)

        buttons = [
            ("导入图像", self.import_image),
            ("拍摄图像", self.capture_image),
            ("图像管理", self.manage_images),
            ("用户登录", self.user_login),
            ("生成报告", self.report_generation)
        ]

        for text, command in buttons:
            btn = ttk.Button(button_frame, text=text, command=command)
            btn.pack(side=tk.LEFT, padx=15, pady=10)

        # 图像列表区域
        self.list_frame = ttk.Frame(self.main_frame)
        self.list_frame.pack(fill=tk.BOTH, expand=True)

        self.image_listbox = tk.Listbox(self.list_frame, 
                                     width=100, 
                                     height=20,
                                     font=('微软雅黑', 11),
                                     selectbackground='#e3f2fd')
        self.image_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(self.list_frame, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.image_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.image_listbox.yview)

    def import_image(self):
        file_types = [("图像文件", "*.jpg *.jpeg *.png *.bmp")]
        file_path = filedialog.askopenfilename(filetypes=file_types)
        if file_path:
            self.images.append(file_path)
            self.image_listbox.insert(tk.END, os.path.basename(file_path))
            messagebox.showinfo("导入成功", f"已成功导入: {os.path.basename(file_path)}")
            self.upload_image_to_api(file_path)
            
    def capture_image(self):
        if not self.current_user:
            messagebox.showwarning("权限不足", "请先登录系统")
            return

        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        if ret:
            filename = f"captured_{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg"
            cv2.imwrite(filename, frame)
            self.images.append(filename)
            self.image_listbox.insert(tk.END, filename)
            messagebox.showinfo("拍摄成功", "图像拍摄并保存成功")
        else:
            messagebox.showerror("错误", "摄像头访问失败")
        cap.release()

    def manage_images(self):
        if not self.current_user:
            messagebox.showwarning("权限不足", "请先登录系统")
            return

        manage_win = Toplevel(self)
        manage_win.title("图像管理")
        manage_win.geometry("800x600")

        list_frame = ttk.Frame(manage_win)
        list_frame.pack(pady=20, fill=tk.BOTH, expand=True)

        manage_listbox = tk.Listbox(list_frame,
                                  width=80,
                                  height=20,
                                  font=('微软雅黑', 11))
        manage_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        for img in self.images:
            manage_listbox.insert(tk.END, os.path.basename(img))

        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        manage_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=manage_listbox.yview)

        btn_frame = ttk.Frame(manage_win)
        btn_frame.pack(pady=15)

        ttk.Button(btn_frame, 
                 text="删除选中", 
                 command=lambda: self.delete_image(manage_listbox)).pack(side=tk.LEFT, padx=10)

        ttk.Button(btn_frame, 
                 text="检测选中", 
                 command=lambda: self.detect_selected_image(manage_listbox)).pack(side=tk.LEFT, padx=10)

    def delete_image(self, listbox):
        selected = listbox.curselection()
        if selected:
            index = selected[0]
            try:
                os.remove(self.images[index])
                del self.images[index]
                listbox.delete(index)
                self.image_listbox.delete(index)
                messagebox.showinfo("删除成功", "图像已成功删除")
            except Exception as e:
                messagebox.showerror("删除失败", f"错误信息: {str(e)}")
        else:
            messagebox.showwarning("操作提示", "请先选择要删除的图像")

    def detect_selected_image(self, listbox):
        selected = listbox.curselection()
        if selected:
            index = selected[0]
            file_id = os.path.basename(self.images[index])
            self.detect_image_from_api(file_id)
        else:
            messagebox.showwarning("操作提示", "请先选择要检测的图像")

    def import_image(self):
        file_types = [("图像文件", "*.jpg *.jpeg *.png *.bmp")]
        file_path = filedialog.askopenfilename(filetypes=file_types)
        if file_path:
            self.images.append(file_path)
            self.image_listbox.insert(tk.END, os.path.basename(file_path))
            messagebox.showinfo("导入成功", f"已成功导入: {os.path.basename(file_path)}")
            self.upload_image_to_api(file_path)

    def detect_image_from_api(self, file_id):
        url = f"http://localhost:8000/api/detect"
        params = {'file_id': file_id}
        response = requests.post(url, params=params)
        if response.status_code == 200:
            defects = response.json().get('defects', [])
            messagebox.showinfo("检测成功", f"检测结果: {defects}")
        else:
            messagebox.showerror("检测失败", f"检测失败: {response.text}")

    def user_login(self):
        login_win = Toplevel(self)
        login_win.title("用户登录")
        login_win.geometry("400x300")

        form_frame = ttk.Frame(login_win)
        form_frame.pack(pady=40)

        # 用户名输入
        ttk.Label(form_frame, text="用户名:").grid(row=0, column=0, padx=10, pady=15)
        username_entry = ttk.Entry(form_frame, width=20)
        username_entry.grid(row=0, column=1, padx=10, pady=15)

        # 密码输入
        ttk.Label(form_frame, text="密码:").grid(row=1, column=0, padx=10, pady=15)
        password_entry = ttk.Entry(form_frame, width=20, show="*")
        password_entry.grid(row=1, column=1, padx=10, pady=15)

        # 登录按钮
        btn_frame = ttk.Frame(login_win)
        btn_frame.pack(pady=20)

        def attempt_login():
            # 模拟用户验证（实际应连接数据库）
            username = username_entry.get()
            password = password_entry.get()
            
            if username == "admin" and password == "admin123":
                self.current_user = username
                messagebox.showinfo("登录成功", f"欢迎回来，{username}！")
                login_win.destroy()
            else:
                messagebox.showerror("登录失败", "用户名或密码错误")

        ttk.Button(btn_frame, text="登录", command=attempt_login).pack(side=tk.LEFT, padx=15)

    def report_generation(self):
        if not self.images:
            messagebox.showwarning("报告生成", "没有可用的检测图像")
            return

        report_win = Toplevel(self)
        report_win.title("检测报告")
        report_win.geometry("1200x900")

        # 报告编辑器
        editor_frame = ttk.Frame(report_win)
        editor_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        self.text_area = scrolledtext.ScrolledText(editor_frame,
                                                wrap=tk.WORD,
                                                font=('宋体', 12),
                                                width=100,
                                                height=30)
        self.text_area.pack(fill=tk.BOTH, expand=True)

        # 初始化报告内容
        self._generate_report_content()

        # 操作按钮
        btn_frame = ttk.Frame(report_win)
        btn_frame.pack(pady=15)

        ttk.Button(btn_frame, 
                 text="导出报告", 
                 command=self.export_report).pack(side=tk.LEFT, padx=15)
        
        ttk.Button(btn_frame,
                 text="插入检测结果",
                 command=self.insert_detection_results).pack(side=tk.LEFT, padx=15)

    def _generate_report_content(self):
        """生成报告基础内容"""
        self.text_area.config(state=tk.NORMAL)
        self.text_area.delete(1.0, tk.END)

        # 报告头
        header = f"""
{'='*60}
车辆零部件表面缺陷检测报告
{'='*60}

检测时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
操作人员：{self.current_user or '未登录用户'}
检测图像数量：{len(self.images)}
{'='*60}

检测图像列表：
"""
        self.text_area.insert(tk.END, header)

        # 图像列表
        for idx, path in enumerate(self.images, 1):
            self.text_area.insert(tk.END, f"{idx}. {os.path.basename(path)}\n")

        # 报告尾
        footer = f"""
{'='*60}
备注：
1. 本报告由智能检测系统自动生成
2. 检测结果需结合原始图像分析
3. 最终解释权归检测单位所有
{'='*60}
"""
        self.text_area.insert(tk.END, footer)
        self.text_area.config(state=tk.DISABLED)

    def insert_detection_results(self):
        """插入模拟检测结果"""
        # 实际应集成检测算法，此处为模拟数据
        defects = {
            "划痕缺陷": len(self.images)*0.3,
            "表面变形": len(self.images)*0.1,
            "锈蚀缺陷": len(self.images)*0.2,
            "装配缺陷": len(self.images)*0.05
        }

        analysis = "\n缺陷分析结果：\n"
        for defect, count in defects.items():
            analysis += f"- {defect}: {int(count)}处\n"

        self.text_area.config(state=tk.NORMAL)
        self.text_area.insert(tk.END, analysis)
        self.text_area.see(tk.END)
        self.text_area.config(state=tk.DISABLED)

    def export_report(self):
        """导出报告文件"""
        file_types = [
            ('Word 文档', '*.docx'),
            ('文本文件', '*.txt'),
            ('所有文件', '*.*')
        ]

        file_path = filedialog.filedialog.askopenfilename(
            title="保存报告",
            defaultextension=".docx",
            filetypes=file_types)

        if file_path:
            try:
                content = self.text_area.get(1.0, tk.END)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                messagebox.showinfo("导出成功", f"报告已保存到：\n{file_path}")
            except Exception as e:
                messagebox.showerror("导出失败", f"错误信息：\n{str(e)}")

if __name__ == "__main__":
    app = Application()
    app.mainloop()
