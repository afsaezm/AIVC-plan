import datetime
import gantt
import math
import pandas as pd
from prettytable import PrettyTable
import numpy as np
import datetime

EE = gantt.Resource('Electronics Engineer')
ME = gantt.Resource('Mechanical Engineer')
ET = gantt.Resource('Electronics Technician')
MT = gantt.Resource('Mechanical Technician')
SE = gantt.Resource('Software Engineer')
SU = gantt.Resource('Supervisor')
BE = gantt.Resource('Back-End Technical Lead')
FE = gantt.Resource('Front-End Technical Lead')
CO = gantt.Resource('Correlator Technical Lead')
PL = gantt.Resource('Planner')

AO  = gantt.Resource('Array Operator')
AOD = gantt.Resource('Astronomer On Duty')
DAS = gantt.Resource('Data Analyst for Science')
CA  = gantt.Resource('Commisioning Astronomer')

AOS_access_time = 0.75
Coordination_operator = 0.5
Safety_procedures = 0.5
AOS_extra_time = AOS_access_time + Coordination_operator + Safety_procedures

FTE_OSF = 1288
FTE_AOS = 512

taskDescription={
#stage 0    
'0.01.AIV.EN':'Provide a timing reference to the Array Elements sited at the OSF pads ',
'0.02.AIV.EN':'Prepare the OSF maintenance labs for conducting the PAS tests',
'0.03.AIV.EN':'Develop a DTX mockup',
'0.13.AIV.EN':'Check and validate the Electrical installation',
'0.14.AIV.EN':'Check and validate the HVAC performance',
'0.15.AIV.EN':'Check and validate the monitoring infrastructure (BMS). ',
'0.16.AIV.EN':'Check and validate the fire system protection',
'0.17.AIV.EN':'Check and validate the patch panel functionality',
'0.18.AIV.EN':'Check and validate the access control system',
'0.19.AIV.EN':'Check the anti-seismic structure',
'0.05.AIV.EN':'Design and prototype the new PSAD',
'0.06.AIV.EN':'Validate the new PSAD',
'0.07.AIV.EN':'Manufacturing the new PSAD',
'0.08.AIV.EN':'Elaborate on the FO connectivity plan for linking the OSF pads to the ATAC',
'0.09.AIV.EN':'Patch Panel and the AOS-OSF fiber infrastructure upgrade ',
'0.10.AIV.EN':'Implement the FO connection between pads located at the OSF and the ATAC',
'0.11.AIV.EN':'Increase the capacity of the Shared-resources from 4 to 8 Array Elements',
'0.12.AIV.EN':'Validate the increased Shared-resources capacity',
'0.04.AIV.EN':'Elaborate a plan to modify the low-frequency timing reference signal distribution',    
#stage 1    
'1.01.AIV.EN':'New Intermediate Frequency (IF) switch PAS ',
'1.02.AIV.EN':'New DTX PAS',
'1.03.AIV.EN':'New PSAD PAS',
#stage 2    
'2.01.AIV.EN':'Antenna mechanical-related tasks',
'2.02.AIV.EN':'Antenna cabin electrical-related tasks ',
'2.03.AIV.EN':'Monitor & Control ICD verification ',
'2.04.AIV.EN':'Signal Path connectivity verification ',
'2.05.AIV.EN':'DTS connection to the ATAC ',
'2.06.AIV.EN':'Front-End (FE) Upgrade',
'2.07.AIV.EN':'Remove the legacy FE from the AE.',
'2.08.AIV.EN':'Install the retrofitted FE into an AE.',
'2.09.AIV.EN':'Update Operations procedures',
'2.10.AIV.EN':'Engineering Verification post FE swap.',
'2.11.AIV.EN':'Verify the Legacy & WSU switching support is functional',
'2.12.AIV.EN':'FO related work at the antenna',    
'2.13.AIV.EN':'AE relocation from the AOS to the OSF',
    
#stage 3        
'3.01.AIV.EN':'Legacy system AE integration',
'3.02.AIV.EN':'WSU AE integration',
'3.03.AIV.EN':'Check the data integrity',

#stage 4            
'4.01.AIV.EN':'Antenna mechanical-related tasks',
'4.02.AIV.EN':'Antenna cabin electrical-related tasks ',
'4.03.AIV.EN':'Monitor & Control ICD verification ',
'4.04.AIV.EN':'Signal Path connectivity verification ',
'4.05.AIV.EN':'DTS connection to the ATAC ',
'4.06.AIV.EN':'Front-End (FE) Upgrade',
'4.07.AIV.EN':'Remove the legacy FE from the AE.',
'4.08.AIV.EN':'Install the retrofitted FE into an AE.',
'4.09.AIV.EN':'Update Operations procedures',
'4.10.AIV.EN':'Engineering Verification post FE swap.',
'4.11.AIV.EN':'Verify the Legacy & WSU switching support is functional',    
'4.12.AIV.EN':'FO related work at the antenna',    
'4.13.AIV.EN':'AE relocation from the OSF to the AOS',
'4.14.AIV.EN':'AE relocation from the AOS to the OSF',    
#stage 5                
'5.01.AIV.EN':'Antenna mechanical-related tasks',
'5.02.AIV.EN':'Antenna cabin electrical-related tasks ',
'5.03.AIV.EN':'Monitor & Control ICD verification ',
'5.04.AIV.EN':'Signal Path connectivity verification ',
'5.05.AIV.EN':'DTS connection to the ATAC ',
'5.06.AIV.EN':'Front-End (FE) Upgrade',
'5.07.AIV.EN':'Remove the legacy FE from the AE.',
'5.08.AIV.EN':'Install the retrofitted FE into an AE.',
'5.09.AIV.EN':'Update Operations procedures',
'5.10.AIV.EN':'Engineering Verification post FE swap.',
'5.11.AIV.EN':'Verify the Legacy & WSU switching support is functional',  
'5.12.AIV.EN':'FO related work at the antenna',    
'5.13.AIV.EN':'AE relocation from the OSF to the AOS',    
'5.14.AIV.EN':'AE relocation from the AOS to the OSF',     
#DSO    
'0.01.AIV.SC':'Fast Switching Script Prep ',
'0.02.AIV.SC':'First Light Script Prep ',
'0.03.AIV.SC':'OTF Script Prep  ',
'0.04.AIV.SC':'Radio Pointing Script Prep ',
'0.5.AIV.SC':'Offset Pointing Script Prep',
'0.05.AIV.SC':'Beam Squint Script Prep ',
'0.07.AIV.SC':'Focus Curve Scrip Prep ',
'0.08.AIV.SC':'Spectral Check Script Prep ',
'0.09.AIV.SC':'Interferometric Checkout Script Prep ',
'0.10.AIV.SC':'Interferometric Focus Script Prep ',
'0.11.AIV.SC':'Interferometric Pointing Script Prep',
'0.14.AIV.SC':'Antenna Position Script Prep',

'2.01.AIV.SC':'Fast Switching  Verification ',
'2.02.AIV.SC':'First Light  Verification ',
'2.03.AIV.SC':'On-the-flight Mapping  Verification ',
'2.04.AIV.SC':'Radio Pointing  Determination ',
'2.05.AIV.SC':'Offset Pointing Verification ',
'2.06.AIV.SC':'Beam Squint  Verification ',
'2.07.AIV.SC':'Focus Curves  Verification',
'2.08.AIV.SC':'Spectral Checkout  Verification ',
'2.09.AIV.SC':'Interferometric Checkout   ',
'2.10.AIV.SC':'Interferometric Pointing  Verification ',
'2.11.AIV.SC':'Interferometric Focus  Verification ',
'2.12.AIV.SC':'Phase Closure  Verification ',
'2.13.AIV.SC':'Amplitude Closure  Verification ',
'2.14.AIV.SC':'Antenna Position  Determination ',
'2.15.AIV.SC':'Go/NOGo  Observing Verification ',
    
'4.01.AIV.SC':'Fast Switching  Verification ',
'4.02.AIV.SC':'First Light Checkout  ',
'4.03.AIV.SC':'On-The-Fly Mapping  Verification ',
'4.04.AIV.SC':'Radio Pointing  Determination ',
'4.08.AIV.SC':'Spectral Checkout  Verification ',
'4.09.AIV.SC':'Interferometric Checkout ',
'4.10.AIV.SC':'Interferometric Pointing  Verification ',
'4.11.AIV.SC':'Interferometric Focus  Verification ',
'4.12.AIV.SC':'Phase Closure  Verification ',
'4.13.AIV.SC':'Amplitude Closure  Verification ',
'4.14.AIV.SC':'Antenna Position  Verification ',
'4.15.AIV.SC':'Go/NoGo Observation  Verification ',
    
'5.01.AIV.SC':'Fast Switching  Verification ',
'5.02.AIV.SC':'First Light Checkout  ',
'5.03.AIV.SC':'On-The-Fly Mapping  Verification ',
'5.04.AIV.SC':'Radio Pointing  Determination ',
'5.08.AIV.SC':'Spectral Checkout  Verification ',
'5.09.AIV.SC':'Interferometric Checkout   ',
'5.10.AIV.SC':'Interferometric Pointing  Verification ',
'5.11.AIV.SC':'Interferometric Focus  Verification ',
'5.14.AIV.SC':'Antenna Position  Determination ',
'5.15.AIV.SC':'Go/NoGo Observation  Verification ',
    
'ATAC.R1_START' : 'ATAC R1 START',
'ATAC.R1_FIN'   : 'ATAC R1 FIN',
'ATAC.R2_START' : 'ATAC R2 START',
'ATAC.R2_FIN'   : 'ATAC R2 FIN'    
}

