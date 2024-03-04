from fpdf import FPDF

# class SurvGPT_PDF(FPDF):
#     def __init__(self, care_plan_json,treatment_summary_json):
#         super().__init__()
#         self.cancer_type = care_plan_json['cancer_type']
#         self.care_plan_json = care_plan_json
#         self.treatment_summary_json = treatment_summary_json
#         self.font_color_info = [0,0,255]

#         #add arial font
#         self.add_font("Arial", style="", fname="./fonts/Arial.ttf", uni=True)
#         self.add_font("Arial", style="B", fname="./fonts/Arial_Bold.ttf", uni=True)
#         self.add_font("Arial", style="I", fname="./fonts/Arial_Italic.ttf", uni=True)
#         self.add_font("Arial", style="BI", fname="./fonts/Arial_Bold_Italic.ttf", uni=True)


#     def add_info_to_cell(self,info,X,Y,col_width,row_height,is_ln=False,align='L',border=False):
#         self.set_text_color(self.font_color_info[0],self.font_color_info[1],self.font_color_info[2])
#         self.x = X
#         self.y = Y
#         self.cell(col_width, row_height, info, ln=is_ln, align=align,border=border)
#         self.set_text_color(0,0,0)

#     def add_info_to_multicell(self,info,X,Y,col_width,row_height,is_ln=False,align='L',border=False):
#         self.set_text_color(self.font_color_info[0],self.font_color_info[1],self.font_color_info[2])
#         self.x = X
#         self.y = Y
#         self.multi_cell(col_width, row_height, info, ln=is_ln, align=align,border=border)
#         self.set_text_color(0,0,0)


#     def header(self):
#         # font
#         self.set_font('Arial', 'B', 12)
#         # Calculate width of the title and position
#         title = f'SurvGPT: Treatment Summary and Survivorship Care Plan for {self.cancer_type}'
#         title_w = self.get_string_width(title) + 6
#         doc_w = self.w
#         self.set_x((doc_w - title_w) / 2)

#         # Title
#         self.cell(0, 10,title , ln=True, align='C')

#     def footer(self):
#         # Set position of the footer
#         self.set_y(-15)
#         # Set font
#         self.set_font('Arial','', 8)
#         # Page number
#         # self.cell(0, 10, f'Page {self.page_no()}', align='C')
#         self.cell(0, 10, 'This survivorship care plan format is adapted from the templates provided by ASCO' )
    
#     def general_info(self):
#         # #Add Page
#         self.add_page()
#         # font
#         self.set_font('Arial', 'B', 11)
#          # set width for each column (2 columns)
#         col_width = self.w / 2.2
#         # set height for each row
#         row_height = self.font_size * 1.5
#         # Section Title
#         self.set_fill_color(211, 211, 211) 
#         self.cell(col_width*2, row_height, 'General Information', ln=False, align='C',border=True,fill=True)
#         self.set_font('Arial', '', 6)
#         self.add_info_to_cell('Filled using patient id',X = self.x-2*col_width,Y = self.y,col_width=2*col_width,row_height=row_height, is_ln=True,align='R')
#         # Table for general information
#         # font
#         self.set_font('Arial', '', 9)
       
#         # set alignment for each cell
#         # self.set_xy(10, 40)
#         # Row 1
#         self.cell(col_width, row_height, 'Patient Name:', border=True)
#         offset = self.get_string_width('Patient Name:')+2
#         self.add_info_to_cell(self.treatment_summary_json['ptnum'],X = self.x-col_width+offset,Y = self.y,col_width=col_width - offset,row_height=row_height, is_ln=False,align='L')  ### temporary fake name
#         self.cell(col_width, row_height, 'Patient DOB:', border=True,ln=False)
#         offset = self.get_string_width('Patient DOB:')+2
#         # self.add_info_to_cell('01/07/1985',X = self.x-col_width+offset,Y = self.y,col_width=col_width - offset,row_height=row_height, is_ln=True,align='L') ### temporary fake DOB
#         self.add_info_to_cell('',X = self.x-col_width+offset,Y = self.y,col_width=col_width - offset,row_height=row_height, is_ln=True,align='L') ### temporary fake DOB

#         # Row 2
#         self.set_font('Arial', 'B', 9)
#         self.cell(col_width*2, row_height, 'Health Care Providers (Including Names, Institution)', border=True,ln=True,align='C')
#         self.set_font('Arial', '', 9)
#         self.cell(col_width*2, row_height, 'Primary Care Provider:', border=True,ln=False)
#         offset = self.get_string_width('Primary Care Provider:')+2
#         # self.add_info_to_cell('Dr. Zephyra Nexis, VidaSphere Health Institute',X = self.x-2*col_width+offset,Y = self.y,col_width=2*col_width - offset,row_height=row_height, is_ln=True,align='L') ### temporary fake 
#         self.add_info_to_cell('',X = self.x-2*col_width+offset,Y = self.y,col_width=2*col_width - offset,row_height=row_height, is_ln=True,align='L')
#         self.cell(col_width*2, row_height, 'Surgeon:', border=True,ln=False)
#         # offset = self.get_string_width('Surgeon:')+2
#         # self.add_info_to_cell('Dr. Kyrona Vexel, PheonixMed Hospital Network',X = self.x-2*col_width+offset,Y = self.y,col_width=2*col_width - offset,row_height=row_height, is_ln=True,align='L') ### temporary fake 
#         self.add_info_to_cell('',X = self.x-2*col_width+offset,Y = self.y,col_width=2*col_width - offset,row_height=row_height, is_ln=True,align='L')
#         self.cell(col_width*2, row_height, 'Radiation Oncologist:', border=True,ln=False)
#         # offset = self.get_string_width('Radiation Oncologist:')+2
#         # self.add_info_to_cell('Dr. Qylix Rendara, ZenithCare Healing Center',X = self.x-2*col_width+offset,Y = self.y,col_width=2*col_width - offset,row_height=row_height, is_ln=True,align='L') ### temporary fake 
#         self.add_info_to_cell('',X = self.x-2*col_width+offset,Y = self.y,col_width=2*col_width - offset,row_height=row_height, is_ln=True,align='L')
#         self.cell(col_width*2, row_height, 'Medical Oncologist:', border=True,ln=False)
#         # offset = self.get_string_width('Medical Oncologist:')+2
#         # self.add_info_to_cell('Dr. Vion Talrex, PheonixMed Hospital Network',X = self.x-2*col_width+offset,Y = self.y,col_width=2*col_width - offset,row_height=row_height, is_ln=True,align='L') ### temporary fake 
#         self.add_info_to_cell('',X = self.x-2*col_width+offset,Y = self.y,col_width=2*col_width - offset,row_height=row_height, is_ln=True,align='L') 
#         self.cell(col_width*2, row_height, 'Other Providers:', border=True,ln=True)
#         # offset = self.get_string_width('Surgeon:')+2
#         # self.add_info_to_cell('Dr. Kyrona Vexel, PheonixMed Hospital Network',X = self.x-col_width+offset,Y = self.y,col_width=col_width - offset,row_height=row_height, is_ln=True,align='L') ### temporary fake 


#     def treatment_summary_table(self):
#         # font
#         self.set_font('Arial', 'B', 11)
#          # set width for each column (2 columns)
#         col_width = self.w / 2.2
#         # set height for each row
#         row_height = self.font_size * 1.5
#         # Section Title
#         self.set_fill_color(211, 211, 211) 
#         self.cell(col_width*2, row_height, 'Treatment Summary', ln=True, align='C',border=True,fill=True)

#         # Table for treatment summary
#         # font
#         self.set_font('Arial', '', 9)
       
#         # set alignment for each cell
#         # self.set_xy(10, 40)

#         # Diagnosis ================= 'Cancer type', 'Diagnosis Date', 'Cancer stage'
#         self.set_font('Arial', 'B', 9)
#         self.cell(col_width*2, row_height, 'Diagnosis', border=True,ln=True,align='C')
#         self.set_font('Arial', '', 9)
#         temp_json = self.treatment_summary_json['Treatment Summary']['Diagnosis']
#         key_names = list(temp_json.keys())

#         #row 1
#         data_text = f'Cancer Type/Location/Histology Subtype: {self.cancer_type}'
#         data_w = self.get_string_width(data_text)+2
#         self.cell(data_w, row_height, f'Cancer Type/Location/Histology Subtype:', border=True) # Cancer Type/Location/Histology Subtype
#         offset = self.get_string_width('Cancer Type/Location/Histology Subtype: ')
#         self.add_info_to_cell(f'{self.cancer_type}',X = self.x-data_w+offset,Y = self.y,col_width=data_w - offset,row_height=row_height, is_ln=False,align='L')
#         ####
#         self.cell(col_width*2-data_w, row_height, f'{key_names[1]}:', border=True,ln=False) # Diagnosis Date
#         offset = self.get_string_width(f'{key_names[1]}: ')
#         self.add_info_to_cell(f'{temp_json[key_names[1]]}',X = self.x-col_width*2+data_w+offset,Y = self.y,col_width=col_width*2-data_w - offset,row_height=row_height, is_ln=True,align='L')

#         #row 2
#         self.cell(col_width*2, row_height, f'{key_names[2]}:', border=True,ln=False) # Stage
#         offset = self.get_string_width(f'{key_names[2]}: ')
#         self.add_info_to_cell(f'{temp_json[key_names[2]]}',X = self.x-col_width*2+offset,Y = self.y,col_width=col_width*2 - offset,row_height=row_height, is_ln=True,align='L')
        
        
#         # Treatment Completed ================= 
#         # 'Surgery', 'Surgery Date(s) (year)', 'Surgical Procedure/location/findings', 'Radiation', 'Body area treated', 'End Date (year)', 'Systemic Therapy (Chemotherapy, hormonal therapy, other)', 'Names of Agents used', 'Persistent symptoms or side effects at completion of treatment'
#         self.set_font('Arial', 'B', 9)
#         self.cell(col_width*2, row_height, 'Treatment Completed', border=True,ln=True,align='C')
#         self.set_font('Arial', '', 9)
#         temp_json = self.treatment_summary_json['Treatment Summary']['Treatment Completed']
#         key_names = list(temp_json.keys())

