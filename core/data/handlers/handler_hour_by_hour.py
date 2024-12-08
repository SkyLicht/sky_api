from core.data.models.hour_by_hour_model import HourByHourModel
from core.data.models.request_model import RequestWeekEffModel
from core.data.types import ShiftType, OutputType
from core.db.util import generate_custom_id


def handle_normalized_hbh(hbh: list[HourByHourModel]) -> list[HourByHourModel]:
    """Handle the normalized hour by hour."""
    _return: list[HourByHourModel] = []
    for hour in range(0, 24):
        for _hour in hbh:
            if _hour.hour == hour:
                _return.append(_hour)
                break
        else:
            _return.append(HourByHourModel(line="J09", date="2024-11-21", hour=hour, smt_in=0, smt_out=0, packing=0))

    _return.sort(key=lambda x: x.hour)

    return _return


def handle_total_output_by_shift_and_output(hbh: list[HourByHourModel], output: OutputType, shift: ShiftType):
    """Handle the output."""
    # Define index ranges for each shift
    shift_ranges = {
        shift.ALL: slice(0, 23),
        ShiftType.FIRST: slice(6, 16),
        ShiftType.SECOND: slice(16, 23),
        ShiftType.THIRD: slice(0, 6),
    }

    # Determine the attribute to sum based on the output type
    # smt_in, smt_out, or packing are the possible attributes in the HourByHourModel. HourByHourModel is the representation of the data store in the DB.
    output_attr = {
        OutputType.PACKING: "packing",
        OutputType.INPUT: "smt_in",
        OutputType.OUTPUT: "smt_out",
    }.get(output)

    if not output_attr:
        raise ValueError(f"Unsupported output type: {output}")

    # Get the range for the specified shift
    shift_range = shift_ranges.get(shift)
    if not shift_range:
        raise ValueError(f"Unsupported shift type: {shift}")

    # Sum the relevant attribute for the selected shift
    return sum(getattr(hour, output_attr) for hour in hbh[shift_range])


def handle_shift_to_work_hours(shift: ShiftType, planned_hours: float) -> float:
    """Handle the shift to work hours."""
    return {
        ShiftType.ALL: planned_hours,
        ShiftType.FIRST: 9.25,
        ShiftType.SECOND: 7.75,
        ShiftType.THIRD: 6.25,
    }.get(shift, 0)


def handle_ie_kpi(total_output: int, target_oee: float, uph: int, planned_hours: float) -> dict:
    """Handle the IE KPI: OEE, Efficiency, and Utilization.
    total_output: The total output for the period.
    target_oee: The target OEE for the period.
    uph: The UPH for the line.
    planned_hours: The planned hours for the period."""

    # print(f"total_output: {total_output}")
    # print(f"target_oee: {target_oee}")
    # print(f"uph: {uph}")
    # print(f"planned_hours: {planned_hours}")

    # Calculate the target output for the planned hours
    uph_installed_capacity = uph * target_oee
    target_output_for_efficiency = round(uph_installed_capacity * planned_hours)
    target_output_for_oee = round(uph * planned_hours)

    # print(f"uph_installed_capacity: {uph_installed_capacity}")
    # print(f"target_output_for_efficiency: {target_output_for_efficiency}")
    # print(f"target_output_for_oee: {target_output_for_oee}")

    # Calculate the OEE
    oee = (total_output / target_output_for_oee)

    # Calculate the efficiency
    efficiency = (total_output / target_output_for_efficiency)

    # Calculate the utilization
    utilization = 0

    return {
        "oee": oee,
        "efficiency": efficiency,
        "utilization": utilization,
        "details": {
            "planed_hours": planned_hours,
            "uph_i": uph_installed_capacity,
            "target_output_for_efficiency": target_output_for_efficiency,
            "target_output_for_oee": target_output_for_oee
        }
    }


def handle_weekly_kpi(request_body: RequestWeekEffModel, data) -> dict:
    """Handle the weekly KPI."""
    _week_summary = {
        "id": generate_custom_id(),
        "week": request_body.week,
        "days": [],
        "week_summary": {
            "efficiency": 0.0,
            "oee": 0.0,
            "utilization": 0.0
        },

    }

    try:

        for records in request_body.dates:
            _day = data.get(records.day, None)
            if _day is None:
                continue
            _line_and_eff = []
            for line in records.lines:

                _line = _day.get(line.name, None)
                if _line is None:
                         continue

                _total = handle_total_output_by_shift_and_output(
                    hbh=handle_normalized_hbh([HourByHourModel(**record) for record in _line['hour_by_hour']]),
                    output=OutputType.from_string(line.output),
                    shift=ShiftType.from_string(line.shift))
                kpi = handle_ie_kpi(
                    total_output=_total,
                    uph=_line['platform']['uph'],
                    planned_hours=handle_shift_to_work_hours(shift=ShiftType.from_string(line.shift),
                                                             planned_hours=_line['work_plan']['planned_hours']),
                    target_oee=_line['work_plan']['target_oee']
                )

                _line_and_eff.append({
                    "id": generate_custom_id(),
                    "line": line.name,
                    "date": records.day,
                    "shift": line.shift,
                    "output": line.output,
                    "target_oee": _line['work_plan']['target_oee'],
                    "uph": _line['platform']['uph'],
                    "uph_installed": kpi['details'].get('uph_i', 0),
                    "target_output_installed": kpi['details'].get('target_output_for_efficiency', 0),
                    "target_output_design": kpi['details'].get('target_output_for_oee', 0),
                    "total_output": _total,
                    "planned_hours": kpi['details'].get('planed_hours', 0),
                    "efficiency": round(kpi.get('efficiency') * 100, 2),
                    "oee": round(kpi.get('oee') * 100, 2),
                    "utilization": round(kpi.get('utilization') * 100, 2)

                })

            if len(_line_and_eff) == 0:
                continue


            _week_summary['days'].append({
                "id": generate_custom_id(),
                "day": records.day,
                "lines": _line_and_eff,
                "summary": {
                    "efficiency": round(sum([line['efficiency'] for line in _line_and_eff]) / len(_line_and_eff), 2),
                    "oee": round(sum([line['oee'] for line in _line_and_eff]) / len(_line_and_eff), 2),
                    "utilization": round(sum([line['utilization'] for line in _line_and_eff]) / len(_line_and_eff), 2)
                }
            })

        _week_summary['week_summary']['efficiency'] = round(
            sum([day['summary']['efficiency'] for day in _week_summary['days']]) / len(_week_summary['days']), 2)
        _week_summary['week_summary']['oee'] = round(
            sum([day['summary']['oee'] for day in _week_summary['days']]) / len(_week_summary['days']), 2)
        _week_summary['week_summary']['utilization'] = round(
            sum([day['summary']['utilization'] for day in _week_summary['days']]) / len(_week_summary['days']), 2)

    except Exception as e:

        print(e)


    return _week_summary
