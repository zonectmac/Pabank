from lib.pabank_operation import pabank_download, clear_cookies, log_out, close_firefox, send_email
from lib.file_util import read_file_email, del_allfile, zip_dir
import get_config, config
from lib.date_util import currency_date_array, get_yesterday
from lib.ftp_file_operation import ftp_upload
import traceback, time
from lib.excel_file_util import write_all_ecxel

if __name__ == "__main__":
    a = 0
    paypalUser = get_config.get_paypalUser()
    for i in range(len(paypalUser)):
        flag = True
        while flag and a < 100:
            try:
                clear_cookies()
                pabank_download(get_config.get_emailFromSend(), get_config.get_emailPassword(),
                                get_config.get_smtpServer(),
                                get_config.get_emailTo(),
                                get_config.get_emailCc(), get_config.get_emailSubject(),
                                read_file_email(), get_config.get_paypalUser()[i],
                                get_config.get_paypalPassword()[i], i + 1)
                flag = False
            except Exception as e:
                a += 1
                log_out()
                flag = True
                print(traceback.print_exc())
    file_name = currency_date_array()[0] + '_' + currency_date_array()[1] + '_' + currency_date_array()[2]
    write_all_ecxel(config.DOWNLOAD_PATH, config.DOWNLOAD_PATH + str(get_yesterday()) + '.xls')
    zip_dir(config.DOWNLOAD_PATH,
            config.DOWNLOAD_PATH + str(get_yesterday()) + '.zip')
    send_email(get_config.get_emailFromSend(), get_config.get_emailPassword(), get_config.get_smtpServer(),
               get_config.get_emailTo(), get_config.get_emailCc(), get_config.get_emailSubject(),
               config.DOWNLOAD_PATH + read_file_email(),
               config.DOWNLOAD_PATH + str(get_yesterday()))
    # ftp_upload(config.DOWNLOAD_PATH, '/pingan/' + currency_date_array()[0] + '_' + currency_date_array()[1] + '_' +
    #            currency_date_array()[2])
    ftp_upload(config.DOWNLOAD_PATH, '/pingan/' + str(get_yesterday()))
    time.sleep(5)
    del_allfile(config.DOWNLOAD_PATH)
    close_firefox()
