"""
models.py
Defines the Job hierarchy (parent + child classes).
Polymorphism: each subclass implements its own execute().
"""


import time
from typing import List

class Job:
    """Parent/base class shared by all job types."""

    def __init__(self, job_id: int, description: str) -> None:
        self.job_id = job_id
        self.description = description
        
        # --- CODE ACTIVITY 3: ĐÓNG GÓI & LOGS ---
        self._status = "pending"  # Thuộc tính ẩn (protected)
        self._logs: List[str] = [] # Danh sách lưu log nội bộ
        self.add_log("Job initialized with status: pending")

    # Getter cho status
    @property
    def status(self) -> str:
        return self._status

    # Setter cho status (Mỗi khi đổi status sẽ tự động ghi Log)
    @status.setter
    def status(self, new_status: str) -> None:
        old_status = self._status
        self._status = new_status
        self.add_log(f"Status changed from '{old_status}' to '{new_status}'")

    # Hàm nội bộ để ghi log kèm mốc thời gian
    def add_log(self, message: str) -> None:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        self._logs.append(f"[{timestamp}] {message}")

    # Hàm công khai (Expose method) để lấy toàn bộ log ra ngoài
    def get_logs(self) -> List[str]:
        return self._logs

    def execute(self) -> None:
        """Must be overridden by subclasses."""
        raise NotImplementedError("Each job must implement its own execution logic.")

    def mark_done(self) -> None:
        # Sử dụng setter thông qua self.status để kích hoạt ghi log tự động
        self.status = "completed" 

    def __repr__(self) -> str:
        return f"<Job id={self.job_id} status={self.status} desc='{self.description}'>"



class EmailJob(Job):

    """Child class: sends an email."""

    def __init__(self, job_id: int, recipient: str) -> None:

        # super() calls parent constructor (DRY)

        super().__init__(job_id, f"Send email to {recipient}")

        self.recipient = recipient


    def execute(self) -> None:

        print(f"Sending email to {self.recipient}...")

        # FIX (models.py): removed self.mark_done() here.
        # Previously mark_done() set job.status="completed" inside execute(),
        # so update_status() in executor.py searched the wrong bucket and
        # added a duplicate — causing Pending:4, Completed:4 in the summary.
        # Status is now managed exclusively by TaskManager.update_status().



class DataProcessingJob(Job):

    """Child class: processes a dataset."""

    def __init__(self, job_id: int, dataset: str) -> None:

        super().__init__(job_id, f"Process dataset {dataset}")

        self.dataset = dataset


    def execute(self) -> None:

        print(f"Processing dataset {self.dataset}...")

        # FIX (models.py): removed self.mark_done() here — same reason as EmailJob above


#activity 2: PriorityJob - Add Job Prioritisation
class PriorityJob(Job):
    """Child class: simulates task prioritisation."""

    def __init__(self, job_id: int, description: str, priority: int) -> None:
        # Gọi constructor của class cha (Job) để kế thừa job_id, description và status
        super().__init__(job_id, description)
        
        # Bổ sung thuộc tính độ ưu tiên (ví dụ: 1 = Thấp, 2 = Trung bình, 3 = Cao)
        self.priority = priority

    def execute(self) -> None:
        # Thực hiện logic chạy job dựa trên độ ưu tiên
        print(f"⭐ [Priority: {self.priority}] Executing high-priority job: {self.description}...")
        
        # Lưu ý: Giữ đúng nguyên tắc FIX của bạn, KHÔNG gọi self.mark_done() ở đây.
        # Trạng thái status sẽ do TaskManager tự cập nhật sau.

    def __repr__(self) -> str:
        # Ghi đè lại hàm hiển thị để nhìn rõ độ ưu tiên khi debug
        return f"<PriorityJob id={self.job_id} priority={self.priority} status={self.status}>"