#         #row 1
#         self.cell(col_width, row_height, f'{key_names[0]}:', border=True) # Surgery
#         offset = self.get_string_width(f'{key_names[0]}: ')
#         self.add_info_to_cell(f'{temp_json[key_names[0]]}',X = self.x-col_width+offset,Y = self.y,col_width=col_width - offset,row_height=row_height, is_ln=False,align='L')
#         ####
#         self.cell(col_width, row_height, f'{key_names[1]}:', border=True,ln=False) # Surgery Date(s) (year)
#         offset = self.get_string_width(f'{key_names[1]}: ')
#         self.add_info_to_cell(f'{temp_json[key_names[1]]}',X = self.x-col_width+offset,Y = self.y,col_width=col_width - offset,row_height=row_height, is_ln=True,align='L')

#         #row 2
#         self.cell(col_width*2, row_height, f'{key_names[2]}:', border=True,ln=False) #Surgical Procedure/location/findings
#         offset = self.get_string_width(f'{key_names[2]}: ')
#         self.add_info_to_cell(f'{temp_json[key_names[2]]}',X = self.x-col_width*2+offset,Y = self.y,col_width=col_width*2 - offset,row_height=row_height, is_ln=True,align='L')

#         #row 3
#         self.cell(self.w / 3.3, row_height, f'{key_names[3]}:', border=True) # Radiation
#         offset = self.get_string_width(f'{key_names[3]}: ')
#         self.add_info_to_cell(f'{temp_json[key_names[3]]}',X = self.x-(self.w / 3.3) +offset,Y = self.y,col_width=(self.w / 3.3) - offset,row_height=row_height, is_ln=False,align='L')
#         ####
#         self.cell(self.w / 3.3, row_height, f'{key_names[4]}:', border=True) # Body area treated
#         offset = self.get_string_width(f'{key_names[4]}: ')
#         self.add_info_to_cell(f'{temp_json[key_names[4]]}',X = self.x-(self.w / 3.3) +offset,Y = self.y,col_width=(self.w / 3.3) - offset,row_height=row_height, is_ln=False,align='L')
#         ####
#         self.cell(self.w / 3.3, row_height, f'{key_names[5]}:', border=True,ln=False) # End Date (year)
#         offset = self.get_string_width(f'{key_names[5]}: ')
#         self.add_info_to_cell(f'{temp_json[key_names[5]]}',X = self.x-(self.w / 3.3) +offset,Y = self.y,col_width=(self.w / 3.3) - offset,row_height=row_height, is_ln=True,align='L')

#         #row 4
#         self.cell(col_width*2, row_height, f'{key_names[6]}:', border=True,ln=False) # Systemic Therapy (Chemotherapy, hormonal therapy, other)
#         offset = self.get_string_width(f'{key_names[6]}: ')
#         self.add_info_to_cell(f'{temp_json[key_names[6]]}',X = self.x-col_width*2+offset,Y = self.y,col_width=col_width*2 - offset,row_height=row_height, is_ln=True,align='L')

#         ############################################################################################################
#         #row 5 
#         self.cell(col_width, row_height, f'{key_names[7]}', border=True,align ='C') # Names of Agents used
#         self.cell(col_width, row_height, f'End Dates (year)', border=True,ln=True,align ='C')
#         # Number of agents used data
#         num_agents = list(temp_json[key_names[7]].keys())
#         i=0
#         while i<len(num_agents):
#             if 'Other' in num_agents[i]:
#                 top = self.y
#                 left = self.x
#                 self.multi_cell(col_width, row_height, f'{num_agents[i]}:', border=False)
#                 offset = self.get_string_width(f'{num_agents[i]}: ')+2
#                 self.add_info_to_multicell(f'{temp_json[key_names[7]][num_agents[i]]}',X = self.x-col_width+offset,Y = top,col_width=col_width - offset,row_height=row_height, is_ln=False,align='C')
#                 end_list = [self.y]
#                 i+=1
#                 if i>=len(num_agents):
#                     self.y = top
#                     self.cell(col_width, row_height, '', align = 'C',border=False, ln=True)
                    
#                 elif 'End' in num_agents[i]:
#                     # self.cell(col_width, row_height, f'{temp_json[key_names[7]][num_agents[i]]}', align = 'C',border=True, ln=True)
#                     self.y = top
#                     self.add_info_to_cell(f'{temp_json[key_names[7]][num_agents[i]]}',X = self.x,Y = self.y,col_width=col_width,row_height=row_height, is_ln=True,align='C',border=False)
#                     end_list.append(self.y)
#                     i+=1
#                 else:
#                     self.y = top
#                     self.cell(col_width, row_height, '', align = 'C',border=False, ln=True)
#                 end = max(end_list)
#                 self.y = end
#                 self.line(left, top, left, end)
#                 self.line(left+col_width, top, left+col_width, end)
#                 self.line(left+2*col_width, top, left+2*col_width, end)
#                 self.line(left, end, left+2*col_width, end)

#                 break 
#             if 'Yes' in temp_json[key_names[7]][num_agents[i]] or 'yes' in temp_json[key_names[7]][num_agents[i]]:
#                 self.cell(col_width, row_height, f'{num_agents[i]}:', border=True)
#                 offset = self.get_string_width(f'Paclitaxel / Docetaxel: ')+2
#                 self.add_info_to_cell(f'{temp_json[key_names[7]][num_agents[i]]}',X = self.x-col_width+offset,Y = self.y,col_width=col_width - offset,row_height=row_height, is_ln=False,align='C')
#                 i+=1
#                 if 'End' in num_agents[i]: # if there is an end date
#                     # self.cell(col_width, row_height, f'{temp_json[key_names[7]][num_agents[i]]}', align = 'C',border=True, ln=True)
#                     self.add_info_to_cell(f'{temp_json[key_names[7]][num_agents[i]]}',X = self.x,Y = self.y,col_width=col_width,row_height=row_height, is_ln=True,align='C',border=True)
#                     i+=1
#                 else:
#                     self.cell(col_width, row_height, '', align = 'C',border=True, ln=True)
    
#             else:
#                 self.cell(col_width, row_height, f'{num_agents[i]}: ', border=True)
#                 offset = self.get_string_width(f'Paclitaxel / Docetaxel: ')+2
#                 self.add_info_to_cell(f'{temp_json[key_names[7]][num_agents[i]]}',X = self.x-col_width+offset,Y = self.y,col_width=col_width - offset,row_height=row_height, is_ln=False,align='C')
#                 self.cell(col_width, row_height, '', align = 'C',border=True, ln=True)
#                 i+=1

#         ###################################################################################################
        
        
#         ############################################################################################################
#         #row 6
#         self.cell(col_width*2, row_height, f'{key_names[8]}:', border=True,ln=False) # Persistent symptoms or side effects at completion of treatment
#         offset = self.get_string_width(f'{key_names[8]}: ')
#         self.add_info_to_cell(f'{temp_json[key_names[8]]}',X = self.x-col_width*2+offset,Y = self.y,col_width=col_width*2 - offset,row_height=row_height, is_ln=True,align='L')
        


#         # Treatment Ongoing =================
#         # 'Need for ongoing (adjuvant) treatment for cancer', 'Ongoing treatment', 'Planned duration', 'Possible side effects'
#         self.set_font('Arial', 'B', 9)
#         self.cell(col_width*2, row_height, 'Treatment Ongoing', border=True,ln=True,align='C')
#         self.set_font('Arial', '', 9)
#         temp_json = self.treatment_summary_json['Treatment Summary']['Treatment Ongoing']
#         key_names = list(temp_json.keys())
#         #row 1
#         self.cell(col_width*2, row_height, f'{key_names[0]}:', border=True,ln=False) # Need for ongoing (adjuvant) treatment for cancer
#         offset = self.get_string_width(f'{key_names[0]}: ')
#         self.add_info_to_cell(f'{temp_json[key_names[0]]}',X = self.x-col_width*2+offset,Y = self.y,col_width=col_width*2 - offset,row_height=row_height, is_ln=True,align='L')

#         #row 2
#         self.cell(self.w / 3.3, row_height, 'Ongoing Treatment Name', border=True,align='C')
#         self.cell(self.w / 3.3, row_height, 'Planned Duration', border=True,align='C')
#         self.cell(self.w / 3.3, row_height, 'Possible Side Effects', border=True,align='C',ln=True)
#         if 'No' in temp_json[key_names[0]] or 'no' in temp_json[key_names[0]]:
#             # self.cell(self.w / 3.3, row_height, 'not given', border=True,align='C')
#             # self.cell(self.w / 3.3, row_height, 'not given', border=True,align='C')
#             # self.cell(self.w / 3.3, row_height, 'not given', border=True,align='C',ln=True)
#             self.add_info_to_cell('not given',X = self.x,Y = self.y,col_width=self.w / 3.3,row_height=row_height, is_ln=False,align='C',border=True)
#             self.add_info_to_cell('not given',X = self.x,Y = self.y,col_width=self.w / 3.3,row_height=row_height, is_ln=False,align='C',border=True)
#             self.add_info_to_cell('not given',X = self.x,Y = self.y,col_width=self.w / 3.3,row_height=row_height, is_ln=True,align='C',border=True)
            
#             self.cell(self.w / 3.3, row_height, '', border=True,align='C')
#             self.cell(self.w / 3.3, row_height, '', border=True,align='C')
#             self.cell(self.w / 3.3, row_height, '', border=True,align='C',ln=True)

#             self.cell(self.w / 3.3, row_height, '', border=True,align='C')
#             self.cell(self.w / 3.3, row_height, '', border=True,align='C')
#             self.cell(self.w / 3.3, row_height, '', border=True,align='C',ln=True)


#         # else:  Need to code for the else part

    
#     def follow_up_care_plan_table(self):
#         pg_flag = 0
#         add_page_list = [3,12,23,34,40,47]
#         # font
#         self.set_font('Arial', 'B', 11)
#          # set width for each column (2 columns)
#         col_width = self.w / 2.2
#         # set height for each row
#         row_height = self.font_size * 1.5
#         # Section Title
#         self.set_fill_color(211, 211, 211) 
#         self.cell(col_width*2, row_height, 'Follow-up Care Plan', ln=True, align='C',border=True,fill=True)

#         # Table for follow up care plan
#         # font
#         self.set_font('Arial', '', 9)
#         task_names = list(self.care_plan_json.keys())[2:]

