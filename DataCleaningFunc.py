import pandas as pd

SUBJID = '受试者代码'
SITEID = '中心编号'
SITENM = '中心名称'
SUBJSAT = '受试者状态'
VISIT = '访视名称'
FORMNM = '表名称'
MODULEMN = '模块名称'
RECREP = '序号'

VISTPT = '访视' # 百奥知系统中，访视时间点通常取名为'访视'
RECREP1 = '序号.1' # 百奥知的AE或CM多记录存在父子记录关系，该常量用来表示子序号

LBTEST = "检查项目"
LBDAT = '采样日期'

AETERM = '不良事件名称'
AESTDAT = '开始日期'
AEENDAT = '结束日期'
CMTRT = '药物名称'
CMSTDAT = '开始日期'
CMENDAT = '结束日期'

def StrtoInt(value):
    """Convert string to integer except illegal values or missing value."""
    if isinstance(value, str) and value.isdigit():
        return int(value)
    else:
        return pd.NA
    
def DateCompare(d1,d2):
    """ Return the result of comparing.
        1. d1 < d2: lt
        2. d1 > d2: gt
        3. d1 = d2: eq"""
    try:
        d1 = pd.to_datetime(d1)
        d2 = pd.to_datetime(d2)
        if d1 < d2:
            return 'lt'
        elif d1 > d2:
            return 'gt'
        else:
            return 'eq'
    except:
        return 'null'
    
def DateInterval(d1, d2):
    """ Return the result of d1 - d2
    """
    try:
        dif = (pd.to_datetime(d1) - pd.to_datetime(d2)).days
        return dif
    except:
        return pd.NA
    
def lab_event(df_lbtests, flag = 'IsCS'):
    """遍历LB表单中所有受试者以及检查项的临床意义，找出所有 异常有意义-正常 的时间段数据
       df_lbtests: 实验室检查表单，包含SUBJID,MODULEMN,LBTEST,VISIT,LBDAT,LBCS(临床意义)
       flag: 在传入df_lbtests之前，必须先创建名为'IsCS'的列，当临床意义=异常有意义时为1，否则为0
    """
    df_lbtests['正常或异常无临床意义的访视'], df_lbtests['正常或异常无临床意义的检查日期'] = pd.NA, pd.NA
    iter_list = [(subjid, item) for subjid in df_lbtests[SUBJID].drop_duplicates() for item in df_lbtests[LBTEST].drop_duplicates()]
    dfs = []
    
    for (subjid, item) in iter_list:
        df = df_lbtests[(df_lbtests[SUBJID]==subjid) & (df_lbtests[LBTEST]==item)]
        df = df.sort_values(by=[SUBJID,LBDAT])
        df = df.reset_index(drop=True)
        lst = df[flag].to_list() # 将df中所有isCS的值转化为列表，方便后续进行判断
        brkpt = 0
        start_ends = []
        # 遍历lst，若i位置的值为1，记录该位置为start。检查i+1时的值，为1则继续往下检索，为0则记录i+1的值为end。
        for i in range(len(lst)):
            if brkpt != 0 and i <= brkpt:
                continue
            if lst[i] == 1:
                start_end = []
                start_end.append(i)
                if i+1 < len(lst):
                    while i+1<len(lst) and lst[i+1] == 1:
                        i += 1
                    if i+1 != len(lst):# 若循环到最后都没有找到0，则不记录
                        start_end.append(i+1)
                    brkpt = i+1
                start_ends.append(start_end)
           
        # 遍历start_ends，根据start，end的索引位置进行赋值 
        for start_end_ in start_ends:
            if len(start_end_) == 2:
                df.at[start_end_[0], '正常或异常无临床意义的访视'] = df.at[start_end_[1], '访视名称']
                df.at[start_end_[0], '正常或异常无临床意义的检查日期'] = df.at[start_end_[1], '采样日期']

        idxes = [idx[0] for idx in start_ends]
        df = df[df.index.isin(idxes)]
        
        dfs.append(df)
                
    df_out = pd.concat(dfs)
    df_out.drop(columns=flag, inplace=True)
    return df_out

def shift_days(df, date_column, shift_value, new_column):
    """
    This function shifts the dates in a DataFrame by a specific number of days and stores the result in a new column.
    The number of days is determined by 'shift_value'.
    If 'shift_value' is a string, it is treated as a column name.
    If 'shift_value' is an integer, it is treated as a constant shift value.
    Positive values will shift the dates forward, and negative values will shift the dates backward.
    """
    df[date_column] = pd.to_datetime(df[date_column], errors='coerce')
    if isinstance(shift_value, str):  # shift_value is a column name
        df[new_column] = df.apply(
            lambda row: (row[date_column] + pd.to_timedelta(row[shift_value], unit='D')).date()
            if pd.notna(row[date_column]) and pd.notna(row[shift_value])
            else pd.NA
            , axis=1)
    else:  # shift_value is a constant shift value
        df[new_column] = df[date_column] + pd.DateOffset(days=shift_value)
        df[new_column] = df.apply(lambda row: (row[date_column] + pd.DateOffset(days=shift_value)).date()
                                  if pd.notna(row[date_column])
                                  else pd.NA
                                  , axis=1)
    return df

def calculate_dates(df, date_column1, date_column2, new_column, operation='subtract'):
    """
    This function calculates the sum, difference, or difference in days of two date columns in a DataFrame.
    The 'operation' parameter should be either 'subtract', or 'shift'.
    """
    df[date_column1] = pd.to_datetime(df[date_column1], errors='coerce')
    df[date_column2] = pd.to_datetime(df[date_column2], errors='coerce')

    if operation == 'subtract':
        df[new_column] = df.apply(lambda row: (row[date_column1] - row[date_column2]).days
                                  if pd.notna(row[date_column1]) and pd.notna(row[date_column2])
                                  else pd.NA                           
                                  , axis=1)
    elif operation == 'shift':
        df[new_column] = df.apply(lambda row: (row[date_column2] - row[date_column1]).days
                                  if pd.notna(row[date_column1]) and pd.notna(row[date_column2])
                                  else pd.NA                          
                                  , axis=1)
    else:
        raise ValueError("The 'operation' parameter should be either 'subtract', or 'difference_in_days'.")

    return df


def merge_reduce(df1, df2): 
    """
    Merges two DataFrames using a left join on the specified SITEID.

    Parameters:
        df1 (DataFrame): The first DataFrame to merge.
        df2 (DataFrame): The second DataFrame to merge.

    Returns:
        DataFrame: A new DataFrame resulting from the left join of df1 and df2.
    """
    return pd.merge(
        df1,
        df2,
        how="left",
        on=SITEID,
    )

def daydif(d1, d2):
    """
    Calculates the difference in days between two dates.

    Args:
        d1 (str or datetime-like): The first date.
        d2 (str or datetime-like): The second date.

    Returns:
        int or pd.NA: The difference in days between d1 and d2, or pd.NA if the input dates are invalid.
    """
    try:
        dif = (pd.to_datetime(d1, errors='coerce') - pd.to_datetime(d2, errors='coerce')).days
        return dif
    except:
        return pd.NA