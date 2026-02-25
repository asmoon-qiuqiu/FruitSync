"""
邮件发送服务工具类
功能：封装SMTP邮件发送逻辑，支持发送验证码邮件
依赖：smtplib（Python内置SMTP客户端）、email（邮件内容构建）
适用场景：密码重置验证码、注册验证码、系统通知等邮件发送场景
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import settings  # 导入项目配置（SMTP服务器信息、发件人邮箱等）
import logging

# 初始化日志器（logger名称为当前模块名，便于日志溯源）
logger = logging.getLogger(__name__)


class EmailService:
    """邮件发送服务类"""

    def __init__(self):
        """初始化SMTP服务器连接参数"""
        self.smtp_host = settings.SMTP_HOST
        self.smtp_port = settings.SMTP_PORT
        self.smtp_user = settings.SMTP_USER
        self.smtp_password = settings.SMTP_PASSWORD
        self.email_from = settings.EMAIL_FROM or settings.SMTP_USER

        def send_verification_code(self, to_email: str, code: str) -> bool:
            """
            发送验证码邮件
            :param to_email: 收件人邮箱
            :param code: 6位验证码
            :return: 发送成功返回True，失败返回False
            """
            try:
                # 构建邮件内容
                subject = "密码重置验证码"
                html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                    .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                              color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                    .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
                    .code-box {{ background: white; padding: 20px; text-align: center; 
                                 margin: 20px 0; border-radius: 5px; border: 2px dashed #667eea; }}
                    .code {{ font-size: 32px; font-weight: bold; color: #667eea; 
                            letter-spacing: 5px; font-family: monospace; }}
                    .footer {{ text-align: center; margin-top: 20px; color: #999; font-size: 12px; }}
                    .warning {{ color: #e74c3c; margin-top: 15px; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>水果商城</h1>
                        <p>密码重置验证</p>
                    </div>
                    <div class="content">
                        <p>尊敬的用户，您好！</p>
                        <p>您正在进行<strong>密码重置</strong>操作，请使用以下验证码完成验证：</p>
                        
                        <div class="code-box">
                            <div class="code">{code}</div>
                            <p style="margin: 10px 0 0 0; color: #666;">验证码有效期：5分钟</p>
                        </div>
                        
                        <p class="warning">
                            ⚠️ 如果这不是您本人的操作，请忽略此邮件并立即修改密码。
                        </p>
                        
                        <p style="margin-top: 30px; color: #666;">
                            此邮件为系统自动发送，请勿直接回复。
                        </p>
                    </div>
                    <div class="footer">
                        <p>© 2025 水果商城 | 用心服务每一位顾客</p>
                    </div>
                </div>
            </body>
            </html>
            """

                # 构建邮件对象
                message = MIMEMultipart("alternative")
                message["Subject"] = subject
                message["From"] = self.email_from
                message["To"] = to_email

                # 将HTML内容添加到邮件对象中
                html_part = MIMEText(html_content, "html", "utf-8")
                message.attach(html_part)

                # 连接SMTP服务器并发送邮件
                with smtplib.SMTP(self.smtp_host, self.smtp_port, timeout=30) as server:
                    server.starttls()  # 启用TLS加密
                    server.login(self.smtp_user, self.smtp_password)  # 登录SMTP服务器
                    server.send_message(message)  # 发送邮件

                logger.info(f"验证码邮件发送成功：{to_email}")
                return True

            except Exception as e:
                logger.error(
                    f"验证码邮件发送失败：{to_email}，错误：{str(e)}", exc_info=True
                )
                return False

    def send_password_reset_success(self, to_email: str, username: str) -> bool:
        """
        发送密码重置成功通知邮件
        :param to_email: 收件人邮箱
        :param username: 用户名
        :return: 发送成功返回True，失败返回False
        """
        try:
            subject = "密码修改成功通知"
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                    .header {{ background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); 
                              color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                    .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
                    .success-icon {{ font-size: 48px; text-align: center; margin: 20px 0; }}
                    .footer {{ text-align: center; margin-top: 20px; color: #999; font-size: 12px; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>水果商城</h1>
                        <p>密码修改通知</p>
                    </div>
                    <div class="content">
                        <div class="success-icon">✅</div>
                        <p>尊敬的 <strong>{username}</strong>，您好！</p>
                        <p>您的账户密码已成功修改，现在可以使用新密码登录了。</p>
                        <p style="color: #e74c3c; margin-top: 20px;">
                            ⚠️ 如果这不是您本人的操作，请立即联系客服！
                        </p>
                        <p style="margin-top: 30px; color: #666;">
                            此邮件为系统自动发送，请勿直接回复。
                        </p>
                    </div>
                    <div class="footer">
                        <p>© 2025 水果商城 | 用心服务每一位顾客</p>
                    </div>
                </div>
            </body>
            </html>
            """

            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = self.email_from
            message["To"] = to_email

            html_part = MIMEText(html_content, "html", "utf-8")
            message.attach(html_part)

            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(message)

            logger.info(f"密码重置成功通知邮件发送成功：{to_email}")
            return True

        except Exception as e:
            logger.error(
                f"密码重置成功通知邮件发送失败：{to_email}，错误：{str(e)}",
                exc_info=True,
            )
            return False

# 创建全局邮件服务实例
email_service = EmailService()