#         # Task 1 : 'Schedule of Clinical Visits'
#         self.set_font('Arial', 'B', 9)
#         self.cell(col_width*2, row_height, f'{task_names[0]}', border=True,ln=True,align='C')
#         # self.set_font('Arial', '', 9)
#         recommend_list = self.care_plan_json[task_names[0]]['recommendation'][task_names[0]]
#         sub_keys = list(recommend_list[0].keys())
#         #row 1
#         self.cell(col_width/3, row_height, f'{sub_keys[0]}', border=True,align='C')
#         self.cell(col_width/2, row_height, f'{sub_keys[1]}', border=True,align='C')
#         self.cell(col_width*2 -(5/6)*col_width, row_height, f'{sub_keys[2]}', border=True,align='C',ln=True)
#         # fill the recommendations
#         self.set_font('Arial', '', 9)
#         for i in range(len(recommend_list)):
#             top = self.y
#             left = self.x
            
#             end_list = []
#             # self.multi_cell(col_width/3, row_height, f'{recommend_list[i][sub_keys[0]].strip()}',align='L')#, border=True)
#             self.add_info_to_multicell(f'{recommend_list[i][sub_keys[0]].strip()}',X=self.x,Y=self.y,col_width = col_width/3,row_height = row_height,is_ln=False,align='L')
#             end_list.append(self.y)
#             self.y = top

#             # self.multi_cell(col_width/2, row_height, f'{recommend_list[i][sub_keys[1]].strip()}',align='L')#, border=True)
#             self.add_info_to_multicell(f'{recommend_list[i][sub_keys[1]].strip()}',X=self.x,Y=self.y,col_width = col_width/2,row_height = row_height,is_ln=False,align='L')
#             end_list.append(self.y)
#             self.y = top


#             # self.multi_cell(col_width*2 -(5/6)*col_width, row_height, f'{recommend_list[i][sub_keys[2]].strip()}',ln=True,align='L')
#             self.add_info_to_multicell(f'{recommend_list[i][sub_keys[2]].strip()}',X=self.x,Y=self.y,col_width = col_width*2 -(5/6)*col_width,row_height = row_height,is_ln=True,align='L')
#             end_list.append(self.y)
#             end = max(end_list)
#             self.y = end
#             self.line(left, end, left+col_width*2, end)
#             self.line(left, top, left, end)
#             self.line(left+col_width/3, top, left+col_width/3, end)
#             self.line(left+col_width/2+col_width/3, top, left+col_width/2+col_width/3, end)
#             self.line(left+col_width*2, top, left+col_width*2, end)
#             pg_flag+=1

#             # if pg_flag in add_page_list:
#             #     self.add_page()
#             if self.y > self.h - 6*row_height:
#                 self.add_page()
            
#         if self.y > self.h - 10*row_height:
#                 self.add_page()    

#         ## Task 2 : 'Cancer Surveillance or Other Recommended Tests'
#         self.set_font('Arial', 'B', 9)
#         self.cell(col_width*2, row_height, f'{task_names[1]}', border=True,ln=True,align='C')
#         # self.set_font('Arial', '', 9)
#         recommend_list = self.care_plan_json[task_names[1]]['recommendation'][task_names[1]]
#         sub_keys = list(recommend_list[0].keys())
#         #row 1
#         self.cell(col_width/3, row_height, f'{sub_keys[0]}', border=True,align='C')
#         self.cell(col_width/3+2, row_height, f'{sub_keys[1]}', border=True,align='C')
#         self.cell(col_width/3, row_height, f'{sub_keys[2]}', border=True,align='C')
#         self.cell(col_width*2 -col_width-2, row_height, f'{sub_keys[3]}', border=True,align='C',ln=True)
#         # fill the recommendations
#         self.set_font('Arial', '', 9)
#         for i in range(len(recommend_list)):
#             top = self.y
#             left = self.x
#             end_list = []
#             # self.multi_cell(col_width/3, row_height, f'{recommend_list[i][sub_keys[0]].strip()}',align='L')#, border=True)
#             self.add_info_to_multicell(f'{recommend_list[i][sub_keys[0]].strip()}',X=self.x,Y=self.y,col_width = col_width/3,row_height = row_height,is_ln=False,align='L')
#             end_list.append(self.y)
#             self.y = top


#             # self.multi_cell(col_width/3 +2, row_height, f'{recommend_list[i][sub_keys[1]].strip()}',align='L')#, border=True)
#             self.add_info_to_multicell(f'{recommend_list[i][sub_keys[1]].strip()}',X=self.x,Y=self.y,col_width = col_width/3+2,row_height = row_height,is_ln=False,align='L')
#             end_list.append(self.y)
#             self.y = top


#             # self.multi_cell(col_width/3, row_height, f'{recommend_list[i][sub_keys[2]].strip()}',align='L')#, border=True)
#             self.add_info_to_multicell(f'{recommend_list[i][sub_keys[2]].strip()}',X=self.x,Y=self.y,col_width = col_width/3,row_height = row_height,is_ln=False,align='L')
#             end_list.append(self.y)
#             self.y = top


#             # self.multi_cell(col_width*2 -col_width-2, row_height, f'{recommend_list[i][sub_keys[3]]}',ln=True,align='L')
#             self.add_info_to_multicell(f'{recommend_list[i][sub_keys[3]]}',X=self.x,Y=self.y,col_width = col_width*2 -col_width-2,row_height = row_height,is_ln=True,align='L')
#             end_list.append(self.y)
#             end = max(end_list)
#             self.y = end
#             self.line(left, end, left+col_width*2, end)
#             self.line(left, top, left, end)
#             self.line(left+col_width/3, top, left+col_width/3, end)
#             self.line(left+2*col_width/3+2, top, left+2*col_width/3+2, end)
#             self.line(left+3*col_width/3+2, top, left+3*col_width/3+2, end)
#             self.line(left+col_width*2, top, left+col_width*2, end)
#             pg_flag+=1

#             # if pg_flag in add_page_list:
#             #     self.add_page()
#             if self.y > self.h - 6*row_height:
#                 self.add_page()
        
#         if self.y > self.h - 10*row_height:
#                 self.add_page()

#         # Task 3 : 'Possible late and long-term effects of cancer treatment'
#         self.set_font('Arial', 'B', 9)
#         self.cell(col_width*2, row_height, f'{task_names[2]}', border=True,ln=True,align='C')
#         # self.set_font('Arial', '', 9)
#         recommend_list = self.care_plan_json[task_names[2]]['recommendation'][task_names[2]]
#         sub_keys = list(recommend_list[0].keys())
#         # row 1
#         self.set_font('Arial', '', 8)
#         instruct_text = 'List of Possible late- and long-term effects that someone with this type of cancer and treatment may experience.'
#         self.multi_cell(col_width*2,row_height,instruct_text,border=True,align='L',ln=True)
#         #row 2
#         self.set_font('Arial', 'B', 9)
#         self.cell(col_width/3, row_height, f'{sub_keys[0]}', border=True,align='C')
#         self.cell(col_width*2 - col_width/3, row_height, f'{sub_keys[1]}', border=True,align='C',ln=True)
        
#         # fill the recommendations
#         self.set_font('Arial', '', 9)
#         for i in range(len(recommend_list)):
#             top = self.y
#             left = self.x
#             end_list = []
#             # self.multi_cell(col_width/3, row_height, f'{recommend_list[i][sub_keys[0]].strip()}',align='L')
#             self.add_info_to_multicell(f'{recommend_list[i][sub_keys[0]].strip()}',X=self.x,Y=self.y,col_width = col_width/3,row_height = row_height,is_ln=False,align='L')
#             end_list.append(self.y)
#             self.y = top

#             # self.multi_cell(col_width*2 - col_width/3, row_height, f'{recommend_list[i][sub_keys[1]]}',ln=True,align='L')
#             self.add_info_to_multicell(f'{recommend_list[i][sub_keys[1]]}',X=self.x,Y=self.y,col_width = col_width*2 - col_width/3,row_height = row_height,is_ln=True,align='L')
#             end_list.append(self.y)
#             end = max(end_list)
#             self.y = end
#             self.line(left, end, left+col_width*2, end)
#             self.line(left, top, left, end)
#             self.line(left+col_width/3, top, left+col_width/3, end)
#             self.line(left+col_width*2, top, left+col_width*2, end)
#             pg_flag+=1
#             # if pg_flag in add_page_list:
#             #     self.add_page()
#             if self.y > self.h - 6*row_height:
#                 self.add_page()

#         if self.y > self.h - 10*row_height:
#                 self.add_page()
        
#         # Task 4 : 'Other issues'
#         self.set_font('Arial', 'B', 9)
#         self.cell(col_width*2, row_height, f'{task_names[3]}', border=True,ln=True,align='C')
#         # self.set_font('Arial', '', 9)
#         recommend_list = self.care_plan_json[task_names[3]]['recommendation'][task_names[3]]
#         sub_keys = list(recommend_list[0].keys())
#         #row 1
#         self.set_font('Arial', '', 8)
#         instruct_text = 'Cancer survivors may experience issues with the areas listed below. If you have any concerns in these or other areas, please speak with your doctors or nurses to find out how you can get help with them.'
#         self.multi_cell(col_width*2,row_height,instruct_text,border=True,align='L',ln=True)
#         #row 2
#         self.set_font('Arial', 'B', 9)
#         self.cell(col_width/3, row_height, f'{sub_keys[0]}', border=True,align='C')
#         self.cell(col_width*2 - col_width/3, row_height, f'{sub_keys[1]}', border=True,align='C',ln=True)

#         # fill the recommendations
#         self.set_font('Arial', '', 9)
#         for i in range(len(recommend_list)):
#             top = self.y
#             left = self.x
#             end_list = []
#             # self.multi_cell(col_width/3, row_height, f'{recommend_list[i][sub_keys[0]].strip()}',align='L')
#             self.add_info_to_multicell(f'{recommend_list[i][sub_keys[0]].strip()}',X=self.x,Y=self.y,col_width = col_width/3,row_height = row_height,is_ln=False,align='L')
#             end_list.append(self.y)
#             self.y = top

#             # self.multi_cell(col_width*2 - col_width/3, row_height, f'{recommend_list[i][sub_keys[1]]}',ln=True,align='L')
#             self.add_info_to_multicell(f'{recommend_list[i][sub_keys[1]]}',X=self.x,Y=self.y,col_width = col_width*2 - col_width/3,row_height = row_height,is_ln=True,align='L')
#             end_list.append(self.y)
#             end = max(end_list)
#             self.y = end
#             self.line(left, end, left+col_width*2, end)
#             self.line(left, top, left, end)
#             self.line(left+col_width/3, top, left+col_width/3, end)
#             self.line(left+col_width*2, top, left+col_width*2, end)
#             pg_flag+=1
#             # if pg_flag in add_page_list:
#             #     self.add_page()
#             if self.y > self.h - 6*row_height:
#                 self.add_page()
            
