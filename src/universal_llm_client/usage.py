
from dataclasses import dataclass


@dataclass
class UsageTracker:
    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0
    request_count: int = 0


    def record(
            self,
            input_tokens: int,
            output_tokens: int,
    ) -> None:
        self.input_tokens += input_tokens
        self.output_tokens += output_tokens
        self.total_tokens += input_tokens + output_tokens
        self.request_count += 1