"""
Circuit breaker implementation for fault tolerance in multi-agent systems.
Based on Netflix Hystrix pattern.
"""

import time
import threading


class CircuitBreaker:
    """
    Prevents cascade failures by temporarily disabling failing agents.
    Based on Netflix Hystrix pattern.
    """

    def __init__(
        self,
        failure_threshold: int = 3,
        timeout_duration: int = 60,
        success_threshold: int = 2
    ):
        self.failure_threshold = failure_threshold
        self.timeout_duration = timeout_duration
        self.success_threshold = success_threshold

        self.failures = {}  # agent_type -> failure count
        self.last_failure_time = {}  # agent_type -> timestamp
        self.successes = {}  # agent_type -> success count
        self.state = {}  # agent_type -> "closed", "open", "half_open"

        self.lock = threading.Lock()

    def is_open(self, agent_type: str) -> bool:
        """Check if circuit breaker is open (blocking requests)"""
        with self.lock:
            current_state = self.state.get(agent_type, "closed")

            if current_state == "open":
                # Check if timeout has passed
                if time.time() - self.last_failure_time.get(agent_type, 0) > self.timeout_duration:
                    # Move to half-open state
                    self.state[agent_type] = "half_open"
                    self.successes[agent_type] = 0
                    return False
                return True

            return False

    def record_success(self, agent_type: str):
        """Record successful execution"""
        with self.lock:
            current_state = self.state.get(agent_type, "closed")

            if current_state == "half_open":
                self.successes[agent_type] = self.successes.get(agent_type, 0) + 1

                if self.successes[agent_type] >= self.success_threshold:
                    # Circuit breaker recovers
                    self.state[agent_type] = "closed"
                    self.failures[agent_type] = 0
                    print(f"✅ Circuit breaker closed for {agent_type}")

            elif current_state == "closed":
                # Reset failure count on success
                self.failures[agent_type] = 0

    def record_failure(self, agent_type: str):
        """Record failed execution"""
        with self.lock:
            current_state = self.state.get(agent_type, "closed")

            if current_state == "half_open":
                # Immediately open circuit on failure in half-open state
                self.state[agent_type] = "open"
                self.last_failure_time[agent_type] = time.time()
                print(f"⚡ Circuit breaker opened for {agent_type}")

            elif current_state == "closed":
                self.failures[agent_type] = self.failures.get(agent_type, 0) + 1

                if self.failures[agent_type] >= self.failure_threshold:
                    # Open circuit breaker
                    self.state[agent_type] = "open"
                    self.last_failure_time[agent_type] = time.time()
                    print(f"⚡ Circuit breaker opened for {agent_type} after {self.failures[agent_type]} failures")