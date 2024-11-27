import asyncio
import logging
import calendar
from datetime import datetime, timedelta
from threading import Lock

# Configure logging to output messages with a specific format
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class AsyncPeriodicExecutor:
    """
    An asynchronous task scheduler that allows scheduling tasks at specific intervals,
    daily times, hourly, weekly, or monthly. Supports programmable tasks.
    """

    _instances = {}  # Dictionary to hold singleton instances by name
    _lock = Lock()   # Lock to ensure thread-safe singleton creation

    def __new__(cls, name, *args, **kwargs):
        """
        Overrides the default method to implement the singleton pattern.
        Ensures that only one instance per name exists.
        """
        with cls._lock:
            if name in cls._instances:
                logger.debug(f"Instance with name '{name}' already exists. Returning existing instance.")
                return cls._instances[name]
            else:
                logger.debug(f"Creating new instance with name '{name}'.")
                instance = super(AsyncPeriodicExecutor, cls).__new__(cls)
                cls._instances[name] = instance
                instance._initialized = False  # Prevents multiple initializations
                return instance

    @classmethod
    def get_instance(cls, name):
        """
        Class method to access the singleton instance by name.

        :param name: The name of the executor instance.
        :return: The executor instance with the given name, or None if it doesn't exist.
        """
        return cls._instances.get(name)

    def __init__(self, name):
        """
        Initializes the executor with a name.

        :param name: The name of the executor instance.
        """
        if getattr(self, '_initialized', False):
            return  # Avoid re-initialization
        self._initialized = True
        self.name = name
        self.programmable_tasks = {}  # Stores programmable tasks
        self.executor_tasks = {}      # Maps task names to asyncio Tasks
        self.loop_task = None         # The main loop task
        self.task_lock = asyncio.Lock()    # Async lock to protect shared resources
        self.stop_event = asyncio.Event()  # Event to signal stopping of tasks
        logger.info(f"Initialized AsyncPeriodicExecutor instance with name '{self.name}'.")

    async def start(self):
        """
        Starts the executor's main loop. Aligns to the next minute and begins
        scheduling tasks.
        """
        self.on_start()
        try:
            # Align to the start of the next minute for consistency
            await self._wait_until_next_minute()
            self.loop_task = asyncio.create_task(self._run_loop())
            await self.loop_task
        finally:
            self.on_end()

    def on_start(self):
        """
        Called when the executor starts. Can be overridden for custom behavior.
        """
        logger.info(f"AsyncPeriodicExecutor '{self.name}' started.")

    def on_end(self):
        """
        Called when the executor stops. Can be overridden for custom behavior.
        """
        logger.info(f"AsyncPeriodicExecutor '{self.name}' stopped.")

    async def stop(self):
        """
        Stops the executor by setting the stop event.
        """
        self.stop_event.set()
        if self.loop_task:
            await self.loop_task  # Wait for the main loop to finish

    async def schedule_task(
            self, func, interval_seconds=None, daily=None, hourly=None,
            weekly_day=None, monthly_day=None, task_name=None,
    ):
        """
        Schedules a programmable task based on the provided scheduling parameters.

        :param func: The async function to execute.
        :param interval_seconds: Schedule task at regular intervals (in seconds).
        :param daily: Schedule task at a specific daily time (HH:MM format).
        :param hourly: If True, schedule task at the top of each hour.
        :param weekly_day: Schedule task weekly on a specific day (0=Monday to 6=Sunday).
        :param monthly_day: Schedule task monthly on a specific day (1-31).
        :param task_name: Optional name for the task; defaults to the function's name.
        """
        if not asyncio.iscoroutinefunction(func):
            raise ValueError("Function must be an async function.")

        # Determine the task type and create the task information dictionary
        task_info = None
        if interval_seconds is not None:
            task_info = {
                "type": "interval",
                "func": func,
                "interval": interval_seconds,
                "name": task_name or func.__name__,
            }
        elif daily is not None:
            task_info = {
                "type": "daily",
                "func": func,
                "time": daily,
                "name": task_name or func.__name__,
            }
        elif hourly:
            task_info = {
                "type": "hourly",
                "func": func,
                "name": task_name or func.__name__,
            }
        elif weekly_day is not None:
            task_info = {
                "type": "weekly",
                "func": func,
                "day": weekly_day,
                "name": task_name or func.__name__,
            }
        elif monthly_day is not None:
            task_info = {
                "type": "monthly",
                "func": func,
                "day": monthly_day,
                "name": task_name or func.__name__,
            }
        else:
            raise ValueError(
                "Specify one of interval_seconds, run_at, hourly, weekly_day, or monthly_day."
            )

        # Add the task to the programmable tasks dictionary
        self.programmable_tasks[task_info["name"]] = task_info

        # If the executor is already running, schedule the task immediately
        if self.loop_task and not self.loop_task.done():
            await self._schedule_task(task_info)

    async def _wait_until_next_minute(self):
        """
        Waits until the start of the next minute to align task scheduling.
        """
        now = datetime.now()
        seconds_until_next_minute = 60 - now.second - now.microsecond / 1_000_000
        if seconds_until_next_minute > 0:
            logger.info(
                f"Waiting {seconds_until_next_minute:.2f} seconds until the next minute starts."
            )
            await asyncio.sleep(seconds_until_next_minute)

    async def _run_loop(self):
        """
        The main loop that runs scheduled tasks.
        """
        # Schedule any programmable tasks
        await self._schedule_programmable_tasks()

        # Wait until the stop event is set
        await self.stop_event.wait()

        # Cancel all running tasks when stopping
        async with self.task_lock:
            for task in self.executor_tasks.values():
                task.cancel()
            self.executor_tasks.clear()

    async def _schedule_programmable_tasks(self):
        """
        Schedules all the programmable tasks stored in self.programmable_tasks.
        """
        for task_name, task_info in self.programmable_tasks.items():
            await self._schedule_task(task_info)

    async def _schedule_task(self, task_info):
        """
        Schedules a task based on its type.

        :param task_info: Configuration dictionary of the task.
        """
        task_name = task_info.get("name")
        # Create an asyncio task to run the programmable task
        scheduled_task = asyncio.create_task(self._run_programmable_task(task_info))

        # Add the scheduled task to the executor_tasks dictionary
        async with self.task_lock:
            self.executor_tasks[task_name] = scheduled_task

    async def _run_programmable_task(self, task_info):
        """
        Runs a programmable task based on its scheduling parameters.

        :param task_info: Configuration dictionary of the task.
        """
        func = task_info["func"]            # The function to execute
        task_name = task_info.get("name", func.__name__)  # Task name
        task_type = task_info["type"]       # Type of scheduling (interval, daily, etc.)

        logger.info(f"Starting {task_type} task '{task_name}'.")

        while not self.stop_event.is_set():
            try:
                schedule = {}
                if task_type == "interval":
                    # For interval tasks, wait for the specified interval
                    interval = task_info["interval"]
                    next_run = datetime.now() + timedelta(seconds=interval)
                    schedule["interval"] = interval
                    # Wait until the next run time or stop event
                    should_continue = await self._wait_until(next_run)
                    if not should_continue:
                        break  # Stop event was set
                    # Execute the function
                    await func()
                    logger.info(f"Task '{task_name}' executed successfully.")
                else:
                    # For other types, calculate the next run time
                    if task_type == "daily":
                        schedule["time"] = task_info["time"]
                    elif task_type == "hourly":
                        schedule["hourly"] = True
                    elif task_type == "weekly":
                        schedule["day"] = task_info["day"]
                    elif task_type == "monthly":
                        schedule["day"] = task_info["day"]
                    else:
                        logger.error(f"Unknown task type: {task_type}")
                        break

                    # Calculate when the task should run next
                    next_run = await self._calculate_next_run(task_type, schedule)
                    if not next_run:
                        logger.error(f"Invalid schedule for task '{task_name}'.")
                        break

                    # Wait until the next scheduled time or stop event
                    should_continue = await self._wait_until(next_run)
                    if not should_continue:
                        break  # Stop event was set

                    # Execute the function
                    await func()
                    logger.info(f"Task '{task_name}' executed successfully.")
            except Exception:
                # Log exceptions without stopping the entire executor
                logger.exception(f"Exception occurred in task '{task_name}'.")
                continue  # Continue to the next iteration

        logger.info(f"Task '{task_name}' stopped.")

    async def _wait_until(self, next_run):
        """
        Waits until the specified datetime, or returns early if the stop event is set.

        :param next_run: The datetime to wait until.
        :return: True if time to run the task, False if stop event was set.
        """
        now = datetime.now()
        seconds_until_next_run = (next_run - now).total_seconds()
        if seconds_until_next_run <= 0:
            return True  # It's time to run the task
        try:
            # Wait for the required time or until the stop event is set
            await asyncio.wait_for(self.stop_event.wait(), timeout=seconds_until_next_run)
            return False  # Stop event was set during the wait
        except asyncio.TimeoutError:
            return True  # Time to run the task

    def add_months(self, sourcedate, months):
        """
        Adds or subtracts months from a datetime object.

        :param sourcedate: The original datetime.
        :param months: Number of months to add (can be negative).
        :return: A new datetime with the months added.
        """
        # Calculate the target month and year
        month = sourcedate.month - 1 + months
        year = sourcedate.year + month // 12
        month = month % 12 + 1
        # Get the last day of the target month to avoid invalid dates
        day = min(sourcedate.day, calendar.monthrange(year, month)[1])
        # Return the new datetime object
        return datetime(year, month, day, sourcedate.hour, sourcedate.minute, sourcedate.second)

    async def _calculate_next_run(self, task_type, schedule):
        """
        Calculates the next run time for a task based on its type and schedule.

        :param task_type: Type of the task (interval, daily, hourly, etc.).
        :param schedule: Scheduling parameters for the task.
        :return: The next datetime when the task should run.
        """
        now = datetime.now()
        if task_type == "interval":
            # For interval tasks, the next run is after the interval
            interval = schedule.get("interval")
            if interval is None:
                return None
            return now + timedelta(seconds=interval)
        elif task_type == "daily":
            # For daily tasks, schedule at the specified time
            time_str = schedule.get("time")
            if not time_str:
                return None
            target_time = datetime.strptime(time_str, "%H:%M").time()
            next_run = datetime.combine(now.date(), target_time)
            if now.time() >= target_time:
                # If the time has passed today, schedule for tomorrow
                next_run += timedelta(days=1)
            return next_run
        elif task_type == "hourly":
            # For hourly tasks, schedule at the top of the next hour
            next_run = now.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
            return next_run
        elif task_type == "weekly":
            # For weekly tasks, schedule on the specified weekday
            day_of_week = schedule.get("day")
            if day_of_week is None:
                return None
            days_ahead = (day_of_week - now.weekday()) % 7
            next_run = now + timedelta(days=days_ahead)
            next_run = next_run.replace(hour=0, minute=0, second=0, microsecond=0)
            if days_ahead == 0 and now.time() >= datetime.min.time():
                # If today is the day but the time has passed, schedule for next week
                next_run += timedelta(weeks=1)
            return next_run
        elif task_type == "monthly":
            # For monthly tasks, schedule on the specified day
            day_of_month = schedule.get("day")
            if day_of_month is None:
                return None
            try:
                # Try to create a date with the specified day
                next_run = now.replace(day=day_of_month, hour=0, minute=0, second=0, microsecond=0)
                if now.day > day_of_month or (now.day == day_of_month and now.time() >= datetime.min.time()):
                    # If the day has passed this month, add one month
                    next_run = self.add_months(next_run, 1)
            except ValueError:
                # Handle cases where the day does not exist in the current month
                # Find the last day of the current month
                last_day = calendar.monthrange(now.year, now.month)[1]
                if day_of_month > last_day:
                    # Set to the last day of the month
                    next_run = now.replace(day=last_day, hour=0, minute=0, second=0, microsecond=0)
                    next_run = self.add_months(next_run, 1)
                else:
                    next_run = now.replace(day=day_of_month, hour=0, minute=0, second=0, microsecond=0)
            return next_run
        else:
            # Unknown task type
            return None
