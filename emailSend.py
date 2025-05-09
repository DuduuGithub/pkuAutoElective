import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# 发送者信息（QQ邮箱和授权码）
sender_email = "2043028591@qq.com"  # 替换为你的 QQ 邮箱
password = "onnifwghoslpbeej"  # QQ 邮箱授权码

# 接收者邮箱
receiver_email = "2300016603@stu.pku.edu.cn"  # 替换为收件人的邮箱

# 邮件服务器配置
smtp_server = "smtp.qq.com"
smtp_port = 465  # QQ邮箱使用 SSL 端口 465


def send_email(subject,body):
    # 创建邮件对象
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))  # 纯文本邮件

    # 创建SMTP对象
    server = None
    try:
        # 连接到 SMTP 服务器
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)  # 使用 SSL 加密连接
        # 登录
        server.login(sender_email, password)
        # 发送邮件
        server.send_message(msg)
        print("邮件发送成功！")
    except Exception as e:
        print(f"邮件发送失败: {e}")
    finally:
        # 安全关闭连接
        if server is not None:
            try:
                server.quit()
            except:
                pass

if __name__ == "__main__":
    send_email("test","test")