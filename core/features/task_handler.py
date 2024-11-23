import asyncio
import logging
import json
import os
import aiohttp
import aiomysql
from datetime import datetime, timedelta
from threading import Lock
# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class AsyncPeriodicExecutor:
    _instances = {}
    _lock = Lock()  # To make singleton creation thread-safe

    def __new__(cls, name, *args, **kwargs):
        with cls._lock:
            if name in cls._instances:
                logger.debug(f"Instance with name '{name}' already exists. Returning existing instance.")
                return cls._instances[name]
            else:
                logger.debug(f"Creating new instance with name '{name}'.")
                instance = super(AsyncPeriodicExecutor, cls).__new__(cls)
                cls._instances[name] = instance
                instance._initialized = False  # Flag to prevent multiple initializations
                return instance

    @classmethod
    def get_instance(cls, name):
        """Access the singleton instance by name."""
        return cls._instances.get(name)

    def __init__(self, name, json_file_path=None):
        if getattr(self, '_initialized', False):
            return  # Avoid re-initialization
        self._initialized = True
        self.name = name
        self.json_file_path = json_file_path
        self.custom_tasks = {}  # Mapping of task names to configurations (hard-coded tasks)
        self.json_tasks = {}    # Mapping of task names to configurations (JSON-defined tasks)
        self.executor_tasks = {}  # Mapping of task names to asyncio Tasks
        self.loop_task = None
        self.task_lock = asyncio.Lock()  # To protect access to executor_tasks
        self.stop_event = asyncio.Event()  # Event to signal tasks to stop
        self.file_mtime = None  # To track JSON file modification time
        logger.info(f"Initialized AsyncPeriodicExecutor instance with name '{self.name}'.")

    async def start(self):
        """Start the execution loop."""
        self.on_start()
        try:
            # Align to the start of the next minute
            await self._wait_until_next_minute()
            self.loop_task = asyncio.create_task(self._run_loop())
            await self.loop_task
        finally:
            self.on_end()

    def on_start(self):
        """Function to execute when the loop starts."""
        logger.info(f"AsyncPeriodicExecutor '{self.name}' started.")

    def on_end(self):
        """Function to execute when the loop ends."""
        logger.info(f"AsyncPeriodicExecutor '{self.name}' stopped.")


    async def schedule_custom_task(
            self, func, interval_seconds=None, run_at=None, hourly= None, weekly_day=None, monthly_day=None, task_name=None
    ):
        """
        Schedule a custom (hard-coded) task.

        :param func: An async function to execute.
        :param interval_seconds: Execute the task at regular intervals (seconds).
        :param hourly: Execute the task at the first minute of each hour.
        :param run_at: Execute the task at a specific time daily (HH:MM).
        :param weekly_day: Execute the task weekly on a specific day (0=Monday, ..., 6=Sunday).
        :param monthly_day: Execute the task monthly on a specific day (1-31).
        :param task_name: Optional name for the task.
        """
        if not asyncio.iscoroutinefunction(func):
            raise ValueError("Function must be an async function.")

        task_info = None
        if interval_seconds is not None:
            task_info = {
                "type": "interval",
                "func": func,
                "interval": interval_seconds,
                "name": task_name or func.__name__,
                "source": "hardcoded"
            }
        elif run_at is not None:
            task_info = {
                "type": "daily",
                "func": func,
                "time": run_at,
                "name": task_name or func.__name__,
                "source": "hardcoded"
            }
        elif hourly is not None:
            task_info = {
                "type": "hourly",
                "func": func,
                "name": task_name or func.__name__,
                "source": "hardcoded"
            }
        elif weekly_day is not None:
            task_info = {
                "type": "weekly",
                "func": func,
                "day": weekly_day,
                "name": task_name or func.__name__,
                "source": "hardcoded"
            }
        elif monthly_day is not None:
            task_info = {
                "type": "monthly",
                "func": func,
                "day": monthly_day,
                "name": task_name or func.__name__,
                "source": "hardcoded"
            }
        else:
            raise ValueError(
                "Specify one of interval_seconds, run_at, weekly_day, or monthly_day."
            )

        self.custom_tasks[task_info["name"]] = task_info

        # Schedule the task immediately if the executor is running
        if self.loop_task and not self.loop_task.done():
            await self._schedule_task(task_info, source='hardcoded')



    async def _wait_until_next_minute(self):
        """Wait until the start of the next minute."""
        now = datetime.now()
        seconds_until_next_minute = 60 - now.second - now.microsecond / 1_000_000
        if seconds_until_next_minute > 0:
            logger.info(
                f"Waiting {seconds_until_next_minute:.2f} seconds until the next minute starts."
            )
            await asyncio.sleep(seconds_until_next_minute)

    async def _run_loop(self):
        """Run the main asynchronous loop."""
        # Schedule hard-coded tasks
        await self._schedule_hardcoded_tasks()
        # Initial load of tasks from the JSON file, if provided
        if self.json_file_path:
            await self.load_tasks_from_json()
            # Start the file watcher coroutine
            file_watcher_task = asyncio.create_task(self._watch_json_file())
        else:
            file_watcher_task = None

        # Wait for the stop event to be set
        await self.stop_event.wait()

        # Cancel all running tasks
        async with self.task_lock:
            for task in self.executor_tasks.values():
                task.cancel()
            self.executor_tasks.clear()

        # Cancel the file watcher task
        if file_watcher_task:
            file_watcher_task.cancel()
            try:
                await file_watcher_task
            except asyncio.CancelledError:
                pass

    async def _schedule_hardcoded_tasks(self):
        """Schedule hard-coded tasks."""
        for task_name, task_info in self.custom_tasks.items():
            await self._schedule_task(task_info, source='hardcoded')

    async def _watch_json_file(self):
        """Watch the JSON file for changes and reload tasks."""
        while not self.stop_event.is_set():
            try:
                await asyncio.sleep(1)  # Check every second
                current_mtime = os.path.getmtime(self.json_file_path)
                if self.file_mtime is None or current_mtime != self.file_mtime:
                    self.file_mtime = current_mtime
                    logger.info("Detected change in JSON file. Reloading tasks.")
                    await self.load_tasks_from_json()
            except Exception as e:
                logger.exception("Error watching JSON file.")
                await asyncio.sleep(5)  # Wait before retrying

    async def load_tasks_from_json(self):
        """Load tasks from the JSON file and update the executor."""
        try:
            with open(self.json_file_path, 'r') as f:
                tasks_data = json.load(f)

            # Convert list to dictionary keyed by task name
            tasks_dict = {task['name']: task for task in tasks_data}

            async with self.task_lock:
                # Update tasks
                await self._update_json_tasks(tasks_dict)

        except Exception as e:
            logger.exception("Error loading tasks from JSON file.")

    async def _update_json_tasks(self, tasks_dict):
        """Update tasks based on the new tasks dictionary from JSON."""
        # Cancel and remove tasks that are no longer active or present
        for task_name in list(self.json_tasks.keys()):
            new_task_info = tasks_dict.get(task_name)
            if not new_task_info or not new_task_info.get('is_active', False):
                logger.info(f"Removing JSON-defined task '{task_name}'.")
                await self._remove_task(task_name)

        # Add or update tasks
        for task_name, task_info in tasks_dict.items():
            if not task_info.get('is_active', False):
                continue  # Skip inactive tasks
            if task_name not in self.json_tasks:
                logger.info(f"Adding new JSON-defined task '{task_name}'.")
                await self._add_task(task_name, task_info, source='json')
            else:
                # Check if the task configuration has changed
                if task_info != self.json_tasks[task_name]:
                    logger.info(f"Updating JSON-defined task '{task_name}'.")
                    await self._remove_task(task_name)
                    await self._add_task(task_name, task_info, source='json')

    async def _add_task(self, task_name, task_info, source):
        """Add and schedule a new task."""
        if source == 'json':
            task_config = {
                "type": task_info.get('type'),
                "action": task_info.get('action'),
                "name": task_name,
                "source": "json"
            }

            # Scheduling parameters
            if task_config["type"] == "interval":
                task_config["interval"] = task_info.get("interval_seconds")
            elif task_config["type"] == "daily":
                task_config["time"] = task_info.get("time")
            elif task_config["type"] == "weekly":
                task_config["day"] = task_info.get("weekly_day")
            elif task_config["type"] == "monthly":
                task_config["day"] = task_info.get("monthly_day")
            else:
                logger.error(f"Unknown task type '{task_config['type']}' for task '{task_name}'.")
                return

            self.json_tasks[task_name] = task_info
            await self._schedule_task(task_config, source='json')
        elif source == 'hardcoded':
            # Already have task_info in the correct format
            self.custom_tasks[task_name] = task_info
            await self._schedule_task(task_info, source='hardcoded')
        else:
            logger.error(f"Unknown task source '{source}' for task '{task_name}'.")

    async def _remove_task(self, task_name):
        """Remove and cancel a task."""
        self.json_tasks.pop(task_name, None)
        self.custom_tasks.pop(task_name, None)
        task = self.executor_tasks.pop(task_name, None)
        if task:
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass

    async def _schedule_task(self, task_info, source):
        """Schedule a single task based on its type and source."""
        task_type = task_info["type"]
        task_name = task_info.get("name")
        scheduled_task = None

        if source == 'json':
            # For JSON-defined tasks
            scheduled_task = asyncio.create_task(self._run_generic_task(task_info))
        elif source == 'hardcoded':
            # For hard-coded tasks
            if task_type == "interval":
                scheduled_task = asyncio.create_task(self._run_interval(task_info))
            elif task_type == "daily":
                scheduled_task = asyncio.create_task(self._run_daily(task_info))
            elif task_type == "hourly":
                scheduled_task = asyncio.create_task(self._run_hourly(task_info))
            elif task_type == "weekly":
                scheduled_task = asyncio.create_task(self._run_weekly(task_info))
            elif task_type == "monthly":
                scheduled_task = asyncio.create_task(self._run_monthly(task_info))
            else:
                logger.error(f"Unknown task type: {task_type}")
                return
        else:
            logger.error(f"Unknown task source '{source}' for task '{task_name}'.")
            return

        async with self.task_lock:
            self.executor_tasks[task_name] = scheduled_task

    async def _run_generic_task(self, task_info):
        """Run a task based on its scheduling and action (JSON-defined tasks)."""
        task_type = task_info["type"]
        action = task_info["action"]
        task_name = task_info.get("name", "Unnamed Task")
        logger.info(f"Starting {task_type} task '{task_name}'.")

        while not self.stop_event.is_set():
            try:
                # Wait until the next scheduled time
                # (Same logic as before for scheduling)
                # ...

                # Execute the action
                await self.execute_action(action, task_name)
            except Exception as e:
                logger.exception(f"Exception occurred in task '{task_name}'.")
                break  # Exit the loop on error

        logger.info(f"Task '{task_name}' stopped.")

    async def _run_interval(self, task):
        """Run a custom task at specified intervals."""
        interval = task["interval"]
        func = task["func"]
        task_name = func.__name__
        logger.info(f"Starting interval task '{task_name}' every {interval} seconds.")
        while not self.stop_event.is_set():
            start_time = datetime.now()
            next_run = start_time + timedelta(seconds=interval)
            try:
                await func()
                duration = (datetime.now() - start_time).total_seconds()
                logger.info(
                    f"Task '{task_name}' executed successfully in {duration:.2f} seconds. Next run at {next_run}."
                )
            except Exception:
                logger.exception(f"Exception occurred in interval task '{task_name}'.")
            # Calculate the exact time to sleep to align with the interval
            sleep_time = interval - (datetime.now().timestamp() % interval)
            try:
                await asyncio.wait_for(self.stop_event.wait(), timeout=sleep_time)
            except asyncio.TimeoutError:
                continue  # Timeout occurred, loop continues
        logger.info(f"Interval task '{task_name}' stopped.")

    async def _run_hourly(self, task):
        """Run a custom task at the first minute of each hour."""
        func = task["func"]
        task_name = func.__name__
        logger.info(f"Starting hourly task '{task_name}' at the first minute of each hour.")

        while not self.stop_event.is_set():
            now = datetime.now()
            # Set the next run to the first minute of the next hour (e.g., 01:01, 02:01, etc.)
            next_run = (now + timedelta(hours=1)).replace(minute=1, second=0, microsecond=0)

            seconds_until_next_run = (next_run - now).total_seconds()
            logger.info(f"Task '{task_name}' scheduled to run at {next_run}.")

            try:
                # Wait until the next run time or until the stop event is set
                await asyncio.wait_for(self.stop_event.wait(), timeout=seconds_until_next_run)
                break  # Stop event was set
            except asyncio.TimeoutError:
                pass  # Timeout occurred, execute the task

            try:
                await func()  # Execute the task
                logger.info(f"Task '{task_name}' executed successfully. Next run at {next_run + timedelta(hours=1)}.")
            except Exception:
                logger.exception(f"Exception occurred in hourly task '{task_name}'.")

        logger.info(f"Hourly task '{task_name}' stopped.")

    async def _run_daily(self, task):
        """Run a custom task daily at a specific time."""
        target_time = datetime.strptime(task["time"], "%H:%M").time()
        func = task["func"]
        task_name = func.__name__
        logger.info(f"Starting daily task '{task_name}' at {target_time.strftime('%H:%M')} each day.")
        while not self.stop_event.is_set():
            now = datetime.now()
            next_run = datetime.combine(now.date(), target_time)
            if now.time() >= target_time:
                next_run += timedelta(days=1)
            seconds_until_next_run = (next_run - now).total_seconds()
            logger.info(f"Task '{task_name}' scheduled to run at {next_run}.")
            try:
                await asyncio.wait_for(self.stop_event.wait(), timeout=seconds_until_next_run)
                break  # Stop event was set
            except asyncio.TimeoutError:
                pass  # Timeout occurred, execute the task
            try:
                await func()
                logger.info(
                    f"Task '{task_name}' executed successfully. Next run at {next_run + timedelta(days=1)}."
                )
            except Exception:
                logger.exception(f"Exception occurred in daily task '{task_name}'.")
        logger.info(f"Daily task '{task_name}' stopped.")

    async def _run_weekly(self, task):
        """Run a custom task weekly on a specific day."""
        day_of_week = task["day"]
        func = task["func"]
        task_name = func.__name__
        logger.info(f"Starting weekly task '{task_name}' on day {day_of_week} (0=Monday, ..., 6=Sunday).")
        while not self.stop_event.is_set():
            now = datetime.now()
            days_ahead = (day_of_week - now.weekday()) % 7
            next_run = (now + timedelta(days=days_ahead)).replace(
                hour=0, minute=0, second=0, microsecond=0
            )
            if days_ahead == 0 and now.time() >= datetime.min.time():
                next_run += timedelta(weeks=1)
            seconds_until_next_run = (next_run - now).total_seconds()
            logger.info(f"Task '{task_name}' scheduled to run at {next_run}.")
            try:
                await asyncio.wait_for(self.stop_event.wait(), timeout=seconds_until_next_run)
                break  # Stop event was set
            except asyncio.TimeoutError:
                pass  # Timeout occurred, execute the task
            try:
                await func()
                logger.info(
                    f"Task '{task_name}' executed successfully. Next run at {next_run + timedelta(weeks=1)}."
                )
            except Exception:
                logger.exception(f"Exception occurred in weekly task '{task_name}'.")
        logger.info(f"Weekly task '{task_name}' stopped.")

    async def _run_monthly(self, task):
        """Run a custom task monthly on a specific day."""
        day_of_month = task["day"]
        func = task["func"]
        task_name = func.__name__
        logger.info(f"Starting monthly task '{task_name}' on day {day_of_month} of each month.")
        while not self.stop_event.is_set():
            now = datetime.now()
            year = now.year
            month = now.month

            if now.day >= day_of_month:
                # Move to the next month
                month += 1
                if month > 12:
                    month = 1
                    year += 1

            try:
                next_run = datetime(year, month, day_of_month)
            except ValueError:
                # Handle invalid day (e.g., February 30)
                last_day = (datetime(year, month + 1, 1) - timedelta(days=1)).day
                next_run = datetime(year, month, last_day)
                logger.warning(
                    f"Adjusted day for task '{task_name}' to the last day of the month: {next_run.day}"
                )

            seconds_until_next_run = (next_run - now).total_seconds()
            logger.info(f"Task '{task_name}' scheduled to run at {next_run}.")
            try:
                await asyncio.wait_for(self.stop_event.wait(), timeout=seconds_until_next_run)
                break  # Stop event was set
            except asyncio.TimeoutError:
                pass  # Timeout occurred, execute the task
            try:
                await func()
                logger.info(
                    f"Task '{task_name}' executed successfully. Next run at {next_run + timedelta(days=30)}."
                )
            except Exception:
                logger.exception(f"Exception occurred in monthly task '{task_name}'.")
        logger.info(f"Monthly task '{task_name}' stopped.")


    async def execute_action(self, action, task_name):
        """Execute an action based on its description."""
        action_type = action.get('type')
        if action_type == 'api_call':
            await self.handle_api_call(action, task_name)
        elif action_type == 'db_update':
            await self.handle_db_update(action, task_name)
        elif action_type == 'api_call_db_update':
            await self.handle_api_call_db_update(action, task_name)
        else:
            logger.error(f"Unknown action type '{action_type}' in task '{task_name}'.")

    async def handle_api_call(self, action, task_name):
        """Handle API call actions."""
        url = action.get('url')
        method = action.get('method', 'GET').upper()
        params = action.get('params', {})
        headers = action.get('headers', {})
        data = action.get('data', {})

        logger.info(f"Task '{task_name}': Making API call to {url} with method {method}.")

        async with aiohttp.ClientSession() as session:
            try:
                async with session.request(method, url, params=params, headers=headers, json=data) as response:
                    response_data = await response.json()
                    logger.info(f"Task '{task_name}': Received response: {response_data}")
                    # Process the response as needed
            except Exception as e:
                logger.exception(f"Task '{task_name}': API call failed.")

    async def handle_db_update(self, action, task_name):
        """Handle database update actions."""
        # Database connection parameters
        db_config = action.get('db_config', {})
        query = action.get('query')
        params = action.get('params', [])

        if not query:
            logger.error(f"Task '{task_name}': No query provided for DB update.")
            return

        logger.info(f"Task '{task_name}': Executing DB query.")

        try:
            pool = await aiomysql.create_pool(**db_config)
            async with pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(query, params)
                    await conn.commit()
                    logger.info(f"Task '{task_name}': DB update successful.")
            pool.close()
            await pool.wait_closed()
        except Exception as e:
            logger.exception(f"Task '{task_name}': DB update failed.")

    async def handle_api_call_db_update(self, action, task_name):
        """Handle actions that involve making an API GET request and updating the database with the results."""
        url = action.get('url')
        method = action.get('method', 'GET').upper()
        params = action.get('params', {})
        headers = action.get('headers', {})
        db_config = action.get('db_config', {})
        query = action.get('query')
        query_params_mapping = action.get('query_params_mapping', [])

        if not url or not query or not query_params_mapping:
            logger.error(f"Task '{task_name}': Missing required parameters for 'api_call_db_update' action.")
            return

        logger.info(f"Task '{task_name}': Making API call to {url} and updating DB.")

        async with aiohttp.ClientSession() as session:
            try:
                async with session.request(method, url, params=params, headers=headers) as response:
                    response_data = await response.json()
                    logger.debug(f"Task '{task_name}': Received response: {response_data}")

                    # Build query parameters based on the mapping
                    query_params = []
                    for key in query_params_mapping:
                        value = response_data
                        # Support nested keys using dot notation
                        for subkey in key.split('.'):
                            if isinstance(value, dict):
                                value = value.get(subkey)
                            else:
                                value = None
                                break
                        query_params.append(value)

                    # Now execute the DB update
                    await self.handle_db_update({
                        'db_config': db_config,
                        'query': query,
                        'params': query_params
                    }, task_name)
            except Exception as e:
                logger.exception(f"Task '{task_name}': API call or DB update failed.")



