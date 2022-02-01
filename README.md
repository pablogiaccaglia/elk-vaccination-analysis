<p align="center">
  <i><span style="font-size: small;">
  	Systems and Methods for Big and Unstructured Data - Delivery #3 - AA 2021/2022 - Prof. Marco Brambilla
  </span></i>
</p>
<h1 align="center">
	<strong>
	ELK Vaccination Campaign Analysis System
	</strong>
	<br>
</h1>
<p align="center">
<span style="font-size: small; ">
		<a href="https://www.mongodb.com">MongoDB</a>		 
		•		
		<a href="Report.pdf">Report</a>   
	</span>
</p>

Considering the scenario in which there’s the need to build a system suitable for analysis over 
data about COVID-19 vaccination statistics, we designed and build a Kibana visualization 
tool relying on the ELK stack. The data stored allows extracting actionable insights 
concerning various statistical purposes, involving information such as vaccine deliveries, 
administered doses amounts, suppliers and age groups. 
The third-part data imported into the database is updated daily as it concerns vaccination campaign 
and so it has been also used to build insightful dashboards providing visualization at various levels 
of granularity.

We focused on the Italian vaccination campaign by relying on the daily updated open data about delivery and administration of **COVID-19** vaccines provided by the <a href="https://www.salute.gov.it">**Italian Ministry of Health**</a>. Of the data available at <a href="https://github.com/italia/covid19-opendata-vaccini">this Github repository</a> only three datasets were picked to feed the system.
The idea is to provide a tool aware of data updates, reason for why we implemented a small data processing pipeline to fetch, slightly change and standardize the data uploaded to the aforementioned repository. More details about this process can be found on the <a href="Report.pdf">Report</a>

# Contents

- ⚙  [System requirements️](#system-requirements)
- 🚀 [Setup instructions](#-setup-instructions)
- 📜 [Report](Report.pdf)
- 👨‍💻 [Usage](#-usage)
	- [Load Dashboards & Indexes](#-Load-Dashboards-&-Indexes)
	- [Enable Python Pipeline](#-Enable-Python-Pipeline)  
- 🗄️ Dumps
  - 🗄️ [Dashboards dump](Exports/Dashboards)
  - 🗄️ [ES Indexes dump](Exports/Indexes) 
- 📷 [Dashboards](#-dashboards)  
- ♻️ [Data pipeline](#-Data-pipeline)
- 📝 [License](#-license)

# System requirements

## Required software

- [Python](https://www.python.org/) 3.8 or higher **(only if you want to update data and/or tweak data update routines)**
- [Elasticsearch](https://www.elastic.co/elasticsearch/)
- [Kibana](https://www.elastic.co/kibana/)  
- Python modules in [requirements.txt](requirements.txt) **(only if you want to update data and/or tweak data update routines)**


# 🚀 Setup instructions

## Clone the repo

    git clone https://github.com/pablogiaccaglia/elastichsearch-vaccination-campaign
    cd elasticsearch_smbud/

## Install required packages

From the project's directory run the following commands:

    pip install -r requirements.txt
    
# 👨‍💻 Usage

## Load Dashboards & Indexes

## Enable Python pipeline

# 📷 Dashboards

In the following chapter we are describing the Kibana dashboards we implemented. We used different indexes and we also tried to cover different ways of representation (bar charts, maps, pie charts) and different functions (cumulative sums, total sums, daily data). Most of the dashboards are interactive: this means you can select an interval with the left click of the mouse and the graph will zoom into it; or for other types you can select/deselect some data (for example, in the map).

Note that even though in Italy the first vaccine against COVID-19 was administered on 27/12/2020, the following charts, when the x-axis is divided into week intervals, the starting week is on /12/2020.


Weekly trend of the number of vaccinations       |  Vaccination status of all age groups
:-------------------------:|:-------------------------:
![](report/latex/Weekly%20trend%20of%20the%20number%20of%20vaccinations.png)|  ![](report/latex/Vaccination%20status%20of%20all%20age%20groups.png)

---

Total number of doses delivered      |  Number of not vaccinated people
:-------------------------:|:-------------------------:
![](report/latex/Total%20number%20of%20doses%20delivered.png)|  ![](report/latex/Number%20of%20not%20vaccinated%20people.png)

---

Gender distribution of weekly vaccine doses administered           |  Doses map
:-------------------------:|:-------------------------:
![](report/latex/Gender%20distribution%20of%20weekly%20vaccine%20doses%20administered.png)|  ![](report/latex/Doses_map.png)

---

<h3><p align="center"><b>Distribution of suppliers of all administered vaccines</b></></h3> 
	
<p align="center">
<img src="https://github.com/pablogiaccaglia/elk-vaccination-analysis/blob/master/report/latex/Distribution%20of%20suppliers%20of%20all%20administered%20vaccines.png" width=550px height=520px/>
</p>

---
	
# ♻️ Data pipeline
	
 <p align= "center">
 <kbd> 
 <img src="report/latex/pipeline.png" align="center" />
 </kbd>
 </>

# 📝 License

This file is part of "ELK Vaccination Campaign Analysis System".

"ELK Vaccination Campaign Analysis System" is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

"ELK Vaccination Campaign Analysis System" is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program (LICENSE.txt).  If not, see <http://www.gnu.org/licenses/>
