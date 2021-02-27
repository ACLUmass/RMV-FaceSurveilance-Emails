from datetime import datetime
import re

# import pandas as pd
# email_df = pd.read_json('../data/src/allMails.json')
# email_df = pd.read_json('../data/allMails_old.json')
# all_dates = email_df.date

def convert_date(date_string):
	d = date_string

	if d:
		d = d.strip()
		d = d.replace(",", " ")
		d = d.replace("\xa0", " ").replace("  ", " ")
		d = d.replace("April1", "April 1").replace("Jlme", "June").replace("M-Kiay", "Monday")\
				.replace("Octo r", "October")
		d = d.replace(" PM", "PM").replace(" AM", "AM")

		d = re.sub("(S)(?![uaeT])", "5", d)
		d = re.sub("(O)(?![c])", "0", d)
		d = re.sub("(\s?:\s?)", ":", d)
		d = re.sub("([013-9]\d)(\d{2})", r"\1:\2", d)


		if "Mon May" not in d:
			for mo in ['January', 'February', 'March', 'April', 'May', 'June', 
					   'July', 'August', 'September', 'October', 'November', 
					   'December', "Monday", "Tuesday", "Wednesday", 'Thursday',
					   "Friday", "Saturday", "Sunday"]:
				mo_len = len(mo)
				# if re.search(r"\s([{} ]{{{},{}}})\s".format(mo, mo_len+1, mo_len+2), d):
				# 	print(mo)
				d = re.sub(r"(\s|^)([{} ]{{{},{}}})(?=\s)".format(mo, mo_len+1, mo_len+2), " {} ".format(mo), d)
		
		d = re.sub("\s{2,3}", " ", d)
		d = d.strip()

		if re.search("Eastern", d):
			# Wednesday, May 18, 2016 2:59:30 PM (UTC-05:00) Eastern Time (US & Canada)
			d = d.split("(", 1)[0].strip()
			dt_d = datetime.strptime(d, "%A %B %d %Y %I:%M:%S%p")
		elif (d == "") | ("·" in d) | ("Subject" in d) | (re.search("\d{4} \d \d", d) is not None) | (re.search("^\d ", d) is not None):
			dt_d = None
		elif re.search("day.*\d:\d\d:\d\d", d):
			# Tuesday, December 20, 2016 3:13:54 PM
			dt_d = datetime.strptime(d, "%A %B %d %Y %I:%M:%S%p")
		elif re.search("day.* \d?\d \d?\d:\d\d", d):
			# Tuesday, January 31, 10:24 AM
			dt_d = None
		elif re.search("day\s[A-Za-z]{3}\s.*\d \d?\d:\d\d", d):
			# Tuesday, Jun 20, 2017, 12:10 PM
			dt_d = datetime.strptime(d, "%A %b %d %Y %I:%M%p")
		elif re.search("day.*, \d?\d:\d\d", d):
			# Monday, Jun 26, 2017, 7:33 PM
			dt_d = datetime.strptime(d, "%A %B %d %Y %I:%M%p")
		elif re.search("day.*\d \d?\d:\d\d", d):
			# Tuesday, December 20, 2016 3:13 PM
			dt_d = datetime.strptime(d, "%A %B %d %Y %I:%M%p")
		elif re.search("(Mon|Tue|Wed|Thu|Fri|Sat|Sun)\s.*at.\d?\d:\d\d", d):
			# Thu, Aug 25, 2016 at 8:32 AM
			dt_d = datetime.strptime(d, "%a %b %d %Y at %I:%M%p")
		elif re.search("\d{4}.*GMT", d):
			# 04/06/2016 9:23 AM (GMT-05:00)
			d = d.split("(GMT")[0].strip()
			dt_d = datetime.strptime(d, "%m/%d/%Y %I:%M%p")
		elif re.search("GMT", d):
			# 5/14/19 4:57 PM (GMT-05:00)
			d = d.split("(GMT")[0].strip()
			dt_d = datetime.strptime(d, "%m/%d/%y %I:%M%p")
		elif re.search("-\d{2}:\d{2}$", d):
			# Wed, 11 May 2016 15:11:14 -0400
			d = d.rsplit(" ", 1)[0]
			dt_d = datetime.strptime(d, "%a %d %b %Y %H:%M:%S")
		elif re.search(" \d{4} \d?\d:\d\d", d):
			# Apr 5, 2016, 2:44 PM
			dt_d = datetime.strptime(d, "%b %d %Y %I:%M%p")
		elif re.search("day.*\d{4}.at.\d?\d:\d\d.*M", d):
			# March 6, 2016 at 4:55:49 PM EST
			d = re.split("[EPC][SD]T", d)[0].strip()
			dt_d = datetime.strptime(d, "%A %B %d %Y at %I:%M%p")
		elif re.search("\d{4}.at.\d?\d:\d\d.*M", d):
			# March 6, 2016 at 4:55:49 PM EST
			d = re.split("[EPC][SD]T", d)[0].strip()
			dt_d = datetime.strptime(d, "%B %d %Y at %I:%M:%S%p")
		elif re.search("\d{4}.at.\d?\d:\d\d", d):
			# March 24, 2016 at 16:02:13
			d = re.split("[EPC][SD]T", d)[0].strip()
			dt_d = datetime.strptime(d, "%B %d %Y at %H:%M:%S")
		elif re.search("\d{1,2}/\d{1,2}/\d{4} \d{2}:\d{2}:\d{2}", d):
			# March 24, 2016 at 16:02:13
			dt_d = datetime.strptime(d, "%m/%d/%Y %I:%M:%S%p")
		elif re.search("\d{1,2}/\d{1,2}/\d{4} \d{2}:\d{2}", d):
			# March 24, 2016 at 16:02:13
			dt_d = datetime.strptime(d, "%m/%d/%Y %I:%M%p")
		else:
			print("couldn't match date " + d)
			dt_d = None
	else:
		dt_d = None

	if dt_d is None:
		return None
	else:
		return dt_d.strftime("%A, %B %d, %Y %I:%M %p")

