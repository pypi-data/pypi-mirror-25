import numpy as np
import pandas as pd
import datetime as dt

class RegressionPeriod:
    def __init__(self, startDate, endDate, coupon, order, criteria=0.9):
        self.criteria = criteria
        self.startDate = startDate
        self.endDate = endDate
        self.coupon = coupon
        self.order = order

def dtToIndex(date):
    return date.strftime("%Y-%m-%d")
		
def get_coupon_periods(df, all_coupons, FN_issue):
	Most_issue = []
	Second_Most_issued = []
	Third_Most_issued = []
	for i in FN_issue.index:
		tmp = FN_issue.loc[i]
		fst_max = np.argmax(tmp)
		tmp = tmp.drop(fst_max)
		sec_max = np.argmax(tmp)
		tmp = tmp.drop(sec_max)
		trd_max = np.argmax(tmp)
		Most_issue.append(float(fst_max.split()[4][:-1]))
		Second_Most_issued.append(float(sec_max.split()[4][:-1]))
		Third_Most_issued.append(float(trd_max.split()[4][:-1]))
		
	most_issued_list = pd.DataFrame({'Mostly Issued' : Most_issue, 'Secondly Issued' : Second_Most_issued, 'Thirdly Issued' : Third_Most_issued}, index = FN_issue.index)
	
	date_index = np.unique(df.index)
	date_index = date_index[date_index >= np.datetime64(dt.datetime.strptime(FN_issue.index[0], '%d-%b-%y'))]
	issue_dist = pd.DataFrame(np.zeros((len(date_index), FN_issue.shape[1])), index = date_index, columns = all_coupons)

	for d in most_issued_list.index:
		m_end = dt.datetime.strptime(d, '%d-%b-%y')
		m_begin = m_end - dt.timedelta(days = m_end.day - 1)
		dat = most_issued_list.ix[d]
		issue_dist[dat['Mostly Issued']][dtToIndex(m_begin):dtToIndex(m_end)] = 1
		issue_dist[dat['Secondly Issued']][dtToIndex(m_begin):dtToIndex(m_end)] = 2
		issue_dist[dat['Thirdly Issued']][dtToIndex(m_begin):dtToIndex(m_end)] = 3
		
	collapse_with_order = {}
	collapse_without_order = {}
	for c in issue_dist.columns:
		c_series = issue_dist[c]
		
		list_with_order = []
		list_without_order = []
		
		prev_order = -1
		prev_has_data = False
		prev_date = None
		for cur_date, cur_order in c_series.iteritems():
			if (not prev_has_data) and cur_order > 0:
				# get with_order Period
				cur_with_period = RegressionPeriod(cur_date, None, c, cur_order)
				
				# get without_order Period
				cur_without_period = RegressionPeriod(cur_date, None, c, None)
				
				prev_has_data = True
			elif prev_has_data and cur_order != prev_order:
				# get with_order Period
				cur_with_period.endDate = prev_date
				list_with_order.append(cur_with_period)
				cur_with_period = RegressionPeriod(cur_date, None, c, cur_order)
				
				# get without_order Period
				if cur_order == 0:
					cur_without_period.endDate = prev_date
					list_without_order.append(cur_without_period)
					
					prev_has_data = False
				
			prev_date = cur_date
			prev_order = cur_order
		
		if prev_has_data:
			# close last get with_order Period
			cur_with_period.endDate = prev_date
			list_with_order.append(cur_with_period)
			
			# close last get without_order Period
			cur_without_period.endDate = prev_date
			list_without_order.append(cur_without_period)
		
			prev_has_data = False
			
		collapse_without_order[c] = list_without_order
		collapse_with_order[c] = list_with_order
		
	return collapse_without_order, collapse_with_order