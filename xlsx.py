import openpyxl



def get_account_info():
    wb = openpyxl.load_workbook('config.xlsx')
    sheet = wb['Sheet1']
    accounts_data = []

    for row in sheet.iter_rows(min_row=2):
        if all(cell.value is None for cell in row):
            break
        account_info = {
            '账号': row[0].value,
            '密码': row[1].value,
            '100': row[2].value,
            '200': row[3].value,
            '500': row[4].value,
            '1000': row[5].value,
            '2000': row[6].value,
        }
        accounts_data.append(account_info)
    return accounts_data
if __name__ == '__main__':
    accounts_data=get_account_info()
    for account in accounts_data:
        print(account)