"""
app.py
Build a few jobs, register them, run them, print a summary.
"""
from task_manager import TaskManager
from executor import Executor
from factory import JobFactory  # Thêm dòng này mang tính Abstraction

def build_jobs():
    # Giả lập dữ liệu thô (có thể đến từ API hoặc file config)
    raw_job_configs = [
        {"id": 1, "type": "email", "config": {"recipient": "user@example.com"}},
        {"id": 2, "type": "dataprocessing", "config": {"dataset": "dataset_A"}},
        {"id": 3, "type": "email", "config": {"recipient": "admin@example.com"}},
        {"id": 4, "type": "priority", "config": {"description": "Fix production server", "priority": 3}},
    ]

    jobs = []
    for raw in raw_job_configs:
        # Sử dụng Factory giúp tách biệt hoàn toàn logic tạo đối tượng khỏi app.py
        job = JobFactory.create_job(raw["type"], raw["id"], raw["config"])
        jobs.append(job)
        
    return jobs


if __name__ == "__main__":
    jobs = build_jobs()

    manager = TaskManager()
    for job in jobs:
        manager.add_job(job)

    Executor(jobs, manager).run()

    print("\n=== SUMMARY ===")
    print(f"Pending:   {len(manager.get_jobs_by_status('pending'))}")
    print(f"Completed: {len(manager.get_jobs_by_status('completed'))}")
    print(f"Failed:    {len(manager.get_jobs_by_status('failed'))}")

    # CHẠY THỬ ĐỂ KIỂM TRA LOG CỦA ACTIVITY 3 XEM HOẠT ĐỘNG KHÔNG:
    print("\n=== INTERNAL LOGS AUDIT (ACTIVITY 3) ===")
    for job in jobs:
        print(f"\nLogs for Job {job.job_id}:")
        for log in job.get_logs():
            print(f"  {log}")


# from models import EmailJob, DataProcessingJob

# from task_manager import TaskManager

# from executor import Executor


# def build_jobs():

#     return [

#         EmailJob(1, "user@example.com"),

#         DataProcessingJob(2, "dataset_A"),

#         EmailJob(3, "admin@example.com"),

#         DataProcessingJob(4, "dataset_B"),

#     ]


# if __name__ == "__main__":

#     jobs = build_jobs()


#     manager = TaskManager()

#     for job in jobs:

#         manager.add_job(job)  # all start as 'pending'


#     # FIX (app.py): pass 'manager' to Executor so it can update statuses.
#     # Previously Executor(jobs).run() had no manager reference — statuses never changed.
#     Executor(jobs, manager).run()


#     print("\n=== SUMMARY ===")

#     print(f"Pending:   {len(manager.get_jobs_by_status('pending'))}")

#     print(f"Completed: {len(manager.get_jobs_by_status('completed'))}")

#     # FIX (app.py): added 'failed' count to summary so failures are visible.
#     print(f"Failed:    {len(manager.get_jobs_by_status('failed'))}")