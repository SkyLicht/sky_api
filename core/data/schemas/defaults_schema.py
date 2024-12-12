from core.data.schemas.all_schemas import SectionSchema, AssignmentSchema, DepartmentSchema, PositionSchema, \
    LayoutSchema
from core.data.types import SectionNickname

assignment_ing = AssignmentSchema(name="Engineer")
assignment_sup = AssignmentSchema(name="Supervisor")
assignment_tech = AssignmentSchema(name="Technician")
assignment_op = AssignmentSchema(name="Operator")


def return_assignments():
    return [assignment_ing, assignment_sup, assignment_tech, assignment_op]


departments_schemas = [
    DepartmentSchema(name="Automation", factory='A6'),
    DepartmentSchema(name="Equipment", factory='A6'),
    DepartmentSchema(name="Industrial Engineer", factory='A6'),
    DepartmentSchema(name="Production", factory='A6'),
    DepartmentSchema(name="Programing", factory='A6'),
    DepartmentSchema(name="Quality", factory='A6'), ]


def return_sections():
    return departments_schemas

positions_schemas = [
    PositionSchema(name="Engineer"),
    PositionSchema(name="Supervisor"),
    PositionSchema(name="Technician SMT"),
]

def return_positions():
    return positions_schemas

sections_schemas = [
    SectionSchema(name="Automation", nickname=SectionNickname.AU.value, factory='A6'),
    SectionSchema(name="Equipment SMT", nickname=SectionNickname.EES.value, factory='A6'),
    SectionSchema(name="Equipment Packing", nickname=SectionNickname.EEP.value, factory='A6'),
    SectionSchema(name="Production", nickname=SectionNickname.PD.value, factory='A6'),
    SectionSchema(name="Industrial Engineering", nickname=SectionNickname.IE.value, factory='A6'),
    SectionSchema(name="Quality", nickname=SectionNickname.QA.value, factory='A6'), ]



