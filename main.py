import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import os
import re


class TrainTicketManagementSystem:
    def __init__(self):
        self.user_username = "jzy"
        self.user_password = "1111"

        self.tickets_file = "D:/jiang/train/tickets.txt"
        self.sale_info_file = "D:/jiang/train/SaleInformation.txt"
        self.logged_in_user = None

        os.makedirs(os.path.dirname(self.tickets_file), exist_ok=True)
        os.makedirs(os.path.dirname(self.sale_info_file), exist_ok=True)
        open(self.tickets_file, 'a').close()
        open(self.sale_info_file, 'a').close()

    def start(self):
        self.root = tk.Tk()
        self.root.title("火车票管理系统")
        self.root.geometry("550x500")
        self.login_screen()
        self.root.mainloop()

    def login_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="欢迎使用火车票管理系统！", font=("Arial", 16)).pack(pady=20)
        tk.Label(self.root, text="用户名：", font=("Arial", 12)).pack()
        self.username_entry = tk.Entry(self.root, font=("Arial", 12))
        self.username_entry.pack(pady=5)
        tk.Label(self.root, text="密码：", font=("Arial", 12)).pack()
        self.password_entry = tk.Entry(self.root, show="*", font=("Arial", 12))
        self.password_entry.pack(pady=5)
        tk.Button(self.root, text="登录", command=self.user_login, font=("Arial", 12)).pack(pady=20)

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def user_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username == self.user_username and password == self.user_password:
            messagebox.showinfo("登录成功", "用户登录成功！")
            self.logged_in_user = "user"
            self.user_menu()
        else:
            messagebox.showerror("登录失败", "用户名或密码错误。")

    def user_menu(self):
        self.clear_screen()
        tk.Label(self.root, text="我的", font=("Arial", 16)).pack(pady=20)
        tk.Button(self.root, text="查看可购买票", command=self.view_available_tickets_screen, font=("Arial", 12)).pack(pady=5)
        tk.Button(self.root, text="退票", command=self.cancel_ticket_screen, font=("Arial", 12)).pack(pady=5)
        tk.Button(self.root, text="查看已购票", command=self.view_purchased_tickets, font=("Arial", 12)).pack(pady=5)
        tk.Button(self.root, text="退出登录", command=self.logout, font=("Arial", 12)).pack(pady=20)

    def view_available_tickets_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="查看可购买票", font=("Arial", 16)).pack(pady=20)
        tk.Label(self.root, text="请输入想查看票务的日期（格式：YYYY年MM月DD日）:", font=("Arial", 12)).pack()
        self.date_entry = tk.Entry(self.root, font=("Arial", 12))
        self.date_entry.pack(pady=5)
        tk.Button(self.root, text="查看", command=self.view_available_tickets, font=("Arial", 12)).pack(pady=20)
        tk.Button(self.root, text="返回", command=self.user_menu, font=("Arial", 12)).pack()

    def view_available_tickets(self):
        date_input = self.date_entry.get()
        if not re.match(r"\d{4}年\d{2}月\d{2}日", date_input):
            messagebox.showerror("错误", "日期格式无效。请使用格式：YYYY年MM月DD日")
            return

        try:
            desired_date = datetime.strptime(date_input, "%Y年%m月%d日")
            date_str = desired_date.strftime("%Y年%m月%d日")
            available_tickets = []

            try:
                with open(self.tickets_file, 'r') as file:
                    for line in file:
                        data = line.strip().split(' ')
                        if data[3].strip() == date_str:
                            available_tickets.append(data)
            except IOError:
                messagebox.showerror("错误", "无法读取车票信息文件。")
                return

            self.clear_screen()
            tk.Label(self.root, text=f"{date_str} 的可购买票", font=("Arial", 16)).pack(pady=20)

            text_area = tk.Text(self.root, font=("Arial", 12), width=80, height=10)
            text_area.pack(pady=5)

            if available_tickets:
                for ticket in available_tickets:
                    text_area.insert(tk.END, "\t".join(ticket) + "\n")
                self.create_purchase_widgets()
            else:
                text_area.insert(tk.END, "指定日期没有可用票务。")

            tk.Button(self.root, text="返回", command=self.view_available_tickets_screen, font=("Arial", 12)).pack(pady=20)

        except ValueError:
            messagebox.showerror("错误", "日期格式无效。请使用格式：YYYY年MM月DD日")

    def create_purchase_widgets(self):
        tk.Label(self.root, text="车次：", font=("Arial", 12)).pack()
        self.train_id_entry = tk.Entry(self.root, font=("Arial", 12))
        self.train_id_entry.pack(pady=5)
        tk.Label(self.root, text="乘客信息（姓名,身份证号）：", font=("Arial", 12)).pack()
        self.passenger_info_entry = tk.Entry(self.root, font=("Arial", 12))
        self.passenger_info_entry.pack(pady=5)
        tk.Button(self.root, text="购买", command=self.purchase_ticket, font=("Arial", 12)).pack(pady=20)

    def purchase_ticket(self):
        train_id = self.train_id_entry.get()
        passenger_info = self.passenger_info_entry.get().split(',')
        if len(passenger_info) != 2:
            messagebox.showerror("错误", "请输入正确的乘客信息（姓名,身份证号）。")
            return
        try:
            tickets_data = []
            with open(self.tickets_file, 'r') as f:
                for line in f:
                    ticket_info = line.strip().split(' ')
                    if ticket_info[0] == train_id:
                        available_tickets = int(ticket_info[6])
                        if available_tickets <= 0:
                            messagebox.showerror("错误", "抱歉，该车次没有可用票务。")
                            return
                        ticket_info[6] = str(available_tickets - 1)
                    tickets_data.append(' '.join(ticket_info))
            with open(self.tickets_file, 'w') as f:
                for line in tickets_data:
                    f.write(line + '\n')
            with open(self.sale_info_file, 'a') as f:
                ticket_info = ' '.join([train_id] + passenger_info)
                f.write(ticket_info + '\n')
            messagebox.showinfo("成功", "车票购买成功！")
            self.user_menu()
        except IOError:
            messagebox.showerror("错误", "文件操作出错。")
        except Exception as e:
            messagebox.showerror("错误", f"发生错误: {str(e)}")

    def cancel_ticket_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="取消车票", font=("Arial", 16)).pack(pady=20)
        tk.Label(self.root, text="用户名：", font=("Arial", 12)).pack()
        self.cancel_username_entry = tk.Entry(self.root, font=("Arial", 12))
        self.cancel_username_entry.pack(pady=5)
        tk.Button(self.root, text="取消", command=self.cancel_ticket, font=("Arial", 12)).pack(pady=20)
        tk.Button(self.root, text="返回", command=self.user_menu, font=("Arial", 12)).pack()

    def cancel_ticket(self):
        username = self.cancel_username_entry.get()
        try:
            sale_data = []
            tickets_data = []
            with open(self.sale_info_file, 'r') as f:
                for line in f:
                    info = line.strip().split(' ')
                    if info[1] != username:
                        sale_data.append(line.strip())
            with open(self.sale_info_file, 'w') as f:
                for line in sale_data:
                    f.write(line + '\n')
            with open(self.tickets_file, 'r') as f:
                for line in f:
                    ticket_info = line.strip().split(' ')
                    if ticket_info[1] == username:
                        ticket_info[6] = str(int(ticket_info[6]) + 1)
                    tickets_data.append(' '.join(ticket_info))
            with open(self.tickets_file, 'w') as f:
                for line in tickets_data:
                    f.write(line + '\n')
            messagebox.showinfo("成功", "车票取消成功！")
            self.user_menu()
        except IOError:
            messagebox.showerror("错误", "文件操作出错。")
        except Exception as e:
            messagebox.showerror("错误", f"发生错误: {str(e)}")

    def view_purchased_tickets(self):
        self.clear_screen()
        tk.Label(self.root, text="查看已购票务", font=("Arial", 16)).pack(pady=20)
        text_area = tk.Text(self.root, font=("Arial", 12), width=80, height=20)
        text_area.pack(pady=5)
        try:
            with open(self.sale_info_file, 'r') as f:
                found_tickets = False
                for line in f:
                    info = line.strip().split(' ')
                    text_area.insert(tk.END, f"车次: {info[0]}, 姓名: {info[1]}, 身份证号: {info[2]}\n")
                    found_tickets = True
                if not found_tickets:
                    text_area.insert(tk.END, "未找到已购买的票务信息。")
        except IOError:
            messagebox.showerror("错误", "无法读取用户购票信息文件。")
        tk.Button(self.root, text="返回", command=self.user_menu, font=("Arial", 12)).pack(pady=20)

    def logout(self):
        self.logged_in_user = None
        messagebox.showinfo("注销", "已成功注销。")
        self.login_screen()


# Main Program
if __name__ == "__main__":
    system = TrainTicketManagementSystem()
    system.start()