taskEfforts={
'0.01.AIV.EN':[[[EE,2,30,8,0]],False],
'0.02.AIV.EN':[[[ET,1,10,8,0],[BE,1,5,8,0],[FE,1,5,8,0],[CO,1,5,8,0]],True],
'0.03.AIV.EN':[[[ME,1,3,2,0],[ME,1,4,2,0],[MT,1,3,8,0],[MT,1,4,2,0]],False],
'0.04.AIV.EN':[[[EE,1,30,8,0]],False],
    
'0.05.AIV.EN':[[[EE,1,60,8,0],[ET,1,12,8,0]],False],
'0.06.AIV.EN':[[[ET,2,60,8,0]],False],
'0.07.AIV.EN':[[[EE,1,5,8,0]],False],
    
'0.08.AIV.EN':[[[ET,1,3,8,0]],False],
'0.09.AIV.EN':[[[ET,2,10,8,0]],False],
'0.10.AIV.EN':[[[ET,1,2,8,0]],False],
    
'0.11.AIV.EN':[[[EE,1,6,8,0],[ET,1,6,8,0]],True],
'0.12.AIV.EN':[[[ET,1,2,8,0]],False],
    
'0.13.AIV.EN':[[[EE,1,10,4,0]],False],
'0.14.AIV.EN':[[[ME,1,9,4,0]],False],
'0.15.AIV.EN':[[[EE,1,6,4,0]],False],
'0.16.AIV.EN':[[[ME,1,6,4,0]],False],
'0.17.AIV.EN':[[[EE,0,0,0,0]],False],
'0.18.AIV.EN':[[[EE,1,3,4,0]],False],
'0.19.AIV.EN':[[[ME,1,6,4,0]],False],

'1.01.AIV.EN':[[[ET,2,35,8,0]],False],
'1.02.AIV.EN':[[[ET,2,18,8,0]],False],
'1.03.AIV.EN':[[[ET,2,9,8,0]],False],    
    
'2.01.AIV.EN':[[[ME,2,1,2,0],[MT,2,1,2,0],[SU,1,1,0.5,0],[PL,1,1,0.5,0]],False],
'2.02.AIV.EN':[[[EE,1,1,1,0],[ET,2,1,3,0],[SU,1,1,0.5,0],[PL,1,1,0.5,0]],False],
'2.03.AIV.EN':[[[ET,1,1,2,0],[SU,1,1,0.5,0],[PL,1,1,0.5,0]],False],
'2.04.AIV.EN':[[[EE,1,1,1,0],[BE,1,1,1,0],[SU,1,1,0.5,0],[PL,1,1,0.5,0]],False],
'2.05.AIV.EN':[[[ET,1,4,8,0],[SU,1,1,0.5,0],[PL,1,1,0.5,0]],False],
'2.06.AIV.EN':[[[ET,1,9,8,0],[MT,1,2,2,0],[SU,1,1,0.5,0],[PL,1,1,0.5,0]],False],
'2.07.AIV.EN':[[[ET,2,1,2,0],[MT,5,1,2,0],[SU,1,1,0.5,0],[PL,1,1,0.5,0]],False],
'2.08.AIV.EN':[[[ET,2,1,2,0],[MT,5,1,2,0],[SU,1,1,0.5,0],[PL,1,1,0.5,0]],False],
'2.09.AIV.EN':[[[EE,1,2,8,0],[SU,1,1,0.5,0],[PL,1,1,0.5,0]],False],
'2.10.AIV.EN':[[[EE,1,3,8,0],[SU,1,1,0.5,0],[PL,1,1,0.5,0]],False],
'2.11.AIV.EN':[[[EE,1,1,2,0],[SU,1,1,0.5,0],[PL,1,1,0.5,0]],False],
'2.12.AIV.EN':[[[ET,2,2,5.5,0],[ET,2,1,8,0],[SU,1,1,0.5,0],[PL,1,1,0.5,0]],True],    
'2.13.AIV.EN':[[[ET,1,1,1,0],[ET,1,1,0.5,0],[MT,2,1,0,0.5],[MT,2,1,2,0],[MT,2,1,7,0],[PL,1,1,0.5,0],[SU,1,1,0.5,0]],False],    
    
'3.01.AIV.EN':[[[EE,1,1,1,0],[SE,1,1,1,0],[SU,1,1,0.5,0],[PL,1,1,0.5,0]],False],
'3.02.AIV.EN':[[[EE,1,1,2,0],[SE,1,1,2,0],[SU,1,1,0.5,0],[PL,1,1,0.5,0]],False],
'3.03.AIV.EN':[[[EE,1,1,2,0],[SU,1,1,0.5,0],[PL,1,1,0.5,0]],False],

    
'4.01.AIV.EN':[[[ME,2,1,0,2],[MT,2,1,0,2],[SU,1,1,0.5,0],[PL,1,1,0.5,0]],False],
'4.02.AIV.EN':[[[EE,1,1,0,1],[ET,2,1,0,3],[SU,1,1,0.5,0],[PL,1,1,0.5,0]],False],
'4.03.AIV.EN':[[[ET,1,1,2,0],[SU,1,1,0.5,0],[PL,1,1,0.5,0]],False],
'4.04.AIV.EN':[[[EE,1,1,1,0],[BE,1,1,1,0],[SU,1,1,0.5,0],[PL,1,1,0.5,0]],False],
'4.05.AIV.EN':[[[ET,1,4,8,0],[SU,1,1,0.5,0],[PL,1,1,0.5,0]],False],
'4.06.AIV.EN':[[[ET,1,9,8,0],[MT,1,2,2,0],[SU,1,1,0.5,0],[PL,1,1,0.5,0]],False],
'4.07.AIV.EN':[[[ET,2,1,0,2],[MT,5,1,0,2],[SU,1,1,0.5,0],[PL,1,1,0.5,0]],False],
'4.08.AIV.EN':[[[ET,2,1,0,2],[MT,5,1,0,2],[SU,1,1,0.5,0],[PL,1,1,0.5,0]],False],
'4.09.AIV.EN':[[[EE,1,2,8,0],[SU,1,1,0.5,0],[PL,1,1,0.5,0]],False],
'4.10.AIV.EN':[[[EE,1,3,8,0],[SU,1,1,0.5,0],[PL,1,1,0.5,0]],False],
'4.11.AIV.EN':[[[EE,1,1,2,0],[SU,1,1,0.5,0],[PL,1,1,0.5,0]],False],
'4.12.AIV.EN':[[[ET,2,2,0,5.5],[ET,2,1,8,0],[SU,1,1,0.5,0],[PL,1,1,0.5,0]],True],    
'4.13.AIV.EN':[[[ET,1,1,1,0],[ET,1,1,3,0],[ET,1,1,0,0.5],[MT,2,1,0,2],[MT,2,1,0,1],[MT,3,1,0,2],[MT,2,1,0,0.5],[MT,4,1,0,7],[SU,1,1,0.5,0],[PL,1,1,0.5,0]],False],        
    
'5.01.AIV.EN':[[[ME,2,1,0,2],[MT,2,1,0,2],[SU,1,1,0.5,0],[PL,1,1,0.5,0]],False],
'5.02.AIV.EN':[[[EE,1,1,0,1],[ET,2,1,0,3],[SU,1,1,0.5,0],[PL,1,1,0.5,0]],False],
'5.03.AIV.EN':[[[ET,1,1,2,0],[SU,1,1,0.5,0],[PL,1,1,0.5,0]],False],
'5.04.AIV.EN':[[[EE,1,1,1,0],[BE,1,1,1,0],[SU,1,1,0.5,0],[PL,1,1,0.5,0]],False],
'5.05.AIV.EN':[[[ET,1,4,8,0],[SU,1,1,0.5,0],[PL,1,1,0.5,0]],False],
'5.06.AIV.EN':[[[ET,1,9,8,0],[MT,1,2,2,0],[SU,1,1,0.5,0],[PL,1,1,0.5,0]],False],
'5.07.AIV.EN':[[[ET,2,1,0,2],[MT,5,1,0,2],[SU,1,1,0.5,0],[PL,1,1,0.5,0]],False],
'5.08.AIV.EN':[[[ET,2,1,0,2],[MT,5,1,0,2],[SU,1,1,0.5,0],[PL,1,1,0.5,0]],False],
'5.09.AIV.EN':[[[EE,1,2,8,0],[SU,1,1,0.5,0],[PL,1,1,0.5,0]],False],
'5.10.AIV.EN':[[[EE,1,3,8,0],[SU,1,1,0.5,0],[PL,1,1,0.5,0]],False],
'5.11.AIV.EN':[[[EE,1,1,2,0],[SU,1,1,0.5,0],[PL,1,1,0.5,0]],False],
'5.12.AIV.EN':[[[ET,2,2,0,5.5],[ET,2,1,8,0],[SU,1,1,0.5,0],[PL,1,1,0.5,0]],True],
    
'ATAC.R1_START' : [[[EE,1,90,8,0],[ET,1,90,4,0]],False],
'ATAC.R1_FIN'   : [[[EE,1,90,8,0],[ET,1,90,4,0]],False],
'ATAC.R2_START' : [[[EE,1,90,8,0],[ET,1,90,4,0]],False],
'ATAC.R2_FIN'   : [[[EE,1,90,8,0],[ET,1,90,4,0]],False],
    
'0.01.AIV.SC':[[[DAS,2,6,2,0]],False],
'0.02.AIV.SC':[[[DAS,2,10,2,0]],False],
'0.03.AIV.SC':[[[DAS,2,6,2,0]],False],
'0.04.AIV.SC':[[[DAS,2,6,2,0]],False],
'0.5.AIV.SC':[[[DAS,2,6,2,0]],False],
'0.05.AIV.SC':[[[DAS,2,6,2,0]],False],
'0.07.AIV.SC':[[[DAS,2,6,2,0]],False],
'0.08.AIV.SC':[[[DAS,3,10,3,0]],False],
'0.09.AIV.SC':[[[DAS,2,6,2,0]],False],
'0.10.AIV.SC':[[[DAS,2,6,2,0]],False],
'0.11.AIV.SC':[[[DAS,2,6,2,0]],False],
'0.14.AIV.SC':[[[DAS,2,6,2,0]],False],
'2.01.AIV.SC':[[[AO,1,2.25,7,0],[DAS,1,2.25,2,0]],False],
'2.02.AIV.SC':[[[AO,3,1,2,0],[DAS,3,1,2,0]],False],
'2.03.AIV.SC':[[[AO,1,2.25,4,0],[DAS,1,2.25,2,0]],False],
'2.04.AIV.SC':[[[AO,3,1,6,0],[DAS,3,1,2,0]],False],
'2.05.AIV.SC':[[[AO,3,1,2,0],[DAS,3,1,2,0]],False],
'2.06.AIV.SC':[[[AO,3,1,4,0],[DAS,3,1,4,0]],False],
'2.07.AIV.SC':[[[AO,3,1,4,0],[DAS,3,1,2,0]],False],
'2.08.AIV.SC':[[[AO,3,5,4,0],[DAS,2,10,4,0],[DAS,1,10,5,0]],False],
'2.09.AIV.SC':[[[AO,2,1,0.75,0],[AO,1,1,1.5,0],[DAS,2,1,0.4,0],[DAS,1,1,1.5,0]],False],
'2.10.AIV.SC':[[[AO,2,1,0.75,0],[AO,1,1,1.5,0],[DAS,2,1,0.4,0],[DAS,1,1,1.5,0]],False],
'2.11.AIV.SC':[[[AO,2,1,0.75,0],[AO,1,1,1.5,0],[DAS,2,1,0.4,0],[DAS,1,1,1.5,0]],False],
'2.12.AIV.SC':[[[AO,1,1,1,0],[AO,1,1,1,0],[DAS,1,1,0.5,0],[DAS,1,1,1,0]],False],
'2.13.AIV.SC':[[[AO,1,1,0.5,0],[AO,1,1,0.5,0],[DAS,1,1,0.25,0],[DAS,1,1,0.5,0]],False],
'2.14.AIV.SC':[[[AO,1,1,1,0],[AO,1,1,1,0],[DAS,1,1,0.5,0],[DAS,1,1,2,0]],False],
'2.15.AIV.SC':[[[AO,1,1,1,0],[DAS,1,1,1,0]],False],
'4.01.AIV.SC':[[[AO,1,1,4,0],[DAS,1,1,2,0]],False],
'4.02.AIV.SC':[[[AO,2,1,2,0],[DAS,2,1,2,0]],False],
'4.03.AIV.SC':[[[AO,1,1,4,0],[DAS,1,1,2,0]],False],
'4.04.AIV.SC':[[[AO,2,1,6,0],[DAS,2,1,2,0]],False],
'4.08.AIV.SC':[[[AO,3,5,2,0],[DAS,2,10,2,0],[DAS,1,10,5,0]],False],
'4.09.AIV.SC':[[[AO,1,1,1,0],[AO,1,1,2,0],[DAS,1,1,0.5,0],[DAS,1,1,2,0]],False],
'4.10.AIV.SC':[[[AO,1,1,1,0],[AO,1,1,2,0],[DAS,1,1,0.5,0],[DAS,1,1,2,0]],False],
'4.11.AIV.SC':[[[AO,1,1,1,0],[AO,1,1,2,0],[DAS,1,1,0.5,0],[DAS,1,1,2,0]],False],
'4.12.AIV.SC':[[[AO,1,1,0.25,0],[AO,1,1,0.5,0],[DAS,1,1,0.1,0],[DAS,1,1,0.5,0]],False],
'4.13.AIV.SC':[[[AO,1,1,0.25,0],[AO,1,1,0.5,0],[DAS,1,1,0.1,0],[DAS,1,1,0.5,0]],False],
'4.14.AIV.SC':[[[AO,1,2,1,0],[AO,1,1,2,0],[DAS,1,2,0.5,0],[DAS,1,1,4,0]],False],
'4.15.AIV.SC':[[[AO,1,1,1,0],[DAS,1,1,1,0]],False],
'5.01.AIV.SC':[[[AO,0,0,0,0],[DAS,0,0,0,0]],False],
'5.02.AIV.SC':[[[AO,2,1,2,0],[DAS,2,1,2,0]],False],
'5.03.AIV.SC':[[[AO,0,0,0,0],[DAS,0,0,0,0]],False],
'5.04.AIV.SC':[[[AO,0,0,0,0],[DAS,0,0,0,0]],False],
'5.08.AIV.SC':[[[AO,3,5,2,0],[DAS,2,10,2,0],[DAS,1,5,5,0]],False],
'5.09.AIV.SC':[[[AO,1,1,1,0],[AO,1,1,2,0],[DAS,1,1,0.5,0],[DAS,1,1,2,0]],False],
'5.10.AIV.SC':[[[AO,1,1,1,0],[AO,1,1,2,0],[DAS,1,1,0.5,0],[DAS,1,1,2,0]],False],
'5.11.AIV.SC':[[[AO,1,1,1,0],[AO,1,1,2,0],[DAS,1,1,0.5,0],[DAS,1,1,2,0]],False],
'5.14.AIV.SC':[[[AO,1,1,1,0],[AO,1,1,2,0],[DAS,1,1,0.5,0],[DAS,1,1,4,0]],False],
'5.15.AIV.SC':[[[AO,1,1,1,0],[DAS,1,1,1,0]],False]    
}