#         if self.y > self.h - 10*row_height:
#                 self.add_page()


#         # Task 5 : 'Lifestyle and behavior'
#         self.set_font('Arial', 'B', 9)
#         self.cell(col_width*2, row_height, f'{task_names[4]}', border=True,ln=True,align='C')
#         # self.set_font('Arial', '', 9)
#         recommend_list = self.care_plan_json[task_names[4]]['recommendation'][task_names[4]]
#         sub_keys = list(recommend_list[0].keys())
#         #row 1
#         self.set_font('Arial', '', 8)
#         instruct_text = 'A number of lifestyle/behaviors can affect your ongoing health, including the risk for the cancer coming back or developing another cancer. Discuss these recommendations with your doctor or nurse.'
#         self.multi_cell(col_width*2,row_height,instruct_text,border=True,align='L',ln=True)
#         #row 2
#         self.set_font('Arial', 'B', 9)
#         self.cell(col_width/2, row_height, f'{sub_keys[0]}', border=True,align='C')
#         self.cell(col_width*2 - col_width/2, row_height, f'{sub_keys[1]}', border=True,align='C',ln=True)

#         # fill the recommendations
#         self.set_font('Arial', '', 9)
#         for i in range(len(recommend_list)):
#             top = self.y
#             left = self.x
#             end_list = []
            
#             # self.multi_cell(col_width/2, row_height, f'{recommend_list[i][sub_keys[0]].strip()}',align='L')
#             self.add_info_to_multicell(f'{recommend_list[i][sub_keys[0]].strip()}',X=self.x,Y=self.y,col_width = col_width/2,row_height = row_height,is_ln=False,align='L')
#             end_list.append(self.y)
#             self.y = top

#             # self.multi_cell(col_width*2 - col_width/2, row_height, f'{recommend_list[i][sub_keys[1]]}',ln=True,align='L')
#             self.add_info_to_multicell(f'{recommend_list[i][sub_keys[1]]}',X=self.x,Y=self.y,col_width = col_width*2 - col_width/2,row_height = row_height,is_ln=True,align='L')
#             end_list.append(self.y)
#             end = max(end_list)
#             self.y = end
#             self.line(left, end, left+col_width*2, end)
#             self.line(left, top, left, end)
#             self.line(left+col_width/2, top, left+col_width/2, end)
#             self.line(left+col_width*2, top, left+col_width*2, end)
#             pg_flag+=1
#             # if pg_flag in add_page_list:
#             #     self.add_page()
#             if self.y > self.h - 6*row_height:
#                 self.add_page()
#         if self.y > self.h - 10*row_height:
#                 self.add_page()


#         # Task 6 : 'Helpful resources'
#         self.set_font('Arial', 'B', 9)
#         self.cell(col_width*2, row_height, f'{task_names[5]}', border=True,ln=True,align='C')
#         # self.set_font('Arial', '', 9)
#         recommend_list = self.care_plan_json[task_names[5]]['recommendation'][task_names[5]]
#         sub_keys = list(recommend_list[0].keys())
#         #row 1
#         top = self.y
#         for i in range(len(recommend_list)):
#             self.set_font('Arial', '', 9)
#             # self.cell(col_width*2, row_height, f'{recommend_list[i][sub_keys[0]]}',ln=True,align='L')
#             self.add_info_to_cell(f'{recommend_list[i][sub_keys[0]]}',X=self.x,Y=self.y,col_width = col_width*2,row_height = row_height,is_ln=True,align='L')
#             pg_flag+=1
#             # if pg_flag in add_page_list:
#             #     self.add_page()
#             if self.y > self.h - 4*row_height:
#                 left = self.x
#                 end = self.y
#                 self.line(left,top,left,end)
#                 self.line(left+col_width*2,top,left+col_width*2,end)
#                 self.add_page()
#                 top = self.y
            
#         left = self.x
#         end = self.y
#         self.line(left,top,left,end)
#         self.line(left+col_width*2,top,left+col_width*2,end)
#         self.line(left,end,left+col_width*2,end)
        
#         # if self.y > self.h - 6*row_height:
#         #         self.add_page()

#         # Other Comments
#         self.set_font('Arial', '', 9)
#         self.cell(col_width*2, row_height*2, f'Other Comments', border=True,ln=True,align='L')
#         # self.set_font('Arial', '', 9)

#         # Generated by and Checked by and delivered on
#         self.cell(2*col_width/3, row_height, f'Generated by: SurvGPT', border=True,align='L')
#         self.cell(2*col_width/3, row_height, f'Checked by:', border=True,align='L')
#         self.cell(2*col_width/3, row_height, f'Delivered on:', border=True,align='L',ln=True)


#     def covert_gen_to_pdf(self):
#         self.set_auto_page_break(auto = True,margin=15)
#         self.general_info()
#         self.treatment_summary_table()
#         self.follow_up_care_plan_table()


