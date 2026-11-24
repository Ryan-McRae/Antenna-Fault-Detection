from src.utils import dbman


def create_tables():
    queries = ["""
    create table temp_set as 
        select * from dataset
    """,
    """
    create table train as 
        select * from temp_set
        with no data
    """,
    """
    create table test as 
        select * from temp_set
        with no data
    """,
    """
    create table val as 
        select * from temp_set
        with no data
    """
    ]
    q = dbman.n_create(queries=queries)
    if q:
        print("Completed")
    else:
        print("Failed")

def ttv_split(pcts:list=[70,20,10],
              feature:str="Fault_Type",
              y:list=[0,1,2,3,4,5]):

    tables = ["train","test","val"]

    for _, val in enumerate(y):
        query = f"""
        create table split_fault as 
            select
                id, "S11 (dB)", "VSWR", "Gain (dBi)", "Eff (%)", "BW (MHz)", 
                "Z_Real (Ohms)", "Z_Imag (Ohms)", "Status", "Fault_Type",
                abs(hashtext(id::text)) % 100 as bucket
            from temp_set ts
            where ts."Fault_Type" = {val}
            order by abs(hashtext(id::text)) % 100
        """
        dbman.create(query=query)

        for i, split_type in enumerate(tables):
            if i == 0:
                cond = f"< {pcts[0]}"
            elif i == 1:
                cond = f"between {pcts[0]} and {(pcts[0]+pcts[1])}"
            else:
                cond = f"> {100 - pcts[2]}"
            query = f"""
                insert into {split_type}
                    select id, "S11 (dB)","VSWR","Gain (dBi)","Eff (%)","BW (MHz)","Z_Real (Ohms)","Z_Imag (Ohms)","Status","Fault_Type"
                    from split_fault sf
                    where sf.bucket {cond}
                """
            dbman.create(query=query)

        dbman.create(query="""drop table split_fault""")

def group_wise_comparison():
    query = """
    select 
            avg(t."S11 (dB)") as s11_mean,
            avg(t."BW (MHz)") as bw_mean,
            avg(t."Eff (%)") as eff_mean,
            avg(t."Gain (dBi)") as gain_mean,
            avg(t."VSWR") as vswr_mean,
            avg(t."Z_Imag (Ohms)") as z_imag_mean,
            avg(t."Z_Real (Ohms)") as z_real_mean
    from train t 
    group by t."Fault_Type"

    """
    df = dbman.extract(query=query)

    return df

def get_table(table:str="train"):
    q = f"""
    select *
    from {table}
    """
    return dbman.extract(query=q)