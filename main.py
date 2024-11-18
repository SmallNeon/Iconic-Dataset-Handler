from dbmgr import DBManager

def main():
    # 文件位置配置
    db_path = 'patient_data.db'
    full_dataset_path = '/media/molloi-lab-linux2/HD-88/ICONIC CCTAS'

    # 初始化 DBManager 实例
    db = DBManager(db_path, full_dataset_path)

    # 调用帮助信息
    # db.help()
    #db.help('en')

    # 初始化数据库
    # db.initialize_database()
    db.scan_and_initialize()


if __name__ == "__main__":
    main()