LearningFactor={
'0.01.AIV.EN':1,
'0.02.AIV.EN':1,
'0.03.AIV.EN':1,
'0.04.AIV.EN':1,
'0.05.AIV.EN':1,
'0.06.AIV.EN':1,
'0.07.AIV.EN':1,
'0.08.AIV.EN':1,
'0.09.AIV.EN':1,
'0.10.AIV.EN':1,
'0.11.AIV.EN':1,
'0.12.AIV.EN':1,
'0.13.AIV.EN':1,
'0.14.AIV.EN':1,
'0.15.AIV.EN':1,
'0.16.AIV.EN':1,
'0.17.AIV.EN':1,
'0.18.AIV.EN':1,
'0.19.AIV.EN':1,
    
'1.01.AIV.EN':1,
'1.02.AIV.EN':1,
'1.03.AIV.EN':1,
        
'2.01.AIV.EN':6,
'2.02.AIV.EN':6,
'2.03.AIV.EN':6,
'2.04.AIV.EN':6,
'2.05.AIV.EN':6,
'2.06.AIV.EN':4,
'2.07.AIV.EN':1,
'2.08.AIV.EN':1,
'2.09.AIV.EN':1,
'2.10.AIV.EN':6,
'2.11.AIV.EN':6,
'2.12.AIV.EN':2,  
'2.13.AIV.EN':1,    

'3.01.AIV.EN':1,
'3.02.AIV.EN':1,
'3.03.AIV.EN':1,
'3.04.AIV.EN':1,    
    
'4.01.AIV.EN':3,
'4.02.AIV.EN':3,
'4.03.AIV.EN':3,
'4.04.AIV.EN':3,
'4.05.AIV.EN':3,
'4.06.AIV.EN':2,
'4.07.AIV.EN':1,
'4.08.AIV.EN':1,
'4.09.AIV.EN':1,
'4.10.AIV.EN':3,
'4.11.AIV.EN':3,
'4.12.AIV.EN':1.5,  
'4.13.AIV.EN':1,
'4.14.AIV.EN':1,    
    
'5.01.AIV.EN':1,
'5.02.AIV.EN':1,
'5.03.AIV.EN':1,
'5.04.AIV.EN':1,
'5.05.AIV.EN':1,
'5.06.AIV.EN':1,
'5.07.AIV.EN':1,
'5.08.AIV.EN':1,
'5.09.AIV.EN':1,
'5.10.AIV.EN':1,
'5.11.AIV.EN':1,
'5.12.AIV.EN':1,
'5.13.AIV.EN':1,
'5.14.AIV.EN':1,    

    
'ATAC.R1_START' : 1,
'ATAC.R1_FIN'   : 1,
'ATAC.R2_START' : 1,
'ATAC.R2_FIN'   : 1,

'0.01.AIV.SC':2,
'0.02.AIV.SC':2,
'0.03.AIV.SC':2,
'0.04.AIV.SC':2,
'0.5.AIV.SC':2,
'0.05.AIV.SC':2,
'0.07.AIV.SC':2,
'0.08.AIV.SC':2,
'0.09.AIV.SC':2,
'0.10.AIV.SC':2,
'0.11.AIV.SC':2,
'0.14.AIV.SC':2,
'2.01.AIV.SC':1.4,
'2.02.AIV.SC':5,
'2.03.AIV.SC':1.4,
'2.04.AIV.SC':2,
'2.05.AIV.SC':1.5,
'2.06.AIV.SC':1.5,
'2.07.AIV.SC':1.5,
'2.08.AIV.SC':5,
'2.09.AIV.SC':5,
'2.10.AIV.SC':5,
'2.11.AIV.SC':5,
'2.12.AIV.SC':1.7,
'2.13.AIV.SC':1.8,
'2.14.AIV.SC':5,
'2.15.AIV.SC':5,
'4.01.AIV.SC':1,
'4.02.AIV.SC':3,
'4.03.AIV.SC':1,
'4.04.AIV.SC':1.2,
'4.08.AIV.SC':2,
'4.09.AIV.SC':5,
'4.10.AIV.SC':5,
'4.11.AIV.SC':5,
'4.12.AIV.SC':1,
'4.13.AIV.SC':1,
'4.14.AIV.SC':3,
'4.15.AIV.SC':5,
'5.01.AIV.SC':1,
'5.02.AIV.SC':1.5,
'5.03.AIV.SC':1,
'5.04.AIV.SC':1,
'5.08.AIV.SC':1.3,
'5.09.AIV.SC':1.5,
'5.10.AIV.SC':1.5,
'5.11.AIV.SC':1.5,
'5.14.AIV.SC':1.5,
'5.15.AIV.SC':1.2    
    
}