# e = email_df[email_df.mailId.str.contains("msp1_155_4")]
# print(e.date)
# print(convert_date("5/14/19 4:57 PM (GMT-05:00)"))



# for i, d in enumerate(all_dates):
# 	if d:
# 		d = d.strip()
# 		d = d.replace(",", " ")
# 		d = d.replace("\xa0", " ").replace("  ", " ")
# 		d = d.replace("April1", "April 1").replace("Jlme", "June").replace("M-Kiay", "Monday")\
# 				.replace("Octo r", "October")
# 		d = d.replace(" PM", "PM").replace(" AM", "AM")

# 		d = re.sub("(S)(?![uaeT])", "5", d)
# 		d = re.sub("(O)(?![c])", "0", d)
# 		d = re.sub("(\s?:\s?)", ":", d)
# 		d = re.sub("([013-9]\d)(\d{2})", r"\1:\2", d)


# 		if "Mon May" not in d:
# 			for mo in ['January', 'February', 'March', 'April', 'May', 'June', 
# 					   'July', 'August', 'September', 'October', 'November', 
# 					   'December', "Monday", "Tuesday", "Wednesday", 'Thursday',
# 					   "Friday", "Saturday", "Sunday"]:
# 				mo_len = len(mo)
# 				# if re.search(r"\s([{} ]{{{},{}}})\s".format(mo, mo_len+1, mo_len+2), d):
# 				# 	print(mo)
# 				d = re.sub(r"(\s|^)([{} ]{{{},{}}})(?=\s)".format(mo, mo_len+1, mo_len+2), " {} ".format(mo), d)
		
# 		d = re.sub("\s{2,3}", " ", d)
# 		d = d.strip()

