from typing import Dict, Any
from models import Job, EmailJob, DataProcessingJob, PriorityJob

class JobFactory:
    """Factory pattern to simplify and decouple object creation."""

    @staticmethod
    def create_job(job_type: str, job_id: int, config: Dict[str, Any]) -> Job:
        """
        Tạo đối tượng Job dựa trên job_type và cấu hình config được truyền vào.
        """
        job_type = job_type.lower()

        if job_type == "email":
            # Yêu cầu config phải có 'recipient'
            return EmailJob(job_id, config["recipient"])
            
        elif job_type == "dataprocessing":
            # Yêu cầu config phải có 'dataset'
            return DataProcessingJob(job_id, config["dataset"])
            
        elif job_type == "priority":
            # Đã bao gồm PriorityJob từ Activity 2 của bạn
            return PriorityJob(job_id, config["description"], config["priority"])
            
        else:
            raise ValueError(f"Unknown job type: '{job_type}'")