ContingencyFactor={
'0.01.AIV.EN':1,
'0.02.AIV.EN':1,
'0.03.AIV.EN':1,
'0.04.AIV.EN':1,
'0.05.AIV.EN':1,
'0.06.AIV.EN':1,
'0.07.AIV.EN':1,
'0.08.AIV.EN':1,
'0.09.AIV.EN':1,
'0.10.AIV.EN':1,
'0.11.AIV.EN':1,
'0.12.AIV.EN':1,
'0.13.AIV.EN':1,
'0.14.AIV.EN':1,
'0.15.AIV.EN':1,
'0.16.AIV.EN':1,
'0.17.AIV.EN':1,
'0.18.AIV.EN':1,
'0.19.AIV.EN':1,
    
'1.01.AIV.EN':1,
'1.02.AIV.EN':1,
'1.03.AIV.EN':1,    
    
'2.01.AIV.EN':1,
'2.02.AIV.EN':1,
'2.03.AIV.EN':1.4,
'2.04.AIV.EN':1.4,
'2.05.AIV.EN':1.4,
'2.06.AIV.EN':1,
'2.07.AIV.EN':1,
'2.08.AIV.EN':1.4,
'2.09.AIV.EN':1,
'2.10.AIV.EN':1.4,
'2.11.AIV.EN':1.4,
'2.12.AIV.EN':1,  
'2.13.AIV.EN':1,    
    
'3.01.AIV.EN':1,
'3.02.AIV.EN':1,
'3.03.AIV.EN':1,
'3.04.AIV.EN':1,        
    
'4.01.AIV.EN':1,
'4.02.AIV.EN':1,
'4.03.AIV.EN':1.2,
'4.04.AIV.EN':1.2,
'4.05.AIV.EN':1.2,
'4.06.AIV.EN':1,
'4.07.AIV.EN':1,
'4.08.AIV.EN':1.2,
'4.09.AIV.EN':1,
'4.10.AIV.EN':1.2,
'4.11.AIV.EN':1.2,
'4.12.AIV.EN':1,    
'4.13.AIV.EN':1,
'4.14.AIV.EN':1,    
    
'5.01.AIV.EN':1,
'5.02.AIV.EN':1,
'5.03.AIV.EN':1.05,
'5.04.AIV.EN':1.05,
'5.05.AIV.EN':1.05,
'5.06.AIV.EN':1,
'5.07.AIV.EN':1,
'5.08.AIV.EN':1.05,
'5.09.AIV.EN':1,
'5.10.AIV.EN':1.05,
'5.11.AIV.EN':1.05,
'5.12.AIV.EN':1,    
'5.13.AIV.EN':1,
'5.14.AIV.EN':1,    
    
    
'ATAC.R1_START' : 1,
'ATAC.R1_FIN'   : 1,
'ATAC.R2_START' : 1,
'ATAC.R2_FIN'   : 1,
    
'0.01.AIV.SC':1,
'0.02.AIV.SC':1,
'0.03.AIV.SC':1,
'0.04.AIV.SC':1,
'0.5.AIV.SC':1,
'0.05.AIV.SC':1,
'0.07.AIV.SC':1,
'0.08.AIV.SC':1,
'0.09.AIV.SC':1,
'0.10.AIV.SC':1,
'0.11.AIV.SC':1,
'0.14.AIV.SC':1,
'2.01.AIV.SC':1,
'2.02.AIV.SC':1,
'2.03.AIV.SC':1,
'2.04.AIV.SC':1,
'2.05.AIV.SC':1,
'2.06.AIV.SC':1,
'2.07.AIV.SC':1,
'2.08.AIV.SC':1,
'2.09.AIV.SC':1,
'2.10.AIV.SC':1,
'2.11.AIV.SC':1,
'2.12.AIV.SC':1,
'2.13.AIV.SC':1,
'2.14.AIV.SC':1,
'2.15.AIV.SC':1,
'4.01.AIV.SC':1,
'4.02.AIV.SC':1,
'4.03.AIV.SC':1,
'4.04.AIV.SC':1,
'4.08.AIV.SC':1,
'4.09.AIV.SC':1,
'4.10.AIV.SC':1,
'4.11.AIV.SC':1,
'4.12.AIV.SC':1,
'4.13.AIV.SC':1,
'4.14.AIV.SC':1,
'4.15.AIV.SC':1,
'5.01.AIV.SC':1,
'5.02.AIV.SC':1,
'5.03.AIV.SC':1,
'5.04.AIV.SC':1,
'5.08.AIV.SC':1,
'5.09.AIV.SC':1,
'5.10.AIV.SC':1,
'5.11.AIV.SC':1,
'5.14.AIV.SC':1,
'5.15.AIV.SC':1    
    
}

