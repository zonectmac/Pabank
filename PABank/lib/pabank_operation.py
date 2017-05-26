from selenium import webdriver
import config
import time
from lib.file_util import is_file_writing, del_allfile, getdoc_size, del_file, zip_dir, file_is_exist
import os
import shutil
from lib.date_util import currency_date_array,get_yesterday
from email_manager import EmailManager
from selenium.common.exceptions import NoSuchElementException
from lib.ftp_file_operation import ftp_upload
import traceback


def get_driver():
    # 'C:\\Users\\Administrator\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\yrv03uop.default'
    firefox_profile = webdriver.FirefoxProfile(config.FF_PROFILES)
    mime_types = 'text/plain,application/pdf,application/vnd.adobe.xfdf,application/vnd.fdf,' \
                 'application/vnd.adobe.xdp+xml,text/csv,application/zip,application/vnd.ms-excel'
    firefox_profile.set_preference('browser.download.dir', config.DOWNLOAD_TEMPORARY_PATH)
    firefox_profile.set_preference('browser.download.folderList', 2)
    firefox_profile.set_preference('browser.download.manager.showWhenStarting', False)
    firefox_profile.set_preference('browser.helperApps.neverAsk.saveToDisk', mime_types)
    return webdriver.Firefox(firefox_profile)


driver = get_driver()


def clear_cookies():
    driver.delete_all_cookies()


def close_firefox():
    driver.quit()


def log_out():
    time.sleep(2)
    try:
        driver.find_element_by_xpath(".//*[@id='safe_logout']/a")
        print('------logout----')
    except Exception as e:
        print(traceback.print_exc())


def pabank_download(server_username, server_pwd, smtp_server, msg_to, msg_cc, msg_subject, msg_content, user, paw, i):
    # file_name = currency_date_array()[0] + '_' + currency_date_array()[1] + '_' + currency_date_array()[2] + '_' + user
    file_name = str(get_yesterday()) + '_' + user
    print(file_name)
    if not login(user, paw, i):
        print('-----------' + user)
        return
    transaction_details(file_name)
    if file_is_exist(config.DOWNLOAD_PATH, file_name + '.xls') > 0:
        # zip_dir(config.DOWNLOAD_PATH,
        #         config.DOWNLOAD_PATH + file_name + '.zip')
        # send_email(server_username, server_pwd, smtp_server, msg_to, msg_cc, msg_subject,
        #            config.DOWNLOAD_PATH + msg_content,
        #            config.DOWNLOAD_PATH + file_name)
        # ftp_upload(config.DOWNLOAD_PATH, '/pingan/'+currency_date_array()[0] + '_' + currency_date_array()[1] + '_' +
        #            currency_date_array()[2])
        log_out()


def send_email(server_username, server_pwd, smtp_server, msg_to, msg_cc, msg_subject, msg_content, zipname):
    mail_cfg = {
        # 邮箱登录设置，使用SMTP登录
        'server_username': server_username,
        'server_pwd': server_pwd,
        'smtp_server': smtp_server,
        # 邮件内容设置
        'msg_to': [msg_to],  # 可以在此添加收件人
        'msg_cc': msg_cc,
        'msg_subject': msg_subject,
        'msg_date': time.strftime('%Y-%m-%d %X', time.localtime()),
        'msg_content': msg_content,

        # 附件
        'attach_file': zipname + '.zip'
    }

    email_manager = EmailManager(**mail_cfg)

    email_manager.run()


def login(user, paw, i):
    driver.implicitly_wait(config.TIMEOUT)
    driver.get(config.LOGIN_BASE_URL + 'ibp/bank/index.html#home/home/index')
    time.sleep(3)
    if is_element_present_by_xpath("html/body/div[4]/div[1]/button"):
        driver.find_element_by_xpath("html/body/div[4]/div[1]/button").click()
        time.sleep(2)
    driver.find_element_by_id('userName').clear()
    driver.find_element_by_id('userName').send_keys(user)
    time.sleep(2)
    driver.find_element_by_id('pwdObject' + str(i) + '-btn-pan').click()
    driver.find_element_by_id('pa_ui_keyboard_close').click()
    time.sleep(2)
    driver.find_element_by_id('pwdObject' + str(i) + '-input').clear()
    driver.find_element_by_id('pwdObject' + str(i) + '-input').send_keys(paw)
    driver.find_element_by_id('login_btn').click()
    time.sleep(10)
    if is_element_present_by_xpath(".//*[@id='account']/a"):
        return True
    return False