class SurvGPT_PDF_2stage(FPDF):
    '''
    This class is used to generate the pdf for the survivorship care plan. This class 
    converts the LLM generations in json file to pdf. 
    Args:
        care_plan_json: json file generated by the LLM model for the care plan
        treatment_summary_json: json file generated by the LLM model for the treatment summary
    '''
    def __init__(self, care_plan_json,treatment_summary_json,general_info_json=None):
        super().__init__()
        '''
        Initialize the class with the care plan json and treatment summary json
        Args:
            care_plan_json: json file generated by the LLM model for the care plan
            treatment_summary_json: json file generated by the LLM model for the treatment summary
        '''
        self.cancer_type = treatment_summary_json['Treatment Summary']['Diagnosis']['Cancer type']#care_plan_json['cancer_type']
        self.care_plan_json = care_plan_json
        self.treatment_summary_json = treatment_summary_json
        if general_info_json!=None:
            self.general_info_json = general_info_json['General Information']
        else:
            self.general_info_json = None
        self.font_color_info = [0,0,255]


        #add arial font
        self.add_font("Arial", style="", fname="./fonts/Arial.ttf", uni=True)
        self.add_font("Arial", style="B", fname="./fonts/Arial_Bold.ttf", uni=True)
        self.add_font("Arial", style="I", fname="./fonts/Arial_Italic.ttf", uni=True)
        self.add_font("Arial", style="BI", fname="./fonts/Arial_Bold_Italic.ttf", uni=True)


    def add_info_to_cell(self,info,X,Y,col_width,row_height,is_ln=False,align='L',border=False):
        '''
        Function to add information to a cell form the generation in a blue font color
        Args:
            info: information to be added to the cell
            X: x coordinate of the cell
            Y: y coordinate of the cell
            col_width: width of the cell
            row_height: height of the cell
            is_ln: boolean to indicate a line break
            align: alignment of the text in the cell
            border: boolean to indicate if the cell has a border
        '''

        self.set_text_color(self.font_color_info[0],self.font_color_info[1],self.font_color_info[2])
        self.x = X
        self.y = Y
        self.cell(col_width, row_height, info, ln=is_ln, align=align,border=border)
        self.set_text_color(0,0,0)

    def add_info_to_multicell(self,info,X,Y,col_width,row_height,is_ln=False,align='L',border=False):
        '''
        Function to add information to a multicell form the generation in a blue font color
        Args:
            info: information to be added to the multicell
            X: x coordinate of the multicell
            Y: y coordinate of the multicell
            col_width: width of the multicell
            row_height: height of the multicell
            is_ln: boolean to indicate a line break
            align: alignment of the text in the multicell
            border: boolean to indicate if the multicell has a border 
        '''
        self.set_text_color(self.font_color_info[0],self.font_color_info[1],self.font_color_info[2])
        self.x = X
        self.y = Y
        self.multi_cell(col_width, row_height, info, ln=is_ln, align=align,border=border)
        self.set_text_color(0,0,0)


    def header(self):
        '''
        Function to add the header to the pdf 
        '''
        # font
        self.set_font('Arial', 'B', 12)
        # Calculate width of the title and position
        title = f'SurvGPT: Treatment Summary and Survivorship Care Plan for Lung Cancer'
        title_w = self.get_string_width(title) + 6
        doc_w = self.w
        self.set_x((doc_w - title_w) / 2)

        # Title
        self.cell(0, 10,title , ln=True, align='C')

    def footer(self):
        '''
        Function to add the footer to the pdf 
        '''
        # Set position of the footer
        self.set_y(-15)
        # Set font
        self.set_font('Arial','', 8)
        # Page number
        # self.cell(0, 10, f'Page {self.page_no()}', align='C')
        self.cell(0, 10, 'This survivorship care plan format is adapted from the templates provided by ASCO' )
    
    def general_info(self):
        '''
        Function to add the general information of the patient to the pdf 
        '''
        # #Add Page
        self.add_page()
        # font
        self.set_font('Arial', 'B', 11)
         # set width for each column (2 columns)
        col_width = self.w / 2.2
        # set height for each row
        row_height = self.font_size * 1.5
        # Section Title
        self.set_fill_color(211, 211, 211) 
        self.cell(col_width*2, row_height, 'General Information', ln=False, align='C',border=True,fill=True)
        self.set_font('Arial', '', 6)
        self.add_info_to_cell('Filled using Synthetic Patient Data',X = self.x-2*col_width,Y = self.y,col_width=2*col_width,row_height=row_height, is_ln=True,align='R')
        # Table for general information
        # font
        self.set_font('Arial', '', 9)
       
        # set alignment for each cell
        # self.set_xy(10, 40)
        # Row 1
        self.cell(col_width, row_height, 'Patient Name:', border=True)
        offset = self.get_string_width('Patient Name:')+2
        if self.general_info_json!=None:
             self.add_info_to_cell(self.general_info_json['Patient Name'],X = self.x-col_width+offset,Y = self.y,col_width=col_width - offset,row_height=row_height, is_ln=False,align='L')
        # self.add_info_to_cell(self.treatment_summary_json['ptnum'],X = self.x-col_width+offset,Y = self.y,col_width=col_width - offset,row_height=row_height, is_ln=False,align='L')  ### temporary fake name
        self.cell(col_width, row_height, 'Patient DOB:', border=True,ln=False)
        offset = self.get_string_width('Patient DOB:')+2
        if self.general_info_json!=None:
            self.add_info_to_cell(self.general_info_json['Patient DOB'],X = self.x-col_width+offset,Y = self.y,col_width=col_width - offset,row_height=row_height, is_ln=True,align='L')
        # self.add_info_to_cell('01/07/1985',X = self.x-col_width+offset,Y = self.y,col_width=col_width - offset,row_height=row_height, is_ln=True,align='L') ### temporary fake DOB
        # self.add_info_to_cell('',X = self.x-col_width+offset,Y = self.y,col_width=col_width - offset,row_height=row_height, is_ln=True,align='L') ### temporary fake DOB

        # Row 2
        self.set_font('Arial', 'B', 9)
        self.cell(col_width*2, row_height, 'Health Care Providers (Including Names, Institution)', border=True,ln=True,align='C')
        self.set_font('Arial', '', 9)
        self.cell(col_width*2, row_height, 'Primary Care Provider:', border=True,ln=False)
        offset = self.get_string_width('Primary Care Provider:')+2
        if self.general_info_json!=None:
            self.add_info_to_cell(self.general_info_json['Primary Care Provider'],X = self.x-2*col_width+offset,Y = self.y,col_width=2*col_width - offset,row_height=row_height, is_ln=True,align='L')
        # self.add_info_to_cell('Dr. Zephyra Nexis, VidaSphere Health Institute',X = self.x-2*col_width+offset,Y = self.y,col_width=2*col_width - offset,row_height=row_height, is_ln=True,align='L') ### temporary fake 
        # self.add_info_to_cell('',X = self.x-2*col_width+offset,Y = self.y,col_width=2*col_width - offset,row_height=row_height, is_ln=True,align='L')
        self.cell(col_width*2, row_height, 'Surgeon:', border=True,ln=False)
        # offset = self.get_string_width('Primary Care Provider::')+2
        if self.general_info_json!=None:
            self.add_info_to_cell(self.general_info_json['Surgeon'],X = self.x-2*col_width+offset,Y = self.y,col_width=2*col_width - offset,row_height=row_height, is_ln=True,align='L')
        # self.add_info_to_cell('Dr. Kyrona Vexel, PheonixMed Hospital Network',X = self.x-2*col_width+offset,Y = self.y,col_width=2*col_width - offset,row_height=row_height, is_ln=True,align='L') ### temporary fake 
        # self.add_info_to_cell('',X = self.x-2*col_width+offset,Y = self.y,col_width=2*col_width - offset,row_height=row_height, is_ln=True,align='L')
        self.cell(col_width*2, row_height, 'Radiation Oncologist:', border=True,ln=False)
        # offset = self.get_string_width('Radiation Oncologist:')+2
        if self.general_info_json!=None:
            self.add_info_to_cell(self.general_info_json['Radiation Oncologist'],X = self.x-2*col_width+offset,Y = self.y,col_width=2*col_width - offset,row_height=row_height, is_ln=True,align='L')
        # self.add_info_to_cell('Dr. Qylix Rendara, ZenithCare Healing Center',X = self.x-2*col_width+offset,Y = self.y,col_width=2*col_width - offset,row_height=row_height, is_ln=True,align='L') ### temporary fake 
        # self.add_info_to_cell('',X = self.x-2*col_width+offset,Y = self.y,col_width=2*col_width - offset,row_height=row_height, is_ln=True,align='L')
        self.cell(col_width*2, row_height, 'Medical Oncologist:', border=True,ln=False)
        # offset = self.get_string_width('Medical Oncologist:')+2
        if self.general_info_json!=None:
            self.add_info_to_cell(self.general_info_json['Medical Oncologist'],X = self.x-2*col_width+offset,Y = self.y,col_width=2*col_width - offset,row_height=row_height, is_ln=True,align='L')
        # self.add_info_to_cell('Dr. Vion Talrex, PheonixMed Hospital Network',X = self.x-2*col_width+offset,Y = self.y,col_width=2*col_width - offset,row_height=row_height, is_ln=True,align='L') ### temporary fake 
        # self.add_info_to_cell('',X = self.x-2*col_width+offset,Y = self.y,col_width=2*col_width - offset,row_height=row_height, is_ln=True,align='L') 
        self.cell(col_width*2, row_height, 'Other Providers:', border=True,ln=False)
        # offset = self.get_string_width('Surgeon:')+2
        if self.general_info_json!=None:
            self.add_info_to_cell(self.general_info_json['Other Providers'],X = self.x-2*col_width+offset,Y = self.y,col_width=2*col_width - offset,row_height=row_height, is_ln=True,align='L')
        # self.add_info_to_cell('Dr. Kyrona Vexel, PheonixMed Hospital Network',X = self.x-col_width+offset,Y = self.y,col_width=col_width - offset,row_height=row_height, is_ln=True,align='L') ### temporary fake 


    def treatment_summary_table(self):
        '''
        Function to add the treatment summary table to the pdf 
        '''
        # font
        self.set_font('Arial', 'B', 11)
         # set width for each column (2 columns)
        col_width = self.w / 2.2
        # set height for each row
        row_height = self.font_size * 1.5
        # Section Title
        self.set_fill_color(211, 211, 211) 
        self.cell(col_width*2, row_height, 'Treatment Summary', ln=True, align='C',border=True,fill=True)

        # Table for treatment summary
        # font
        self.set_font('Arial', '', 9)
       
        # set alignment for each cell
        # self.set_xy(10, 40)

        # Diagnosis ================= 'Cancer type', 'Diagnosis Date', 'Cancer stage'
        self.set_font('Arial', 'B', 9)
        self.cell(col_width*2, row_height, 'Diagnosis', border=True,ln=True,align='C')
        self.set_font('Arial', '', 9)
        temp_json = self.treatment_summary_json['Treatment Summary']['Diagnosis']
        key_names = list(temp_json.keys())

        #row 1
        data_text = f'Cancer Type/Location/Histology Subtype: {self.cancer_type}'
        data_w = self.get_string_width(data_text)+2
        self.cell(data_w, row_height, f'Cancer Type/Location/Histology Subtype:', border=True) # Cancer Type/Location/Histology Subtype
        offset = self.get_string_width('Cancer Type/Location/Histology Subtype: ')
        self.add_info_to_cell(f'{self.cancer_type}',X = self.x-data_w+offset,Y = self.y,col_width=data_w - offset,row_height=row_height, is_ln=False,align='L')
        ####
        self.cell(col_width*2-data_w, row_height, f'{key_names[1]}:', border=True,ln=False) # Diagnosis Date
        offset = self.get_string_width(f'{key_names[1]}: ')
        self.add_info_to_cell(f'{temp_json[key_names[1]]}',X = self.x-col_width*2+data_w+offset,Y = self.y,col_width=col_width*2-data_w - offset,row_height=row_height, is_ln=True,align='L')

        #row 2
        self.cell(col_width*2, row_height, f'{key_names[2]}:', border=True,ln=False) # Stage
        offset = self.get_string_width(f'{key_names[2]}: ')
        self.add_info_to_cell(f'{temp_json[key_names[2]]}',X = self.x-col_width*2+offset,Y = self.y,col_width=col_width*2 - offset,row_height=row_height, is_ln=True,align='L')
        
        
        # Treatment Completed ================= 
        # 'Surgery', 'Surgery Date(s) (year)', 'Surgical Procedure/location/findings', 'Radiation', 'Body area treated', 'End Date (year)', 'Systemic Therapy (Chemotherapy, hormonal therapy, other)', 'Names of Agents used', 'Persistent symptoms or side effects at completion of treatment'
        self.set_font('Arial', 'B', 9)
        self.cell(col_width*2, row_height, 'Treatment Completed', border=True,ln=True,align='C')
        self.set_font('Arial', '', 9)
        temp_json = self.treatment_summary_json['Treatment Summary']['Treatment Completed']
        key_names = list(temp_json.keys())

        #row 1
        self.cell(col_width, row_height, f'{key_names[0]}:', border=True) # Surgery
        offset = self.get_string_width(f'{key_names[0]}: ')
        self.add_info_to_cell(f'{temp_json[key_names[0]]}',X = self.x-col_width+offset,Y = self.y,col_width=col_width - offset,row_height=row_height, is_ln=False,align='L')
        ####
        self.cell(col_width, row_height, f'{key_names[1]}:', border=True,ln=False) # Surgery Date(s) (year)
        offset = self.get_string_width(f'{key_names[1]}: ')
        self.add_info_to_cell(f'{temp_json[key_names[1]]}',X = self.x-col_width+offset,Y = self.y,col_width=col_width - offset,row_height=row_height, is_ln=True,align='L')

        #row 2
        top = self.y
        left = self.x
        self.cell(col_width*2, row_height, f'{key_names[2]}:', border=False,ln=False) #Surgical Procedure/location/findings
        offset = self.get_string_width(f'{key_names[2]}: ')
        self.add_info_to_multicell(f'{temp_json[key_names[2]]}',X = self.x-col_width*2+offset,Y = self.y,col_width=col_width*2 - offset,row_height=row_height, is_ln=True,align='L')
        end = self.y
        self.line(left, top, left, end)
        self.line(left+2*col_width, top, left+2*col_width, end)
        self.line(left, end, left+2*col_width, end)

        #row 3
        top = self.y
        left = self.x
        self.cell(self.w / 3.3, row_height, f'{key_names[3]}:', border=False) # Radiation
        offset = self.get_string_width(f'{key_names[3]}: ')
        self.add_info_to_cell(f'{temp_json[key_names[3]]}',X = self.x-(self.w / 3.3) +offset,Y = self.y,col_width=(self.w / 3.3) - offset,row_height=row_height, is_ln=False,align='L')
        end_list = [self.y]
        ####
        self.y = top
        self.cell(self.w / 3.3, row_height, f'{key_names[4]}:', border=False) # Body area treated
        offset = self.get_string_width(f'{key_names[4]}: ')
        self.add_info_to_multicell(f'{temp_json[key_names[4]]}',X = self.x-(self.w / 3.3) +offset,Y = self.y,col_width=(self.w / 3.3) - offset,row_height=row_height, is_ln=False,align='L')
        end_list.append(self.y)
        ####
        self.y = top
        self.cell(self.w / 3.3, row_height, f'{key_names[5]}:', border=False,ln=False) # End Date (year)
        offset = self.get_string_width(f'{key_names[5]}: ')
        self.add_info_to_cell(f'{temp_json[key_names[5]]}',X = self.x-(self.w / 3.3) +offset,Y = self.y,col_width=(self.w / 3.3) - offset,row_height=row_height, is_ln=True,align='L')
        end_list.append(self.y)
        end = max(end_list)
        self.y = end
        self.line(left, top, left, end)
        self.line(left+self.w / 3.3, top, left+self.w / 3.3, end)
        self.line(left+2*self.w / 3.3, top, left+2*self.w / 3.3, end)
        self.line(left+3*self.w / 3.3, top, left+3*self.w / 3.3, end)
        self.line(left, end, left+3*self.w / 3.3, end)

        #row 4
        self.cell(col_width*2, row_height, f'{key_names[6]}:', border=True,ln=False) # Systemic Therapy (Chemotherapy, hormonal therapy, other)
        offset = self.get_string_width(f'{key_names[6]}: ')
        self.add_info_to_cell(f'{temp_json[key_names[6]]}',X = self.x-col_width*2+offset,Y = self.y,col_width=col_width*2 - offset,row_height=row_height, is_ln=True,align='L')

        ############################################################################################################
        # Names of Agents used =================
        # temp_json = self.treatment_summary_json['Treatment Summary']['Names of Agents used']
        # num_agents = list(temp_json.keys())

        # #row 5 
        # self.cell(col_width, row_height, f'Names of Agents used', border=True,align ='C') # Names of Agents used
        # self.cell(col_width, row_height, f'End Dates (year)', border=True,ln=True,align ='C')
        # # Number of agents used data
        # i=0
        # while i<len(num_agents):
        #     if 'Other' in num_agents[i]:
        #         top = self.y
        #         left = self.x
        #         self.multi_cell(col_width, row_height, f'{num_agents[i]}:', border=False)
        #         offset = self.get_string_width(f'{num_agents[i]}: ')+2
        #         self.add_info_to_multicell(f'{temp_json[num_agents[i]]}',X = self.x-col_width+offset,Y = top,col_width=col_width - offset,row_height=row_height, is_ln=False,align='C')
        #         end_list = [self.y]
        #         i+=1
        #         if i>=len(num_agents):
        #             self.y = top
        #             self.cell(col_width, row_height, '', align = 'C',border=False, ln=True)
                    
        #         elif 'End' in num_agents[i]:
        #             # self.cell(col_width, row_height, f'{temp_json[key_names[7]][num_agents[i]]}', align = 'C',border=True, ln=True)
        #             self.y = top
        #             self.add_info_to_cell(f'{temp_json[num_agents[i]]}',X = self.x,Y = self.y,col_width=col_width,row_height=row_height, is_ln=True,align='C',border=False)
        #             end_list.append(self.y)
        #             i+=1
        #         else:
        #             self.y = top
        #             self.cell(col_width, row_height, '', align = 'C',border=False, ln=True)
        #         end = max(end_list)
        #         self.y = end
        #         self.line(left, top, left, end)
        #         self.line(left+col_width, top, left+col_width, end)
        #         self.line(left+2*col_width, top, left+2*col_width, end)
        #         self.line(left, end, left+2*col_width, end)

        #         break 
        #     if 'Yes' in temp_json[num_agents[i]] or 'yes' in temp_json[num_agents[i]]:
        #         self.cell(col_width, row_height, f'{num_agents[i]}:', border=True)
        #         offset = self.get_string_width(f'Paclitaxel / Docetaxel: ')+2
        #         self.add_info_to_cell(f'{temp_json[num_agents[i]]}',X = self.x-col_width+offset,Y = self.y,col_width=col_width - offset,row_height=row_height, is_ln=False,align='C')
        #         i+=1
        #         if i>=len(num_agents):
        #             self.y = top
        #             self.cell(col_width, row_height, '', align = 'C',border=False, ln=True)
                   
        #         if 'End' in num_agents[i]: # if there is an end date
        #             # self.cell(col_width, row_height, f'{temp_json[key_names[7]][num_agents[i]]}', align = 'C',border=True, ln=True)
        #             self.add_info_to_cell(f'{temp_json[num_agents[i]]}',X = self.x,Y = self.y,col_width=col_width,row_height=row_height, is_ln=True,align='C',border=True)
        #             i+=1
        #         else:
        #             self.cell(col_width, row_height, '', align = 'C',border=True, ln=True)
    
        #     else:
        #         self.cell(col_width, row_height, f'{num_agents[i]}: ', border=True)
        #         offset = self.get_string_width(f'Paclitaxel / Docetaxel: ')+2
        #         self.add_info_to_cell(f'{temp_json[num_agents[i]]}',X = self.x-col_width+offset,Y = self.y,col_width=col_width - offset,row_height=row_height, is_ln=False,align='C')
        #         i+=1
        #         if i>=len(num_agents):
        #             self.y = top
        #             self.cell(col_width, row_height, '', align = 'C',border=False, ln=True)
                   
        #         if 'End' in num_agents[i]: # if there is an end date
        #             # self.cell(col_width, row_height, f'{temp_json[key_names[7]][num_agents[i]]}', align = 'C',border=True, ln=True)
        #             self.add_info_to_cell(f'{temp_json[num_agents[i]]}',X = self.x,Y = self.y,col_width=col_width,row_height=row_height, is_ln=True,align='C',border=True)
        #             i+=1
        #         else:
        #             self.cell(col_width, row_height, '', align = 'C',border=True, ln=True)
    
        ############################################################################################################
        # #row 5  Names of Agents used
        # temp_json = self.treatment_summary_json['Treatment Summary']['Names of Agents used']
        # num_agents = list(temp_json.keys())
        # self.cell(col_width, row_height, f'Names of Agents used', border=True,align ='C') # Names of Agents used
        # self.cell(col_width, row_height, f'End Dates (year)', border=True,ln=True,align ='C')
        # # Number of agents used data
        # # num_agents = list(temp_json[key_names[7]].keys())
        # i=0
        # while i<len(num_agents):
        #     if 'Other' in num_agents[i]:
        #         other_key_names = list(temp_json[num_agents[i]].keys())
        #         top = self.y
        #         left = self.x
        #         self.cell(col_width, row_height, f'{num_agents[i]}:', border=False,ln=True)
        #         offset = self.get_string_width(f'Paclitaxel / Docetaxel: ')+2
        #         # 
        #         if isinstance(temp_json[num_agents[i]][other_key_names[0]],str):
        #             temp_top = self.y
        #             self.add_info_to_multicell(f'{temp_json[num_agents[i]][other_key_names[0]]}',X = self.x-col_width+offset,Y = self.y,col_width=col_width - offset,row_height=row_height, is_ln=False,align='L')
        #             self.y = temp_top
        #             self.add_info_to_multicell(f'{temp_json[num_agents[i]][other_key_names[1]]}',X = self.x,Y = self.y,col_width=col_width ,row_height=row_height, is_ln=True,align='C')
        #         else:
        #             for other_agent_no in range(len(temp_json[num_agents[i]][other_key_names[0]])):
        #                 temp_top = self.y
        #                 self.add_info_to_multicell(f'{temp_json[num_agents[i]][other_key_names[0]][other_agent_no]}',X = self.x,Y = self.y,col_width=col_width,row_height=row_height, is_ln=False,align='L')
        #                 end_list = [self.y]
        #                 self.y = temp_top
        #                 self.add_info_to_multicell(f'{temp_json[num_agents[i]][other_key_names[1]][other_agent_no]}',X = self.x,Y = self.y,col_width=col_width ,row_height=row_height, is_ln=True,align='C')
        #                 end_list.append(self.y)
        #                 self.y = max(end_list)
        #         end = self.y
        #         self.line(left, top, left, end)
        #         self.line(left+col_width, top, left+col_width, end)
        #         self.line(left+2*col_width, top, left+2*col_width, end)
        #         self.line(left, end, left+2*col_width, end)
        #         i+=1

        #         break 

        #     self.cell(col_width, row_height, f'{num_agents[i]}:', border=True)
        #     offset = self.get_string_width(f'Paclitaxel / Docetaxel: ')+2
        #     temp_keys = list(temp_json[num_agents[i]].keys())
        #     self.add_info_to_cell(f'{temp_json[num_agents[i]][temp_keys[0]]}',X = self.x-col_width+offset,Y = self.y,col_width=col_width - offset,row_height=row_height, is_ln=False,align='C')
        #     self.add_info_to_cell(f'{temp_json[num_agents[i]][temp_keys[1]]}',X = self.x,Y = self.y,col_width=col_width,row_height=row_height, is_ln=True,align='C',border=True)
                
        #     i+=1

        ############################################################################################################
        temp_json = self.treatment_summary_json['Treatment Summary']['Names of Agents used in Completed Treatments']
        # check if list
        if isinstance(temp_json, list):
            #convert to dictionary
            temp_json = {f'Agent {i+1}':temp_json[i] for i in range(len(temp_json))}
            # temp_json = temp_json
        num_agents = list(temp_json.keys())
        self.cell(col_width, row_height, f'Names of Agents used', border=True,align ='C') # Names of Agents used
        self.cell(col_width, row_height, f'End Dates (year)', border=True,ln=True,align ='C')
        # Number of agents used data
        # num_agents = list(temp_json[key_names[7]].keys())
        i=0
        while i<len(num_agents):
            top = self.y
            left = self.x
            agent_json = temp_json[num_agents[i]]
            agent_key = list(agent_json.keys())
            if agent_json[agent_key[0]] in ['Not given','not given','No','no']:
                self.add_info_to_cell(f'',X = self.x,Y = self.y,col_width=col_width,row_height=row_height, is_ln=False,align='C')
                self.add_info_to_cell(f'',X = self.x,Y = self.y,col_width=col_width,row_height=row_height, is_ln=True,align='C')
                # break
            else:
                self.add_info_to_cell(f'{agent_json[agent_key[0]]}',X = self.x,Y = self.y,col_width=col_width,row_height=row_height, is_ln=False,align='C')
                self.add_info_to_cell(f'{agent_json[agent_key[1]]}',X = self.x,Y = self.y,col_width=col_width,row_height=row_height, is_ln=True,align='C')
            i+=1
            end = self.y
            self.line(left, top, left, end)
            self.line(left+col_width, top, left+col_width, end)
            self.line(left+2*col_width, top, left+2*col_width, end)
            self.line(left, end, left+2*col_width, end)

        ############################################################################################################
        # Persistent symptoms or side effects at completion of treatment =================
        symptom = self.treatment_summary_json['Treatment Summary']['Persistent symptoms or side effects at completion of treatment']
        #row 6
        top = self.y
        left = self.x
        self.cell(col_width*2, row_height, f'Persistent symptoms or side effects at completion of treatment:', border=False,ln=False) # Persistent symptoms or side effects at completion of treatment
        offset = self.get_string_width(f'Persistent symptoms or side effects at completion of treatment: ')
        is_symptoms = symptom['Symptoms of side effects']
        self.add_info_to_cell(f'{is_symptoms}',X = self.x-col_width*2+offset,Y = self.y,col_width=col_width*2 - offset,row_height=row_height, is_ln=True,align='L')
        if isinstance(symptom['Symptom or side effect types'],str):
             effects_text = f'{symptom["Symptom or side effect types"]}'
        else:
            effects_text = ''
            for effects in symptom['Symptom or side effect types']:
                effects_text += f'{effects}, '
        self.add_info_to_multicell(f'{effects_text}',X = self.x,Y = self.y,col_width=col_width*2 ,row_height=row_height, is_ln=True,align='L')
        end = self.y
        self.line(left, top, left, end)
        self.line(left+col_width*2, top, left+col_width*2, end)
        self.line(left, end, left+col_width*2, end)


        # Treatment Ongoing =================
        # 'Need for ongoing (adjuvant) treatment for cancer', 'Ongoing treatment', 'Planned duration', 'Possible side effects'
        self.set_font('Arial', 'B', 9)
        self.cell(col_width*2, row_height, 'Treatment Ongoing', border=True,ln=True,align='C')
        self.set_font('Arial', '', 9)
        temp_json = self.treatment_summary_json['Treatment Summary']['Treatment Ongoing and Side Effects']
        key_names = list(temp_json.keys())
        #row 1
        self.cell(col_width*2, row_height, f'{key_names[0]}:', border=True,ln=False) # Need for ongoing (adjuvant) treatment for cancer
        offset = self.get_string_width(f'{key_names[0]}: ')
        self.add_info_to_cell(f'{temp_json[key_names[0]]}',X = self.x-col_width*2+offset,Y = self.y,col_width=col_width*2 - offset,row_height=row_height, is_ln=True,align='L')

        #row 2
        self.cell(2*self.w / 5.5, row_height, 'Ongoing Treatment Name', border=True,align='C')
        self.cell(self.w / 5.5, row_height, 'Planned Duration', border=True,align='C')
        self.cell(2*self.w / 5.5, row_height, 'Possible Side Effects', border=True,align='C',ln=True)
        if 'No' in temp_json[key_names[0]] or 'no' in temp_json[key_names[0]]:
            # self.cell(self.w / 3.3, row_height, 'not given', border=True,align='C')
            # self.cell(self.w / 3.3, row_height, 'not given', border=True,align='C')
            # self.cell(self.w / 3.3, row_height, 'not given', border=True,align='C',ln=True)
            self.add_info_to_cell('not given',X = self.x,Y = self.y,col_width=2*self.w / 5.5,row_height=row_height, is_ln=False,align='C',border=True)
            self.add_info_to_cell('not given',X = self.x,Y = self.y,col_width=self.w / 5.5,row_height=row_height, is_ln=False,align='C',border=True)
            self.add_info_to_cell('not given',X = self.x,Y = self.y,col_width=2*self.w / 5.5,row_height=row_height, is_ln=True,align='C',border=True)
            
            self.cell(2*self.w / 5.5, row_height, '', border=True,align='C')
            self.cell(self.w / 5.5, row_height, '', border=True,align='C')
            self.cell(2*self.w / 5.5, row_height, '', border=True,align='C',ln=True)

            self.cell(2*self.w / 5.5, row_height, '', border=True,align='C')
            self.cell(self.w / 5.5, row_height, '', border=True,align='C')
            self.cell(2*self.w / 5.5, row_height, '', border=True,align='C',ln=True)


        else:
            
            for ong_treat in (key_names[1:]):
                if self.y > self.h - 6*row_height:
                    self.add_page()
                top = self.y
                left = self.x
                self.add_info_to_multicell(f'{temp_json[ong_treat][0]}',X = self.x,Y = self.y,col_width=2*self.w / 5.5,row_height=row_height, is_ln=False,align='C',border=False)
                end_list = [self.y]
                self.y = top
                self.add_info_to_multicell(f'{temp_json[ong_treat][1]}',X = self.x,Y = self.y,col_width=self.w / 5.5,row_height=row_height, is_ln=False,align='C',border=False)
                end_list.append(self.y)
                self.y = top
                self.add_info_to_multicell(f'{temp_json[ong_treat][2]}',X = self.x,Y = self.y,col_width=2*self.w / 5.5,row_height=row_height, is_ln=True,align='C',border=False)
                end_list.append(self.y)
                self.y = max(end_list)
                
                end = self.y       
                self.line(left, top, left, end)
                self.line(left+2*self.w / 5.5, top, left+2*self.w / 5.5, end)
                self.line(left+3*self.w / 5.5, top, left+3*self.w / 5.5, end)
                self.line(left+5*self.w / 5.5, top, left+5*self.w / 5.5, end)
                self.line(left, end, left+5*self.w / 5.5, end)
                    
    def follow_up_care_plan_table(self):
        '''
        Function to add the follow up care plan table to the pdf 
        '''
        pg_flag = 0
        add_page_list = [3,12,23,34,40,47]
        # font
        self.set_font('Arial', 'B', 11)
         # set width for each column (2 columns)
        col_width = self.w / 2.2
        # set height for each row
        row_height = self.font_size * 1.5
        # Section Title
        self.set_fill_color(211, 211, 211) 
        if self.y > self.h - 10*row_height:
                    self.add_page()
        self.cell(col_width*2, row_height, 'Follow-up Care Plan', ln=True, align='C',border=True,fill=True)

        # Table for follow up care plan
        # font
        self.set_font('Arial', '', 9)
        task_names = list(self.care_plan_json.keys())#[2:]

        # Task 1 : 'Schedule of Clinical Visits'
        self.set_font('Arial', 'B', 9)
        self.cell(col_width*2, row_height, f'{task_names[0]}', border=True,ln=True,align='C')
        # self.set_font('Arial', '', 9)
        recommend_list = self.care_plan_json[task_names[0]]['recommendation'][task_names[0]]
        sub_keys = list(recommend_list[0].keys())
        #row 1
        self.cell(col_width/3, row_height, f'{sub_keys[0]}', border=True,align='C')
        self.cell(col_width/2, row_height, f'{sub_keys[1]}', border=True,align='C')
        self.cell(col_width*2 -(5/6)*col_width, row_height, f'{sub_keys[2]}', border=True,align='C',ln=True)
        # fill the recommendations
        self.set_font('Arial', '', 9)
        for i in range(len(recommend_list)):
            if self.y > self.h - 10*row_height:
                self.add_page()
            top = self.y
            left = self.x
            
            end_list = []
            # self.multi_cell(col_width/3, row_height, f'{recommend_list[i][sub_keys[0]].strip()}',align='L')#, border=True)
            self.add_info_to_multicell(f'{recommend_list[i][sub_keys[0]].strip()}',X=self.x,Y=self.y,col_width = col_width/3,row_height = row_height,is_ln=False,align='L')
            end_list.append(self.y)
            self.y = top

            # self.multi_cell(col_width/2, row_height, f'{recommend_list[i][sub_keys[1]].strip()}',align='L')#, border=True)
            self.add_info_to_multicell(f'{recommend_list[i][sub_keys[1]].strip()}',X=self.x,Y=self.y,col_width = col_width/2,row_height = row_height,is_ln=False,align='L')
            end_list.append(self.y)
            self.y = top

            # self.multi_cell(col_width*2 -(5/6)*col_width, row_height, f'{recommend_list[i][sub_keys[2]].strip()}',ln=True,align='L')
            self.add_info_to_multicell(f'{recommend_list[i][sub_keys[2]].strip()}',X=self.x,Y=self.y,col_width = col_width*2 -(5/6)*col_width,row_height = row_height,is_ln=True,align='L')
            end_list.append(self.y)
            end = max(end_list)
            self.y = end
            self.line(left, end, left+col_width*2, end)
            self.line(left, top, left, end)
            self.line(left+col_width/3, top, left+col_width/3, end)
            self.line(left+col_width/2+col_width/3, top, left+col_width/2+col_width/3, end)
            self.line(left+col_width*2, top, left+col_width*2, end)
            pg_flag+=1

            # if pg_flag in add_page_list:
            #     self.add_page()
            
            
        if self.y > self.h - 10*row_height:
                self.add_page()    

        ## Task 2 : 'Cancer Surveillance or Other Recommended Tests'
        self.set_font('Arial', 'B', 9)
        self.cell(col_width*2, row_height, f'{task_names[1]}', border=True,ln=True,align='C')
        # self.set_font('Arial', '', 9)
        recommend_list = self.care_plan_json[task_names[1]]['recommendation'][task_names[1]]
        #if there are no recommendations
        if len(recommend_list)==0:
            self.cell(col_width*2, row_height, f'No recommendations', border=True,ln=True,align='C')
           
        else:
            sub_keys = list(recommend_list[0].keys())
            #row 1
            self.cell(col_width/3, row_height, f'{sub_keys[0]}', border=True,align='C')
            self.cell(col_width/3+2, row_height, f'{sub_keys[1]}', border=True,align='C')
            self.cell(col_width/3, row_height, f'{sub_keys[2]}', border=True,align='C')
            self.cell(col_width*2 -col_width-2, row_height, f'{sub_keys[3]}', border=True,align='C',ln=True)
            # fill the recommendations
            self.set_font('Arial', '', 9)
            for i in range(len(recommend_list)):
                if self.y > self.h - 10*row_height:
                    self.add_page()
                top = self.y
                left = self.x
                end_list = []
                # self.multi_cell(col_width/3, row_height, f'{recommend_list[i][sub_keys[0]].strip()}',align='L')#, border=True)
                self.add_info_to_multicell(f'{recommend_list[i][sub_keys[0]].strip()}',X=self.x,Y=self.y,col_width = col_width/3,row_height = row_height,is_ln=False,align='L')
                end_list.append(self.y)
                self.y = top


                # self.multi_cell(col_width/3 +2, row_height, f'{recommend_list[i][sub_keys[1]].strip()}',align='L')#, border=True)
                self.add_info_to_multicell(f'{recommend_list[i][sub_keys[1]].strip()}',X=self.x,Y=self.y,col_width = col_width/3+2,row_height = row_height,is_ln=False,align='L')
                end_list.append(self.y)
                self.y = top


                # self.multi_cell(col_width/3, row_height, f'{recommend_list[i][sub_keys[2]].strip()}',align='L')#, border=True)
                self.add_info_to_multicell(f'{recommend_list[i][sub_keys[2]].strip()}',X=self.x,Y=self.y,col_width = col_width/3,row_height = row_height,is_ln=False,align='L')
                end_list.append(self.y)
                self.y = top


                # self.multi_cell(col_width*2 -col_width-2, row_height, f'{recommend_list[i][sub_keys[3]]}',ln=True,align='L')
                self.add_info_to_multicell(f'{recommend_list[i][sub_keys[3]]}',X=self.x,Y=self.y,col_width = col_width*2 -col_width-2,row_height = row_height,is_ln=True,align='L')
                end_list.append(self.y)
                end = max(end_list)
                self.y = end
                self.line(left, end, left+col_width*2, end)
                self.line(left, top, left, end)
                self.line(left+col_width/3, top, left+col_width/3, end)
                self.line(left+2*col_width/3+2, top, left+2*col_width/3+2, end)
                self.line(left+3*col_width/3+2, top, left+3*col_width/3+2, end)
                self.line(left+col_width*2, top, left+col_width*2, end)
                pg_flag+=1

            # if pg_flag in add_page_list:
            #     self.add_page()
            
        
        if self.y > self.h - 10*row_height:
                self.add_page()

        # Task 3 : 'Possible late and long-term effects of cancer treatment'
        self.set_font('Arial', 'B', 9)
        self.cell(col_width*2, row_height, f'{task_names[2]}', border=True,ln=True,align='C')
        # self.set_font('Arial', '', 9)
        recommend_list = self.care_plan_json[task_names[2]]['recommendation'][task_names[2]]
        sub_keys = list(recommend_list[0].keys())
        # row 1
        self.set_font('Arial', '', 8)
        instruct_text = 'List of Possible late- and long-term effects that someone with this type of cancer and treatment may experience.'
        self.multi_cell(col_width*2,row_height,instruct_text,border=True,align='L',ln=True)
        #row 2
        self.set_font('Arial', 'B', 9)
        self.cell(col_width/3, row_height, f'{sub_keys[0]}', border=True,align='C')
        self.cell(col_width*2 - col_width/3, row_height, f'{sub_keys[1]}', border=True,align='C',ln=True)
        
        # fill the recommendations
        self.set_font('Arial', '', 9)
        for i in range(len(recommend_list)):
            if self.y > self.h - 10*row_height:
                self.add_page()
            top = self.y
            left = self.x
            end_list = []
            # self.multi_cell(col_width/3, row_height, f'{recommend_list[i][sub_keys[0]].strip()}',align='L')
            self.add_info_to_multicell(f'{recommend_list[i][sub_keys[0]].strip()}',X=self.x,Y=self.y,col_width = col_width/3,row_height = row_height,is_ln=False,align='L')
            end_list.append(self.y)
            self.y = top

            # self.multi_cell(col_width*2 - col_width/3, row_height, f'{recommend_list[i][sub_keys[1]]}',ln=True,align='L')
            self.add_info_to_multicell(f'{recommend_list[i][sub_keys[1]]}',X=self.x,Y=self.y,col_width = col_width*2 - col_width/3,row_height = row_height,is_ln=True,align='L')
            end_list.append(self.y)
            end = max(end_list)
            self.y = end
            self.line(left, end, left+col_width*2, end)
            self.line(left, top, left, end)
            self.line(left+col_width/3, top, left+col_width/3, end)
            self.line(left+col_width*2, top, left+col_width*2, end)
            pg_flag+=1
            # if pg_flag in add_page_list:
            #     self.add_page()
            

        if self.y > self.h - 10*row_height:
                self.add_page()
        
        # Task 4 : 'Other issues'
        self.set_font('Arial', 'B', 9)
        self.cell(col_width*2, row_height, f'{task_names[3]}', border=True,ln=True,align='C')
        # self.set_font('Arial', '', 9)
        recommend_list = self.care_plan_json[task_names[3]]['recommendation'][task_names[3]]
        sub_keys = list(recommend_list[0].keys())
        #row 1
        self.set_font('Arial', '', 8)
        instruct_text = 'Cancer survivors may experience issues with the areas listed below. If you have any concerns in these or other areas, please speak with your doctors or nurses to find out how you can get help with them.'
        self.multi_cell(col_width*2,row_height,instruct_text,border=True,align='L',ln=True)
        #row 2
        self.set_font('Arial', 'B', 9)
        self.cell(col_width/3, row_height, f'{sub_keys[0]}', border=True,align='C')
        self.cell(col_width*2 - col_width/3, row_height, f'{sub_keys[1]}', border=True,align='C',ln=True)

        # fill the recommendations
        self.set_font('Arial', '', 9)
        for i in range(len(recommend_list)):
            if self.y > self.h - 10*row_height:
                self.add_page()
            top = self.y
            left = self.x
            end_list = []
            # self.multi_cell(col_width/3, row_height, f'{recommend_list[i][sub_keys[0]].strip()}',align='L')
            self.add_info_to_multicell(f'{recommend_list[i][sub_keys[0]].strip()}',X=self.x,Y=self.y,col_width = col_width/3,row_height = row_height,is_ln=False,align='L')
            end_list.append(self.y)
            self.y = top

            # self.multi_cell(col_width*2 - col_width/3, row_height, f'{recommend_list[i][sub_keys[1]]}',ln=True,align='L')
            self.add_info_to_multicell(f'{recommend_list[i][sub_keys[1]]}',X=self.x,Y=self.y,col_width = col_width*2 - col_width/3,row_height = row_height,is_ln=True,align='L')
            end_list.append(self.y)
            end = max(end_list)
            self.y = end
            self.line(left, end, left+col_width*2, end)
            self.line(left, top, left, end)
            self.line(left+col_width/3, top, left+col_width/3, end)
            self.line(left+col_width*2, top, left+col_width*2, end)
            pg_flag+=1
            # if pg_flag in add_page_list:
            #     self.add_page()
            
            
        if self.y > self.h - 10*row_height:
                self.add_page()


        # Task 5 : 'Lifestyle and behavior'
        self.set_font('Arial', 'B', 9)
        self.cell(col_width*2, row_height, f'{task_names[4]}', border=True,ln=True,align='C')
        # self.set_font('Arial', '', 9)
        recommend_list = self.care_plan_json[task_names[4]]['recommendation'][task_names[4]]
        sub_keys = list(recommend_list[0].keys())
        #row 1
        self.set_font('Arial', '', 8)
        instruct_text = 'A number of lifestyle/behaviors can affect your ongoing health, including the risk for the cancer coming back or developing another cancer. Discuss these recommendations with your doctor or nurse.'
        self.multi_cell(col_width*2,row_height,instruct_text,border=True,align='L',ln=True)
        #row 2
        self.set_font('Arial', 'B', 9)
        self.cell(col_width/2, row_height, f'{sub_keys[0]}', border=True,align='C')
        self.cell(col_width*2 - col_width/2, row_height, f'{sub_keys[1]}', border=True,align='C',ln=True)

        # fill the recommendations
        self.set_font('Arial', '', 9)
        for i in range(len(recommend_list)):
            if self.y > self.h - 10*row_height:
                self.add_page()
            top = self.y
            left = self.x
            end_list = []
            
            # self.multi_cell(col_width/2, row_height, f'{recommend_list[i][sub_keys[0]].strip()}',align='L')
            self.add_info_to_multicell(f'{recommend_list[i][sub_keys[0]].strip()}',X=self.x,Y=self.y,col_width = col_width/2,row_height = row_height,is_ln=False,align='L')
            end_list.append(self.y)
            self.y = top

            # self.multi_cell(col_width*2 - col_width/2, row_height, f'{recommend_list[i][sub_keys[1]]}',ln=True,align='L')
            self.add_info_to_multicell(f'{recommend_list[i][sub_keys[1]]}',X=self.x,Y=self.y,col_width = col_width*2 - col_width/2,row_height = row_height,is_ln=True,align='L')
            end_list.append(self.y)
            end = max(end_list)
            self.y = end
            self.line(left, end, left+col_width*2, end)
            self.line(left, top, left, end)
            self.line(left+col_width/2, top, left+col_width/2, end)
            self.line(left+col_width*2, top, left+col_width*2, end)
            pg_flag+=1
            # if pg_flag in add_page_list:
            #     self.add_page()
            
        if self.y > self.h - 10*row_height:
                self.add_page()


        # Task 6 : 'Helpful resources'
        self.set_font('Arial', 'B', 9)
        self.cell(col_width*2, row_height, f'{task_names[5]}', border=True,ln=True,align='C')
        # self.set_font('Arial', '', 9)
        recommend_list = self.care_plan_json[task_names[5]]['recommendation'][task_names[5]]
        # check if there are no recommendations
        if len(recommend_list)!=0:
            sub_keys = list(recommend_list[0].keys())
            #row 1
            top = self.y
            for i in range(len(recommend_list)):
                if self.y > self.h - 6*row_height:
                    self.add_page()
                self.set_font('Arial', '', 9)
                # self.cell(col_width*2, row_height, f'{recommend_list[i][sub_keys[0]]}',ln=True,align='L')
                self.add_info_to_cell(f'{recommend_list[i][sub_keys[0]]}',X=self.x,Y=self.y,col_width = col_width*2,row_height = row_height,is_ln=True,align='L')
                pg_flag+=1
                # if pg_flag in add_page_list:
                #     self.add_page()
                if self.y > self.h - 4*row_height:
                    left = self.x
                    end = self.y
                    self.line(left,top,left,end)
                    self.line(left+col_width*2,top,left+col_width*2,end)
                    self.add_page()
                    top = self.y
                
            left = self.x
            end = self.y
            self.line(left,top,left,end)
            self.line(left+col_width*2,top,left+col_width*2,end)
            self.line(left,end,left+col_width*2,end)
        
        # if self.y > self.h - 6*row_height:
        #         self.add_page()

        # Other Comments
        self.set_font('Arial', '', 9)
        self.cell(col_width*2, row_height*2, f'Other Comments', border=True,ln=True,align='L')
        # self.set_font('Arial', '', 9)

        # Generated by and Checked by and delivered on
        self.cell(2*col_width/3, row_height, f'Generated by: SurvGPT', border=True,align='L')
        self.cell(2*col_width/3, row_height, f'Checked by:', border=True,align='L')
        self.cell(2*col_width/3, row_height, f'Delivered on:', border=True,align='L',ln=True)


    def covert_gen_to_pdf(self):
        '''
        Overall function to convert the generations in json to pdf 
        '''
        self.set_auto_page_break(auto = True,margin=15)
        self.general_info()
        self.treatment_summary_table()
        self.follow_up_care_plan_table()
        