taskDependencies={
    
'0.01.AIV.EN':['na'],
'0.02.AIV.EN':['na'],
'0.03.AIV.EN':['na'],
'0.04.AIV.EN':['na'],
    
'0.05.AIV.EN':['na'],
'0.06.AIV.EN':['0.05.AIV.EN'],
'0.07.AIV.EN':['0.06.AIV.EN'],
    
'0.08.AIV.EN':['na'],
'0.09.AIV.EN':['0.08.AIV.EN'],
'0.10.AIV.EN':['0.09.AIV.EN'],
    
'0.11.AIV.EN':['na'],
'0.12.AIV.EN':['0.11.AIV.EN'],
    
'0.13.AIV.EN':['na'],
'0.14.AIV.EN':['0.13.AIV.EN'],
'0.15.AIV.EN':['0.14.AIV.EN'],
'0.16.AIV.EN':['0.15.AIV.EN'],
'0.17.AIV.EN':['0.16.AIV.EN'],
'0.18.AIV.EN':['0.17.AIV.EN'],
'0.19.AIV.EN':['0.15.AIV.EN'],    

'1.01.AIV.EN':['na'],        
'1.02.AIV.EN':['na'],
'1.03.AIV.EN':['na'],        
    
'2.01.AIV.EN':['2.08.AIV.EN'],
'2.02.AIV.EN':['2.01.AIV.EN'],
'2.03.AIV.EN':['na'],
'2.04.AIV.EN':['2.12.AIV.EN'],
'2.05.AIV.EN':['na'],
'2.06.AIV.EN':['na'],
'2.07.AIV.EN':['2.13.AIV.EN'],
'2.08.AIV.EN':['2.07.AIV.EN'],
'2.09.AIV.EN':['na'],
'2.10.AIV.EN':['2.04.AIV.EN'],
'2.11.AIV.EN':['2.10.AIV.EN'],
'2.12.AIV.EN':['2.02.AIV.EN'],   
'2.13.AIV.EN':['na'],    

'3.01.AIV.EN':['na'],
'3.02.AIV.EN':['3.01.AIV.EN'],
'3.03.AIV.EN':['3.02.AIV.EN'],
'3.04.AIV.EN':['na'],        
    
'4.01.AIV.EN':['4.08.AIV.EN'],
'4.02.AIV.EN':['4.01.AIV.EN'],
'4.03.AIV.EN':['na'],
'4.04.AIV.EN':['4.12.AIV.EN'],
'4.05.AIV.EN':['na'],
'4.06.AIV.EN':['na'],
'4.07.AIV.EN':['na'],
'4.08.AIV.EN':['4.07.AIV.EN'],
'4.09.AIV.EN':['na'],
'4.10.AIV.EN':['4.04.AIV.EN'],
'4.11.AIV.EN':['4.10.AIV.EN'],
'4.12.AIV.EN':['4.02.AIV.EN'],    
'4.13.AIV.EN':['na'],        
'5.01.AIV.EN':['5.08.AIV.EN'],
'5.02.AIV.EN':['5.01.AIV.EN'],
'5.03.AIV.EN':['na'],
'5.04.AIV.EN':['5.12.AIV.EN'],
'5.05.AIV.EN':['na'],
'5.06.AIV.EN':['na'],
'5.07.AIV.EN':['na'],
'5.08.AIV.EN':['5.07.AIV.EN'],
'5.09.AIV.EN':['na'],
'5.10.AIV.EN':['5.04.AIV.EN'],
'5.11.AIV.EN':['5.10.AIV.EN'],
'5.12.AIV.EN':['5.02.AIV.EN'],
    
'ATAC.R1_START' : ['na'],
'ATAC.R1_FIN'   : ['na'],
'ATAC.R2_START' : ['na'],
'ATAC.R2_FIN'   : ['na'],
    
'0.01.AIV.SC':['na'],
'0.02.AIV.SC':['na'],
'0.03.AIV.SC':['na'],
'0.04.AIV.SC':['na'],
'0.5.AIV.SC':['na'],
'0.05.AIV.SC':['na'],
'0.07.AIV.SC':['na'],
'0.08.AIV.SC':['na'],
'0.09.AIV.SC':['na'],
'0.10.AIV.SC':['na'],
'0.11.AIV.SC':['na'],
'0.14.AIV.SC':['na'],
    
'2.01.AIV.SC':['2.11.AIV.EN'],
'2.02.AIV.SC':['2.11.AIV.EN'],
'2.03.AIV.SC':['2.11.AIV.EN'],
'2.04.AIV.SC':['2.02.AIV.SC'],
'2.05.AIV.SC':['2.04.AIV.SC'],
'2.06.AIV.SC':['2.04.AIV.SC'],
'2.07.AIV.SC':['2.04.AIV.SC'],
'2.08.AIV.SC':['2.04.AIV.SC'],
'2.09.AIV.SC':['2.04.AIV.SC'],
'2.10.AIV.SC':['2.09.AIV.SC'],
'2.11.AIV.SC':['2.09.AIV.SC'],
'2.12.AIV.SC':['2.09.AIV.SC'],
'2.13.AIV.SC':['2.09.AIV.SC'],
'2.14.AIV.SC':['2.09.AIV.SC'],
'2.15.AIV.SC':['2.09.AIV.SC'],
'4.01.AIV.SC':['4.11.AIV.EN'],
'4.02.AIV.SC':['4.11.AIV.EN'],
'4.03.AIV.SC':['4.11.AIV.EN'],
'4.04.AIV.SC':['4.02.AIV.SC'],
'4.08.AIV.SC':['4.04.AIV.SC'],
'4.09.AIV.SC':['4.04.AIV.SC'],
'4.10.AIV.SC':['4.09.AIV.SC'],
'4.11.AIV.SC':['4.09.AIV.SC'],
'4.12.AIV.SC':['4.09.AIV.SC'],
'4.13.AIV.SC':['4.09.AIV.SC'],
'4.14.AIV.SC':['4.09.AIV.SC'],
'4.15.AIV.SC':['4.09.AIV.SC'],
'5.01.AIV.SC':['5.11.AIV.EN'],
'5.02.AIV.SC':['5.11.AIV.EN'],
'5.03.AIV.SC':['5.11.AIV.EN'],
'5.04.AIV.SC':['5.02.AIV.SC'],
'5.08.AIV.SC':['5.04.AIV.SC'],
'5.09.AIV.SC':['5.04.AIV.SC'],
'5.10.AIV.SC':['5.09.AIV.SC'],
'5.11.AIV.SC':['5.09.AIV.SC'],
'5.14.AIV.SC':['5.09.AIV.SC'],
'5.15.AIV.SC':['5.09.AIV.SC']    
}


