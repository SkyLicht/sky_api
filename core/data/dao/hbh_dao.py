import json

from colorama import Fore, Style
from sqlalchemy import and_

from core.data.handlers.translator import translate_hour_by_hour_schema_list_to_model_list
from core.data.models.hour_by_hour_model import HourByHourModel, PlatformModel, WorkPlanModel
from core.data.schemas.hour_by_hour_schema import HourByHourSchema, PlatformSchema, WorkPlanSchema
from core.db.util import QueryResult, QueryResultError, QueryResultErrorType


class HbhDAO:
    def __init__(self, connection):
        self.session = connection
        # logger

    def query_all(self) -> list[HourByHourModel] | None:
        try:
            result = self.session.query(HourByHourSchema).all()  # Assuming HourByHour is a mapped class
            print(f"{Fore.GREEN}Data fetched from hour_by_hour.{Style.RESET_ALL}")

            return translate_hour_by_hour_schema_list_to_model_list(result)

        except Exception as e:
            print(f"{Style.BRIGHT}{e}{Style.RESET_ALL}")
            return None

        finally:
            self.session.close()
            print(f"{Fore.GREEN}Session close{Style.RESET_ALL}")

    def query_add_record(self, record):
        try:
            self.session.add(record)
            self.session.commit()
            print(f"{Fore.GREEN}Record pushed{Style.RESET_ALL}")
            self.session.close()
            print(f"{Fore.GREEN}Session close{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}{e}{Style.RESET_ALL}")

    def query_add_records(self, records):
        try:
            for record in records:
                self.session.add(record)
            self.session.commit()
            print(f"{Fore.GREEN}All hour by hours pushed{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}{e}{Style.RESET_ALL}")
            self.session.rollback()
        finally:
            self.session.close()
            print(f"{Fore.GREEN}Session close{Style.RESET_ALL}")

    # if record exists, update it. Otherwise, insert it
    def query_update_hour(self, record):
        try:
            last_hour = self.session.query(HourByHourSchema).filter(HourByHourSchema.date == record.date).filter(
                HourByHourSchema.hour == record.hour).filter(HourByHourSchema.line == record.line).first()
            if last_hour is not None:
                last_hour.smt_in = record.smt_in
                last_hour.smt_out = record.smt_out
                last_hour.packing = record.packing
                self.session.commit()
                print(f"{Fore.GREEN}Record {Fore.YELLOW}{record.to_dict()} updated{Style.RESET_ALL}")
            else:
                self.session.add(record)
                self.session.commit()
                print(f"{Fore.GREEN}Record {Fore.YELLOW}{record.to_dict()} pushed{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}{e}{Style.RESET_ALL}")
            self.session.close()
        finally:
            print(f"{Fore.GREEN}Session close{Style.RESET_ALL}")

    def query_update_hours(self, records):
        try:
            for record in records:
                last_hour = self.session.query(HourByHourSchema).filter(HourByHourSchema.date == record.date).filter(
                    HourByHourSchema.hour == record.hour).filter(HourByHourSchema.line == record.line).first()
                if last_hour is not None:
                    last_hour.smt_in = record.smt_in
                    last_hour.smt_out = record.smt_out
                    last_hour.packing = record.packing
                    print(f"{Fore.GREEN}Record {Fore.YELLOW}{record.to_dict()} {Fore.BLUE}updated{Style.RESET_ALL}")
                else:
                    self.session.add(record)
                    print(f"{Fore.GREEN}Record {Fore.YELLOW}{record.to_dict()} {Fore.BLUE}pushed{Style.RESET_ALL}")
            self.session.commit()
            return True
        except Exception as e:
            print(f"{Fore.RED}{e}{Style.RESET_ALL}")
            self.session.rollback()
        finally:
            self.session.close()
            print(f"{Fore.GREEN}Session close{Style.RESET_ALL}")


class PlatformDAO:
    def __init__(self, connection):
        self.session = connection

    def query_all(self) -> list[PlatformModel] | None:
        try:
            result = self.session.query(PlatformSchema).all()
            print(f"{Fore.GREEN}Data fetched from platform.{Style.RESET_ALL}")
            return []
        except Exception as e:
            print(f"{Fore.RED}{e}{Style.RESET_ALL}")
            self.session.close()
            return None

    def query_add_record(self, record: PlatformSchema):
        try:
            self.session.add(record)
            self.session.commit()
            print(f"{Fore.GREEN}Record pushed{Style.RESET_ALL}")
            print(f"{Fore.GREEN}Session close{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}{e}{Style.RESET_ALL}")
        finally:
            self.session.close()
            print(f"{Fore.GREEN}Session close{Style.RESET_ALL}")

    def query_add_records(self, records: list[PlatformSchema]):
        try:
            for record in records:
                self.session.add(record)

            self.session.commit()
            print(f"{Fore.GREEN}All platforms pushed{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}{e}{Style.RESET_ALL}")
            self.session.rollback()
        finally:
            self.session.close()
            print(f"{Fore.GREEN}Session close{Style.RESET_ALL}")