layout_j01 = [
    LayoutSchema(
        index= 1,
        is_ct= True,
        version= 1,
        station_id= "cNNz99cpQpmcuEc",
        line_id=  "lxL6Pz3KSOmnefj",
        layout_section_id= "3oKQl-OoSVC2TWf"
    ),
    LayoutSchema(
        index= 2,
        is_ct= True,
        version= 1,
        station_id= "qUhjQU75QCKW_eu",
        line_id= "lxL6Pz3KSOmnefj",
        layout_section_id= "3oKQl-OoSVC2TWf"
    ),
    LayoutSchema(
        index= 3,
        is_ct= True,
        version= 1,
        station_id= "ygc6_l0dTlesAf5",
        line_id= "lxL6Pz3KSOmnefj",
        layout_section_id= "3oKQl-OoSVC2TWf"
    ),
    LayoutSchema(
        index= 4,
        is_ct= True,
        version= 1,
        station_id= "_tFYJxleTrGZGfB",
        line_id= "lxL6Pz3KSOmnefj",
        layout_section_id= "3oKQl-OoSVC2TWf"
    ),
    LayoutSchema(
        index= 5,
        is_ct= True,
        version= 1,
        station_id= "Jbe8mUtWRBuMXak",
        line_id= "lxL6Pz3KSOmnefj",
        layout_section_id= "3oKQl-OoSVC2TWf"
    ),
    LayoutSchema(
        index= 6,
        is_ct= True,
        version= 1,
        station_id= "vlkpEjlvSKqru9F",
        line_id= "lxL6Pz3KSOmnefj",
        layout_section_id= "3oKQl-OoSVC2TWf"
    ),
    LayoutSchema(
        index= 7,
        is_ct= True,
        version= 1,
        station_id= "jHKjyGnQQ_qfgnj",
        line_id= "lxL6Pz3KSOmnefj",
        layout_section_id= "3oKQl-OoSVC2TWf"
    ),
    LayoutSchema(
        index= 8,
        is_ct= True,
        version= 1,
        station_id= "d_SjoOTFR9OZsom",
        line_id= "lxL6Pz3KSOmnefj",
        layout_section_id= "3oKQl-OoSVC2TWf"
    ),
    LayoutSchema(
        index= 9,
        is_ct= True,
        version= 1,
        station_id= "GEEwowSlTvmepmq",
        line_id= "lxL6Pz3KSOmnefj",
        layout_section_id= "3oKQl-OoSVC2TWf"
    ),
    LayoutSchema(
        index= 10,
        is_ct= True,
        version= 1,
        station_id= "G-MGdovFTR2HsjT",
        line_id= "lxL6Pz3KSOmnefj",
        layout_section_id= "3oKQl-OoSVC2TWf"
    ),
    LayoutSchema(
        index= 11,
        is_ct= True,
        version= 1,
        station_id= "H8OucfcrQdedjIC",
        line_id= "lxL6Pz3KSOmnefj",
        layout_section_id= "3oKQl-OoSVC2TWf"
    ),
    LayoutSchema(
        index= 12,
        is_ct= True,
        version= 1,
        station_id= "0KpgoRocTEaDH0q",
        line_id= "lxL6Pz3KSOmnefj",
        layout_section_id= "tW2BtQcYR9ud6F4"
    ),
    LayoutSchema(
        index= 13,
        is_ct= True,
        version= 1,
        station_id= "4H4iyr3nSqeGbCA",
        line_id= "lxL6Pz3KSOmnefj",
        layout_section_id= "tW2BtQcYR9ud6F4"
    ),
    LayoutSchema(
        index= 14,
        is_ct= True,
        version= 1,
        station_id= "_tFYJxleTrGZGfB",
        line_id= "lxL6Pz3KSOmnefj",
        layout_section_id= "tW2BtQcYR9ud6F4"
    ),
    LayoutSchema(
        index= 15,
        is_ct= True,
        version= 1,
        station_id= "Jbe8mUtWRBuMXak",
        line_id= "lxL6Pz3KSOmnefj",
        layout_section_id= "tW2BtQcYR9ud6F4"
    ),
    LayoutSchema(
        index= 16,
        is_ct= True,
        version= 1,
        station_id= "vlkpEjlvSKqru9F",
        line_id= "lxL6Pz3KSOmnefj",
        layout_section_id= "tW2BtQcYR9ud6F4"
    ),
    LayoutSchema(
        index= 17,
        is_ct= True,
        version= 1,
        station_id= "jHKjyGnQQ_qfgnj",
        line_id= "lxL6Pz3KSOmnefj",
        layout_section_id= "tW2BtQcYR9ud6F4"
    ),
    LayoutSchema(
        index= 18,
        is_ct= True,
        version= 1,
        station_id= "slp-H2FtQ_KDAuY",
        line_id= "lxL6Pz3KSOmnefj",
        layout_section_id= "tW2BtQcYR9ud6F4"
    ),
    LayoutSchema(
        index= 19,
        is_ct= True,
        version= 1,
        station_id= "FHcdu_gZRSSo8cp",
        line_id= "lxL6Pz3KSOmnefj",
        layout_section_id= "tW2BtQcYR9ud6F4"
    ),
    LayoutSchema(
        index= 20,
        is_ct= True,
        version= 1,
        station_id= "aw-okrCRSyCuz9W",
        line_id= "lxL6Pz3KSOmnefj",
        layout_section_id= "tW2BtQcYR9ud6F4"
    ),
    LayoutSchema(
        index= 21,
        is_ct= True,
        version= 1,
        station_id= "6WomxVDnQCGWlH7",
        line_id= "lxL6Pz3KSOmnefj",
        layout_section_id= "tW2BtQcYR9ud6F4"
    ),
    LayoutSchema(
        index= 22,
        is_ct= True,
        version= 1,
        station_id= "FgtWb0paRnaO01-",
        line_id= "lxL6Pz3KSOmnefj",
        layout_section_id= "tW2BtQcYR9ud6F4"
    ),
    LayoutSchema(
        index= 23,
        is_ct= True,
        version= 1,
        station_id= "ooPBLDGZQwGNh_m",
        line_id= "lxL6Pz3KSOmnefj",
        layout_section_id= "tW2BtQcYR9ud6F4"
    ),
    LayoutSchema(
        index= 24,
        is_ct= True,
        version= 1,
        station_id= "MTorvp7tTLOkWgx",
        line_id= "lxL6Pz3KSOmnefj",
        layout_section_id= "tW2BtQcYR9ud6F4"
    ),
    LayoutSchema(
        index= 25,
        is_ct= True,
        version= 1,
        station_id= "c5tKgFkPTjKNVjb",
        line_id= "lxL6Pz3KSOmnefj",
        layout_section_id= "tW2BtQcYR9ud6F4"
    ),
    LayoutSchema(
        index= 26,
        is_ct= True,
        version= 1,
        station_id= "SodCoStmS_WmH5V",
        line_id= "lxL6Pz3KSOmnefj",
        layout_section_id= "tW2BtQcYR9ud6F4"
    ),
    LayoutSchema(
        index= 27,
        is_ct= True,
        version= 1,
        station_id= "9EvzYQjZTaKXH9l",
        line_id= "lxL6Pz3KSOmnefj",
        layout_section_id= "tW2BtQcYR9ud6F4"
    ),
    LayoutSchema(
        index= 28,
        is_ct= True,
        version= 1,
        station_id= "KE-BpJy_Qz-diAk",
        line_id= "lxL6Pz3KSOmnefj",
        layout_section_id= "tW2BtQcYR9ud6F4"
    ),
    LayoutSchema(
        index= 29,
        is_ct= True,
        version= 1,
        station_id= "sKDkzR3VTjWCFDi",
        line_id= "lxL6Pz3KSOmnefj",
        layout_section_id= "xQLyjx92QryA2tO"
    ),
    LayoutSchema(
        index= 30,
        is_ct= True,
        version= 1,
        station_id= "SU-AaOV1T6SI0SH",
        line_id= "lxL6Pz3KSOmnefj",
        layout_section_id= "xQLyjx92QryA2tO"
    ),
    LayoutSchema(
        index= 31,
        is_ct= True,
        version= 1,
        station_id= "47YfJyNFSduh1w9",
        line_id= "lxL6Pz3KSOmnefj",
        layout_section_id= "xQLyjx92QryA2tO"
    ),
    LayoutSchema(
        index= 32,
        is_ct= True,
        version= 1,
        station_id= "7EX92Y59QR-q_hJ",
        line_id= "lxL6Pz3KSOmnefj",
        layout_section_id= "xQLyjx92QryA2tO"
    ),
    LayoutSchema(
        index= 33,
        is_ct= True,
        version= 1,
        station_id= "LTJuggqNTJez3wb",
        line_id= "lxL6Pz3KSOmnefj",
        layout_section_id= "xQLyjx92QryA2tO"
    ),
    LayoutSchema(
        index= 34,
        is_ct= True,
        version= 1,
        station_id= "2I3ca2y6QF2x-uF",
        line_id= "lxL6Pz3KSOmnefj",
        layout_section_id= "xQLyjx92QryA2tO"
    ),
    LayoutSchema(
        index= 35,
        is_ct= True,
        version= 1,
        station_id= "YYlN2RSbTr6y5-E",
        line_id= "lxL6Pz3KSOmnefj",
        layout_section_id= "xQLyjx92QryA2tO"
    ),
    LayoutSchema(
        index= 36,
        is_ct= True,
        version= 1,
        station_id= "7p9gvu-FTNOk0l2",
        line_id= "lxL6Pz3KSOmnefj",
        layout_section_id= "xQLyjx92QryA2tO"
    ),
    LayoutSchema(
        index= 37,
        is_ct= True,
        version= 1,
        station_id= "YcPhUrS1RTCdAeI",
        line_id= "lxL6Pz3KSOmnefj",
        layout_section_id= "xQLyjx92QryA2tO"
    ),
    LayoutSchema(
        index= 38,
        is_ct= True,
        version= 1,
        station_id= "udR_RE1wQjGjVo_",
        line_id= "lxL6Pz3KSOmnefj",
        layout_section_id= "xQLyjx92QryA2tO"
    ),
    LayoutSchema(
        index= 39,
        is_ct= True,
        version= 1,
        station_id= "FRBguAzRQ3Odbr3",
        line_id= "lxL6Pz3KSOmnefj",
        layout_section_id= "xQLyjx92QryA2tO"
    ),
    LayoutSchema(
        index= 40,
        is_ct= True,
        version= 1,
        station_id= "udR_RT1wQjGjVo4",
        line_id= "lxL6Pz3KSOmnefj",
        layout_section_id= "xQLyjx92QryA2tO"
    ),
    LayoutSchema(
        index= 41,
        is_ct= True,
        version= 1,
        station_id= "6Sf0iIoGSwKhbvy",
        line_id= "lxL6Pz3KSOmnefj",
        layout_section_id= "xQLyjx92QryA2tO"
    ),
    LayoutSchema(
        index= 42,
        is_ct= True,
        version= 1,
        station_id= "jn-FrBjSQgGm3Zs",
        line_id= "lxL6Pz3KSOmnefj",
        layout_section_id= "xQLyjx92QryA2tO"
    ),
    LayoutSchema(
        index= 43,
        is_ct= True,
        version= 1,
        station_id= "qv6dp7uAQua98nb",
        line_id= "lxL6Pz3KSOmnefj",
        layout_section_id= "xQLyjx92QryA2tO"
    ),
    LayoutSchema(
        index= 44,
        is_ct= True,
        version= 1,
        station_id= "YPsYvYAATEWham9",
        line_id= "lxL6Pz3KSOmnefj",
        layout_section_id= "xQLyjx92QryA2tO"
    ),
    LayoutSchema(
        index= 45,
        is_ct= True,
        version= 1,
        station_id= "2I3ca7y6QF2x-uj",
        line_id= "lxL6Pz3KSOmnefj",
        layout_section_id= "xQLyjx92QryA2tO"
    ),
    LayoutSchema(
        index= 46,
        is_ct= True,
        version= 1,
        station_id= "YYWPJK6GSLetTcW",
        line_id= "lxL6Pz3KSOmnefj",
        layout_section_id= "xQLyjx92QryA2tO"
    ),
    LayoutSchema(
        index= 47,
        is_ct= True,
        version= 1,
        station_id= "IFpYG1ZUSdOFdft",
        line_id= "lxL6Pz3KSOmnefj",
        layout_section_id= "xQLyjx92QryA2tO"
    ),
    LayoutSchema(
        index= 48,
        is_ct= True,
        version= 1,
        station_id= "MktYRIrUSxe9lTS",
        line_id= "lxL6Pz3KSOmnefj",
        layout_section_id= "xQLyjx92QryA2tO"
    )


]

def return_layout():
    return layout_j01