def returnTaskDuration(taskName):
    taskDescription=taskEfforts.get(taskName)
    duration=0
    if taskDescription[1]:
        for i in taskDescription[0]:
            if  i[0] != SU and i[0] !=PL:
                duration += i[2]
    else:
        for i in taskDescription[0]:
            if i[2] > duration:
                duration = i[2]
    duration=math.ceil(duration*ContingencyFactor.get(taskName)*LearningFactor.get(taskName))            
    return duration
    
def returnTaskResources(taskName,unique=False):
    taskDescription=taskEfforts.get(taskName)
    resources=[]
    for i in taskDescription[0]:
        for j in range(i[1]):
            resources.append(i[0])
    if unique:
        resources=set(resources)
    return resources         
    
def createAntennaRetrofitTask(listOfTasks,startDate,name):
    t=[]    
    for i in listOfTasks:
        s=i.split('.')
        color="#000000"
        if s[-1]=='EN':
            color="#DFFF00"
            if s[1]=='06':
                color="#CCCCFF"
        if s[-1]=='SC':
            color="#40E0D0"            
        if taskDependencies.get(i)[0]=='na':
            a=gantt.Task(name=i,duration=returnTaskDuration(i),resources=returnTaskResources(i),start=startDate,color=color)
        else:        
            a=gantt.Task(name=i,duration=returnTaskDuration(i),resources=returnTaskResources(i),color=color)    
        t.append(a)   
        
    j=0    
    for i in listOfTasks:    
        if taskDependencies.get(i)[0] != 'na':
            index=listOfTasks.index(taskDependencies.get(i)[0])
            t[j].add_depends([t[index]]) 
        j=j+1     
        
    tt=[]
    for i in t:
        tt.append(i.start_date())   
    ttt=sorted(list(enumerate(tt)), key=lambda tup: tup[1])
    taskSequence=[]
    for i in ttt:
        taskSequence.append(i[0])     
        
    antennaRetrofit = gantt.Project(name=name)
    
    for i in taskSequence:
        antennaRetrofit.add_task(t[i])        
    return antennaRetrofit   
    
