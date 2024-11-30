from core.api.querys.work_plna_query import WorkPlanQuery


async def handle_both_dates(query: WorkPlanQuery):
    work_plan_data = {
        "line": query.line,
        "start_date": query.start_date,
        "end_date": query.end_date,
        "factory": query.factory,
        "plan_details": f"Work plan from {query.start_date} to {query.end_date}"
    }
    return work_plan_data

async def handle_start_date_only(query: WorkPlanQuery):
    work_plan_data = {
        "line": query.line,
        "start_date": query.start_date,
        "end_date": None,
        "factory": query.factory,
        "plan_details": f"Work plan starting from {query.start_date}"
    }
    return work_plan_data

async def handle_end_date_only(query: WorkPlanQuery):
    work_plan_data = {
        "line": query.line,
        "start_date": None,
        "end_date": query.end_date,
        "factory": query.factory,
        "plan_details": f"Work plan up to {query.end_date}"
    }
    return work_plan_data

async def handle_line_only(query: WorkPlanQuery):
    work_plan_data = {
        "line": query.line,
        "start_date": None,
        "end_date": None,
        "factory": query.factory,
        "plan_details": f"Work plan for line {query.line}"
    }
    return work_plan_data