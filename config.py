import platform


from data_base import job_db

system_info = platform.system()

BOT_TOKEN = ""
if system_info == "Windows":
    BOT_TOKEN = job_db.execute("""SELECT key FROM api_analyses WHERE system = ?""", (system_info,)).fetchone()[0]
elif system_info == "Linux":
    BOT_TOKEN = job_db.execute("""SELECT key FROM api_analyses WHERE system = ?""", (system_info,)).fetchone()[0]