import os
import sqlite3
from datetime import datetime


class DBManager:
    def __init__(self, db_path, full_dataset_path):
        self.db_path = db_path
        self.full_dataset_path = full_dataset_path

    def help(self, language=None):
        # 获取系统默认语言或使用用户指定语言
        if language is None:
            language = "zh"

        # 多语言帮助信息
        help_text = {
            "en": """
            DBManager Usage Instructions:

            1. Initialize Database:
               Initialize the database file and create the table structure. If the database already exists, you will be prompted to confirm.
               Method:
                   db_manager.initialize_database()

            2. Add New Patient Record:
               Add a new patient record to the database, including patient ID and NII file path. Records include creation and update timestamps.
               Method:
                   db_manager.add_new_patient(patient_id, nii_path)
               Parameters:
                   - patient_id: Unique patient identifier (string)
                   - nii_path: Path to the NII file (string)

            3. Update Patient Record:
               Update the NII file path for a patient by ID, with a modification timestamp.
               Method:
                   db_manager.update_patient_record(patient_id, new_nii_path)
               Parameters:
                   - patient_id: Unique patient identifier (string)
                   - new_nii_path: New NII file path (string)

            4. Scan Folder to Initialize Database:
               Scan the specified folder to initialize the database by adding all patient records from the folder.
               Existing records will be skipped.
               Method:
                   db_manager.scan_and_initialize()

            5. Scan Folder to Add Missing Patients:
               Scan the specified folder to add missing patient records to the database.
               Method:
                   db_manager.scan_and_add_missing_patients()

            Example:
                db_manager = DBManager('patients.db', 'shant')
                
                # Initialize Database
                db_manager.initialize_database()
                
                # Add New Patient Record
                db_manager.add_new_patient('patient_001', '/path/to/nii_file.nii')
                
                # Update Patient Record
                db_manager.update_patient_record('patient_001', '/new/path/to/nii_file.nii')
                
                # Scan Folder to Initialize Database
                db_manager.scan_and_initialize()
                
                # Scan Folder to Add Missing Patients
                db_manager.scan_and_add_missing_patients()

            Note:
            - Ensure that `full_dataset_path` points to a valid patient data folder.
            - The folder structure should consist of one folder per patient, with the folder name as the patient ID, containing `.nii` files.
            """,

            "zh": """
            DBManager 使用说明:

            1. 初始化数据库:
               初始化数据库文件并创建表结构。如果数据库已存在，会提示是否确认操作。
               方法:
                   db_manager.initialize_database()

            2. 添加新患者记录:
               向数据库添加一条新的患者记录，包括患者 ID 和 NII 文件路径。记录会包含创建和更新时间戳。
               方法:
                   db_manager.add_new_patient(patient_id, nii_path)
               参数:
                   - patient_id: 患者唯一标识符 (字符串)
                   - nii_path: NII 文件路径 (字符串)

            3. 更新患者记录:
               根据患者 ID 更新对应的 NII 文件路径，并记录修改时间。
               方法:
                   db_manager.update_patient_record(patient_id, new_nii_path)
               参数:
                   - patient_id: 患者唯一标识符 (字符串)
                   - new_nii_path: 新的 NII 文件路径 (字符串)

            4. 扫描文件夹初始化数据库:
               从指定的文件夹扫描患者数据并初始化数据库，添加文件夹中所有患者数据记录。
               如果患者记录已存在，将会跳过。
               方法:
                   db_manager.scan_and_initialize()

            5. 扫描文件夹添加缺失患者:
               从指定的文件夹扫描患者数据，添加数据库中缺失的患者记录。
               方法:
                   db_manager.scan_and_add_missing_patients()

            示例:
                db_manager = DBManager('patients.db', 'shant')
                
                # 初始化数据库
                db_manager.initialize_database()
                
                # 添加新患者记录
                db_manager.add_new_patient('patient_001', '/path/to/nii_file.nii')
                
                # 更新患者记录
                db_manager.update_patient_record('patient_001', '/new/path/to/nii_file.nii')
                
                # 扫描文件夹初始化数据库
                db_manager.scan_and_initialize()
                
                # 扫描文件夹添加缺失患者
                db_manager.scan_and_add_missing_patients()
            
            注意:
            - 确保 `full_dataset_path` 指向有效的患者数据文件夹。
            - 文件夹结构应为每个患者一个文件夹，文件夹名作为患者 ID，内部包含 `.nii` 文件。
            """
        }

        # 打印指定语言的帮助信息
        print(help_text.get(language, help_text["en"]))


    def connect_db(self):
        return sqlite3.connect(self.db_path)

    def initialize_database(self):
        if os.path.exists(self.db_path):
            response = input(f"数据库 '{self.db_path}' 已存在。是否继续初始化？(y/n): ").strip().lower()
            if response != 'y':
                print("初始化已取消。")
                return
        
        conn = self.connect_db()
        cursor = conn.cursor()
        
        # 创建表结构
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS patient_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id TEXT UNIQUE,
                nii_path TEXT,
                created_at TEXT,
                updated_at TEXT
            )
        ''')
        conn.commit()
        print("数据库表 'patient_data' 已创建或确认存在。")
        conn.close()

    def add_new_patient(self, patient_id, nii_path):
        conn = self.connect_db()
        cursor = conn.cursor()
        timestamp = datetime.now().isoformat()
        
        try:
            cursor.execute('''
                INSERT INTO patient_data (patient_id, nii_path, created_at, updated_at)
                VALUES (?, ?, ?, ?)
            ''', (patient_id, nii_path, timestamp, timestamp))
            conn.commit()
            print(f"成功添加患者记录: {patient_id}")
        except sqlite3.IntegrityError:
            print(f"患者 ID '{patient_id}' 已存在，添加失败。")
        finally:
            conn.close()

    def update_patient_record(self, patient_id, new_nii_path):
        conn = self.connect_db()
        cursor = conn.cursor()
        timestamp = datetime.now().isoformat()
        
        cursor.execute('''
            UPDATE patient_data
            SET nii_path = ?, updated_at = ?
            WHERE patient_id = ?
        ''', (new_nii_path, timestamp, patient_id))
        
        if cursor.rowcount > 0:
            conn.commit()
            print(f"成功更新患者记录: {patient_id}")
        else:
            print(f"未找到患者 ID '{patient_id}'，更新失败。")
        conn.close()

    def scan_and_initialize(self):
        conn = self.connect_db()
        cursor = conn.cursor()
        timestamp = datetime.now().isoformat()
        
        for patient_folder in os.listdir(self.full_dataset_path):
            patient_path = os.path.join(self.full_dataset_path, patient_folder)
            if os.path.isdir(patient_path):
                patient_id = patient_folder  # 用文件夹名作为患者 ID
                for nii_file in os.listdir(patient_path):
                    if nii_file.endswith(".nii"):
                        nii_path = os.path.join(patient_path, nii_file)
                        cursor.execute('SELECT 1 FROM patient_data WHERE nii_path = ?', (nii_path,))
                        if cursor.fetchone():
                            print(f"NII 文件路径 '{nii_path}' 已存在。请检查文件夹是否指定正确。否则请使用 'scan_and_add_missing_patients' 方法添加缺失患者。")
                        else:
                            try:
                                cursor.execute('''
                                    INSERT INTO patient_data (patient_id, nii_path, created_at, updated_at)
                                    VALUES (?, ?, ?, ?)
                                ''', (patient_id, nii_path, timestamp, timestamp))
                            except sqlite3.IntegrityError:
                                pass  # 忽略已存在的记录
        
        conn.commit()
        print("数据库初始化完成。")
        conn.close()

    def scan_and_add_missing_patients(self):
        conn = self.connect_db()
        cursor = conn.cursor()
        timestamp = datetime.now().isoformat()
        
        for patient_folder in os.listdir(self.full_dataset_path):
            patient_path = os.path.join(self.full_dataset_path, patient_folder)
            if os.path.isdir(patient_path):
                patient_id = patient_folder  # 用文件夹名作为患者 ID
                cursor.execute('SELECT 1 FROM patient_data WHERE patient_id = ?', (patient_id,))
                if not cursor.fetchone():
                    for nii_file in os.listdir(patient_path):
                        if nii_file.endswith(".nii"):
                            nii_path = os.path.join(patient_path, nii_file)
                            cursor.execute('''
                                INSERT INTO patient_data (patient_id, nii_path, created_at, updated_at)
                                VALUES (?, ?, ?, ?)
                            ''', (patient_id, nii_path, timestamp, timestamp))
                            print(f"添加缺失患者记录: {patient_id}")
        
        conn.commit()
        print("扫描完成，缺失患者已添加。")
        conn.close()
