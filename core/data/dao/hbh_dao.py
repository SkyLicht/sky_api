from colorama import Fore, Style

from core.data.handlers.translator import translate_hour_by_hour_schema_list_to_model_list
from core.data.models.hour_by_hour_model import HourByHourModel
from core.data.schemas.hour_by_hour_schema import HourByHourSchema


class HbhDAO:
    def __init__(self, connection):
        self.session = connection
        # logger

    def query_all(self)-> list[HourByHourModel] | None:
        try:
            result = self.session.query(HourByHourSchema).all()  # Assuming HourByHour is a mapped class
            print(f"{Fore.GREEN}Data fetched from hour_by_hour.{Style.RESET_ALL}")
            return translate_hour_by_hour_schema_list_to_model_list(result)

        except Exception as e:
            print(f"{Style.BRIGHT}{e}{Style.RESET_ALL}")
            return None


    def query_add_record(self, record):
        try:
            self.session.add(record)
            self.session.commit()
            print(f"{Fore.GREEN}Record pushed{Style.RESET_ALL}")
            self.session.close()
            print(f"{Fore.GREEN}Session close{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}{e}{Style.RESET_ALL}")


    def query_add_all_records(self, records):
        try:
            for record in records:
                self.session.add(record)
            self.session.commit()
            print(f"{Fore.GREEN}All users pushed{Style.RESET_ALL}")
            print(f"{Fore.GREEN}Session close{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}{e}{Style.RESET_ALL}")
            self.session.rollback()
        finally:
            self.session.close()
            print(f"{Fore.GREEN}Session close{Style.RESET_ALL}")

    # if record exists, update it. Otherwise, insert it
    def query_update_last_hour(self, record):
        try:
            last_hour = self.session.query(HourByHourSchema).filter(HourByHourSchema.date == record.date).filter(
                HourByHourSchema.hour == record.hour).filter(HourByHourSchema.line == record.line).first()
            if last_hour is not None:
                last_hour.smt_in = record.smt_in
                last_hour.smt_out = record.smt_out
                last_hour.packing = record.packing
                self.session.commit()
                print(f"{Fore.GREEN}Record {Fore.YELLOW}{record.to_dic()} updated{Style.RESET_ALL}")
            else:
                self.session.add(record)
                self.session.commit()
                print(f"{Fore.GREEN}Record {Fore.YELLOW}{record.to_dic()} pushed{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}{e}{Style.RESET_ALL}")
        finally:
            self.session.close()
            print(f"{Fore.GREEN}Session close{Style.RESET_ALL}")