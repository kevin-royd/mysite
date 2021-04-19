import os
from django.core.mail import send_mail

os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'

if __name__ == '__main__':
    send_mail(
        '来自kenken的测试邮件',
        '欢迎访问www.baidu.com，搜索专注于Python、Django和机器学习技术的分享！',
        'kevinken163@sina.com',
        ['guiyuan163@gmail.com'],
    )

    # 还可以发送带有html格式的邮件