def createStage(setOfTasks,caption,duration):

    print('\\begin{table}[H]')
    print('\\begin{minipage}{\\textwidth}')
    print('\centering')
    print('\scalebox{0.8}{')
    print('\\begin{tabular}{|c|c|c|}') 
    print('\hline')
    print('\\rowcolor{gray!50}')
    print('\\textbf{Task ID} & \\textbf{Duration [Days]} & \\textbf{Repetitions} \\\\ ')
    print('\hline')
    print('\hline')

    totalDuration=0
    for j in setOfTasks:                
        for i in j[0]:
            print(i,end=' & ')
            print(returnTaskDuration(i),end=' & ')
            print(j[1],end='\\\\') 
            print()
            print('\hline')
            totalDuration=totalDuration+returnTaskDuration(i)*j[1]        
    print('\hline')    
    print('Working days',end=' & ')
    print('\multicolumn{2}{|c|}{%d Days}'%totalDuration,end='\\\\')
    print()
    print('\hline')    
    print('\hline')    
    print(str(caption),end=' & ')
    print('\multicolumn{2}{|c|}{%d Days}'%duration,end='\\\\')
    
    print()
        
    print('\hline')
    print('\end{tabular}}')
    print('\end{minipage}')
    print('\caption{Summary of the %s activities and the duration of each one.}'%(caption))
    print('\end{table}')   
    return(totalDuration)
    
def createStageSumaryTex(setOfTasks,caption,duration):
    fileName=caption+str('.tex')
    f = open(fileName, "w")    
    f.write('\\begin{table}[H]\n')
    f.write('\\begin{minipage}{\\textwidth}\n')
    f.write('\centering\n')
    f.write('\scalebox{0.8}{\n')
    f.write('\\begin{tabular}{|c|c|c|}\n') 
    f.write('\hline\n')
    f.write('\\rowcolor{gray!50}\n')
    f.write('\\textbf{Task ID} & \\textbf{Duration [Days]} & \\textbf{Repetitions} \\\\ \n')
    f.write('\hline\n')
    f.write('\hline\n')
    totalDuration=0
    for j in setOfTasks:                
        for i in j[0]:
            f.write(str(i) + ' & ')
            f.write(str(returnTaskDuration(i))+' & '+str(j[1])+'\\\\ \n')            
            f.write('\hline \n')
            totalDuration=totalDuration+returnTaskDuration(i)*j[1]        
            
    f.write('\hline \n')    
    f.write('Working days & ')    
    f.write('\multicolumn{2}{|c|}{%d Days}'%totalDuration + '\\\\\n')    
    f.write('\hline\n')    
    f.write('\hline\n')    
    f.write(str(caption) + ' & ')    
    f.write('\multicolumn{2}{|c|}{%d Days}'%duration + '\\\\\n')            
    f.write('\hline\n')
    f.write('\end{tabular}}\n')
    f.write('\end{minipage}\n')
    f.write('\caption{Summary of the %s activities and the duration of each one.}\n'%(caption))
    f.write('\end{table}\n')     
    f.close()  
    return(totalDuration)    
                                   
def printTasks(project,level=0):
    for i in range(level):
        print(end='#')
    print(end=' ')    
    try:
        t=project.tasks        
        print(project.name)
        #print('(%d)'%len(t))
        for j in t:
            printTasks(project=j,level=level+1)
    except:
        taskId=project.name
        team=taskId.split('.')[-1]        
        if team=='EN':
            print('{color:red}',end=' ')
        elif  team=='SC':              
            print('{color:green}',end=' ')
        else:
            print('{color:black}',end=' ')
            
        print(project.name,end=' ')    
        print('{color}',end='\t\t')
        
        print('[#',end='')
        print(taskDescription.get(project.name),end='')
        print(']')
        
def listTasks(project,a):  
    if hasattr(project,'tasks'):
        t=project.tasks        
        for j in t:
            listTasks(project=j,a=a)
    else:                         
        a.append(project.name)

def listTasksUnique(project):
    a=[]
    listTasks(project,a)
    b=set(a)
    return b
        
        
        
def daterange(start_date,end_date):
    days = int((end_date - start_date).days)
    for n in range(days):
        yield start_date + datetime.timedelta(n)
        
def getResourcesPerDay(currentDay,resource,df):
    role=resource.name
    currentDay=pd.to_datetime(currentDay)
    a=df[(df['Start'] <= currentDay) & (df['End'] >= currentDay) & (df['Resource']==role)]
    t=a['Persons'].sum()
    return a,t
    
def resourceDemand(resource,start_date,end_date,df):
    t=[]
    r=[]
    for single_date in daterange(start_date, end_date):
        t.append(single_date)
        r.append(getResourcesPerDay(single_date,resource,df)[1])
    return t,r                      
                  
def createDataFrame(listOfResources):    
    df = pd.DataFrame(columns=['Task','Resource','Persons' ,'OSF', 'AOS','Start','End','Days','H/d','Stage','Team','Workers'])
    hh=[]
    index=0
    # go through the list of resources to be analyzed
    for j in listOfResources:
        # go through the list of tasks to be done by the analyzed resource
        for i in list(j.tasks):
            # Analyze the current task
            k=taskEfforts.get(i.name)[0]
            for c in k:
                h_d_osf = 0
                h_d_aos = 0
                h_d     = 0            
                if c[0]==j:
                    cf = ContingencyFactor.get(i.name)
                    lf = LearningFactor.get(i.name)                
                    if j == PL or j == SU:
                        cf=1
                        lf=1
                    persons= c[1]
                    h_d_osf= c[3]*cf*lf
                    days   = c[2]
                    if c[4] > 0:
                        h_d_aos = c[4]*cf*lf + AOS_extra_time

                    hh_osf = persons*h_d_osf
                    hh_aos = persons*h_d_aos

                    hh_osf = hh_osf*days
                    hh_aos = hh_aos*days                    
                    #h_d    = h_d_osf + h_d_aos
                    
                    start_date     = i.start_date()
                    end_date       = i.end_date()
                    time_duration  = i.end_date() - i.start_date() + datetime.timedelta(days=1)               
                    duration_days  = time_duration.days
                    #h_d            = (hh_osf+hh_aos)/duration_days/persons
                    h_d            = (hh_osf+hh_aos)/duration_days
                    #persons        = c[1]
                    persons        = h_d / 8

                    hh.append([i.name,j.name,persons,hh_osf,hh_aos,start_date,end_date])
                    df.loc[index]=[i.name,j.name,persons,hh_osf,hh_aos,pd.to_datetime(start_date),pd.to_datetime(end_date),duration_days,h_d,i.name.split('.')[0],i.name.split('.')[-1],c[1]]

                    index=index+1    

    return df                

