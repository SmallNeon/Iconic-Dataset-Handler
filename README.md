Database File Structure Description

The database file is in SQLite format and stores patient-related information. The structure is as follows:

Table Name: patient_data

Column Name	Data Type	Description
id	INTEGER	Primary key, auto-increment
patient_id	TEXT	Patient ID, usually corresponds to folder name
file_path	TEXT	File path, unique
file_type	TEXT	File type (e.g., .nii, .txt)
created_at	TEXT	Record creation time (ISO format)
updated_at	TEXT	Record update time (ISO format)

	•	id: Auto-increment primary key used to uniquely identify a record.
	•	patient_id: Records the unique identifier of the patient, typically derived from the folder name.
	•	file_path: Stores the specific file path and ensures uniqueness.
	•	file_type: Marks the file type (file extension) for easier classification and management.
	•	created_at and updated_at: Record the data creation and modification timestamps, respectively.

Brief README

Patient Record Management Tool

This project is designed to batch manage patient data by scanning folders and saving it into an SQLite database.

Features

	1.	Multi-threaded scanning of all files in the target folder.
	2.	Store patient data (file paths, file types, etc.) into the database.
	3.	Automatically skip existing records.
	4.	Real-time progress display, including the number of files checked and new records added.

Database Structure

	•	Data is stored in patients.db.
	•	The table name is patient_data, containing patient IDs, file paths, file types, and timestamps for creation and modification.

Notes

	•	Each patient occupies a separate folder.

数据库文件结构说明

数据库文件为 SQLite 格式，保存患者相关信息，结构如下：

表名：patient_data

列名	数据类型	描述
id	INTEGER	主键，自增
patient_id	TEXT	患者 ID，通常为文件夹名
file_path	TEXT	文件路径，唯一
file_type	TEXT	文件类型（如 .nii, .txt）
created_at	TEXT	记录创建时间（ISO 格式）
updated_at	TEXT	记录更新时间（ISO 格式）

	•	id：自动递增主键，用于标识唯一记录。
	•	patient_id：记录患者的唯一标识，通常来源于文件夹名。
	•	file_path：保存具体文件路径，确保唯一性。
	•	file_type：标记文件类型（后缀名），便于分类管理。
	•	created_at 和 updated_at：分别记录数据的创建和修改时间。

简短 README

患者记录管理工具

本项目旨在通过扫描文件夹批量管理患者数据，并保存至 SQLite 数据库中。

功能

	1.	多线程扫描目标文件夹中的所有文件。
	2.	将患者数据（文件路径、文件类型等）存储至数据库。
	3.	自动跳过已存在的记录。
	4.	实时显示进度，包含已检查和新增记录数量。

数据库结构

	•	数据存储在 patients.db 中。
	•	数据表名为 patient_data，包含患者 ID、文件路径、文件类型、创建和修改时间等信息。

注意事项

	•	每个患者单独占用一个文件夹。