# 		try:
# 			if re.search("Eastern", d):
# 				# Wednesday, May 18, 2016 2:59:30 PM (UTC-05:00) Eastern Time (US & Canada)
# 				d = d.split("(", 1)[0].strip()
# 				dt_d = datetime.strptime(d, "%A %B %d %Y %H:%M:%S%p")
# 			elif (d == "") | ("·" in d) | (re.search("\d{4} \d \d", d) is not None) | (re.search("^\d ", d) is not None):
# 				dt_d = None
# 			elif re.search("day.*\d:\d\d:\d\d", d):
# 				# Tuesday, December 20, 2016 3:13:54 PM
# 				dt_d = datetime.strptime(d, "%A %B %d %Y %H:%M:%S%p")
# 			elif re.search("day.* \d?\d \d?\d:\d\d", d):
# 				# Tuesday, January 31, 10:24 AM
# 				dt_d = None
# 			elif re.search("day\s[A-Za-z]{3}\s.* \d?\d:\d\d", d):
# 				# Tuesday, Jun 20, 2017, 12:10 PM
# 				dt_d = datetime.strptime(d, "%A %b %d %Y %H:%M%p")
# 			elif re.search("day.*, \d?\d:\d\d", d):
# 				# Monday, Jun 26, 2017, 7:33 PM
# 				dt_d = datetime.strptime(d, "%A %B %d %Y %H:%M%p")
# 			elif re.search("day.*\d:\d\d", d):
# 				# Tuesday, December 20, 2016 3:13 PM
# 				dt_d = datetime.strptime(d, "%A %B %d %Y %H:%M%p")
# 			elif re.search("(Mon|Tue|Wed|Thu|Fri|Sat|Sun).*at.\d?\d:\d\d", d):
# 				# Thu, Aug 25, 2016 at 8:32 AM
# 				dt_d = datetime.strptime(d, "%a %b %d %Y at %H:%M%p")
# 			elif re.search("GMT", d):
# 				# 04/06/2016 9:23 AM (GMT-05:00
# 				d = d.split("(GMT")[0].strip()
# 				dt_d = datetime.strptime(d, "%m/%d/%Y %H:%M%p")
# 			elif re.search("-\d{2}:\d{2}$", d):
# 				# Wed, 11 May 2016 15:11:14 -0400
# 				d = d.rsplit(" ", 1)[0]
# 				dt_d = datetime.strptime(d, "%a %d %b %Y %H:%M:%S")
# 			elif re.search(" \d{4} \d?\d:\d\d", d):
# 				# Apr 5, 2016, 2:44 PM
# 				dt_d = datetime.strptime(d, "%b %d %Y %H:%M%p")
# 			elif re.search("\d{4}.at.\d?\d:\d\d.*M", d):
# 				# March 6, 2016 at 4:55:49 PM EST
# 				d = re.split("[EPC][SD]T", d)[0].strip()
# 				dt_d = datetime.strptime(d, "%B %d %Y at %H:%M:%S%p")
# 			elif re.search("\d{4}.at.\d?\d:\d\d", d):
# 				# March 24, 2016 at 16:02:13
# 				d = re.split("[EPC][SD]T", d)[0].strip()
# 				dt_d = datetime.strptime(d, "%B %d %Y at %H:%M:%S")
# 			elif re.search("\d{1,2}/\d{1,2}/\d{4} \d{2}:\d{2}:\d{2}", d):
# 				# March 24, 2016 at 16:02:13
# 				dt_d = datetime.strptime(d, "%m/%d/%Y %H:%M:%S%p")
# 			elif re.search("\d{1,2}/\d{1,2}/\d{4} \d{2}:\d{2}", d):
# 				# March 24, 2016 at 16:02:13
# 				dt_d = datetime.strptime(d, "%m/%d/%Y %H:%M%p")


# 			print(dt_d)
# 			if dt_d is None:
# 				print("SDJGLISUILDSULIUS")

# 		except Exception as e:
# 			print(i, "/", len(all_dates))
# 			print("no!", d)
# 			print("before:", og_d)
# 			print(e)
# 			break
# 	else:
# 		print(None)