def createDataFramePerDay(start,end,df):
    currentDay=start
    newDataFrame=pd.DataFrame(columns=['date','Resource','H/d'])
    index=0
    while currentDay <= end:
        currentDayPd=pd.to_datetime(currentDay)
        selection=df[(df['Start'] <= currentDayPd) & (df['End'] >= currentDayPd)]
        temp=selection[['Task','Resource','H/d']]
        listOfResources=temp['Resource'].unique()
        for i in listOfResources:
            total=temp.loc[temp['Resource']==i,'H/d'].sum()
            newDataFrame.loc[index]=[currentDayPd,i,total]
            index=index+1
        currentDay = currentDay+ datetime.timedelta(days=1)
    return(newDataFrame)    
    

def createFTETableLatex(df,fileName="FTE_per_role"):
    table = PrettyTable()
    f = open(fileName+".tex", "w")
    roles=list(sorted(df['Resource'].unique()))
    f.write('\\begin{table}[H]\n')
    f.write('\\begin{minipage}{\\textwidth}\n')
    f.write('\centering\n')
    f.write('\scalebox{0.8}{\n')
    f.write('\\begin{tabular}{|c|c|c|c|}\n') 
    f.write('\hline\n')
    f.write('\\rowcolor{gray!50}\n')
    f.write('\\textbf{Task ID} & \\textbf{Man Hours at OSF [Hrs]} & \\textbf{Man Hours at AOS [Hrs]} & \\textbf{FTEs\\footnote{$AOS_{FTE}=%d \ OSF_{FTE}=%d$}} \\\\ \n'%(FTE_AOS,FTE_OSF))
    table.field_names = ["Task ID", "Man Hours at OSF [Hrs]", "Man Hours at AOS [Hrs]", "FTEs"]
    f.write('\hwrite\n')
    f.write('\hwrite\n')
    totalFTE=0
    for i in roles:
        f.write(str(i)+' & ')
        aos=df.loc[df['Resource']==i, 'AOS'].sum()
        osf=df.loc[df['Resource']==i, 'OSF'].sum()
        FTE=osf/FTE_OSF + aos/FTE_AOS
        totalFTE += FTE
        f.write('%d & %d & %.2f\\\\ \n'%(osf,aos,FTE))    
        table.add_row([i,np.round(osf,2),np.round(aos,2),np.round(FTE,2)])
        f.write('\hline \n')
    f.write('\hwrite \n')    
    f.write('Total & %d & %d & %.2f\\\\ \n'%(df['OSF'].sum(),df['AOS'].sum(),totalFTE))    
    table.add_row(["Total",np.round(df['OSF'].sum(),2),np.round(df['AOS'].sum(),2),np.round(totalFTE,2)])
    f.write('\hline \n')    
    f.write('\end{tabular}} \n')
    f.write('\end{minipage} \n')
    f.write('\caption{Working Hours per role} \n')
    f.write('\end{table} \n')   
    f.close()
    print(table)
    
    
#'0.01.AIV.EN':[[[EE,2,30,8,0]],False],    
def createEffortTable(listOfTasks,fileName):
    f = open(fileName+".tex", "w")
    f.write('\\begin{table}[H]\n')
    f.write('\\begin{minipage}{\\textwidth}\n')
    f.write('\centering\n')    
    f.write('\\begin{tabular}{|p{\ea}|p{\eb}|p{\ec}|p{\ed}|p{\ee}|}\n')
    f.write('\hline\n')
    f.write('\\rowcolor{gray!50}\n')
    f.write('\\textbf{Specialist} & \\textbf{Number of people} & \\textbf{Working hours per day} & \\textbf{Location} & \\textbf{Duration in days}\\\\ \n')      
    f.write('\hline \n')    
    s=''
    for i in listOfTasks:
        s=s+str(i)+' '
        
    for i in [listOfTasks[0]]:
        #print('h2. %s, %s'%(i,taskDescription.get(i)))
        print('||Role||Number of people||Working hours per day||Location||Duration in days||')
        efforts=taskEfforts.get(i)
        
        for j in efforts[0]:
            f.write('\hline \n') 
            f.write(str(j[0].name))    # resource
            f.write(' & ')
            f.write(str(j[1]))         # number of people
            f.write(' & ')
            f.write(str(j[3]+j[4]))    # working hours per day
            f.write(' & ')
            location=''
            if j[3] != 0:
                f.write('OSF')
                location='OSF'
            if j[4] != 0:
                f.write('AOS')
                location='AOS'
            f.write(' & ')
            f.write(str(j[2]))         # Duration in days
            f.write(' \\\\ \n') 
            print('|%s|%d|%.1f|%s|%d|'%(j[0].name,j[1],j[3]+j[4],location,j[2]))                                        
        
    f.write('\hline \n')    
    f.write('\end{tabular} \n')
    f.write('\end{minipage} \n')        
    f.write('\caption{Resources required for the task: %s}\n'%s)
    f.write('\end{table} \n')  
    

    # tabulate the learning factor
    f.write('% correction table\n')
    
    f.write('\\begin{table}[H]\n')
    f.write('\\begin{minipage}{\\textwidth}\n')
    f.write('\centering\n')    
    f.write('\\begin{tabular}{|c|c|c|}\n')
    f.write('\hline\n')
    f.write('\\rowcolor{gray!50}\n')
    f.write('\\textbf{Task ID} & \\textbf{Learning factor} & \\textbf{Contingency factor} \\\\ \n')      
    f.write('\hline \n')            
    for i in listOfTasks:    
        f.write('\hline \n') 
        f.write(i) 
        f.write(' & ')
        f.write(str(LearningFactor.get(i)))
        f.write(' & ')
        f.write(str(ContingencyFactor.get(i)))
        f.write(' \\\\ \n')            
    f.write('\hline \n')    
    f.write('\end{tabular} \n')
    f.write('\end{minipage} \n')        
    f.write('\caption{Correction factors for the task: %s}\n'%s)
    f.write('\end{table} \n')  
    
    
    
    now = datetime.datetime.now()
    f.write('% created: \n')
    f.write('%'+str(now)+'\n')  
    f.close()

def createEffortDataFrame(listOfTasks):    
    df = pd.DataFrame(columns=['Task','Role','NumberOfPeople','OSF','AOS','DurationInDays','Team','Description'])
    index=0
    for i in listOfTasks:
        team=i.split('.')[-1]
        efforts=taskEfforts.get(i)
        for j in efforts[0]:
            df.loc[index]=[i,
                           j[0].name,
                           j[1],
                           j[3],
                           j[4],
                           j[2],
                           team,
                           taskDescription.get(i)
                          ]
            index=index+1
    return df        
            
        
    
    