class WorkPlanDAO:
    def __init__(self, connection):
        self.session = connection

    def query_all(self) -> list[WorkPlanModel] | None:
        try:
            result = self.session.query(WorkPlanSchema).all()
            print(f"{Fore.GREEN}Data fetched from work_plan.{Style.RESET_ALL}")
            return result
        except Exception as e:
            print(f"{Fore.RED}{e}{Style.RESET_ALL}")
            self.session.close()
            return None

    def query_add_record(self, record: WorkPlanSchema):
        try:
            self.session.add(record)
            self.session.commit()
            print(f"{Fore.GREEN}Record pushed{Style.RESET_ALL}")
            print(f"{Fore.GREEN}Session close{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}{e}{Style.RESET_ALL}")
        finally:
            self.session.close()
            print(f"{Fore.GREEN}Session close{Style.RESET_ALL}")

    def query_add_records(self, records: list[WorkPlanSchema]):
        try:
            for record in records:
                self.session.add(record)

            self.session.commit()
            print(f"{Fore.GREEN}All work_plans pushed{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}{e}{Style.RESET_ALL}")
            self.session.rollback()
        finally:
            self.session.close()
            print(f"{Fore.GREEN}Session close{Style.RESET_ALL}")

    def get_work_hour_by_week(self, week: int = None, date: str = None, date_range: tuple = None, dates: list = None):
        """
        Join PlatformSchema, WorkPlanSchema, and HourByHourSchema, filtered by week.
        :param week: The week number to filter by.
        :param date: The date to filter by.
        :param date_range: The date range to filter by.
        :param dates: A list of dates to filter by.
        :return: List of joined records as dictionaries.
        """
        query = (
            self.session.query(
                WorkPlanSchema,
                PlatformSchema,
                HourByHourSchema
            )
            .join(
                PlatformSchema,
                WorkPlanSchema.platform_id == PlatformSchema.id
            )
            .join(
                HourByHourSchema,
                and_(
                    WorkPlanSchema.line == HourByHourSchema.line,
                    WorkPlanSchema.date == HourByHourSchema.date
                )
            )
        )

        # Apply filters dynamically
        if week:
            query = query.filter(WorkPlanSchema.week == week)
        if date:
            query = query.filter(WorkPlanSchema.date == date)
        if date_range:
            query = query.filter(WorkPlanSchema.date.between(date_range[0], date_range[1]))
        if dates:
            query = query.filter(WorkPlanSchema.date.in_(dates))
        # Execute query and fetch results
        results = query.all()

        print(f"{Fore.GREEN}Data fetched from work_plan, platform, and hour_by_hour.{Style.RESET_ALL}")

        by_work_plan = {}
        for work_plan, platform, hour in results:

            if work_plan.date not in by_work_plan:
                by_work_plan[work_plan.date] = {}
            if work_plan.line not in by_work_plan[work_plan.date]:
                by_work_plan[work_plan.date][work_plan.line] = {
                    "work_plan": work_plan.to_dic_short(),
                    "platform": platform.to_dic_short(),
                    "hour_by_hour": []
                }

            by_work_plan[work_plan.date][work_plan.line]['hour_by_hour'].append(hour.to_dict())

        # sort hour_by_hour records by hour
        for date, lines in by_work_plan.items():
            for line, records in lines.items():
                records['hour_by_hour'] = sorted(records['hour_by_hour'], key=lambda x: x['hour'])

        # print(json.dumps(by_work_plan, indent=4))
        return QueryResult(data=by_work_plan)

    def query_create_record(self, record: WorkPlanSchema) -> QueryResult:

        find_platform = self.session.query(PlatformSchema).filter(
            PlatformSchema.id == record.platform_id
        ).first()

        if find_platform is None:
            return QueryResult(error=QueryResultError(message=f"Platform with id {record.platform_id} not found",
                                                      error_type=QueryResultErrorType.DATABASE_ERROR, tip=""))

        find_work_plan = self.session.query(WorkPlanSchema).filter(
            WorkPlanSchema.date == record.date,
            WorkPlanSchema.line == record.line,
            WorkPlanSchema.factory == record.factory
        ).first()

        if find_work_plan:
            find_work_plan.uph_i = record.uph_i
            find_work_plan.target_oee = record.target_oee
            find_work_plan.planned_hours = record.planned_hours
            find_work_plan.week = record.week
            find_work_plan.state = record.state
            self.session.commit()
            return QueryResult(data=find_work_plan)
        else:
            self.session.add(record)
            self.session.commit()
            return QueryResult(data=record)








