def transaction_details(file_name):
    driver.find_element_by_xpath(".//*[@id='account']/a").click()
    time.sleep(5)
    driver.find_element_by_xpath(".//*[@id='menuItems']/li[2]/a").click()
    time.sleep(5)
    # 选择昨天的时间
    js = "$('input[id=tranListDate_start]').attr('readonly',false)"  # 4.jQuery，设置为空（同3）
    driver.execute_script(js)
    time.sleep(5)
    driver.find_element_by_id("tranListDate_start").clear()
    driver.find_element_by_id('tranListDate_start').send_keys(str(get_yesterday()))
    time.sleep(3)
    js = "$('input[id=tranListDate_end]').attr('readonly',false)"  # 4.jQuery，设置为空（同3）
    driver.execute_script(js)
    time.sleep(5)
    driver.find_element_by_id("tranListDate_end").clear()
    driver.find_element_by_id('tranListDate_end').send_keys(str(get_yesterday()))
    time.sleep(5)
    driver.find_element_by_xpath(".//*[@id='query_tranList_btn']/a").click()
    if not (os.path.exists(config.DOWNLOAD_TEMPORARY_PATH) and os.path.isdir(config.DOWNLOAD_TEMPORARY_PATH)):
        os.makedirs(config.DOWNLOAD_TEMPORARY_PATH)
    if not (os.path.exists(config.DOWNLOAD_PATH) and os.path.isdir(config.DOWNLOAD_PATH)):
        os.makedirs(config.DOWNLOAD_PATH)
    if not (os.path.exists(config.DOWNLOAD_PATH_FINAL) and os.path.isdir(config.DOWNLOAD_PATH_FINAL)):
        os.makedirs(config.DOWNLOAD_PATH_FINAL)
    time.sleep(2)
    if is_element_present_by_xpath(
            ".//*[@id='tranList_item_container']/div/table/thead/tr/td[1]") \
            and is_element_present_by_xpath(".//*[@id='downloadTransferDetailBtn']/a"):
        print('aaa')
        del_allfile(config.DOWNLOAD_TEMPORARY_PATH)
        time.sleep(3)
        downloading()
        copy_file(config.DOWNLOAD_TEMPORARY_PATH, '.xls', file_name)


def copy_file(path, file_type, file_name):
    file_dir = os.listdir(path)
    for tmp in file_dir:
        if os.path.exists(path + tmp) and os.path.isfile(
                        path + tmp):
            if os.path.splitext(path + tmp)[1] == file_type:
                while getdoc_size(path + tmp) == 0 and not file_is_exist(config.DOWNLOAD_PATH,
                                                                         tmp):
                    del_file(path + tmp)
                    del_file(path + tmp + '.part')
                    downloading()
                    del_file(path + tmp + '.part')
                    print('----while--3-')
                shutil.move(path + tmp,
                            config.DOWNLOAD_PATH + file_name + file_type)
                print('--copyfile--')


def downloading():
    print('down')
    driver.find_element_by_xpath(".//*[@id='downloadTransferDetailBtn']/a").click()
    time.sleep(5)
    file_dir = os.listdir(config.DOWNLOAD_TEMPORARY_PATH)
    for tmp in file_dir:
        if os.path.exists(config.DOWNLOAD_TEMPORARY_PATH + tmp) and os.path.isfile(
                        config.DOWNLOAD_TEMPORARY_PATH + tmp):
            if os.path.splitext(config.DOWNLOAD_TEMPORARY_PATH + tmp)[1] == '.part':
                while is_file_writing(config.DOWNLOAD_TEMPORARY_PATH + tmp):
                    time.sleep(1)
                    print('----while--2-')


def is_element_present_by_xpath(element):
    try:
        driver.find_element_by_xpath(element)
    except NoSuchElementException as e:
        return False
    return True
